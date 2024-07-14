from django.urls import path
from .views import DoctorRoutineListView, DoctorRoutineDetailView, SlotDateListView, SlotDateDetailView, SlotListView, SlotDetailView

urlpatterns = [
    path('routine/', DoctorRoutineListView.as_view(), name="routine"),
    path('routine/<int:pk>/', DoctorRoutineDetailView.as_view(), name="routine-detail"),
    path('slotDate/', SlotDateListView.as_view(), name="slotDate-list"),
    path('slotDate/<int:pk>/', SlotDateDetailView.as_view(), name="slotDate-detail"),
    path('slot/', SlotListView.as_view(), name="slot-list"),
    path('slot/<int:pk>/', SlotDetailView.as_view(), name='slot-detail'),
]