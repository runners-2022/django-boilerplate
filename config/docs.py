# Django
from django.conf import settings
from django.urls import include, path
from django.utils.translation import ugettext_lazy as _

# DRF
from rest_framework import permissions

# Third party
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Main Section
description = _(
    """
러너스 백엔드 서버 API 문서입니다.

# Response Data
<br/>
## 성공
```json
{
    "code": " ... ",
    "message": " ... ",
    "result": { ... }
}
```
<br/>
## 실패
```json
{
    "code": " ... ",
    "message": " ... ",
    "errors": { ... },
}
```
<br/>
## 세부 안내

`code` Status 코드입니다.

`message` 상세 메시지입니다.

`result` 응답 결과 데이터입니다.

`errors` 오류 발생시 나타나는 필드입니다.

<br/>"""
)

public = bool(settings.DJANGO_ENV in ('local',))

if settings.DJANGO_ENV == "local":
    permission_classes = (permissions.AllowAny,)
else:
    permission_classes = (permissions.AllowAny,)

schema_url_patterns = [
    path(r"^api/", include("config.api_router")),
]

schema_view = get_schema_view(
    openapi.Info(
        title="러너스 API 문서",
        default_version="v1",
        description=description,
    ),
    public=public,
    permission_classes=permission_classes,
    patterns=schema_url_patterns,
)
