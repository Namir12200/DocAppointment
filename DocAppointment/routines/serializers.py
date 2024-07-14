from rest_framework import serializers
from .models import DoctorRoutine, SlotDate, Slot
from accounts.serializers import ProfileSerializer
from .models import Profile

class DoctorRoutineSerializer(serializers.ModelSerializer):
    doctor = ProfileSerializer(read_only=True)
    days = serializers.ListField(
        child = serializers.CharField()
    )
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', queryset=Profile.objects.all(), write_only=True)

    class Meta:
        model = DoctorRoutine
        fields = "__all__"

class SlotDateSerializer(serializers.ModelSerializer):
    doctor = DoctorRoutineSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', queryset=DoctorRoutine.objects.all(), write_only=True)
    class Meta:
        model = SlotDate
        fields = "__all__"

class SlotSerializer(serializers.ModelSerializer):
    patient = ProfileSerializer(read_only=True)
    slot_date = SlotDateSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(source='patient', queryset=Profile.objects.all(), write_only=True)
    routine_id = serializers.PrimaryKeyRelatedField(queryset=DoctorRoutine.objects.all(), write_only=True, allow_null=True)

    class Meta:
        model = Slot
        fields = "__all__"



    def create(self, validated_data):
        routine_id = validated_data.get('routine_id')
        routine = DoctorRoutine.objects.get(pk=routine_id)
        slotDate = routine.get_slot_date()
        slotDate.total_patients += 1
        slotDate.save()
        validated_data['slot_date_id'] = slotDate.pk

        slot = Slot(patient_id=validated_data.get('patient_id'), description=validated_data.get('description'), slot_date_id=validated_data.get('slot_date_id'))
        slot.save()
        return slot