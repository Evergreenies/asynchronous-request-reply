import secrets
import requests

from typing import AnyStr

_N_BYTES = 16


def generate_token():
    """Generate random message token."""
    return secrets.token_hex(_N_BYTES)


def return_job_result(method: str, url: str, json: AnyStr):
    """
    Redirect result to the consumer service by requesting to provided `url`.

    :param method: HTTP Method (GET, POST, etc)
    :type method: str
    :param url: url of destination/consumer service
    :type url: str
    :param json: processed data
    :type json: dict
    :return:
    :rtype:
    """
    headers = {'Content-Type': 'application/json'}
    return requests.request(method, url, json=json,
                            headers=headers, timeout=15)
