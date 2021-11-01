import pytest
from fastapi.exceptions import RequestValidationError, RequestErrorModel
from pydantic import ValidationError

from app.core.exceptions import JsonError, GzipError
from app.models.http_exception import HttpException
from app.models.resource_created import ResourceCreated
from app.tests.utils.utils import get_test_data_path, send_request, get_endpoint
from fastapi import status


@pytest.mark.parametrize('test_file_name', ['example.json', 'example.gz', 'no-policies.json'])
def test_create_mta_sts_report_success(test_file_name: str):
    test_file_path = get_test_data_path(test_file_name)
    endpoint, _ = get_endpoint('create_mta_sts_report')

    response = send_request('create_mta_sts_report', files={'report': open(test_file_path, 'rb')})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.headers.get('content-type') == 'application/json'
    # pydantic validates the response format
    resource_created = ResourceCreated(**response.json())
    assert response.headers.get('location') == f'{endpoint}/{resource_created.identifier}'


@pytest.mark.parametrize('test_file_name', ['date_error.json', 'missing_required_field.json'])
def test_create_mta_sts_report_invalid_json(test_file_name: str):
    test_file_path = get_test_data_path(test_file_name)

    response = send_request('create_mta_sts_report', files={'report': open(test_file_path, 'rb')})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.headers.get('content-type') == 'application/json'
    # pydantic validates the response format
    exception = HttpException(**response.json())
    assert exception.detail.code == JsonError.ERROR_CODE
    assert exception.detail.message == JsonError.MESSAGE


def test_create_mta_sts_report_invalid_gz():
    test_file_path = get_test_data_path('truncated.gz')

    response = send_request('create_mta_sts_report', files={'report': open(test_file_path, 'rb')})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.headers.get('content-type') == 'application/json'
    # pydantic validates the response format
    exception = HttpException(**response.json())
    assert exception.detail.code == GzipError.ERROR_CODE
    assert exception.detail.message == GzipError.MESSAGE


@pytest.mark.parametrize('files', [None])
def test_create_mta_sts_report_missing_parameter(files):
    response = send_request('create_mta_sts_report', files=files)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.headers.get('content-type') == 'application/json'
    # pydantic validates the response format
    exception = RequestErrorModel(**response.json())
