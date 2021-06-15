from rest_framework import serializers
from blob import models


class BlobImageSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the blob image model"""
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.BlobImage
        fields = ['id', 'owner', 'name', 'description', 'image']
        extra_kwargs = {
            'url': {
                'view_name': 'blobimage-detail'
            }
        }
