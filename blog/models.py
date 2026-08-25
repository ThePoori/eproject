from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = Post.Status.PUBLISHED)

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DR", "Draft"
        PUBLISHED = "PB", "Published"
        REJECTED = "RE", "Rejected"
    # User
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'blog', verbose_name = "نویسنده")
    # Text Fields
    title = models.CharField(max_length = 250, verbose_name = "عنوان")
    description = models.TextField(verbose_name = "توضیحات")
    slug = models.SlugField(max_length = 250, verbose_name = "اسلاگ")
    # Date
    publish = models.DateTimeField(default = timezone.now, verbose_name = "تاریخ")
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    # Choose Fields
    status = models.CharField(max_length = 2, choices = Status.choices, default = Status.DRAFT)
    # Manages
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(
                fields = ["publish"]
            )
        ]
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=(self.id, ))


class Ticket(models.Model):
    message = models.TextField(verbose_name = "متن")
    name = models.CharField(max_length = 250, verbose_name = "نام")
    email = models.EmailField(verbose_name = "ایمیل")
    phone = models.CharField(max_length = 11, verbose_name = "شماره همراه")
    subject = models.CharField(max_length = 250, verbose_name = "موضوع")

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def __str__(self):
        return self.name