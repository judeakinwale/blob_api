from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blob import views


app_name = 'blob'

router = DefaultRouter()
router.register('image', views.BlobImageViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
