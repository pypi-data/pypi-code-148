from django.db import models

from huscy.consents.models import Consent, ConsentCategory, ConsentFile
from huscy.projects.models import Project
from huscy.subjects.models import Subject


class ProjectConsentCategory(models.Model):
    consent_category = models.OneToOneField(ConsentCategory, on_delete=models.PROTECT)

    @property
    def name(self):
        return self.consent_category.name

    @property
    def template_text_fragments(self):
        return self.consent_category.template_text_fragments


class ProjectConsent(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    consent = models.ForeignKey(Consent, on_delete=models.PROTECT)

    @property
    def name(self):
        return self.consent.name

    @property
    def text_fragments(self):
        return self.consent.text_fragments


class ProjectConsentFile(models.Model):
    project_consent = models.ForeignKey(ProjectConsent, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    consent_file = models.OneToOneField(ConsentFile, on_delete=models.PROTECT)

    class Meta:
        unique_together = 'project_consent', 'subject'
