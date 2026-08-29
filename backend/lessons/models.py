from django.db import models
from courses.models import Course
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Section(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="sections",)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        unique_together = ("course", "order")

    def __str__(self):
        return self.title


class Lesson(models.Model):
    section = models.ForeignKey(Section,on_delete=models.CASCADE,related_name="lessons",)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    notes = models.FileField(upload_to="lesson_notes/",blank=True,null=True,)
    duration = models.PositiveIntegerField(default=0,help_text="Duration in minutes",)
    
    is_published = models.BooleanField(default=False)
    is_preview = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        unique_together = ("section", "order")
        indexes = [
            models.Index(fields=["section", "order"]),
        ]

    def __str__(self):
        return f"{self.section.title} - {self.title}"


class LessonProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_progress",
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="progress",
    )

    completed = models.BooleanField(default=False)
    watched_percentage = models.PositiveSmallIntegerField(default=0,
            validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    last_watched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "lesson")
        ordering = ["lesson"]

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"


class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson,on_delete=models.CASCADE,related_name="quiz",)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    passing_score = models.PositiveSmallIntegerField(
        default=70,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
    )

    time_limit = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Time limit in minutes"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["lesson"]
        indexes = [
            models.Index(fields=["lesson"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    question = models.TextField()

    explanation = models.TextField(
        blank=True,
        help_text="Shown after quiz submission."
    )

    marks = models.PositiveSmallIntegerField(default=1)

    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]
        unique_together = ("quiz", "order")
        indexes = [
            models.Index(fields=["quiz", "order"]),
        ]

    def __str__(self):
        return f"Q{self.order} - {self.quiz.title}"


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options",
    )

    option_text = models.CharField(max_length=500)

    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.option_text


class QuizAttempt(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="attempts",
    )

    total_questions = models.PositiveIntegerField(default=0)

    correct_answers = models.PositiveIntegerField(default=0)

    score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
    )
    percentage = models.PositiveSmallIntegerField(default=0)

    passed = models.BooleanField(default=False)

    started_at = models.DateTimeField(auto_now_add=True)

    submitted_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submitted_at"]
        indexes = [
            models.Index(fields=["student", "quiz"]),
        ]

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"


class StudentAnswer(models.Model):
    attempt = models.ForeignKey( QuizAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    question = models.ForeignKey(Question,on_delete=models.CASCADE,)
    selected_option = models.ForeignKey( 
        Option,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,)

    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ("attempt", "question")

    def __str__(self):
        return f"{self.attempt.student.username} - Question {self.question.id}"