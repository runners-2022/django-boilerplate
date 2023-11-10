from unittest import mock

import pytest
import requests
from icecream import IceCreamDebugger
from requests_mock import Mocker as RequestsMocker

from runners.bases.modules.gateways import Gateway


@pytest.fixture(scope="class")
def gateway():
    # Using localhost:65535 to prevent sending any real HTTP request to real server by mistakes.
    # And plus, it's because python urllib.parse.urljoin does not permits custom protocol schemes (mock://).
    return Gateway("http://localhost:65535/api/")


@pytest.mark.usefixtures("gateway")
class TestBaseGateway:
    @pytest.mark.unit
    def test_get_url(self, ic: IceCreamDebugger, gateway: Gateway):
        assert ic(gateway.get_url("just-a-url") == "http://localhost:65535/api/just-a-url")

    @pytest.mark.unit
    def test_request(self, ic: IceCreamDebugger, requests_mock: RequestsMocker, gateway: Gateway):
        requests_mock.request(
            "POST",
            "http://localhost:65535/api/a-mocked-url",
            json={
                "message": "hello",
            },
        )
        data = gateway.request("POST", "a-mocked-url")
        assert data == {"message": "hello"}

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "status,payload",
        (
            (400, {"message": "bad request"}),
            (404, {"message": "not found"}),
            (500, {"message": "error from server"}),
        ),
    )
    def test_request_api_server_errors(
        self, ic: IceCreamDebugger, requests_mock: RequestsMocker, gateway: Gateway, status, payload
    ):
        requests_mock.request(
            "POST",
            "http://localhost:65535/api/a-mocked-erroneous-url",
            status_code=status,
            json=payload,
        )
        with pytest.raises(requests.HTTPError):
            gateway.request("POST", "a-mocked-erroneous-url")

    @pytest.mark.unit
    def test_request_unexpected_errors(self, ic: IceCreamDebugger, gateway: Gateway):
        with mock.patch("requests.request") as request_mock:
            request_mock.side_effect = requests.ConnectionError()

            # .request() should propagate exceptions, for now.
            with pytest.raises(requests.RequestException):
                gateway.request("POST", "this-request-will-be-mocked")
