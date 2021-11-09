import gzip
import io
import json

from app.core.exceptions import GzipError, JsonError
from app.schemas.mta_sts_report import MtaStsReport
from fastapi import UploadFile
from pydantic import ValidationError


class MtaSts:

    # The magic bytes for gz or tar.gz is 1f8b
    MAGIC_BYTE_GZ = b"\x1f\x8b"

    @staticmethod
    def unzip(buffer: bytes) -> bytes:
        compressed_file = io.BytesIO(buffer)
        try:
            return gzip.GzipFile(fileobj=compressed_file).read()
        except Exception as e:
            raise GzipError(e)

    @classmethod
    async def parse(cls, raw_content: UploadFile) -> MtaStsReport:
        buffer = await raw_content.read()
        if buffer.startswith(cls.MAGIC_BYTE_GZ):
            buffer = cls.unzip(buffer)

        try:
            raw_report = json.loads(buffer)
        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as e:
            raise JsonError(e)
        try:
            return MtaStsReport(**raw_report)
        except ValidationError as e:
            raise JsonError(e)
