# Python
from functools import wraps

# Django
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache

# Django Rest Framework
from rest_framework.serializers import SerializerMetaclass

# Third Party
from drf_yasg import openapi


# Main Section
def swagger_decorator(
    tag,
    id=None,
    description='',
    request=None,
    response=None,
    method=None
):
    data = dict(
        operation_id=_(id),
        operation_description=_(description),
        tags=[tag],
        responses={},
        method=method
    )

    if request:
        data['request_body'] = request

    for response_code in response.keys():
        message = None
        serializer = None

        if isinstance(response[response_code], str):
            message = response[response_code]
            data['responses'][response_code] = openapi.Response(_(message))

        elif isinstance(response[response_code], SerializerMetaclass):
            serializer = response[response_code]
            data['responses'][response_code] = openapi.Response(_('ok'), serializer)

        elif isinstance(response[response_code], tuple) or isinstance(response[response_code], list):
            print(response[response_code])
            for value in response[response_code]:
                if isinstance(value, str):
                    message = value
                elif isinstance(value, SerializerMetaclass):
                    serializer = value

            data['responses'][response_code] = openapi.Response(_(message), serializer)

    return data


def cache_decorator(suggest_type, timeout=1800):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs['user']
            cache_key = f'{user.id}_{suggest_type}'
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result

        return wrapper

    return decorator
