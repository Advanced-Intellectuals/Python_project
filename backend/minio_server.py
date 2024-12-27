from minio import Minio
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class MinioServer():
    __bucket_name: str

    def __init__(self):
        self.__minio_client = Minio(
            '185.105.91.138:9000',
            access_key=os.getenv('MINIO_ACCESS_KEY'),
            secret_key=os.getenv('MINIO_SECRET_KEY'),
            secure=False
        )
        self.__bucket_name = "online.cinema"

        found = self.__minio_client.bucket_exists(self.__bucket_name)
        if not found:
            self.__minio_client.make_bucket(self.__bucket_name)

    def put_file(self, source_path: str, file_id: str) -> bool:
        try:
            self.__minio_client.fput_object(
                self.__bucket_name, file_id, source_path
            )
            return True
        except Exception:
            return False

    def get_object_url(self, object_id):
        return self.__minio_client.presigned_get_object(
            self.__bucket_name, object_id, expires=timedelta(hours=3))
