from rest_framework import permissions

class IsRoutineOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user == obj.doctor.user) and (obj.doctor.is_doctor)
    
class IsSlotDateOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.doctor.doctor.user == request.user
    
class IsSlotOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user == obj.patient.user or request.user == obj.slot_date.doctor.doctor.user
        return request.user == obj.patient.user