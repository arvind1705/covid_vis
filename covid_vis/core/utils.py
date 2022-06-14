import random
from datetime import date

from django.contrib.auth.models import User
from faker import Faker

from .models import Patient


def faker_data():
    date_start = date(2022, 5, 1)
    date_end = date(2022, 6, 1)
    user = User.objects.get(pk=2)
    for _ in range(2):

        fake = Faker()
        p = Patient()
        p.name = fake.name()
        p.phone = fake.phone_number()
        p.email = fake.email()
        p.created_at = fake.date_between_dates(date_start=date_start, date_end=date_end)
        p.updated_at = fake.date_between_dates(date_start=date_start, date_end=date_end)
        p.created_by = user
        p.covid_positive = True
        p.deceased = fake.boolean()
        p.recovered = fake.boolean()
        p.dob = fake.date()
        p.gender = random.choice(["M", "F"])
        p.vaccination_status = random.choice(["F", "S", "P", "N"])
        p.case = random.choice(["V", "T"])
        p.save()
