from django.urls import path
from .views import PatientHistoryListView, PatientHistoryDetailView

urlpatterns = [
    path('record/', PatientHistoryListView.as_view(), name='record-list'),
    path('record/<int:pk>/', PatientHistoryDetailView.as_view(), name='record-detail'),
]