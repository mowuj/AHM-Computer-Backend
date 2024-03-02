from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()


router.register('', views.CartViewset)
router.register('cartProduct', views.CartProductViewset)


urlpatterns = [
    path('', include(router.urls)),
]
