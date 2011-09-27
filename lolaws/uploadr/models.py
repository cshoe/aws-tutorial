from django.db import models
from django.conf import settings

from sorl.thumbnail import ImageField
from storages.backends.s3boto import S3BotoStorage

from lolaws.core.utils import get_storage

stored_image_storage = get_storage(storage_name='StoredImage', use_local_storage=getattr(settings, "DEBUG", False))

# Create your models here.
class StoredImage(models.Model):
    image = ImageField(upload_to="filez", storage=stored_image_storage)
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-upload_date']
