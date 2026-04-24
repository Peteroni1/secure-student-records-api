# records/views.py
import logging
import time
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import StudentRecord, PaymentTransaction
from .serializers import StudentRecordSerializer, PaymentTransactionSerializer
from .permissions import IsAdminOrFaculty, IsOwnerOrStaff

security_logger = logging.getLogger('records.security')

# Simple in-memory rate limiter tracker for Python 3.14 compatibility
IP_TRACKER = {}

class StudentRecordViewSet(ModelViewSet):
    serializer_class = StudentRecordSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name__in=['Admin', 'Faculty']).exists():
            return StudentRecord.objects.all()
        return StudentRecord.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdminOrFaculty]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        return [permission() for permission in permission_classes]

class SecurePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Universal Rate Limiting Logic (5 requests per minute)
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        current_time = time.time()
        
        if ip not in IP_TRACKER:
            IP_TRACKER[ip] = []
            
        # Clean out timestamps older than 60 seconds
        IP_TRACKER[ip] = [t for t in IP_TRACKER[ip] if current_time - t < 60]
        
        if len(IP_TRACKER[ip]) >= 5:
            security_logger.warning(
                f"SECURITY ALERT: Rate Limit breach / Brute Force detected from IP: {ip}"
            )
            return Response(
                {"error": "Too many transaction attempts. Rate limit exceeded."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
            
        # Record the successful attempt timestamp
        IP_TRACKER[ip].append(current_time)

        serializer = PaymentTransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)