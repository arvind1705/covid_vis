# Create your views here.
"""
views.py
"""
import datetime

import django_tables2 as tables
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
from django_filters import FilterSet
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import Hospital, Patient


class HospitalTable(tables.Table):
    """Hospital Table"""

    class Meta:
        """
        _summary_attrs = ['name', 'address', 'city', 'state',
        'zip_code', 'phone_number', 'email']
        """

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
        """
        This function will render over the default id column.
        By adding <a href> HTML formatting around the id number a link will be added,
        thus acting the same as linkify. The record stands for the entire record
        for the row from the table data.
        """
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
    template_name = "hospital.html"

    filterset_class = HospitalFilter


# views.py
def index(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = {}

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
        .annotate(c=Count("recovered"))
        .values("day", "c")
    )

    hospitals_list = HospitalTable(Hospital.objects.all())

    data.update({"covid_positive": get_label_data(covid_positive_count_by_day)})
    data.update({"deceased": get_label_data(deceased_count_by_day)})
    data.update({"recovered": get_label_data(recovered_count_by_day)})
    data.update({"active": get_label_data(active_count_by_day)})
    data.update({"hospitals_list": hospitals_list})

    return render(request, "index.html", data)


def hospital(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    hospitals_list = HospitalTable(Hospital.objects.all())
    hospitals_list.paginate(page=request.GET.get("page", 1), per_page=10)
    return render(request, "hospital.html", {"hospitals_list": hospitals_list})


def graphs(request):
    """_summary_"""
    today = datetime.date.today()
    data = {}

    age_0_18 = Patient.objects.filter(
        dob__lte=today - relativedelta(years=1),
        dob__gte=today - relativedelta(years=18),
    ).count()
    age_19_40 = Patient.objects.filter(
        dob__lte=today - relativedelta(years=19),
        dob__gte=today - relativedelta(years=40),
    ).count()
    age_41_60 = Patient.objects.filter(
        dob__lte=today - relativedelta(years=41),
        dob__gte=today - relativedelta(years=60),
    ).count()
    age_61_100 = Patient.objects.filter(
        dob__lte=today - relativedelta(years=61),
        dob__gte=today - relativedelta(years=100),
    ).count()

    age_data = {
        "0-18": str(age_0_18),
        "19-40": str(age_19_40),
        "41-60": str(age_41_60),
        "Above 60": str(age_61_100),
    }
    age_data = {
        "labels": ",".join(age_data.keys()),
        "data": ",".join(age_data.values()),
    }

    first_vaccinated_count = Patient.objects.filter(vaccination_status="F").count()
    second_vaccinated_count = Patient.objects.filter(vaccination_status="S").count()
    precautions_count = Patient.objects.filter(vaccination_status="P").count()
    total_vaccine_count = (
        first_vaccinated_count + second_vaccinated_count + precautions_count
    )

    total_patients = Patient.objects.count()

    not_vaccinated_count = (
        total_patients
        - first_vaccinated_count
        - second_vaccinated_count
        - precautions_count
    )

    vaccine_data = {
        "Total": str(total_vaccine_count),
        "First Dose": str(first_vaccinated_count),
        "Second Dose": str(second_vaccinated_count),
        "Precaution Dose": str(precautions_count),
        "Not Vaccinated": str(not_vaccinated_count),
    }

    vaccine_data = {
        "labels": ",".join(vaccine_data.keys()),
        "data": ",".join(vaccine_data.values()),
    }

    data.update({"age_data": age_data})
    data.update({"vaccine_data": vaccine_data})
    return render(request, "graphs.html", data)


def get_label_data(data):
    """_summary_

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    labels, datas, count = [], [], 0
    for day in data:
        labels.append(day["day"].strftime("%d %b"))
        datas.append(str(day["c"]))
        count += day["c"]
    # sorted(labels, key=lambda x: datetime.datetime.strptime(x, '%d %b'))
    return {"labels": ",".join(labels), "data": ",".join(datas), "sum": count}


def links(request):
    """_summary_

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    return render(request, "links.html")


def helpline(request):
    """_summary_

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    return render(request, "helpline.html")


def hospital_detail(request, hospital_id):
    """_summary_
    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    hospital_data = Hospital.objects.get(id=hospital_id)
    hospitals_list = HospitalTable(Hospital.objects.filter(id=hospital_id))
    return render(
        request,
        "hospital_detail.html",
        {"hospital": hospital_data, "hospitals_list": hospitals_list},
    )
