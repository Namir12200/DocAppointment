from django.dispatch import receiver
from django.db.models.signals import pre_delete
from .models import Slot

@receiver(pre_delete, sender=Slot)
def decrement_slot(sender, instance, **kwargs):
    instance.slot_date.total_patients -= 1
    instance.slot_date.save()
