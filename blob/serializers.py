from rest_framework import serializers
from blob import models


class BlobImageSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the blob image model"""
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.BlobImage
        fields = ['id', 'url', 'owner', 'name', 'description', 'image']
        extra_kwargs = {
            'url': {'view_name': 'blob:blobimage-detail'}
        }


class BlobFileSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the blob file model"""
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.BlobFile
        fields = ['id', 'url', 'owner', 'name', 'description', 'file']
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'view_name': 'blob:blobfile-detail'}
        }
