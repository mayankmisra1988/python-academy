# from django.urls import path

# from .views import (CourseListView,CourseDetailView,)

# urlpatterns = [
#     path("",CourseListView.as_view(),name="course-list",),
#     path("<slug:slug>/",CourseDetailView.as_view(),name="course-detail",),
# ]

from django.urls import path
from .views import (
    CourseListView,
    CourseDetailView,
    CourseDiagnosticView,
)

urlpatterns = [
    path("", CourseListView.as_view(), name="course-list"),
    path(
        "diagnostic/",
        CourseDiagnosticView.as_view(),
        name="course-diagnostic",
    ),
    path(
        "<slug:slug>/",
        CourseDetailView.as_view(),
        name="course-detail",
    ),
]