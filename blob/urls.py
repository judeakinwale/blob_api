from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blob import views


app_name = 'blob'

router = DefaultRouter()
router.register('image', views.BlobImageViewSet)
router.register('file', views.BlobFileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
