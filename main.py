from enum import Enum
from typing import Optional, List, Set
from fastapi import FastAPI, Query, Path, Cookie, Header, File, UploadFile, HTTPException
from pydantic import BaseModel, Field, HttpUrl


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class UnsupportedFile(HTTPException):
    def __init__(self):
        super(HTTPException, self).__init__(status_code=400, detail='Not supported')


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(None, title="The description of the item", max_length=300)
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []
    image: Optional[Image] = None

    class Config:
        schema_extra = {
            'examples': {
                'normal': {
                    'name': 'Foo',
                    'description': 'A very nice Item',
                    'price': 35.4,
                    'tax': 3.2
                },
                'tax_free': {
                    'name': 'Foo',
                    'description': 'A very cheap Item',
                    'price': 21.1
                }
            }
        }


app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World!'}


@app.post(
    '/items/',
    response_model=Item,
    response_model_include={'price'}
)
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict


@app.put('/items/{item_id}')
async def update_item(item: Item, item_id: int = Path(..., title='The ID of the item to get'), q: Optional[str] = None):
    result = {'item_id': item_id, **item.dict()}
    if q:
        result.update({'q': q})
    return result


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10, q: Optional[List[str]] = Query(['foo', 'bar'], title='Query string', description='A list of quries', example=['hello', 'world']), ads_id: Optional[str] = Cookie(None), user_agent: Optional[str] = Header(None)):
    results = {'items': fake_items_db[skip: skip + limit]}
    if q:
        results['q'] = q
    if ads_id:
        results['ads_id'] = ads_id
    if user_agent:
        results['user_agent'] = user_agent
    return results


@app.get('/users/{user_id}/items/{item_id}')
async def read_item(user_id: int, needy: str, item_id: int = Path(..., title='The ID of the item to get'), q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id, "needy": needy}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.post('/files/')
async def create_file(file: bytes = File(...)):
    return {'file_size': len(file)}


@app.post('/upload-file/')
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type != 'application/x-gzip':
        raise UnsupportedFile()
    content = await file.read()
    return {'filename': file.filename, 'file_size': len(content), 'content_type': file.content_type}
