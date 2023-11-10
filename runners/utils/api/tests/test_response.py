from rest_framework.response import Response as DrfResponse

import pytest
from dacite import MissingValueError, WrongTypeError
from faker import Faker

from runners.utils.api.response import Response

fake = Faker()


class TestResponse:
    @pytest.mark.unit
    @pytest.mark.parametrize(
        "status,code,message,errors",
        (
            (
                400,
                400831,
                fake.pystr(),
                {
                    "field_errors": {
                        "field_one": ["error_message_for_field_one"],
                        "field_two": ["error_message_for_field_two_1", "error_message_for_field_two_2"],
                    },
                    "non_field_errors": ["error_one", "error_two"],
                },
            ),
        ),
    )
    def test_response_with_valid_args(self, ic, status, code, message, errors):
        try:
            ic(Response(status=status, code=code, message=message, errors=errors))
        except Exception as exc:
            pytest.fail(f"No exception expected but got: {exc!s}")

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "status,code,message,errors,exception",
        (
            (999, 500413, fake.pystr(), None, ValueError),
            (404, 40040, fake.pystr(), None, ValueError),
            (200, 200176, "", None, ValueError),
            (400, 400313, fake.pystr(), {"non_field_errors": {"field": []}}, MissingValueError),
            (400, 400313, fake.pystr(), {"field_errors": {}}, MissingValueError),
            (
                400,
                400313,
                fake.pystr(),
                {
                    "field_errors": 1,
                    "non_field_errors": {},
                },
                WrongTypeError,
            ),
        ),
    )
    def test_response_with_invalid_args(self, ic, status, code, message, errors, exception):
        with pytest.raises(exception):
            ic(Response(status=status, code=code, message=message, errors=errors))

    @pytest.mark.unit
    def test_response_construct_from_drf_response(self, faker, ic):
        drf_response = DrfResponse(
            data={"x": 2.0, "y": 3.0},
            status=200,
            template_name="test-template.html",
            headers={
                "X-Test-Header": "Hello World",
            },
            exception=False,
            content_type="text/html",
        )

        # Construct Response from DRF Response but with override of headers
        response = Response.from_drf_response(
            drf_response,
            status=201,
            code=201491,
            message="A message",
            headers={
                "X-Custom-Header-For-Test": "Doom",
            },
        )

        # Most of data should be preserved
        assert ic(response.status_code == 201)
        assert ic(response.template_name == "test-template.html")

        headers = response._headers.keys()
        assert ic("X-Test-Header" not in headers)
        assert ic(response["X-Custom-Header-For-Test"] == "Doom")

        assert ic(response.content_type == "text/html")
        assert ic(
            response.data == {"code": 201491, "message": "A message", "errors": None, "result": {"x": 2.0, "y": 3.0}}
        )
