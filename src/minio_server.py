from minio import Minio
import os
from dotenv import load_dotenv

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

    def get_file(self, file_id: str):
        try:
            response = self.__minio_client.get_object(
                self.__bucket_name, file_id
            )
            return response
        except Exception:
            return None

    def put_file(self, source_path: str, file_id: str) -> bool:
        try:
            self.__minio_client.fput_object(
                self.__bucket_name, file_id, source_path
            )
            return True
        except Exception:
            return False


def main():
    minio_server = MinioServer()
    data = minio_server.get_file("2024-12-01 01.40.30.jpg")

    if data:
        print(data.data)
    else:
        print(data)


main()
