from rest_framework.test import APITestCase
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from routines.models import DoctorRoutine, SlotDate, Slot
import datetime
from django.urls import reverse
from rest_framework import status
from patientRecord.models import PatientHistory
import json

class PatientHistoryViewTestCase(APITestCase):
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
        url = reverse('token_obtain_pair')
        self.token = self.client.post(url, {"username": user1['username'], "password": user1['password']})

        self.user2 = User.objects.create(username=user2['username'], email=user2['email'], password=make_password(user2['password']))
        self.profile2 = Profile.objects.get(user__pk = self.user2.pk)
        self.token2 = self.client.post(url, {"username": user2['username'], "password": user2['password']})

        self.user3 = User.objects.create(username=user3['username'], email=user3['email'], password=make_password(user3['password']))
        self.profile3 = Profile.objects.get(user__pk = self.user3.pk)
        self.token3 = self.client.post(url, {"username": user3['username'], "password": user3['password']})

        data = {
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

        med_data = {
            "morning": ["medicine 1", "medicine 2"],
            "noon": ["medicine 3"],
            "night": ["medicine 2"]
        }

        self.doctor = DoctorRoutine.objects.create(doctor=self.profile1, institution=data['institution'], visiting_cost=data['visiting_cost'], new_customer_cost=data["new_customer_cost"], patients_per_day=data['patients_per_day'], days=data['days'])
        self.slotdate = SlotDate.objects.create(doctor = self.doctor, appointment_date=datetime.date(2024, 7, 15), total_patients = 0)
        self.slot = Slot.objects.create(patient=self.profile3, slot_date=self.slotdate, description="I don't feel so good")
        self.slot2 = Slot.objects.create(patient = self.profile2, slot_date=self.slotdate, description="I feel quite sick") 
        self.record = PatientHistory.objects.create(patient=self.profile2, doctor=self.profile1, visit_date=self.slotdate.appointment_date, meds=json.dumps(obj=med_data))

    def test_get_slots(self):
        url = reverse('record-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        
        url = reverse('record-list') + '?patient_ID=' + str(self.profile1.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        url = reverse('record-list') + '?doctor_ID=' + str(self.profile1.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        url = reverse('record-list') + '?doctor_ID=' + str(self.profile1.pk) + '&patient_ID=' + str(self.profile2.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        url = reverse('record-list') + '?patient_ID=' + str(self.profile2.pk)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token2.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        url = reverse('record-list') + '?patient_ID=' + str(self.profile3.pk)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token3.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_post_slot(self):
        url = reverse('record-list')
        med_data = {
            "morning": ["medicine 1", "medicine 2"],
            "noon": ["medicine 3"],
            "night": ["medicine 2"]
        }
        data = {
            "patient_id": self.profile3.pk,
            "doctor_id": self.profile1.pk,
            "meds": json.dumps(med_data),
            "visit_date": str(self.slot.slot_date.appointment_date)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.data['access'])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['patient']['id'], self.profile3.pk)
        self.assertEqual(response.data['doctor']['id'], self.profile1.pk)
        # print("In testing: ", response.data['visit_date'], str(self.slot.slot_date.appointment_date))
        self.assertEqual(response.data['visit_date'], str(datetime.date.today()))
        self.assertEqual(response.data['meds'], data['meds'])

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_specific_slot(self):
        url = reverse('record-detail', args=[self.record.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token3.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token2.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_specific_slot(self):
        url = reverse('record-detail', args=[self.record.pk])
        med_data = {
            "morning": ["medicine 1", "medicine 2"],
            "noon": ["medicine 3"],
            "night": ["medicine 4"]
        }
        data = {
            "patient_id": self.profile2.pk,
            "doctor_id": self.profile1.pk,
            "meds": json.dumps(med_data),
            "visit_date": self.slotdate.appointment_date
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token2.data['access'])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.data['access'])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.data['meds'])['night'], med_data['night'])

    def test_delete_specific_slot(self):
        url = reverse('record-detail', args=[self.record.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token2.data['access'])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.data['access'])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)