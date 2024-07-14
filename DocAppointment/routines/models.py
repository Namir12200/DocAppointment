from django.db import models
from accounts.models import Profile
from django.contrib.postgres.fields import ArrayField
import datetime

# Create your models here.
day_order = {
    "SUN": 0,
    "MON": 1,
    "TUE": 2,
    "WED": 3,
    "THU": 4,
    "FRI": 5,
    "SAT": 6
}

class DoctorRoutine(models.Model):
    day_choices = [
        ("SUN", "Sunday"),
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
    ]
    doctor = models.OneToOneField(Profile, on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    visiting_cost = models.IntegerField(null=False)
    new_customer_cost = models.IntegerField(null=False)
    patients_per_day = models.PositiveSmallIntegerField(null=False)
    days = ArrayField(models.CharField(choices=day_choices, max_length=3, unique=True), size=7)

    def get_closest_day(self, current_day=(datetime.datetime.now().weekday() + 1) % 7):
        closestDayVal = 8
        for day in self.days:
            day_difference = day_order[day] - current_day

            if day_difference <= 0:
                day_difference += 7

            closestDayVal = min(closestDayVal, day_difference)

        return closestDayVal

    def get_slot_date(self, testing=True):
        slotDate = SlotDate.objects.filter(doctor=self.pk).order_by('-appointment_date')[:1]
        closestDayVal = 8
        new_date = None

        if len(slotDate) == 0 or slotDate[0].appointment_date < datetime.date.today():
            closestDayVal = self.get_closest_day()
            new_date = datetime.date.today() + datetime.timedelta(days=closestDayVal)
        
        elif len(slotDate) > 0 and slotDate[0].total_patients < self.patients_per_day:
            return slotDate[0]

        else:
            closestDayVal = self.get_closest_day(current_day=(slotDate[0].appointment_date.weekday() + 1) % 7)
            new_date = slotDate[0].appointment_date + datetime.timedelta(days=closestDayVal)

        slotDate = SlotDate(doctor=self, appointment_date=new_date, total_patients=0)
        if testing:
            slotDate.save()

        return slotDate            

class SlotDate(models.Model):
    doctor = models.ForeignKey(DoctorRoutine, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    total_patients = models.IntegerField()

class Slot(models.Model):
    patient = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField()
    slot_date = models.ForeignKey(SlotDate, on_delete=models.CASCADE)
    serial = models.DateTimeField(auto_now_add=True)