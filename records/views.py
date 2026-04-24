# records/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import StudentRecord
from .serializers import StudentRecordSerializer
from .permissions import IsAdminOrFaculty, IsOwnerOrStaff

class StudentRecordViewSet(ModelViewSet):
    serializer_class = StudentRecordSerializer

    def get_queryset(self):
        user = self.request.user
        # Admins and Faculty have administrative rights to view all records
        if user.groups.filter(name__in=['Admin', 'Faculty']).exists():
            return StudentRecord.objects.all()
        # Students can only see their own records
        return StudentRecord.objects.filter(owner=user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the owner of the record
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            # Only Admins can create or delete
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            # Faculty and Admins can update
            permission_classes = [IsAdminOrFaculty]
        else:
            # Viewing (list/retrieve) requires authentication and object ownership validation
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
            
        return [permission() for permission in permission_classes]