import os
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from blob import models, serializers


# For creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create context for serializer
serializer_context = {'request': Request(request)}


FILE_URL = reverse('blob:blobfile-list')


def file_detail_url(blob_file_id):
    return reverse('blob:blobfile-detail', args=[blob_file_id])


def sample_blob_file(user, **kwargs):
    defaults = {
        'name': 'Test file',
        'description': 'test description'
    }
    defaults.update(kwargs)
    return models.BlobFile.objects.create(owner=user, **defaults)


class PublicBlobFileApiTest(TestCase):
    """test public (unauthenticated) blob file api access"""
    def setUp(self):
        self.client = APIClient()

    def test_unauthentication_required(self):
        """test that authentication is required"""
        res = self.client.get(FILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBlobFileApiTest(TestCase):
    """test authenticated access to the blob file api endpionts"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.blob_file = sample_blob_file(user=self.user)

    def tearDown(self):
        self.blob_file.file.delete()
        if os.path.exists('test_file_for_file_uploads.txt'):
            os.remove('test_file_for_file_uploads.txt')

    def test_retrieve_blob_files(self):
        """test retrieving a list of blob files"""
        sample_blob_file(user=self.user, name='Test file 2')
        files = models.BlobFile.objects.all()
        serializer = serializers.BlobFileSerializer(files, many=True, context=serializer_context)

        res = self.client.get(FILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_blob_files_not_limited_to_user(self):
        """test that all created files are returned"""
        user2 = get_user_model().objects.create_user(
            'testuser2@gmail.com',
            'testpass2'
        )
        sample_blob_file(user=user2)

        files = models.BlobFile.objects.all()
        serializer = serializers.BlobFileSerializer(files, many=True, context=serializer_context)

        res = self.client.get(FILE_URL)
        print(f"\n {res.data} \n")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_view_blob_file_detail(self):
        """test viewing a blob file detail"""
        serializer = serializers.BlobFileSerializer(self.blob_file, context=serializer_context)
        url = file_detail_url(self.blob_file.id)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_sample_blob_file(self):
        """test creating a simple blob file without a file"""
        payload = {
            'name': 'Test image',
            'description': 'test file 2'
        }
        res = self.client.post(FILE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        file = models.BlobFile.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(file, key))

    def test_creating_full_blob_file(self):
        """test creating a blob file with an uploaded file"""
        with open('test_file_for_file_uploads.txt', 'w+') as file:
            file.write('hello')
            file.seek(0)
            payload = {
                'name': 'Test txt file',
                'description': 'test text file description',
                'file': file
            }
            res = self.client.post(FILE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('file', res.data)

    def test_partial_update_blob_file(self):
        """test updating a blob file using patch"""
        payload = {
            'name': 'Different file 2'
        }
        url = file_detail_url(self.blob_file.id)

        res = self.client.patch(url, payload)

        self.blob_file.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.blob_file.name, payload['name'])

    def test_full_update_blob_file(self):
        """test updating a blob file using put"""
        with open('test_file_for_file_uploads.txt', 'w+') as file:
            file.write('hello')
            file.seek(0)
            payload = {
                'name': 'Test txt file',
                'description': 'test text file description',
                'file': file
            }
            url = file_detail_url(self.blob_file.id)

            res = self.client.put(url, payload)

        self.blob_file.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.blob_file.name, payload['name'])
        self.assertEqual(self.blob_file.description, payload['description'])
        self.assertIn('file', res.data)

    def test_upload_file_to_blob_file(self):
        """test updating a sample blob file with an image"""
        url = file_detail_url(self.blob_file.id)
        with open('test_file_for_file_uploads.txt', 'w+') as file:
            file.write('hello 2')
            file.seek(0)
            res = self.client.patch(url, {'file': file}, format='multipart')

        self.blob_file.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('file', res.data)

    def test_upload_invalid_file(self):
        """test that uploading an invalid file returns an error"""
        url = file_detail_url(self.blob_file.id)
        res = self.client.patch(url, {'file': 'ff'})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
