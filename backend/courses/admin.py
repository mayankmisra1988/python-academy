from django.contrib import admin
from .models import Category, Course


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "instructor",
        "level",
        "price",
        "is_free",
        "is_published",
        "created_at",
    )

    list_filter = (
        "level",
        "is_free",
        "is_published",
        "category",
    )

    search_fields = (
        "title",
        "description",
    )
    
    prepopulated_fields = {
        "slug": ("title",)
    }

    list_editable = (
        "is_published",
    )