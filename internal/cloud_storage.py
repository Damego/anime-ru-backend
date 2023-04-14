from asyncio import get_event_loop
from base64 import b64encode
from os import environ
from typing import BinaryIO
from functools import partial

from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from imagekitio.models.results.UploadFileResult import UploadFileResult

from .abstract import BaseCloudStorage, Singleton


class ImageKitCloudStorage(BaseCloudStorage, Singleton):
    def __init__(self):
        self.image_kit = ImageKit(
            environ["IMAGEKIT_PUBLIC_KEY"],
            environ["IMAGEKIT_PRIVATE_KEY"],
            environ["IMAGEKIT_URL_ENDPOINT"]
        )

    async def upload_file(self, path: str, file: bytes | BinaryIO, file_name: str) -> str:
        file = file if isinstance(file, bytes) else file.read()
        base64 = b64encode(file)  # imagekit doesn't work with bytes except base64
        upload_options = UploadFileRequestOptions(
            folder=path
        )

        loop = get_event_loop()
        result: UploadFileResult = await loop.run_in_executor(
            None,
            partial(self.image_kit.upload_file, base64, file_name, upload_options)
        )
        return result.url
