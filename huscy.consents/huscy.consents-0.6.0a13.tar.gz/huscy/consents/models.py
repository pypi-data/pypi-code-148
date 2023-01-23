from django.db import models


class Consent(models.Model):
    name = models.CharField(max_length=128)
    text_fragments = models.JSONField()

    def __str__(self):
        return self.name


class ConsentFile(models.Model):
    consent = models.ForeignKey(Consent, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    filehandle = models.FileField()


class ConsentCategory(models.Model):
    name = models.CharField(max_length=128)
    template_text_fragments = models.JSONField(default=list)
