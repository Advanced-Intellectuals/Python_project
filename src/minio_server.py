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

    def get_file(self, file_name: str, dest_path: str) -> bool:
        try:
            self.__minio_client.fget_object(
                self.__bucket_name, file_name, dest_path
            )
            return True
        except Exception:
            return False

    def put_file(self, source_path: str, file_name: str):
        try:
            self.__minio_client.fput_object(
                self.__bucket_name, file_name, source_path
            )
            return True
        except Exception:
            return False


def main():
    minio_server = MinioServer()
    status = minio_server.put_file("./2024-12-01 01.40.30.jpg",
                                   "2024-12-01 01.40.30.jpg")

    print(status)


main()
