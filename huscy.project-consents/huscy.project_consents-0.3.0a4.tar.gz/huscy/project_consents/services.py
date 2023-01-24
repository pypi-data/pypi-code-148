from .models import ProjectConsent, ProjectConsentCategory
from huscy.consents.services import (create_consent, create_consent_category,
                                     update_consent, update_consent_category)


def create_project_consent_category(name, template_text_fragments):
    consent_category = create_consent_category(name, template_text_fragments)
    return ProjectConsentCategory.objects.create(consent_category=consent_category)


def create_project_consent(project, name, text_fragments):
    consent = create_consent(name, text_fragments)
    return ProjectConsent.objects.create(project=project, consent=consent)


def update_project_consent_category(project_consent_category, name=None,
                                    template_text_fragments=None):
    update_consent_category(project_consent_category.consent_category,
                            name=name,
                            template_text_fragments=template_text_fragments)
    return project_consent_category


def update_project_consent(project_consent, name=None, text_fragments=None):
    update_consent(project_consent.consent, name, text_fragments)
    return project_consent
