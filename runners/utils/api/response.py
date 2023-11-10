from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from rest_framework.response import Response as BaseResponse

logger = logging.getLogger(__name__)


@dataclass
class Data:
    code: int
    message: str
    errors: Optional[ErrorInfo]
    result: Dict[str, Any]


@dataclass
class ErrorInfo:
    field_errors: Dict[str, List[str]]
    non_field_errors: List[str]


class Response(BaseResponse):
    """
    Response class wrapping existing DRF's Response class with extra arguments to force response format.
    """

    def __init__(
        self,
        status: int,
        *,
        code: int,
        message: str,
        errors: Optional[ErrorInfo] = None,
        data: Any = None,
        template_name: str = None,
        headers: Optional[Dict[str, str]] = None,
        exception: bool = False,
        content_type: str = None,
    ):
        formatted_data = self.format_extra_data(code, message, errors, data)
        super().__init__(
            status=status,
            data=formatted_data,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )

    def format_extra_data(
        self, code: int, message: str, errors: Optional[ErrorInfo] = None, data: Any = None
    ) -> Dict[str, Any]:

        code = int(code)
        if not (100 <= code < 600):
            raise ValueError("code must be integer in [100, 600)")

        message = str(message)
        if len(message) == 0:
            raise ValueError("message must not be empty")

        if 100 <= code < 400:
            data = {
                "code": code,
                "message": message,
                "data": data or []
            }

        elif 400 <= code < 600:
            data = {
                "code": code,
                "message": message,
                "errors": errors,
            }

        return data

    @classmethod
    def from_drf_response(
        cls,
        drf_response: BaseResponse,
        *,
        code: int,
        message: str,
        errors: Optional[ErrorInfo] = None,
        data: Any = None,
        **kwargs,
    ) -> Response:
        return cls(
            status=kwargs.get("status", drf_response.status_code),
            code=code,
            message=message,
            errors=errors,
            data=drf_response.data or data,
            template_name=kwargs.get("template_name", drf_response.template_name),
            headers=kwargs.get("headers", drf_response.headers),
            exception=kwargs.get("exception", drf_response.exception),
            content_type=kwargs.get("content_type", drf_response.content_type),
        )
