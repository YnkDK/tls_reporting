import gzip
import io
import json
from typing import Union, BinaryIO, List

from fastapi import UploadFile

from app.core.exceptions import GzipError, JsonError
from app.core.mta_sts.meta import Meta
from app.core.mta_sts.policy import Policy


class MtaSts:

    # The magic bytes for gz or tar.gz is 1f8b
    MAGIC_BYTE_GZ = b'\x1f\x8b'

    def __init__(self, report_name: str):
        self.__meta = Meta(report_name)
        self.__policies = []

    @property
    def meta(self) -> Meta:
        return self.__meta

    @property
    def policies(self) -> List[Policy]:
        return self.__policies

    @staticmethod
    def unzip(buffer: bytes) -> bytes:
        compressed_file = io.BytesIO(buffer)
        try:
            return gzip.GzipFile(fileobj=compressed_file).read()
        except Exception as e:
            raise GzipError(e)

    async def parse(self, raw_content: Union[BinaryIO, UploadFile]):
        buffer = await raw_content.read()

        if buffer.startswith(MtaSts.MAGIC_BYTE_GZ):
            buffer = MtaSts.unzip(buffer)

        try:
            raw_report = json.loads(buffer)
            self.__meta.build(raw_report)
            for raw_policy in raw_report['policies']:
                p = Policy()
                p.build(raw_policy)
                self.__policies.append(p)
        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as e:
            raise JsonError(e)
