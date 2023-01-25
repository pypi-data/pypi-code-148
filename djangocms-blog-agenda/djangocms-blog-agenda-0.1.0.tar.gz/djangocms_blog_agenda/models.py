from django.db import models
from django.utils.translation import gettext_lazy as _
from djangocms_blog.models import Post


class PostExtension(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="extension")
    event_date = models.DateTimeField(verbose_name=_("Event date"))
