import secrets

from django.conf import settings
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status








from rest_framework import generics, permissions

from .models import Course
from .serializers import (
    CourseListSerializer,
    CourseDetailSerializer,
)


class CourseListView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]

    queryset = Course.objects.filter(
        is_published=True
    ).select_related(
        "category",
        "instructor",
    )


class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.AllowAny]

    lookup_field = "slug"

    queryset = Course.objects.filter(
        is_published=True
    ).select_related(
        "category",
        "instructor",
    )


class CourseDiagnosticView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        expected_token = settings.COURSE_DIAGNOSTIC_TOKEN
        supplied_token = request.headers.get("X-Diagnostic-Token", "")

        if (
            not expected_token
            or not secrets.compare_digest(
                supplied_token,
                expected_token,
            )
        ):
            return Response(
                {"detail": "Not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response({
            "database_engine": connection.vendor,
            # "database_name": connection.settings_dict.get("NAME"),
            "total_courses": Course.objects.count(),
            "published_courses": Course.objects.filter(
                is_published=True
            ).count(),
        })