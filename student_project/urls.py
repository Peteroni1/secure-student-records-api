# student_project/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from records.views import StudentRecordViewSet

router = DefaultRouter()
router.register(r'student-records', StudentRecordViewSet, basename='student-records')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication Routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('api/', include(router.urls)),
]