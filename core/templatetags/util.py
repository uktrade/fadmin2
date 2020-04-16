import os
import json

from copy import copy

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def render_front_end_script():
    if not settings.DEBUG:
        return mark_safe(
            '<script '
            'type="text/javascript" ' 
            'src="http://localhost:3000/static/js/bundle.js">' 
            '</script>'
        )
    else:
        assets_manifest_path = os.path.join(
            settings.BASE_DIR, "front_end/build/asset-manifest.json"
        )
        with open(assets_manifest_path) as assets_manifest:
            asset_json = json.load(assets_manifest)
            scripts = []

            for key in asset_json:
                if asset_json[key].endswith(".js"):
                    scripts.append(
                        '<script '
                        'type="text/javascript" '
                        f'src="/{asset_json[key]}">'
                        '</script>'
                    )

            return mark_safe(
                ''.join(scripts)
            )


@register.filter('startswith')
def startswith(text, starts):
    return text.startswith(starts)


@register.filter
def instances_and_widgets(bound_field):
    """Allows the access of both model instance
    and form widget in template"""
    instance_widgets = []
    index = 0
    for instance in bound_field.field.queryset.all():
        widget = copy(bound_field[index])
        instance_widgets.append((instance, widget))
        index += 1
    return instance_widgets
