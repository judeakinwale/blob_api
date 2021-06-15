from django.http import request
from django.shortcuts import render
from rest_framework import viewsets, permissions
from blob import serializers, models

# Create your views here.


class BlobImageViewSet(viewsets.ModelViewSet):
    """viewset for images in blob storage"""
    queryset = models.BlobImage.objects.all()
    serializer_class = serializers.BlobImageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """create a new image"""
        return serializer.save(owner=self.request.user)


class BlobFileViewSet(viewsets.ModelViewSet):
    """viewset for files in blob storage"""
    queryset = models.BlobFile.objects.all()
    serializer_class = serializers.BlobFileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """create a new file"""
        return serializer.save(owner=self.request.user)
