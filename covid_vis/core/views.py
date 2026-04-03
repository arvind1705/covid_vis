import datetime

import django_tables2 as tables
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.html import format_html
from django_filters import FilterSet
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import Hospital, Patient


class HospitalTable(tables.Table):
    class Meta:
        model = Hospital
        fields = (
            "name",
            "total_no_of_beds",
            "no_icu_beds",
            "beds_available",
            "is_covid_care_center",
            "oxygen_concentrator_available",
            "ambulance_available",
        )
        template_name = "django_tables2/bootstrap4.html"
        orderable = False

    def render_name(self, record):
        return format_html(
            '<a href="{}">{}</a>',
            reverse("hospital_detail", kwargs={"hospital_id": record.id}),
            record.name,
        )


class HospitalFilter(FilterSet):
    class Meta:
        model = Hospital
        fields = {"name": ["contains"]}


class FilteredHospitalListView(SingleTableMixin, FilterView):
    table_class = HospitalTable
    model = Hospital
    template_name = "hospital_list.html"
    filterset_class = HospitalFilter


class PatientTable(tables.Table):
    class Meta:
        model = Patient
        fields = (
            "name",
            "phone",
            "covid_positive",
            "vaccination_status",
            "case",
            "recovered",
            "deceased",
        )
        template_name = "django_tables2/bootstrap4.html"
        orderable = False

    def render_name(self, record):
        return format_html(
            '<a href="{}">{}</a>',
            reverse("patient_detail", kwargs={"patient_id": record.id}),
            record.name,
        )


class PatientFilter(FilterSet):
    class Meta:
        model = Patient
        fields = {
            "name": ["contains"],
            "covid_positive": ["exact"],
            "vaccination_status": ["exact"],
            "case": ["exact"],
        }


class FilteredPatientListView(SingleTableMixin, FilterView):
    table_class = PatientTable
    model = Patient
    template_name = "patient_list.html"
    filterset_class = PatientFilter


def index(request):
    hospital_agg = Hospital.objects.aggregate(
        total_beds=Sum("total_no_of_beds"),
        available_beds=Sum("beds_available"),
        icu_beds=Sum("no_icu_beds"),
        total_hospitals=Count("id"),
    )
    patient_agg = Patient.objects.aggregate(
        total_patients=Count("id"),
        covid_positive=Count("id", filter=Q(covid_positive=True)),
        recovered=Count("id", filter=Q(recovered=True)),
        deceased=Count("id", filter=Q(deceased=True)),
    )

    context = {
        "total_hospitals": hospital_agg["total_hospitals"] or 0,
        "total_beds": hospital_agg["total_beds"] or 0,
        "available_beds": hospital_agg["available_beds"] or 0,
        "icu_beds": hospital_agg["icu_beds"] or 0,
        "total_patients": patient_agg["total_patients"] or 0,
        "covid_positive": patient_agg["covid_positive"] or 0,
        "recovered": patient_agg["recovered"] or 0,
        "deceased": patient_agg["deceased"] or 0,
    }
    return render(request, "index.html", context)


def graphs(request):
    today = datetime.date.today()
    data = {}

    age_0_18 = Patient.objects.filter(
        dob__gte=today - relativedelta(years=18),
        dob__lte=today,
    ).count()
    age_19_40 = Patient.objects.filter(
        dob__gte=today - relativedelta(years=40),
        dob__lt=today - relativedelta(years=18),
    ).count()
    age_41_60 = Patient.objects.filter(
        dob__gte=today - relativedelta(years=60),
        dob__lt=today - relativedelta(years=40),
    ).count()
    age_61_100 = Patient.objects.filter(
        dob__gte=today - relativedelta(years=150),
        dob__lt=today - relativedelta(years=60),
    ).count()

    age_data = {
        "labels": "0-18,19-40,41-60,Above 60",
        "data": f"{age_0_18},{age_19_40},{age_41_60},{age_61_100}",
    }

    first_vaccinated_count = Patient.objects.filter(vaccination_status="F").count()
    second_vaccinated_count = Patient.objects.filter(vaccination_status="S").count()
    precautions_count = Patient.objects.filter(vaccination_status="P").count()
    total_vaccine_count = first_vaccinated_count + second_vaccinated_count + precautions_count
    total_patients = Patient.objects.count()
    not_vaccinated_count = total_patients - total_vaccine_count

    vaccine_data = {
        "labels": "Total,First Dose,Second Dose,Precaution Dose,Not Vaccinated",
        "data": f"{total_vaccine_count},{first_vaccinated_count},{second_vaccinated_count},{precautions_count},{not_vaccinated_count}",
    }

    covid_positive_count_by_day = (
        Patient.objects.filter(covid_positive=True)
        .annotate(day=TruncDay("updated_at"))
        .values("day")
        .annotate(c=Count("covid_positive"))
        .values("day", "c")
    )
    deceased_count_by_day = (
        Patient.objects.filter(deceased=True)
        .annotate(day=TruncDay("updated_at"))
        .values("day")
        .annotate(c=Count("deceased"))
        .values("day", "c")
    )
    recovered_count_by_day = (
        Patient.objects.filter(recovered=True)
        .annotate(day=TruncDay("updated_at"))
        .values("day")
        .annotate(c=Count("recovered"))
        .values("day", "c")
    )
    active_count_by_day = (
        Patient.objects.filter(recovered=False, covid_positive=True)
        .annotate(day=TruncDay("updated_at"))
        .values("day")
        .annotate(c=Count("covid_positive"))
        .values("day", "c")
    )

    data.update({"age_data": age_data})
    data.update({"vaccine_data": vaccine_data})
    data.update({"covid_positive": get_label_data(covid_positive_count_by_day)})
    data.update({"deceased": get_label_data(deceased_count_by_day)})
    data.update({"recovered": get_label_data(recovered_count_by_day)})
    data.update({"active": get_label_data(active_count_by_day)})

    return render(request, "graphs.html", data)


