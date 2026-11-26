from rest_framework.permissions import BasePermission
from api.models import Problem
from student.models import StudentProfile


class OwnerOnly(BasePermission):

    def has_object_permission(self, request, view, obj):


        if isinstance(obj,Problem):
        
            return request.user == obj.posted_by
        
        elif isinstance(obj,StudentProfile):
            
            return request.user == obj.user