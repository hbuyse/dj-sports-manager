# -*- coding: utf-8
"""Representation of the 'sponsoring' application and its configuration."""

# Standard library
import logging

# Django
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class SportsManagerConfig(AppConfig):
    """Representation of the 'sports-manager' application and its configuration."""

    name = 'sports_manager'

    def ready(self):
        """Run when Django starts."""
        logger.debug("App {} ready.".format(self.name))
