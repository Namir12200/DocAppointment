from django.test import TestCase
from patientRecord.models import PatientHistory
from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib.auth.hashers import make_password
# from routines.models import DoctorRoutine, SlotDate, Slot
from patientRecord.models import PatientHistory
import datetime
import json

class PatientHistoryModelTestCase(TestCase):
    def setUp(self):
        user1 = {
            "username": "Jack",
            "email": "jack@email.com",
            "password": "1234"
        }
        user2 = {
            "username": "John",
            "email": "john@email.com",
            "password": "1234"            
        }
        user3 = {
            "username": "James",
            "email": "james@email.com",
            "password": "1234"
        }
        
        self.user1 = User.objects.create(username=user1['username'], email=user1['email'], password=make_password(user1['password']))
        self.profile1 = Profile.objects.get(user__pk = self.user1.pk)
        self.profile1.is_doctor = True
        self.profile1.save()

        self.user2 = User.objects.create(username=user2['username'], email=user2['email'], password=make_password(user2['password']))
        self.profile2 = Profile.objects.get(user__pk = self.user2.pk)

        self.user3 = User.objects.create(username=user3['username'], email=user3['email'], password=make_password(user3['password']))
        self.profile3 = Profile.objects.get(user__pk = self.user3.pk)

    def test_model_creation(self):
        med_data = {
            "morning": ["medicine 1", "medicine 2"],
            "noon": ["medicine 3"],
            "night": ["medicine 2"]
        }
        data = {
            "patient": self.profile2,
            "doctor": self.profile1,
            "visit_date": datetime.date.today(),
            "meds": med_data
        }
        record = PatientHistory.objects.create(**data)
        self.assertEqual(record.patient.pk, self.profile2.pk)
        self.assertEqual(record.doctor.pk, self.profile1.pk)
        self.assertEqual(record.visit_date, data["visit_date"])
        self.assertEqual(record.meds, data['meds'])