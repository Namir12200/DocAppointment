from django.shortcuts import render
from .serializers import PatientHistorySerializer
from .models import PatientHistory
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from routines.models import Slot
from rest_framework import status
from django.shortcuts import get_object_or_404
from .permissions import IsRecordDoctorOrRecordPatient
# Create your views here.

class PatientHistoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = []
        patientID = request.query_params.get('patient_ID')
        doctorID = request.query_params.get('doctor_ID')
        if patientID is not None and doctorID is not None:
            records = PatientHistory.objects.filter(patient__pk=patientID).filter(doctor__pk=doctorID)
        elif doctorID is not None:
            records = PatientHistory.objects.filter(doctor__pk=doctorID)
        else:
            records = PatientHistory.objects.filter(patient__pk=patientID)

        serializer = PatientHistorySerializer(records, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PatientHistorySerializer(data=request.data)
        if serializer.is_valid():
            chosen_slot = Slot.objects.filter(patient__pk=request.data['patient_id']).filter(slot_date__doctor__doctor__pk=request.data['doctor_id'])[0]
            chosen_slot.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PatientHistoryDetailView(APIView):
    permission_classes = [IsAuthenticated, IsRecordDoctorOrRecordPatient]

    def get_object(self, pk):
        record = get_object_or_404(PatientHistory, pk=pk)
        self.check_object_permissions(self.request, record)
        return record
    
    def get(self, request, pk):
        record = self.get_object(pk=pk)
        serializer = PatientHistorySerializer(record)
        return Response(serializer.data)
    
    def put(self, request, pk):
        record = self.get_object(pk=pk)
        serializer = PatientHistorySerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        record = self.get_object(pk=pk)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)