from django.conf import settings
from django.core.files.storage import default_storage

from storages.backends.s3boto import S3BotoStorage

def get_storage(storage_name=None, use_default_bucket=False, use_default_url=False, use_local_storage=False):
    """
    Highly recommended that a URL is used for the bucket or a Cloudfront url is provided. Otherwise, django-storages
    hits the AWS api to generate a URL on every lookup.

    """
    bucket_names = getattr(settings, 'S3_BUCKET_NAMES', {})

    bucket_name = None
    try:
        bucket_name = bucket_names[storage_name]
    except KeyError:
        if use_default_bucket:
            try:
                bucket_name = bucket_names['default']
            except KeyError:
                # no bucket name. setting to None to try local
                bucket_name = None
        if bucket_name is None and use_local_storage is True:
            return default_storage

    if bucket_name is None:
        raise NoStorageFound

    storage_urls = getattr(settings, 'STORAGE_URLS', {})
    storage_url = None
    try:
        storage_url = storage_urls[storage_name]
    except KeyError:
        if use_default_url:
            try:
                storage_url = storage_urls['default']
            except KeyError:
                # LOG THIS
                pass

    if storage_url is not None:
        return S3BotoStorage(bucket=bucket_name, custom_domain=storage_url)

    return S3BotoStorage(bucket=bucket_name)

class NoStorageFound(Exception):
    pass