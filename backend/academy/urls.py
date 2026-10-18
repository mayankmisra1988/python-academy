# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static


# urlpatterns = [
#     path("admin/", admin.site.urls),

#     # Authentication
#     path(
#         "api/auth/",
#         include("accounts.urls")
#     ),

#     # Courses
#     path(
#         "api/courses/",
#         include("courses.urls")
#     ),

#     # Lessons
#     path(
#         "api/lessons/",
#         include("lessons.urls")
#     ),

#     # Enrollments
#     path(
#         "api/enrollments/",
#         include("enrollments.urls")
#     ),

#     # Dashboard
#     path(
#         "api/dashboard/",
#         include("dashboard.urls")
#     ),

#     # Certificates
#     path(
#         "api/certificates/",
#         include("certificates.urls")
#     ),
# ]


# # Serve media files during development
# if settings.DEBUG:
#     urlpatterns += static(
#         settings.MEDIA_URL,
#         document_root=settings.MEDIA_ROOT
#     )



from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    # API Schema
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    # Swagger UI
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),

    # Authentication
    path(
        "api/auth/",
        include("accounts.urls")
    ),

    # Courses
    path(
        "api/courses/",
        include("courses.urls")
    ),

    # Lessons
    path(
        "api/lessons/",
        include("lessons.urls")
    ),

    # Enrollments
    path(
        "api/enrollments/",
        include("enrollments.urls")
    ),

    # Dashboard
    path(
        "api/dashboard/",
        include("dashboard.urls")
    ),

    # Certificates
    path(
        "api/certificates/",
        include("certificates.urls")
    ),
]


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
)
