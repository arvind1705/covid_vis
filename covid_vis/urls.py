"""covid_vis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from covid_vis.core import views

admin.site.site_header = "Chikkamagaluru Covid Administration"

urlpatterns = [
    path(
        "admin/login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("admin/", admin.site.urls),
    path("hospital/", views.FilteredHospitalListView.as_view(), name="hospital"),
    path("<int:hospital_id>", views.hospital_detail, name="hospital_detail"),
    path("graphs/", views.graphs, name="graphs"),
    path("helpline/", views.helpline, name="helpline"),
    re_path("", views.index, name="index"),
]
