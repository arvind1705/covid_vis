"""
models.py
"""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class Hospital(models.Model):
    """Hospital Model"""

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    phone = PhoneNumberField()
    website = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_no_of_beds = models.IntegerField(default=0, verbose_name="Total No. of Beds")
    no_icu_beds = models.IntegerField(default=0, verbose_name="No. of ICU Beds")
    bed_occupied = models.IntegerField(default=0, verbose_name="No. of Beds Occupied")
    beds_available = models.IntegerField(
        default=0, verbose_name="No. of Beds Available"
    )
    hospital_admin = models.ForeignKey(User, on_delete=models.CASCADE)
    is_covid_care_center = models.BooleanField(
        default=False,
        verbose_name="Covid Care Center",
    )
    oxygen_concentrator_available = models.BooleanField(
        default=False,
        verbose_name="Oxygen concentrator",
    )
    ambulance_available = models.BooleanField(
        default=False,
        verbose_name="Ambulance",
    )
    image_link = models.CharField(max_length=500, blank=True)
    ambulance_driver_name = models.CharField(max_length=100, blank=True)
    ambulance_driver_phone = PhoneNumberField(blank=True)

    def clean(self):
        super().clean()
        if self.bed_occupied > self.total_no_of_beds:
            raise ValidationError(
                {"bed_occupied": "Beds occupied cannot exceed total beds"}
            )
        if self.no_icu_beds > self.total_no_of_beds:
            raise ValidationError(
                {"no_icu_beds": "ICU beds cannot exceed total beds"}
            )

    def save(self, *args, **kwargs):
        self.beds_available = self.total_no_of_beds - self.bed_occupied
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Patient(models.Model):
    """Patient Model"""

    name = models.CharField(max_length=100)
    phone = PhoneNumberField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, editable=False, null=True, blank=True, on_delete=models.DO_NOTHING
    )
    covid_positive = models.BooleanField(default=False)
    deceased = models.BooleanField(default=False)
    recovered = models.BooleanField(default=False)
    dob = models.DateField()
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    VACCINE_CHOICES = (
        ("F", "First"),
        ("S", "Second"),
        ("P", "Precautionary"),
        ("N", "Not Yet"),
    )
    vaccination_status = models.CharField(max_length=1, choices=VACCINE_CHOICES)
    CASE_CHOICES = (
        ("T", "Testing"),
        ("V", "Vaccination"),
    )
    case = models.CharField(max_length=1, choices=CASE_CHOICES)

    def clean(self):
        super().clean()
        if self.recovered and self.deceased:
            raise ValidationError(
                "Patient cannot be both recovered and deceased"
            )

    def __str__(self):
        return f"{self.name}"
