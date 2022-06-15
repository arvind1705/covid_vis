# Create your views here.
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncHour
from django.shortcuts import render

from .models import Patient
from .utils import faker_data


# views.py
def index(request):
    covid_positive_count_by_day = (
        Patient.objects.filter(covid_positive=True)
        .annotate(day=TruncHour("created_at"))
        .values("day")
        .annotate(c=Count("covid_positive"))
        .values("day", "c")
    )
    deceased_count_by_day = (
        Patient.objects.filter(deceased=True)
        .annotate(day=TruncHour("created_at"))
        .values("day")
        .annotate(c=Count("deceased"))
        .values("day", "c")
    )
    recovered_count_by_day = (
        Patient.objects.filter(recovered=True)
        .annotate(day=TruncHour("created_at"))
        .values("day")
        .annotate(c=Count("recovered"))
        .values("day", "c")
    )
    active_count_by_day = (
        Patient.objects.filter(recovered=False, covid_positive=True)
        .annotate(day=TruncHour("created_at"))
        .values("day")
        .annotate(c=Count("recovered"))
        .values("day", "c")
    )

    data = {}

    data.update({"covid_positive": get_label_data(covid_positive_count_by_day)})
    data.update({"deceased": get_label_data(deceased_count_by_day)})
    data.update({"recovered": get_label_data(recovered_count_by_day)})
    data.update({"active": get_label_data(active_count_by_day)})

    return render(request, "index.html", data)


def get_label_data(data):
    # faker_data()
    labels = []
    datas = []
    for day in data:
        labels.append(day["day"].strftime("%H"))
        datas.append(day["c"])
    print(labels, datas)
    return {"labels": ",".join(labels), "data": datas, "sum": sum(datas)}
