import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.storage_endpoint,
            aws_access_key_id=settings.storage_access_key,
            aws_secret_access_key=settings.storage_secret_key,
            use_ssl=settings.storage_secure,
        )

    def upload_file(self, file_obj, bucket_name: str, object_name: str, content_type: str = "application/octet-stream") -> bool:
        """Upload a file to an S3 bucket"""
        try:
            self.s3_client.upload_fileobj(
                file_obj,
                bucket_name,
                object_name,
                ExtraArgs={"ContentType": content_type}
            )
            return True
        except ClientError as e:
            logger.error(f"Failed to upload file to {bucket_name}/{object_name}: {e}")
            return False

    def get_presigned_url(self, bucket_name: str, object_name: str, expiration: int = 3600) -> str | None:
        """Generate a presigned URL to share an S3 object"""
        try:
            response = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": object_name},
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL for {bucket_name}/{object_name}: {e}")
            return None

    def download_file(self, bucket_name: str, object_name: str, file_path: str) -> bool:
        """Download a file from an S3 bucket to a local path"""
        try:
            self.s3_client.download_file(bucket_name, object_name, file_path)
            return True
        except ClientError as e:
            logger.error(f"Failed to download file {bucket_name}/{object_name}: {e}")
            return False

storage_service = StorageService()
