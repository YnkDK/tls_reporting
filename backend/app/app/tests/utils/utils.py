import os
from typing import Tuple

import requests
from app.core.config import settings

OPERATION_ID_ENDPOINTS = dict()


def get_test_data_path(filename: str = None) -> str:
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    data_dir = os.path.join(dir_path, "data")
    if filename:
        return os.path.join(data_dir, filename)
    return data_dir


def init_operation_id_endpoints():
    """Caches the mapping between operation ids and endpoint/request method based on the the OpenAPI definition."""
    server_api = settings.SERVER_NAME
    open_api = requests.get(f"{server_api}/openapi.json").json()

    for path in open_api["paths"]:
        for method in open_api["paths"][path]:
            operation_id = open_api["paths"][path][method]["operationId"]
            OPERATION_ID_ENDPOINTS[operation_id] = (f"{server_api}{path}", method)


def get_endpoint(operation_id: str) -> Tuple[str, str]:
    """Gets endpoint and method type based on the operation id as found in the OpenAPI definition"""
    if len(OPERATION_ID_ENDPOINTS) == 0:
        init_operation_id_endpoints()
    return OPERATION_ID_ENDPOINTS[operation_id]


def send_request(
    operation_id: str,
    params=None,
    data=None,
    headers=None,
    cookies=None,
    files=None,
    auth=None,
    timeout=None,
    allow_redirects=True,
    proxies=None,
    hooks=None,
    stream=None,
    verify=True,
    cert=None,
    json=None,
) -> requests.Response:
    """Sends a request to the endpoint identified by the operation id as found in the OpenAPI definition.

    All keyword arguments are passed directly to the requests.request method.

    :param operation_id: Endpoint identified by the operation id as found in the OpenAPI definition.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart
        encoding upload. ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``,
        3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional
        headers to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection.
        Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param hooks: (optional) Dictionary mapping an event to a hook.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    """
    endpoint, method = get_endpoint(operation_id=operation_id)
    return requests.request(
        method=method,
        url=endpoint,
        params=params,
        data=data,
        headers=headers,
        cookies=cookies,
        files=files,
        auth=auth,
        timeout=timeout,
        allow_redirects=allow_redirects,
        proxies=proxies,
        hooks=hooks,
        stream=stream,
        verify=verify,
        cert=cert,
        json=json,
    )


def pydandict_example(schema: dict, definitions=None):
    if definitions is None:
        definitions = schema["definitions"]
    example = dict()
    if schema["type"] == "object":
        for property_name, value in schema["properties"].items():
            if "example" in value:
                example[property_name] = value["example"]
            elif "allOf" in value:
                definition = value["allOf"][0]["$ref"].split("/")[-1]
                example[property_name] = pydandict_example(
                    definitions[definition], definitions
                )
            elif "type" in value and value["type"] == "array":
                definition = value["items"]["$ref"].split("/")[-1]
                example[property_name] = [
                    pydandict_example(definitions[definition], definitions)
                ]
    return example
