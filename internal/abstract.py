from abc import ABC
from typing import BinaryIO


class Singleton:
    instance = None

    def __new__(cls):
        if cls.instance is not None:
            return cls.instance
        instance = super().__new__(cls)
        cls.instance = instance
        return instance


class BaseCloudStorage(ABC):
    def upload_file(self, path: str, file: bytes | BinaryIO, file_name: str):
        ...
