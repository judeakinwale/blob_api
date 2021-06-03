from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from core import serializers

# Create your views here.


class CreateUserApiView(generics.CreateAPIView):
    """create a new user"""
    serializer_class = serializers.UserSerializer


class ManageUserApiView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """retrieve and return the authenticated user"""
        return self.request.user
