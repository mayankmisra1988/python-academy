from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100,unique=True,)
    slug = models.SlugField(unique=True,)
    description = models.TextField(blank=True,)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"


class Course(models.Model):
    LEVEL_CHOICES = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    )

    instructor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="courses",)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name="courses",)
    title = models.CharField(max_length=255,)
    slug = models.SlugField(unique=True,)
    short_description = models.CharField(max_length=300,)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="courses/",blank=True,null=True,)
    level = models.CharField(max_length=20,choices=LEVEL_CHOICES,default="beginner",)
    price = models.DecimalField(max_digits=8,decimal_places=2,default=0,)
    is_free = models.BooleanField(default=True,)
    is_published = models.BooleanField(default=False,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)
    
    def save(self, *args, **kwargs):
        self.is_free = self.price == 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]