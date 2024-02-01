from django.conf import settings
from botocore.config import Config
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    Custom storage backend for handling media files using Amazon S3.
    This class extends S3Boto3Storage and customizes settings for media file storage.
    """

    # Set the location within the S3 bucket for storing media files
    location = settings.MEDIAFILES_LOCATION
    # Set whether to overwrite existing files with the same name
    file_overwrite = settings.AWS_S3_FILE_OVERWRITE
    use_accelerate_endpoint = settings.AWS_S3_ACCELERATE

    def __init__(self, **settings):
        """
        Initialize the MediaStorage with custom configurations.
        Args:
        **settings: Additional settings to be passed to the parent class.
        """
        super().__init__(**settings)
        # Configure additional settings for the S3 connection using botocore
        self.config = Config(
                s3={'addressing_style': self.addressing_style, 'use_accelerate_endpoint': self.use_accelerate_endpoint},
                signature_version=self.signature_version,
                proxies=self.proxies,
                retries={'max_attempts': 5},
                connect_timeout=10,
                read_timeout=10,
                max_pool_connections=10,
        )
