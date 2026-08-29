


from django.urls import path
from .views import (
    CourseCurriculumView,
    LessonDetailView,
    LessonProgressView,
    LessonProgressDetailView,
    QuizDetailView,
    QuizSubmitView,
)

urlpatterns = [

    path(
        "courses/<int:course_id>/curriculum/",
        CourseCurriculumView.as_view(),
        name="course-curriculum",
    ),

    path(
        "<int:pk>/",
        LessonDetailView.as_view(),
        name="lesson-detail",
    ),

    path(
        "progress/",
        LessonProgressView.as_view(),
        name="lesson-progress",
    ),

    path(
        "progress/<int:pk>/",
        LessonProgressDetailView.as_view(),
        name="lesson-progress-detail",
    ),

    path(
        "<int:lesson_id>/quiz/",
        QuizDetailView.as_view(),
    ),

    path(
        "quizzes/<int:quiz_id>/submit/",
        QuizSubmitView.as_view(),
    ),
]