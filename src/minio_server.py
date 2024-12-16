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

    def get_file(self, file_name: str, dest_name: str):
        status = self.__minio_client.fget_object(
            self.__bucket_name, file_name, dest_name
        )

        return status


def main():
    minio_server = MinioServer()
    print('I am here')
    print(minio_server.get_file(
        "2024-12-01 01.40.30.jpg", "./2024-12-01 01.40.30.jpg")
    )


main()
