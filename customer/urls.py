from django.urls import include, path
from .views import UserLoginApiView, UserLogoutView, CustomerDataView, UserRegistrationApiView, activate
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('data', CustomerDataView, basename='data')
urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('active/<uid64>/<token>/', activate, name = 'activate'),
]