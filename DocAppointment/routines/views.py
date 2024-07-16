from rest_framework.views import APIView
from .models import DoctorRoutine, Slot, SlotDate
from accounts.serializers import ProfileSerializer
from .serializers import DoctorRoutineSerializer, SlotSerializer, SlotDateSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permissions import IsRoutineOwnerOrReadOnly, IsSlotDateOwnerOrReadOnly, IsSlotOwnerOrReadOnly
from django.db.utils import IntegrityError
import datetime
from .tasks import removeSlotDate

day_order = {
    "SUN": 0,
    "MON": 1,
    "TUE": 2,
    "WED": 3,
    "THU": 4,
    "FRI": 5,
    "SAT": 6
}

def sort_day(day):
    return day_order[day]

def get_closest_day(routine, current_day=(datetime.datetime.now().weekday() + 1) % 7):
    closestDayVal = 8
    for day in routine.days:
        day_difference = day_order[day] - current_day

        if day_difference <= 0:
            day_difference += 7

        closestDayVal = min(closestDayVal, day_difference)

    return closestDayVal

# Create your views here.
class DoctorRoutineListView(APIView):
    permission_classes = [IsAuthenticated, IsRoutineOwnerOrReadOnly]

    def get(self, request):
        name = request.query_params.get('name')
        routines = []
        if name is not None:
            routines = DoctorRoutine.objects.filter(doctor__user__username__icontains=name)
        else:
            routines = DoctorRoutine.objects.all()

        serializer = DoctorRoutineSerializer(routines, many=True)
        return Response(serializer.data)


    def post(self, request):
        # routine = DoctorRoutine.objects.filter(doctor__user=request.user)
        # if len(routine) > 0:
        #     return Response({
        #         "Already Exists": "A Routine for this doctor already exists"
        #     })

        try:
            request.data['days'] = sorted(list( set( request.data.get('days') ) ), key=sort_day)
            serializer = DoctorRoutineSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({
                "Already Exists": "A Routine for this doctor already exists"
            })

    
class DoctorRoutineDetailView(APIView):
    permission_classes = [IsAuthenticated, IsRoutineOwnerOrReadOnly]

    def get_object(self, pk):
        routine = get_object_or_404(DoctorRoutine, pk=pk)
        self.check_object_permissions(self.request, routine)
        return routine
    
    def get(self, request, pk):
        routine = self.get_object(pk=pk)
        serializer = DoctorRoutineSerializer(routine)
        return Response(serializer.data)
    
    def put(self, request, pk):
        request.data['days'] = sorted(list( set( request.data.get('days') ) ), key=sort_day)
        routine = self.get_object(pk=pk)
        serializer = DoctorRoutineSerializer(routine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        routine = self.get_object(pk=pk)
        routine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SlotDateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        slotDates = SlotDate.objects.filter(doctor__doctor__user__pk=request.user.pk)
        
        serializer = SlotDateSerializer(slotDates, many=True)
        return Response(serializer.data)

class SlotDateDetailView(APIView):
    permission_classes = [IsAuthenticated, IsSlotDateOwnerOrReadOnly]

    def get_object(self, pk):
        slotDate = get_object_or_404(SlotDate, pk=pk)
        self.check_object_permissions(self.request, slotDate)
        return slotDate

    def get(self, request, pk):
        slotDate = self.get_object(pk=pk)
        serializer = SlotDateSerializer(slotDate)
        return Response(serializer.data)
    
    def put(self, request, pk):
        slotDate = self.get_object(pk=pk)
        serializer = SlotDateSerializer(slotDate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        slotDate = self.get_object(pk=pk)
        slotDate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Fix slot delete to reduce total number of patients in slot date

class SlotListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):    
        slots = []
        slotDate_id = request.query_params.get("date_ID")
        if slotDate_id is not None:
            slots = Slot.objects.filter(slot_date__pk=slotDate_id)
        else:
            slots = Slot.objects.filter(patient__user__pk=request.user.pk)
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data)

    
    def post(self, request):
        serializer = SlotSerializer(data=request.data)
        if serializer.is_valid():
            slot = serializer.create(validated_data=request.data)
            return Response({
                "id": slot.pk,
                "patient": ProfileSerializer(slot.patient).data,
                "slot_date": SlotDateSerializer(slot.slot_date).data,
                "serial": slot.serial 
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SlotDetailView(APIView):
    permission_classes = [IsAuthenticated, IsSlotOwnerOrReadOnly]

    def get_object(self, pk):
        slot = get_object_or_404(Slot, pk=pk)
        self.check_object_permissions(self.request, slot)
        return slot

    def get(self, request, pk):
        slot = self.get_object(pk=pk)
        serializer = SlotSerializer(slot)
        return Response(serializer.data)
    
    def put(self, request, pk):
        slot = self.get_object(pk=pk)
        serializer = SlotSerializer(slot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        slot = self.get_object(pk=pk)
        slot_date = slot.slot_date
        slot.delete()
        if(slot_date.total_patients == 0):
            removeSlotDate.delay(slot_date.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)