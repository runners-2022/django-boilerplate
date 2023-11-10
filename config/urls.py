# Django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views

# Config
from config.docs import schema_view
from config.redirects import redirect_admin_view, redirect_swagger_view

# DRF
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = (
    [
        path("", redirect_admin_view),

        # Admin
        path("jet/", include("jet.urls", "jet")),
        path(settings.ADMIN_URL, admin.site.urls),

        # Allauth
        path("accounts/", include("allauth.urls")),

        # Advanced Filters
        path("advanced_filters/", include("advanced_filters.urls")),

        # DRF auth token
        path("auth-token/", obtain_auth_token),

        # django-health-check
        path("ht/", include("health_check.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

# API URLS
urlpatterns += [
    # API base url
    path("api/", redirect_swagger_view),
    path("api/", include("config.api_router")),

    # Swagger
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
