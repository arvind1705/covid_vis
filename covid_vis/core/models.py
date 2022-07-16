"""
models.py
"""
from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()
# Create your models here.
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

    @property
    def _get_beds_available(self):
        "Returns the person's full name."
        return self.total_no_of_beds - self.bed_occupied

    def save(self, *args, **kwargs):
        self.beds_available = self._get_beds_available
        super(Hospital, self).save(*args, **kwargs)

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
    deceased = models.BooleanField(default=False)  # If patient is deceased
    recovered = models.BooleanField(default=False)  # If patient is recovered
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

    def __str__(self):
        return f"{self.name}"
