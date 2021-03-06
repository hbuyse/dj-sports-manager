#! /usr/bin/env python
"""Context processors."""

# Django
from django.conf import settings


def sports_manager_data(request):
    return {'sports_manager': settings.SPORTS_MANAGER}
