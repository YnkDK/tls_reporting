import requests
import pytest

from app.models.http_exception import HttpException
from app.models.resource_created import ResourceCreated
from app.tests.utils.utils import get_server_api, get_test_data_path
from fastapi import status


@pytest.mark.parametrize('test_file_name', ['example.json', 'example.gz', 'no-policies.json'])
def test_create_mta_sts_report_success(test_file_name: str):
    server_api = get_server_api()
    test_file_path = get_test_data_path(test_file_name)

    response = requests.post(f'{server_api}/mta-sts/', files={'report': open(test_file_path, 'rb')})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.headers.get('content-type') == 'application/json'
    assert ResourceCreated(**response.json()), 'pydantic validates the response'


@pytest.mark.parametrize('test_file_name', ['date_error.json'])
def test_create_mta_sts_report_failure(test_file_name: str):
    server_api = get_server_api()
    test_file_path = get_test_data_path(test_file_name)

    response = requests.post(f'{server_api}/mta-sts/', files={'report': open(test_file_path, 'rb')})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.headers.get('content-type') == 'application/json'
    assert HttpException(**response.json()), 'pydantic validates the response'
