import tempfile
from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status, permissions, authentication
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from blob import models, serializers


# For creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create context for serializer
# serializer_context = {'request': Request(request)}
serializer_context = {'request': Request(request)}

IMAGE_URL = reverse('blob:blobimage-list')


def image_detail_url(blob_image_id):
    """return url for recipe detail"""
    return reverse('blob:blobimage-detail', args=[blob_image_id])


def sample_blob_image(user, **kwargs):
    """create and return a blob image"""
    defaults = {
        'name': 'sample image',
    }
    defaults.update(kwargs)
    return models.BlobImage.objects.create(owner=user, **defaults)


class PublicBlobImageApiTest(TestCase):
    """test unauthenticated blob image api requests"""
    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(IMAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBlobImageApiTest(TestCase):
    """test authenticated blob image api requests"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.blob_image = sample_blob_image(user=self.user)

    def tearDown(self):
        self.blob_image.image.delete()

    def test_retrieve_blob_images(self):
        """test retrieving a list of blob images"""
        sample_blob_image(user=self.user, name='Test image 1')
        images = models.BlobImage.objects.all()
        serializer = serializers.BlobImageSerializer(images, many=True, context=serializer_context)

        res = self.client.get(IMAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_blob_images_not_limited_to_user(self):
        """test that the images for all users are returned"""
        user2 = get_user_model().objects.create_user(
            'testuser2@gmail.com',
            'testpass2'
        )
        sample_blob_image(user=user2)

        images = models.BlobImage.objects.all()
        serializer = serializers.BlobImageSerializer(images, many=True, context=serializer_context)

        res = self.client.get(IMAGE_URL)
        print(f"\n {res.data} \n")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_view_blob_image_detail(self):
        """test viewing a blob image detail"""
        serializer = serializers.BlobImageSerializer(self.blob_image, context=serializer_context)
        url = image_detail_url(self.blob_image.id)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_sample_blob_image(self):
        """test creating a sample blob image without an image file"""
        payload = {
            'name': 'A real image',
            'description': 'Some test description'
        }
        res = self.client.post(IMAGE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        image = models.BlobImage.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(image, key))

    def test_creating_full_blob_image(self):
        """test creating a blob image with a description and an uploaded image"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            payload = {
                'name': 'Full image',
                'description': 'test images',
                'image': ntf
            }
            res = self.client.post(IMAGE_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('image', res.data)

    def test_partial_update_blob_image(self):
        """test updating an image with patch"""
        payload = {
            'name': 'Updated image'
        }

        url = image_detail_url(self.blob_image.id)
        res = self.client.patch(url, payload)

        self.blob_image.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.blob_image.name, payload['name'])

    def test_full_update_blob_image(self):
        """test updating an image with patch"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            payload = {
                'name': 'Updated image 2',
                'description': 'test description',
                'image': ntf
            }

            url = image_detail_url(self.blob_image.id)
            res = self.client.put(url, payload)

        self.blob_image.refresh_from_db()
        self.assertEqual(self.blob_image.name, payload['name'])
        self.assertEqual(self.blob_image.description, payload['description'])
        self.assertIn('image', res.data)

    def test_upload_image_to_blob_image(self):
        """test updating a sample blob image with an image"""
        url = image_detail_url(self.blob_image.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.patch(url, {'image': ntf}, format='multipart')

        self.blob_image.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)

    def test_upload_invalid_image(self):
        """test that uploading an invalid image produces an error"""
        url = image_detail_url(self.blob_image.id)
        res = self.client.patch(url, {'image': 'bb'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
