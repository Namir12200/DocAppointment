from rest_framework import permissions

class IsRecordDoctorOrRecordPatient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.patient.user == request.user or obj.doctor.user == request.user
        return obj.doctor.user == request.user