def get_label_data(data):
    labels, datas, count = [], [], 0
    for day in data:
        labels.append(day["day"].strftime("%d %b"))
        datas.append(str(day["c"]))
        count += day["c"]
    return {"labels": ",".join(labels), "data": ",".join(datas), "sum": count}


def helpline(request):
    return render(request, "helpline.html")


def hospital_detail(request, hospital_id):
    hospital_data = get_object_or_404(Hospital, id=hospital_id)

    is_covid_care_center = "Yes" if hospital_data.is_covid_care_center else "No"
    oxygen_concentrator_available = "Available" if hospital_data.oxygen_concentrator_available else "Not Available"

    return render(
        request,
        "hospital_detail.html",
        {
            "hospital": hospital_data,
            "is_covid_care_center": is_covid_care_center,
            "oxygen_concentrator_available": oxygen_concentrator_available,
        },
    )


def patient_detail(request, patient_id):
    patient_data = get_object_or_404(Patient, id=patient_id)

    vaccination_status_map = dict(Patient.VACCINE_CHOICES)
    case_map = dict(Patient.CASE_CHOICES)

    return render(
        request,
        "patient_detail.html",
        {
            "patient": patient_data,
            "vaccination_status_display": vaccination_status_map.get(
                patient_data.vaccination_status, "Unknown"
            ),
            "case_display": case_map.get(patient_data.case, "Unknown"),
        },
    )


def api_hospitals(request):
    hospitals = Hospital.objects.values(
        "id",
        "name",
        "address",
        "city",
        "phone",
        "total_no_of_beds",
        "beds_available",
        "no_icu_beds",
        "is_covid_care_center",
        "oxygen_concentrator_available",
        "ambulance_available",
    )
    return JsonResponse(list(hospitals), safe=False)


def api_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    data = {
        "id": hospital.id,
        "name": hospital.name,
        "address": hospital.address,
        "city": hospital.city,
        "phone": str(hospital.phone),
        "total_no_of_beds": hospital.total_no_of_beds,
        "beds_available": hospital.beds_available,
        "no_icu_beds": hospital.no_icu_beds,
        "is_covid_care_center": hospital.is_covid_care_center,
        "oxygen_concentrator_available": hospital.oxygen_concentrator_available,
        "ambulance_available": hospital.ambulance_available,
    }
    return JsonResponse(data)


def api_patients(request):
    patients = Patient.objects.values(
        "id",
        "name",
        "phone",
        "email",
        "covid_positive",
        "vaccination_status",
        "case",
        "recovered",
        "deceased",
    )
    return JsonResponse(list(patients), safe=False)


def api_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    data = {
        "id": patient.id,
        "name": patient.name,
        "phone": str(patient.phone),
        "email": patient.email,
        "covid_positive": patient.covid_positive,
        "vaccination_status": patient.vaccination_status,
        "case": patient.case,
        "recovered": patient.recovered,
        "deceased": patient.deceased,
        "dob": str(patient.dob),
    }
    return JsonResponse(data)


def api_stats(request):
    hospital_agg = Hospital.objects.aggregate(
        total_beds=Sum("total_no_of_beds"),
        available_beds=Sum("beds_available"),
        icu_beds=Sum("no_icu_beds"),
        total_hospitals=Count("id"),
    )
    patient_agg = Patient.objects.aggregate(
        total_patients=Count("id"),
        covid_positive=Count("id", filter=Q(covid_positive=True)),
        recovered=Count("id", filter=Q(recovered=True)),
        deceased=Count("id", filter=Q(deceased=True)),
    )
    data = {
        "total_hospitals": hospital_agg["total_hospitals"] or 0,
        "total_beds": hospital_agg["total_beds"] or 0,
        "available_beds": hospital_agg["available_beds"] or 0,
        "icu_beds": hospital_agg["icu_beds"] or 0,
        "total_patients": patient_agg["total_patients"] or 0,
        "covid_positive": patient_agg["covid_positive"] or 0,
        "recovered": patient_agg["recovered"] or 0,
        "deceased": patient_agg["deceased"] or 0,
    }
    return JsonResponse(data)
