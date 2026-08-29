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