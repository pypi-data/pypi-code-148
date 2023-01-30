from celery import shared_task
from django.conf import settings
from network_service_client.client import (
    Client as NetworkClient,
    Network as NetworkDTO,
    NetworksNames,
)
from organizations.did_factory.models import FactoryArgsModel
from organizations.did_factory.factory import Creator
from organizations.models import Organization, OrganizationDID


@shared_task
def create_organization_did(organization_id: int) -> None:
    organization = Organization.objects.get(pk=organization_id)
    for net in organization.networks:
        network_data: NetworkDTO = NetworkClient(
            service_host=settings.NETWORK_SERVICE_HOST
        ).get_network_by_name(
            NetworksNames[net]
        )  # TODO ADD LACC SOME DAY ?
        props = FactoryArgsModel(net=network_data)
        context = Creator().create_object(props).request()
        did: str = context.create_did(
            organization.keys.address,
            settings.ISSUER_ADDRESS,
            str(organization.keys.public_key),
            settings.ISSUER_PRIVATE_KEY,
            organization.keys.private_key,  # TODO: encrypt this
        )

        organization_did = OrganizationDID(
            network_name=NetworksNames.AlastriaDefaultName,
            organization=organization,
            did=did,
        )

        organization_did.save()
