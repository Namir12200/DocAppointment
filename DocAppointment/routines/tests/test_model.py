from django.test import TestCase
from routines.models import DoctorRoutine, SlotDate, Slot
from accounts.models import Profile
from django.contrib.auth.models import User
import datetime

class DoctorRoutineTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="Jack", email="namirulislam16@email.com", password="1234")
        self.profile = Profile.objects.get(user=self.user)
        self.profile.is_doctor = True

    def test_create_doctor_routine(self):
        data = {
            "doctor_id": self.profile.pk,
            "institution": "Japan Bangladesh",
            "visiting_cost": 500,
            "new_customer_cost": 700,
            "patients_per_day": 10,
            "days": [
                "SUN",
                "MON",
                "SUN",
                "TUE"
            ]
        }
        self.doctor = DoctorRoutine.objects.create(doctor=self.profile, institution=data['institution'], visiting_cost=data['visiting_cost'], new_customer_cost=data["new_customer_cost"], patients_per_day=data['patients_per_day'], days=data['days'])
        self.assertEqual(self.doctor.doctor.pk, data['doctor_id'])
        self.assertEqual(self.doctor.days.sort(), list(set(data['days'])).sort()) # Needs to be sorted to work

class SlotDateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="Jack", email="namirulislam16@email.com", password="1234")
        self.profile = Profile.objects.get(user=self.user)
        self.profile.is_doctor = True
        data = {
            "doctor_id": self.profile.pk,
            "institution": "Japan Bangladesh",
            "visiting_cost": 500,
            "new_customer_cost": 700,
            "patients_per_day": 10,
            "days": [
                "SUN",
                "MON",
                "SUN",
                "TUE"
            ]
        }
        self.doctor = DoctorRoutine.objects.create(doctor=self.profile, institution=data['institution'], visiting_cost=data['visiting_cost'], new_customer_cost=data["new_customer_cost"], patients_per_day=data['patients_per_day'], days=data['days'])

    def test_create_slot_date(self):
        data = {
            "doctor": self.doctor,
            "appointment_date": datetime.date(2024, 7, 15),
            "total_patients": 0
        }
        self.slotdate = SlotDate.objects.create(doctor=data['doctor'], appointment_date=data['appointment_date'], total_patients=data["total_patients"])
        self.assertEqual(self.slotdate.doctor, self.doctor)
        self.assertEqual(self.slotdate.appointment_date, datetime.date(2024, 7, 15))
        self.assertEqual(self.slotdate.total_patients, 0)

class SlotModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="Jack", email="jack@email.com", password="1234")
        self.profile = Profile.objects.get(user=self.user)
        self.user2 = User.objects.create(username="James", email="james@email.com", password="1234")
        self.profile2 = Profile.objects.get(user=self.user2)
        self.profile.is_doctor = True
        data = {
            "doctor_id": self.profile.pk,
            "institution": "Japan Bangladesh",
            "visiting_cost": 500,
            "new_customer_cost": 700,
            "patients_per_day": 10,
            "days": [
                "SUN",
                "MON",
                "SUN",
                "TUE"
            ]
        }
        self.doctor = DoctorRoutine.objects.create(doctor=self.profile, institution=data['institution'], visiting_cost=data['visiting_cost'], new_customer_cost=data["new_customer_cost"], patients_per_day=data['patients_per_day'], days=data['days'])
        data = {
            "doctor": self.doctor,
            "appointment_date": datetime.date(2024, 7, 15),
            "total_patients": 0
        }
        self.slotdate = SlotDate.objects.create(doctor=data['doctor'], appointment_date=data['appointment_date'], total_patients=data["total_patients"])
        
    def test_create_slot(self):
        data = {
            "description" : "Very sick",
            "patient" : self.profile2,
            "slot_date" : self.slotdate
        }
        slot = Slot.objects.create(**data)
        self.assertEqual(slot.description, data["description"])
        self.assertEqual(slot.patient.user.username, self.user2.username)
        self.assertEqual(slot.slot_date, data['slot_date'])