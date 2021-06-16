from django.contrib import admin
from blob import models

# Register your models here.

admin.site.register(models.BlobImage)
admin.site.register(models.BlobFile)
