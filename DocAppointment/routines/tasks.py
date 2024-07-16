from celery import shared_task
from .models import SlotDate
import datetime
from django_celery_beat.models import CrontabSchedule, PeriodicTask

@shared_task
def removeSlotDate(slot_date_id):
    slot_date = SlotDate.objects.get(pk=slot_date_id)
    slot_date.delete()

@shared_task
def removeOldSlotDates():
    slot_dates = SlotDate.objects.filter(appointment_date__lt=datetime.date.today())
    for slot_date in slot_dates:
        slot_date.delete()

schedule, _ = CrontabSchedule.objects.get_or_create(
    minute="0",
    hour="0",
    day_of_week="*",
    day_of_month="*",
    month_of_year="*"
)

try:
    PeriodicTask.objects.get_or_create(
        crontab=schedule,
        name='remove-unused-slotDates',
        task='routines.tasks.removeOldSlotDates'
    )
except Exception:
    pass