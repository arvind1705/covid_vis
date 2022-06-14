# Create your views here.
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.shortcuts import render

from .models import Patient


# views.py
def index(request):
    covid_positive_count_by_day = (
        Patient.objects.annotate(day=TruncDay("created_at"))
        .values("day")
        .annotate(c=Count("covid_positive"))
        .values("day", "c")
    )
    deceased_count_by_day = (
        Patient.objects.annotate(day=TruncDay("updated_at"))
        .values("day")
        .annotate(c=Count("deceased"))
        .values("day", "c")
    )
    recovered_count_by_day = (
        Patient.objects.annotate(day=TruncDay("updated_at"))
        .values("day")
        .annotate(c=Count("recovered"))
        .values("day", "c")
    )

    data = {}

    data.update({"covid_positive": get_label_data(covid_positive_count_by_day)})
    data.update({"deceased": get_label_data(deceased_count_by_day)})
    data.update({"recovered": get_label_data(recovered_count_by_day)})

    return render(request, "index.html", data)


def get_label_data(data):
    labels = []
    datas = []
    for day in data:
        labels.append(day["day"].strftime("%d"))
        datas.append(day["c"])
    return {"labels": labels, "data": datas, "sum": sum(datas)}