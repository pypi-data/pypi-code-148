from django.dispatch import receiver
from .models import Organization, OrganizationKeys, UserProxy
from django.db.models.signals import post_save
from mnemonic import Mnemonic
from eth_account import Account
from organizations.tasks import create_organization_did
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.http.request import HttpRequest


@receiver(post_save, sender=UserProxy)
def post_save_profile(sender, instance, **kwargs):
    if kwargs.get("created"):
        instance.is_staff = True
        instance.save()
        form = PasswordResetForm({"email": instance.email})
        if form.is_valid():
            request = HttpRequest()
            request.META["SERVER_NAME"] = settings.SERVER_NAME
            request.META["SERVER_PORT"] = settings.SERVER_PORT
            form.save(
                request=request,
                use_https=settings.USE_HTTPS,
                from_email=settings.DEFAULT_FROM_EMAIL,
                html_email_template_name="organizations/welcome_operator.html",
            )


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
