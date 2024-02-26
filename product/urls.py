from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()


router.register('list', views.ProductViewset)
router.register('category', views.CategoryViewset)
router.register('brand', views.BrandViewset)
router.register('review', views.ReviewViewset)
router.register('add_to_card', views.CartViewset)


urlpatterns = [
    path('', include(router.urls)),
]
