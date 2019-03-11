# -*- coding: utf-8 -*-

"""Apps mixins."""

# Standard library
import logging

# Django
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import ugettext_lazy as _  # noqa

logger = logging.getLogger(__name__)


class StaffMixin(UserPassesTestMixin):
    """Mixin allows you to require a user with `is_staff` set to True."""

    raise_exception = True

    def test_func(self):
        """Check if the logged user is staff."""
        return self.request.user.is_staff


class SuperuserMixin(UserPassesTestMixin):
    """Mixin allows you to require a user with `is_superuser` set to True."""

    raise_exception = True

    def test_func(self):
        """Check if the logged user is superuser."""
        return self.request.user.is_superuser


class OwnerMixin(UserPassesTestMixin):
    """Mixin that test if the logged user owns the page."""

    owner_kwargs = 'username'
    raise_exception = True

    def test_func(self):
        """Check if the logged user is the owner of the page."""
        return self.request.user.get_username() == self.kwargs.get(self.owner_kwargs)


class OwnerOrStaffMixin(UserPassesTestMixin):
    """Mixin that check if the user logged in has the rights to view the page."""

    owner_kwargs = 'username'
    permission_denied_message = _("You do not have the right to view this page.")            # from AccessMixin
    raise_exception = True

    def test_func(self):
        """Check if the user logged in has the rights to view the page."""
        if self.request.user.is_staff:
            logger.info(_("Staff user %(username)s accessed '%(url)s' page") % {
                'username': self.request.user.get_username(),
                'url': self.request.path
            })
            ret = True
        elif self.request.user.get_username() == self.kwargs.get(self.owner_kwargs):
            ret = True
        else:
            ret = False
        return ret
