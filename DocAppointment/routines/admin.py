from django.contrib import admin
from .models import DoctorRoutine, Slot, SlotDate
# Register your models here.

admin.site.register(DoctorRoutine)
admin.site.register(SlotDate)
admin.site.register(Slot)