from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django_resized import ResizedImageField
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from django.core.files.storage import default_storage

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
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_posts', verbose_name = "نویسنده")
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
    reading_time = models.PositiveIntegerField(verbose_name = "زمان مطالعه")
    
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


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments', verbose_name = "پست")
    name = models.CharField(max_length = 250, verbose_name = "نام")
    body = models.TextField(verbose_name = "متن کامنت")
    created = models.DateTimeField(auto_now_add = True, verbose_name = "تاریخ ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name = "تاریخ ویرایش")
    active = models.BooleanField(default=False, verbose_name = "وضعیت")

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields = ["created"]),
        ]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f"{self.name} : {self.post}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name="پست")
    image_file = ResizedImageField(upload_to="post_images/", size=[500, 500], quality=75, crop=["middle", "center"])
    title = models.CharField(max_length=250, verbose_name="عنوان", null=True, blank=True)
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields = ["created"]),
        ]
        verbose_name = "تصویر"
        verbose_name_plural = "تصویر ها"

    def __str__(self):
        return self.title if self.title else "None"


@receiver(post_delete, sender=Image)
def delete_image_file(sender, instance, **kwargs):
    if instance.image_file:
        default_storage.delete(instance.image_file.name)