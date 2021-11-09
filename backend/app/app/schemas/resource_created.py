import cuid
import pydantic
from app.schemas import IDENTIFIER_INFORMATION


class ResourceCreated(pydantic.BaseModel):
    """The new resource is effectively created before this reaches the client."""

    identifier: str = pydantic.Field(..., **IDENTIFIER_INFORMATION)

    def __init__(self, **kwargs):
        if len(kwargs) == 0:
            kwargs["identifier"] = cuid.cuid()
        super().__init__(**kwargs)

    @staticmethod
    def openapi_examples() -> dict:
        return {
            "cuid": {"value": {"identifier": IDENTIFIER_INFORMATION["example"]}},
            "integer": {"value": {"identifier": "7"}},
            "guid": {"value": {"identifier": "99e94e87-bce0-505b-bd92-5a151cc50788"}},
            "objectid": {"value": {"identifier": "59cd65f7bcf86cd799439011"}},
        }
