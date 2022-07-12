# Create your views here.
import datetime

import django_tables2 as tables
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.shortcuts import render
from django.utils import timezone as tz

from .models import Hospital, Patient

# from .utils import faker_data



class HospitalTable(tables.Table):
    class Meta:
        model = Hospital
        fields = ("name", "total_no_of_beds", "bed_occupied", "beds_available")


# views.py
def index(request):
    d = tz.now() - datetime.timedelta(days=10)
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

    table = HospitalTable(Hospital.objects.all())

    data = {}

    data.update({"covid_positive": get_label_data(covid_positive_count_by_day)})
    data.update({"deceased": get_label_data(deceased_count_by_day)})
    data.update({"recovered": get_label_data(recovered_count_by_day)})
    data.update({"active": get_label_data(active_count_by_day)})
    data.update({"table": table})

    return render(request, "index.html", data)


def get_label_data(data):
    # faker_data()
    labels = []
    datas = []
    for day in data:
        labels.append(day["day"].strftime("%d"))
        datas.append(day["c"])
    print(labels, datas)
    return {"labels": ",".join(labels), "data": datas, "sum": sum(datas)}
