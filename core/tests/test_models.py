from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from blob import models as blob_models


def sample_user(email='test@gmail.com', password='testpass'):
    """create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """test creating and retrieving models"""
    # Test creating and saving users with the custom user model
    def test_create_user_with_email_successful(self):
        """test creating a user with email is successful"""
        email = 'test@gmail.com'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_is_normalized(self):
        """test that the new user email is normalized"""
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(
            email,
            'testpass'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test creating new user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass')

    def test_create_new_superuser(self):
        """test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'testpass'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_blob_image_str(self):
        """test the blob image string representation"""
        blob_image = blob_models.BlobImage.objects.create(
            owner=sample_user(),
            name="Blank Image",
            description="A simple black image",
        )
        self.assertEqual(str(blob_image), blob_image.name)

    def test_blob_file_str(self):
        """test the string representation of the blob file"""
        blob_file = blob_models.BlobFile.objects.create(
            owner=sample_user(),
            name="Empty File",
            description="An empty file",
        )
        self.assertEqual(str(blob_file), blob_file.name)
