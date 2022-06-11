# Create your views here.
from django.shortcuts import render


# views.py
def index(request):
    return render(request, "index.html")
