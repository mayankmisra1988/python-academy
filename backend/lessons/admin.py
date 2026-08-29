from django.contrib import admin

from .models import (
    Section,
    Lesson,
    LessonProgress,
    Quiz,
    Question,
    Option,
    QuizAttempt,
    StudentAnswer,
)


# =========================================================
# SECTION → LESSONS
# =========================================================

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "order",
    )

    list_filter = (
        "course",
    )

    search_fields = (
        "title",
    )

    ordering = (
        "course",
        "order",
    )

    inlines = [
        LessonInline,
    ]


# =========================================================
# QUESTION → OPTIONS
# =========================================================

class OptionInline(admin.TabularInline):
    model = Option

    extra = 4

    min_num = 4
    max_num = 4

    fields = (
        "option_text",
        "is_correct",
    )


class QuestionInline(admin.StackedInline):
    model = Question

    extra = 1

    fields = (
        "question",
        "explanation",
        "marks",
        "order",
    )


# =========================================================
# LESSON
# =========================================================

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "section",
        "duration",
        "is_published",
        "is_preview",
    )

    list_filter = (
        "is_published",
        "is_preview",
        "section",
    )

    search_fields = (
        "title",
    )

    ordering = (
        "section",
        "order",
    )


# =========================================================
# QUIZ
# =========================================================

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "lesson",
        "passing_score",
        "time_limit",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
        "lesson__title",
    )

    ordering = (
        "lesson",
    )

    inlines = [
        QuestionInline,
    ]


# =========================================================
# QUESTION
# =========================================================

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "quiz",
        "marks",
        "order",
    )

    list_filter = (
        "quiz",
    )

    search_fields = (
        "question",
        "quiz__title",
    )

    ordering = (
        "quiz",
        "order",
    )

    inlines = [
        OptionInline,
    ]


# =========================================================
# OPTION
# =========================================================

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):

    list_display = (
        "option_text",
        "question",
        "is_correct",
    )

    list_filter = (
        "is_correct",
        "question__quiz",
    )

    search_fields = (
        "option_text",
        "question__question",
    )


# =========================================================
# LESSON PROGRESS
# =========================================================

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "lesson",
        "completed",
        "watched_percentage",
        "last_watched_at",
    )

    list_filter = (
        "completed",
        "lesson",
    )

    search_fields = (
        "user__username",
        "user__email",
        "lesson__title",
    )

    readonly_fields = (
        "last_watched_at",
    )


# =========================================================
# STUDENT ANSWER INLINE
# =========================================================

class StudentAnswerInline(admin.TabularInline):

    model = StudentAnswer

    extra = 0

    can_delete = False

    show_change_link = False

    readonly_fields = (
        "question",
        "selected_option",
        "is_correct",
    )


# =========================================================
# QUIZ ATTEMPT
# =========================================================

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "quiz",
        "correct_answers",
        "total_questions",
        "score",
        "percentage",
        "passed",
        "submitted_at",
    )

    list_filter = (
        "passed",
        "quiz",
    )

    search_fields = (
        "student__username",
        "student__email",
        "quiz__title",
    )

    readonly_fields = (
        "student",
        "quiz",
        "correct_answers",
        "total_questions",
        "score",
        "percentage",
        "passed",
        "started_at",
        "submitted_at",
    )

    ordering = (
        "-submitted_at",
    )

    inlines = [
        StudentAnswerInline,
    ]