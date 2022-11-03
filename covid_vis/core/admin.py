from django.contrib import admin

from .models import Hospital, Patient


class HospitalAdmin(admin.ModelAdmin):
    exclude = ("beds_available",)

    def get_queryset(self, request):
        qs = super(HospitalAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(hospital_admin=request.user)


class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_by", "created_at", "updated_at")
    exclude = ("created_by",)
    actions = None
    search_fields = ['id', "name"]

    def get_queryset(self, request):
        qs = super(PersonAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user

        obj.save()


# Register your models here.
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Patient, PersonAdmin)
