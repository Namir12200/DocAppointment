from rest_framework.test import APITestCase
from accounts.models import Profile
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from routines.models import DoctorRoutine, SlotDate, Slot
from django.contrib.auth.hashers import make_password
import datetime

# Slot delete test has yet to be fixed

class DoctorRoutineViewsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="Jack", email="namirulislam16@email.com", password=make_password("1234"))
        self.profile = Profile.objects.get(user=self.user)
        url = reverse('token_obtain_pair')
        self.token = self.client.post(url, {"username": "Jack", "password": "1234"})
        self.user2 = User.objects.create(username="James", email="namirulislam@email.com", password=make_password("1234"))
        self.profile2 = Profile.objects.get(user=self.user2)
        self.profile2.is_doctor = True
        self.profile2.save()
        self.token2 = self.client.post(url, {"username": "James", "password": "1234"})
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
        self.doctor = DoctorRoutine.objects.create(doctor=self.profile2, institution=data['institution'], visiting_cost=data['visiting_cost'], new_customer_cost=data["new_customer_cost"], patients_per_day=data['patients_per_day'], days=data['days'])

        self.user3 = User.objects.create(username="John", email="john@email.com", password=make_password("1234"))
        self.profile3 = Profile.objects.get(user=self.user3)
        self.token3 = self.client.post(url, {"username": "John", "password": "1234"})
        self.doctor2 = DoctorRoutine.objects.create(doctor=self.profile3, institution=data['institution'], visiting_cost=data['visiting_cost'], new_customer_cost=data["new_customer_cost"], patients_per_day=data['patients_per_day'], days=data['days'])

    def test_create_unpermitted_routine(self):
        url = reverse("routine")
        data = {
            "doctor_id": self.profile.pk,
            "institution": "Japan Bangladesh",
            "visiting_cost": 500,
            "new_customer_cost": 700,
            "patients_per_day": 10,
            "days": [
                "MON",
                "THU",
                "SUN",
                "SAT"
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION=self.token.data["access"])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_routine(self):
        url = reverse("routine")
        self.profile.is_doctor = True
        data = {
            "doctor_id": self.profile.pk,
            "institution": "Japan Bangladesh",
            "visiting_cost": 500,
            "new_customer_cost": 700,
            "patients_per_day": 10,
            "days": [
                "MON",
                "THU",
                "SUN",
                "SAT"
            ]
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.data["access"])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['doctor']['id'], self.profile.pk)
        self.assertEqual(response.data['days'], ["SUN", "MON", "THU", "SAT"])

    def test_duplicate_routine(self):
        url = reverse("routine")
        self.profile2.is_doctor = True
        data = {
            "doctor_id": self.profile2.pk,
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


        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token2.data["access"])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data["Already Exists"], "A Routine for this doctor already exists")

    def test_get_routines(self):
        url = reverse("routine")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.data["access"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        url = reverse("routine") + "?name=Ame"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_routine(self):
        url = reverse("routine-detail", args=[self.doctor.pk])
        data = {
            "doctor_id": self.profile2.pk,
            "institution": "Japan Bangladesh",
            "visiting_cost": 500,
            "new_customer_cost": 700,
            "patients_per_day": 10,
            "days": [
                "SAT",
                "MON",
                "SAT",
                "TUE"
            ]
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token2.data["access"])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['doctor']['id'], self.profile2.pk)
        self.assertEqual(response.data['days'], ["MON", "TUE", "SAT"])

    def test_delete_routine(self):
        url = reverse("routine-detail", args=[self.doctor.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token2.data["access"])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class SlotDateViewsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="Jackson", email="jackson@email.com", password=make_password("1234"))
        self.profile = Profile.objects.get(user=self.user)
        url = reverse('token_obtain_pair')
        self.token = self.client.post(url, {"username": "Jackson", "password": "1234"})
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
        self.doctor = DoctorRoutine.objects.create(doctor=self.profile, institution=data['institution'], visiting_cost=data['visiting_cost'], new_customer_cost=data["new_customer_cost"], patients_per_day=data['patients_per_day'], days=data['days'])

        self.user2 = User.objects.create(username="James", email="namirulislam@email.com", password=make_password("1234"))
        self.profile2 = Profile.objects.get(user=self.user2)
        self.token2 = self.client.post(url, {"username": "James", "password": "1234"})
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
        self.doctor2 = DoctorRoutine.objects.create(doctor=self.profile2, institution=data['institution'], visiting_cost=data['visiting_cost'], new_customer_cost=data["new_customer_cost"], patients_per_day=data['patients_per_day'], days=data['days'])
        self.slotdate = SlotDate.objects.create(doctor = self.doctor2, appointment_date=datetime.date(2024, 7, 15), total_patients = 0)

        self.user3 = User.objects.create(username="John", email="john@email.com", password=make_password("1234"))
        self.profile3 = Profile.objects.get(user=self.user3)
        self.token3 = self.client.post(url, {"username": "John", "password": "1234"})


    def test_get_slotdates(self):
        url = reverse('slotDate-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token2.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_specific_slot(self):
        url = reverse('slotDate-detail', args=[self.slotdate.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token2.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_specific_slot(self):
        url = reverse('slotDate-detail', args=[self.slotdate.pk])
        data = {
            "doctor_id": self.doctor.pk,
            "appointment_date": datetime.date(2024, 7, 15),
            "total_patients": 1,
        }

        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.data['access'])
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token2.data['access'])
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_patients'], data['total_patients'])

    def test_delete_specific_slot(self):
        url = reverse('slotDate-detail', args=[self.slotdate.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token.data['access'])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token2.data['access'])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class SlotViewsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="Jackson", email="jackson@email.com", password=make_password("1234"))
        self.profile = Profile.objects.get(user=self.user)
        url = reverse('token_obtain_pair')
        self.token = self.client.post(url, {"username": "Jackson", "password": "1234"})
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
        self.doctor = DoctorRoutine.objects.create(doctor=self.profile, institution=data['institution'], visiting_cost=data['visiting_cost'], new_customer_cost=data["new_customer_cost"], patients_per_day=data['patients_per_day'], days=data['days'])

        self.user2 = User.objects.create(username="James", email="james@email.com", password=make_password("1234"))
        self.profile2 = Profile.objects.get(user=self.user2)
        self.token2 = self.client.post(url, {"username": "James", "password": "1234"})

        self.user3 = User.objects.create(username="John", email="john@email.com", password=make_password("1234"))
        self.profile3 = Profile.objects.get(user=self.user3)
        self.token3 = self.client.post(url, {"username": "John", "password": "1234"})
        self.slotdate = SlotDate.objects.create(doctor = self.doctor, appointment_date=datetime.date(2024, 7, 15), total_patients = 0)
        self.slot = Slot.objects.create(patient=self.profile3, slot_date=self.slotdate, description="I don't feel so good")

        
    def test_get_slots(self):
        url = reverse('slot-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token3.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        url = reverse('slot-list') + "?date_ID="+str(self.slot.slot_date.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['patient']['user']['username'], self.user3.username)

    def test_post_slot(self):
        url = reverse('slot-list')
        data = {
            "description": "I am very sick",
            "patient_id": self.profile2.pk,
            "routine_id": self.doctor.pk
        }
        last_date = self.doctor.get_slot_date(testing=False)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + self.token2.data['access'])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['patient']['id'], self.profile2.pk)
        self.assertEqual(str(last_date.appointment_date), response.data['slot_date']['appointment_date'])

    def test_get_specific_slot(self):
        url = reverse('slot-detail', args=[self.slot.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token2.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token3.data['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_specific_slot(self):
        url = reverse('slot-detail', args=[self.slot.pk])
        data = {
            "description": "I think I am dying"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.data['access'])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token2.data['access'])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token3.data['access'])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)