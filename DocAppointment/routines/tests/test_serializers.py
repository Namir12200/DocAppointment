from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib.auth.hashers import make_password
from routines.serializers import DoctorRoutineSerializer, SlotDateSerializer, SlotSerializer
from routines.models import DoctorRoutine, SlotDate
import datetime

class RoutineSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="Jackson", email="jack@email.com", password=make_password("1234"))
        self.profile = Profile.objects.get(user=self.user)
    
    def test_routine_serializer(self):
        data = {
            "doctor_id":self.profile.pk,
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
        serializer = DoctorRoutineSerializer(data=data)
        self.assertTrue(serializer.is_valid())

class SlotDateSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="Jackson", email="jack@email.com", password=make_password("1234"))
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


    def test_slotDate_serializer(self):
        data = {
            "doctor_id": self.doctor.pk,
            "appointment_date": datetime.date(2024, 7, 15),
            "total_patients": 7,
        }
        serializer = SlotDateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

class SlotSerializerTestCase(APITestCase):
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


    def test_slot_serializer(self):
        data = {
            "description": "I am very sick",
            "patient_id": self.profile2.pk,
            "routine_id": 50
        }
        serializer = SlotSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        data = {
            "description": "I am very sick",
            "patient_id": self.profile2.pk,
            "routine_id": self.doctor.pk
        }
        serializer = SlotSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        slot_date = self.doctor.get_slot_date(testing=False)
        slot = serializer.create(validated_data=data)
        self.assertEqual(slot.patient.pk, self.profile2.pk)
        self.assertEqual(slot.slot_date.appointment_date, slot_date.appointment_date)
        self.assertEqual(slot.slot_date.total_patients, 1)

        data = {
            "doctor": self.doctor,
            "appointment_date": datetime.date(2024, 7, 16),
            "total_patients": 10
        }
        self.slotdate = SlotDate.objects.create(doctor=data['doctor'], appointment_date=data['appointment_date'], total_patients=data["total_patients"])

        data = {
            "description": "I am very sick",
            "patient_id": self.profile2.pk,
            "routine_id": self.doctor.pk
        }
        serializer = SlotSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        slot_date = self.doctor.get_slot_date(testing=False)
        slot = serializer.create(validated_data=data)
        self.assertEqual(slot.patient.pk, self.profile2.pk)
        self.assertEqual(slot.slot_date.appointment_date, slot_date.appointment_date)
        self.assertGreater(slot.slot_date.appointment_date, self.slotdate.appointment_date)
        self.assertEqual(slot.slot_date.total_patients, 1)
