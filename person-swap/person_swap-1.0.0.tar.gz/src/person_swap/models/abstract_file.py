from django.conf import settings
from django.db import models


class FileType(models.TextChoices):
    IMAGE = "Image"
    MP3 = "MP3"
    VIDEO = "Video"
    OTHER = "Other"


class AbstractFile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    public = models.BooleanField(default=True, null=True, blank=True)
    title = models.CharField(max_length=120, null=True, blank=True)
    type = models.CharField(
        max_length=5,
        choices=FileType.choices,
        default=FileType.OTHER,
    )

    def save(self, *args, **kwargs):
        # TODO SAVE OWNER
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or self._meta.label.split('.')[1] + ' ' + str(self.pk)
