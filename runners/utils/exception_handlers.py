# Python
import logging
import traceback

# Django
from django.utils.translation import ugettext_lazy as _

# Django Rest Framework
from rest_framework.settings import api_settings
from rest_framework import status, exceptions
from rest_framework.exceptions import APIException, _get_error_details

# Third Party
from drf_pretty_exception_handler import exception_handler

# Local
from runners.utils.api.response import Response


class CustomForbiddenException(exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = 'error'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class CustomBadRequestError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)


logger = logging.getLogger(__name__)

_non_field_errors_key = api_settings.NON_FIELD_ERRORS_KEY

_code_and_message_defaults = {
    status.HTTP_400_BAD_REQUEST: (400, _("값이 올바르지 않습니다.")),
    status.HTTP_403_FORBIDDEN: (403, _("접근 권한이 없습니다.")),
    status.HTTP_500_INTERNAL_SERVER_ERROR: (500, _("서버에 예기치 못한 오류가 발생했습니다.")),
}

_unknown_code_and_message = (404, _("데이터가 없습니다."))


def custom_exception_handler(exc, context):
    # 에러 로그 표기
    print(traceback.format_exc())

    response = exception_handler(exc, context)
    data = response.data

    status = data.pop("status_code")
    default_code, default_message = _code_and_message_defaults.get(status, _unknown_code_and_message)

    if errors := data.pop("errors", None):

        stale_non_field_errors = errors.pop(_non_field_errors_key, [])
        non_field_errors = []
        field_errors = errors

        for error_item in stale_non_field_errors:
            if isinstance(error_item, str):
                non_field_errors.append(error_item)
            else:
                field_errors.update(error_item)

        errors = {
            "field_errors": {k: list(map(str, v)) for k, v in field_errors.items()},
            "non_field_errors": non_field_errors,
        }
        print('field_errors : ', field_errors)
        print('non_field_errors : ', non_field_errors)

    response = Response.from_drf_response(response, code=default_code, message=default_message, errors=errors)

    return response
