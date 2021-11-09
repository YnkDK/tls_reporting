import io
import json

import pytest
from app.core.exceptions import GzipError, JsonError
from app.schemas.http_exception import HttpException
from app.schemas.mta_sts_report import MtaStsReport
from app.schemas.resource_created import ResourceCreated
from app.tests.utils.utils import (
    get_endpoint,
    get_test_data_path,
    pydandict_example,
    send_request,
)
from fastapi import status
from fastapi.encoders import jsonable_encoder


@pytest.mark.parametrize(
    "test_file_name", ["example.json", "example.gz", "no-policies.json"]
)
def test_create_mta_sts_report_success(test_file_name: str):
    test_file_path = get_test_data_path(test_file_name)
    endpoint, _ = get_endpoint("create_mta_sts_report")

    response = send_request(
        "create_mta_sts_report", files={"report": open(test_file_path, "rb")}
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.headers.get("content-type") == "application/json"
    # pydantic validates the response format
    resource_created = ResourceCreated(**response.json())
    assert (
        response.headers.get("location") == f"{endpoint}/{resource_created.identifier}"
    )


def test_create_mta_sts_report_success_from_model():
    endpoint, _ = get_endpoint("create_mta_sts_report")
    openapi_example = io.StringIO()
    example = pydandict_example(MtaStsReport.schema())
    json.dump(jsonable_encoder(example), openapi_example)
    openapi_example.seek(0)

    response = send_request("create_mta_sts_report", files={"report": openapi_example})

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.headers.get("content-type") == "application/json"
    # pydantic validates the response format
    resource_created = ResourceCreated(**response.json())
    assert (
        response.headers.get("location") == f"{endpoint}/{resource_created.identifier}"
    )


@pytest.mark.parametrize(
    "test_file_name", ["date_error.json", "missing_required_field.json"]
)
def test_create_mta_sts_report_invalid_json(test_file_name: str):
    test_file_path = get_test_data_path(test_file_name)

    response = send_request(
        "create_mta_sts_report", files={"report": open(test_file_path, "rb")}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.headers.get("content-type") == "application/json"
    # pydantic validates the response format
    exception = HttpException(**response.json())
    assert exception.detail.code == JsonError.ERROR_CODE
    assert exception.detail.message == JsonError.MESSAGE


def test_create_mta_sts_report_invalid_gz():
    test_file_path = get_test_data_path("truncated.gz")

    response = send_request(
        "create_mta_sts_report", files={"report": open(test_file_path, "rb")}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.headers.get("content-type") == "application/json"
    # pydantic validates the response format
    exception = HttpException(**response.json())
    assert exception.detail.code == GzipError.ERROR_CODE
    assert exception.detail.message == GzipError.MESSAGE


@pytest.mark.parametrize("files", [None])
def test_create_mta_sts_report_missing_parameter(files):
    expected_error = {
        "detail": [
            {
                "loc": ["body", "report"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
    response = send_request("create_mta_sts_report", files=files)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.headers.get("content-type") == "application/json"
    assert response.json() == expected_error
