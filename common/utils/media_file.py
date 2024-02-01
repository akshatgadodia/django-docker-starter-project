import os
import uuid
import boto3
from botocore.client import Config
from django.conf import settings
from django.core.files.storage import default_storage

from common.logging import LogInfo
from common.messages import FILE_DOES_NOT_EXISTS


def get_client_object():
    """
    Creates and returns an S3 client object configured with the provided AWS credentials
    and endpoint URL from Django settings.
    Returns:
        boto3.client: An S3 client object ready to interact with the specified S3-compatible storage.
    """
    return boto3.client('s3',
                        endpoint_url=settings.AWS_ENDPOINT_URL,
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        config=Config(signature_version=settings.AWS_S3_SIGNATURE_NAME))


def save_file(file, file_dir):
    """
    Save a file to the default media folder.
    Args:
        file: File object to be saved.
        file_dir: Directory name to be stored in.
    Returns:
        str or False: The file path if successful, False if an exception occurs.
    """
    try:
        # Generate a unique filename using UUID and original file extension
        filename = str(uuid.uuid4()) + "." + file.name.split('.')[-1]

        if settings.STORE_MEDIA_IN_S3:
            # Save file to S3 if configured to store media in S3
            return default_storage.save(f"{file_dir}/{filename}", file)
        else:
            # Save file to the default media folder if not storing in S3
            dir_path = os.path.join(settings.MEDIA_ROOT, file_dir)
            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)
            return default_storage.save(os.path.join(file_dir, filename), file)
    except Exception as exc:
        LogInfo.exception(exc)
        return False


def delete_file(file_name):
    """
    Delete a file from the default media folder or S3 bucket.
    Args:
        file_name: Name of the file to be deleted.
    Returns:
        None
    """
    try:
        if settings.STORE_MEDIA_IN_S3:
            s3_client = get_client_object()
            s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_name)
        else:
            # Delete file from the default media folder if not storing in S3
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
    except Exception as e:
        LogInfo.exception(e)
        print(f"Error deleting file: {str(e)}")


def check_if_file_exists(file_name):
    try:
        s3_client = get_client_object()
        s3_client.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_name)
    except Exception:
        raise Exception(FILE_DOES_NOT_EXISTS)


def generate_media_filename(file_name):
    return str(uuid.uuid4()) + "." + file_name.split('.')[-1]


def generate_absolute_media_url(relative_url):
    return f"{settings.MEDIA_URL}{relative_url}"
