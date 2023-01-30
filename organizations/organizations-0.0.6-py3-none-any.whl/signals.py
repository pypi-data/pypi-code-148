from django.dispatch import receiver
from .models import Organization, OrganizationKeys, UserProxy, OrganizationOnboardingNotification
from django.db.models.signals import post_save
from mnemonic import Mnemonic
from eth_account import Account
from organizations.tasks import create_organization_did
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.http.request import HttpRequest
from django.core import mail
from templates_service_client.client import Client
from templates_service_client.validators import (
    OperatorOnboardingValidator
)
from .service import OrganizationsService
from django.utils.timezone import now
from django.utils.html import strip_tags





@receiver(post_save, sender=UserProxy)
def post_save_profile(sender, instance, **kwargs):
    if kwargs.get("created"):
        instance.is_staff = True
        instance.save()
        print(sender)
        print(type(sender))
        print(dir(sender))
        print(kwargs)
        

@receiver(post_save, sender=OrganizationOnboardingNotification)
def post_save_onboarding_request(sender, instance, **kwargs):
    template_client = Client(settings.TEMPLATES_SERVICE_HOST)
    html_message = template_client.get_operators_onboarding_template_rendered(OperatorOnboardingValidator(
                project=settings.TEMPLATES_PROJECT_NAME,
                organization_name=instance.organization.name,
                app_path=settings.APP_PATH,
                web_path=settings.WEB_PATH
            )).text.replace("\n", "")
    mail.send_mail("Onboarding", strip_tags(html_message), settings.DEFAULT_FROM_EMAIL, [instance.operator.email], html_message=html_message)

@receiver(post_save, sender=Organization)
def post_save_organization(sender, instance, **kwargs):
    if kwargs.get("created"):
        mnemo = Mnemonic("english")
        words = mnemo.generate(strength=256)
        mnemo.to_seed(words)
        mnemo.to_entropy(words)
        new_organization_acct = Account.create(words)
        organization_keys = OrganizationKeys(
            address=new_organization_acct.address,
            private_key=new_organization_acct.key.hex(),
            public_key=new_organization_acct._key_obj.public_key,
            mnemonic=words,
        )
        organization_keys.save()
        instance.keys = organization_keys
        instance.save()
        create_organization_did.delay(instance.pk)
    else:
        for operator in instance.operators.all(): # TODO PUT IT IN A TASK
            if not OrganizationOnboardingNotification.objects.filter(organization=instance, operator=operator).first():
                OrganizationOnboardingNotification(
                    organization=instance, 
                    operator=operator,
                    sended_at=now()
                ).save()
