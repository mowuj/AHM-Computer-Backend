from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('list', views.BillingDetailsViewset) 

urlpatterns = [
    path('', include(router.urls)),
    path('user-billing-details/', views.ShowUserBillingDetails.as_view(), name='user-billing-details'),
    path('user-billing-details-update/<int:id>/', views.UpdateBillingDetails.as_view(), name='user-billing-details-update'),
]