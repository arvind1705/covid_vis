from django.contrib import admin

from .models import Hospital, Patient


class HospitalAdmin(admin.ModelAdmin):
    exclude = ("beds_available",)


class PersonAdmin(admin.ModelAdmin):
    exclude = ("created_by",)
    actions = None

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user

        obj.save()


# Register your models here.
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Patient, PersonAdmin)
