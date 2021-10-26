import cuid as cuid
import pydantic


class ResourceCreated(pydantic.BaseModel):
    """The new resource is effectively created before this reaches the client.
    """
    identifier: str = pydantic.Field(
        ...,
        title='The new identifier.',
        description='The identifier of the newly created resource.',
        max_length=64,
        min_length=1,
        examples={
            'integer': '7',
            'cuid': 'cjld2cyuq0000t3rmniod1foy',
            'guid': 'deadbeef-dead-beef-dead-beef00000075'
        },
        example='cjld2cyuq0000t3rmniod1foy'
    )

    def __init__(self, **kwargs):
        if 'identifier' not in kwargs:
            kwargs['identifier'] = cuid.cuid()
        super().__init__(**kwargs)
