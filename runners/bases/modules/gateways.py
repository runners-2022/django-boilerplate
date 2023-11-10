import logging
from typing import Any
from urllib.parse import urljoin

import requests

logger = logging.getLogger(__name__)


class Gateway:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_url(self, path: str) -> str:
        return urljoin(self.base_url, path)

    def request(self, method: str, path: str, *args, **kwargs) -> Any:
        try:
            response = requests.request(method, self.get_url(path), *args, **kwargs)
        except requests.RequestException as exc:
            # Write logs for possible request errors
            logger.warning(f"Unexpected exception caught: {exc!s}")
            raise

        # Raise exception for HTTP error status codes such as 400, 404, 500.
        # response.raise_for_status()

        return response.json()
