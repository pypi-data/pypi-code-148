from django.http import HttpResponse
from django.template import loader

from airavata_custos_portal.apps.api.views import get_config


def home(request, clientId=None):
    template = loader.get_template('airavata_custos_portal_frontend/index.html')
    context = {
        'config': get_config(request).data,
    }

    return HttpResponse(template.render(context, request))
