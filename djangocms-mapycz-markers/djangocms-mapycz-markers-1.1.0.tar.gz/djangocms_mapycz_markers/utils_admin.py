"""Utils for Aldryn forms submissions list.

Usage:
ALDRYN_FORMS_SUBMISSION_LIST_DISPLAY_FIELD = "djangocms_mapycz_markers.utils_admin.form_submission_field"
"""
from typing import Optional

from aldryn_forms.models import FormPlugin, FormSubmission
from django.utils.html import format_html_join

from .cms_plugins import ConnectorCMSPlugin
from .models import MarkerPlugin


def form_submission_field(submitted_form: FormSubmission) -> str:
    """Aldryn forms submission."""
    links = set()
    for form in FormPlugin.objects.filter(name=submitted_form.name):
        plugin: Optional[ConnectorCMSPlugin] = form.get_children().filter(plugin_type='ConnectorCMSPlugin').first()
        if plugin is None:
            continue  # Form does not have the ConnectorPlugin.
        connector = plugin.get_plugin_instance()[0]  # (instance, class)
        if connector.map is None:
            continue  # MapPlugin is not defined.
        if connector.latitude is None or connector.longitude is None:
            return ""  # Geographical coordinate names missing.
        post = {field.name: field.value for field in submitted_form.get_form_data()}
        latitude, longitude = post.get(connector.latitude), post.get(connector.longitude)
        if latitude is None or longitude is None:
            return ""  # Geographical coordinate values missing.
        address = post.get(connector.address)
        for marker in MarkerPlugin.objects.filter(latitude=latitude, longitude=longitude):
            map = marker.get_parent()
            links.add((
                map.placeholder.page.get_absolute_url(),
                address,
                map.placeholder.page.get_title(submitted_form.language)
            ))
    return format_html_join(', ', '<a href="{}" target="_top" title="{}">{}</a>', links)
