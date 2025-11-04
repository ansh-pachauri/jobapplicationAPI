from rest_framework.routers import DefaultRouter
from .views import ApplicantViewSet, JobViewSet, ApplicationSet, apply
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



router = DefaultRouter()
router.register(r'applicants', ApplicantViewSet,basename='applicant')
router.register(r'jobs', JobViewSet,basename='job')
router.register(r'applications', ApplicationSet,basename='application')

urlpatterns = [
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh token
    
    path('apply/', apply, name='apply'),
    path('', include(router.urls)),
]

