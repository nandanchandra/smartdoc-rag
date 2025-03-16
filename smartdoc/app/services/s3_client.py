import boto3
from app.settings import settings
from fastapi import HTTPException
from loguru import logger


class S3Client:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(S3Client, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        try:
            session = boto3.Session(
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_s3_region,
            )
            self.s3_client = session.client(
                "s3",
                config=boto3.session.Config(
                    signature_version=settings.aws_s3_signature_version,
                    s3={"addressing_style": settings.aws_s3_addressing_style},
                ),
            )

            self.bucket_name = settings.aws_s3_bucket_name

            logger.info(f"S3 Client initialized for bucket: {self.bucket_name}")

        except Exception as e:
            logger.error(f"Failed to initialize S3 Client: {str(e)}")
            raise HTTPException(
                status_code=500, detail="S3 Client initialization failed."
            )

    def _get_s3_path_key(self, user_id: str, file_name: str) -> str:
        return f"{user_id}/{file_name}"
    
    def get_object(self, bucket_name: str, key: str) -> bytes:
        bucket = bucket_name or self.bucket_name
        try:
            s3_response = self.s3_client.get_object(Bucket=bucket, Key=key)
            if "Body" not in s3_response:
                logger.warning(f"S3 object (Bucket: {bucket}, Key: {key}) has no 'Body' field.")
                return b""
            content = s3_response["Body"].read()
            return content
        except Exception as e:
            logger.error(f"Failed to fetch object from S3: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch object from S3.")

    def generate_presigned_url(
        self, user_id: str, file_name: str, expiration: int = 60
    ):
        try:
            key = self._get_s3_path_key(user_id, file_name)
            params = {
                "Bucket": self.bucket_name,
                "Key": key,
            }

            url = self.s3_client.generate_presigned_url(
                "put_object", Params=params, ExpiresIn=expiration
            )

            logger.info(f"Generated presigned URL for user: {user_id}, file: {key}")

            return url
        except Exception as e:

            logger.error(f"Failed to generate presigned URL: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def start_multipart_upload(self, user_id: str, file_name: str):
        try:
            key = self._get_s3_path_key(user_id, file_name)
            params = {"Bucket": self.bucket_name, "Key": key}

            response = self.s3_client.create_multipart_upload(**params)

            upload_id = response["UploadId"]
            logger.info(
                f"Multipart upload started for file: {key}, upload_id: {upload_id}"
            )
            return upload_id
        except Exception as e:

            logger.error(f"Failed to start multipart upload: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def generate_multipart_presigned_urls(
        self, user_id: str, file_name: str, upload_id: str, part_numbers: int
    ):
        try:
            key = self._get_s3_path_key(user_id, file_name)
            presigned_urls = [
                self.s3_client.generate_presigned_url(
                    "upload_part",
                    Params={
                        "Bucket": self.bucket_name,
                        "Key": key,
                        "PartNumber": part_num,
                        "UploadId": upload_id,
                    },
                    ExpiresIn=3600,
                )
                for part_num in range(1, part_numbers + 1)
            ]

            logger.info(
                f"Generated multipart presigned URLs for file: {key} and parts: {part_numbers}"
            )
            return presigned_urls
        except Exception as e:

            logger.error(f"Failed to generate multipart presigned URLs: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def complete_multipart_upload(
        self, user_id: str, file_name: str, upload_id: str, parts: list
    ):
        try:
            key = self._get_s3_path_key(user_id, file_name)
            sorted_parts = sorted(
                [
                    {"ETag": part["etag"].strip('"'), "PartNumber": part["PartNumber"]}
                    for part in parts
                ],
                key=lambda x: x["PartNumber"],
            )
            params = {
                "Bucket": self.bucket_name,
                "Key": key,
                "UploadId": upload_id,
                "MultipartUpload": {"Parts": sorted_parts},
            }

            response = self.s3_client.complete_multipart_upload(**params)

            logger.info(
                f"Multipart upload completed for file: {key}, upload_id: {upload_id}"
            )
            return response
        except Exception as e:

            logger.error(f"Failed to complete multipart upload: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))


s3_client = S3Client()
