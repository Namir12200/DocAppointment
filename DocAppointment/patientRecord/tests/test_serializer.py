from rest_framework.test import APITestCase
from patientRecord.serializers import PatientHistorySerializer
from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib.auth.hashers import make_password
import datetime
import json
from rest_framework import serializers

class PatientHistorySerializerTestCase(APITestCase):
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

    def test_patientHistory_serializer(self):
        med_data = {
            "morning": ["medicine 1", "medicine 2"],
            "noon": ["medicine 3"],
            "night": ["medicine 2"]
        }
        data = {
            "patient_id": self.profile1.pk,
            "doctor_id": self.profile1.pk,
            "visit_date": datetime.date.today(),
            "meds": json.dumps(med_data)
        }


        serializer = PatientHistorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors)

        data['patient_id'] = self.profile2.pk
        serializer = PatientHistorySerializer(data=data)
        self.assertTrue(serializer.is_valid())        