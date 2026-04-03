import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .admin import HospitalAdmin, PatientAdmin
from .models import Hospital, Patient

User = get_user_model()


class HospitalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_hospital_str(self):
        hospital = Hospital.objects.create(
            name="Test Hospital",
            address="123 Test St",
            city="Test City",
            state="Test State",
            zipcode="123456",
            phone="+919999999999",
            website="http://test.com",
            hospital_admin=self.user,
        )
        self.assertEqual(str(hospital), "Test Hospital")

    def test_hospital_beds_available_calculation(self):
        hospital = Hospital.objects.create(
            name="Test Hospital",
            address="123 Test St",
            city="Test City",
            state="Test State",
            zipcode="123456",
            phone="+919999999999",
            website="http://test.com",
            hospital_admin=self.user,
            total_no_of_beds=100,
            bed_occupied=30,
        )
        self.assertEqual(hospital.beds_available, 70)

    def test_hospital_clean_validation_beds_occupied_exceeds_total(self):
        hospital = Hospital(
            name="Test Hospital",
            address="123 Test St",
            city="Test City",
            state="Test State",
            zipcode="123456",
            phone="+919999999999",
            website="http://test.com",
            hospital_admin=self.user,
            total_no_of_beds=100,
            bed_occupied=150,
        )
        with self.assertRaises(ValidationError):
            hospital.clean()

    def test_hospital_clean_validation_icu_exceeds_total(self):
        hospital = Hospital(
            name="Test Hospital",
            address="123 Test St",
            city="Test City",
            state="Test State",
            zipcode="123456",
            phone="+919999999999",
            website="http://test.com",
            hospital_admin=self.user,
            total_no_of_beds=100,
            no_icu_beds=150,
        )
        with self.assertRaises(ValidationError):
            hospital.clean()


class PatientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_patient_str(self):
        patient = Patient.objects.create(
            name="Test Patient",
            phone="+919999999999",
            email="test@example.com",
            dob=datetime.date(1990, 1, 1),
            gender="M",
            vaccination_status="F",
            case="T",
            created_by=self.user,
        )
        self.assertEqual(str(patient), "Test Patient")

    def test_patient_clean_validation_recovered_and_deceased(self):
        patient = Patient(
            name="Test Patient",
            phone="+919999999999",
            email="test@example.com",
            dob=datetime.date(1990, 1, 1),
            gender="M",
            vaccination_status="F",
            case="T",
            recovered=True,
            deceased=True,
        )
        with self.assertRaises(ValidationError):
            patient.clean()


class HospitalAdminTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin", password="adminpass123"
        )
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            address="123 Test St",
            city="Test City",
            state="Test State",
            zipcode="123456",
            phone="+919999999999",
            website="http://test.com",
            hospital_admin=self.user,
        )

    def test_hospital_admin_list_display(self):
        admin = HospitalAdmin(Hospital, None)
        self.assertIn("name", admin.list_display)
        self.assertIn("city", admin.list_display)

    def test_hospital_admin_search_fields(self):
        admin = HospitalAdmin(Hospital, None)
        self.assertIn("name", admin.search_fields)


class PatientAdminTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin", password="adminpass123"
        )
        self.patient = Patient.objects.create(
            name="Test Patient",
            phone="+919999999999",
            email="test@example.com",
            dob=datetime.date(1990, 1, 1),
            gender="M",
            vaccination_status="F",
            case="T",
            created_by=self.user,
        )

    def test_patient_admin_list_display(self):
        admin = PatientAdmin(Patient, None)
        self.assertIn("name", admin.list_display)
        self.assertIn("covid_positive", admin.list_display)

    def test_patient_admin_search_fields(self):
        admin = PatientAdmin(Patient, None)
        self.assertIn("name", admin.search_fields)
