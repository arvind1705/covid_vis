# Create your views here.
import datetime

import django_tables2 as tables
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.shortcuts import render
from django.utils import timezone as tz

from .models import Hospital, Patient


class HospitalTable(tables.Table):
    class Meta:
        model = Hospital
        fields = ("name", "total_no_of_beds", "bed_occupied", "beds_available")
        template_name = "django_tables2/semantic.html"


class CareCenterTable(tables.Table):
    class Meta:
        model = Hospital
        fields = ("name", "phone")
        template_name = "django_tables2/semantic.html"


# views.py
def index(request):
    d = tz.now() - datetime.timedelta(days=10)
    today = datetime.date.today()
    data = {}

    covid_positive_count_by_day = (
        Patient.objects.filter(covid_positive=True, updated_at__lt=d)
        .annotate(day=TruncDay("created_at"))
        .values("day")
        .annotate(c=Count("covid_positive"))
        .values("day", "c")
    )
    deceased_count_by_day = (
        Patient.objects.filter(deceased=True, updated_at__lt=d)
        .annotate(day=TruncDay("created_at"))
        .values("day")
        .annotate(c=Count("deceased"))
        .values("day", "c")
    )
    recovered_count_by_day = (
        Patient.objects.filter(recovered=True, updated_at__lt=d)
        .annotate(day=TruncDay("created_at"))
        .values("day")
        .annotate(c=Count("recovered"))
        .values("day", "c")
    )
    active_count_by_day = (
        Patient.objects.filter(recovered=False, covid_positive=True, updated_at__lt=d)
        .annotate(day=TruncDay("created_at"))
        .values("day")
        .annotate(c=Count("recovered"))
        .values("day", "c")
    )

    hospitals_list = HospitalTable(Hospital.objects.all())
    care_center_list = CareCenterTable(
        Hospital.objects.filter(is_covid_care_center=True)
    )

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

    data.update({"covid_positive": get_label_data(covid_positive_count_by_day)})
    data.update({"deceased": get_label_data(deceased_count_by_day)})
    data.update({"recovered": get_label_data(recovered_count_by_day)})
    data.update({"active": get_label_data(active_count_by_day)})
    data.update({"hospitals_list": hospitals_list})
    data.update({"care_center_list": care_center_list})
    data.update({"age_data": age_data})

    return render(request, "index.html", data)


def get_label_data(data):
    labels = []
    datas = []
    for day in data:
        labels.append(day["day"].strftime("%d"))
        datas.append(day["c"])
    return {"labels": ",".join(labels), "data": datas, "sum": sum(datas)}
