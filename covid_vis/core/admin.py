from django.contrib import admin

from .models import Hospital, Patient


class HospitalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "total_no_of_beds",
        "beds_available",
        "is_covid_care_center",
        "hospital_admin",
    )
    list_filter = ("is_covid_care_center", "city")
    search_fields = ("name", "address", "city")
    exclude = ("beds_available",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(hospital_admin=request.user)


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "phone",
        "covid_positive",
        "vaccination_status",
        "case",
        "recovered",
        "deceased",
        "created_by",
    )
    list_filter = ("covid_positive", "vaccination_status", "case", "recovered", "deceased")
    search_fields = ("id", "name", "phone", "email")
    exclude = ("created_by",)
    actions = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()


admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Patient, PatientAdmin)
