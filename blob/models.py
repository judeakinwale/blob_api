from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.


class BlobImage(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Owner"), on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="images/%Y/%m/%d/", null=True)

    class Meta:
        verbose_name = _("BlobImage")
        verbose_name_plural = _("BlobImages")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blob:image_detail", kwargs={"pk": self.pk})


class BlobFile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Owner"), on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="files/%Y/%m/%d/", max_length=100, null=True)

    class Meta:
        verbose_name = _("BlobFile")
        verbose_name_plural = _("BlobFiles")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blob:file_detail", kwargs={"pk": self.pk})
