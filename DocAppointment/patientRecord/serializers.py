from rest_framework import serializers
from .models import PatientHistory
from accounts.models import Profile
from accounts.serializers import ProfileSerializer

class PatientHistorySerializer(serializers.ModelSerializer):
    doctor = ProfileSerializer(read_only=True)
    patient = ProfileSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', queryset=Profile.objects.all(), write_only = True)
    patient_id = serializers.PrimaryKeyRelatedField(source='patient', queryset=Profile.objects.all(), write_only = True)

    class Meta:
        model = PatientHistory
        fields = "__all__"

    def validate(self, data):
        if data['patient'] == data['doctor']:
            raise serializers.ValidationError({"doctor": "You cannot just treat yourself"})
        return data