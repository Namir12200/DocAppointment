from django.db import models
from accounts.models import Profile

# Create your models here.
class PatientHistory(models.Model):
    patient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='doctor')
    visit_date = models.DateField(auto_now_add=True)
    meds = models.JSONField()

    class Meta:
        unique_together = ('patient', 'doctor', 'visit_date')