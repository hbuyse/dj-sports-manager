# -*- coding: utf-8 -*-

# Django
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffMixin(UserPassesTestMixin):
    """
    Mixin allows you to require a user with `is_staff` set to True.
    """
    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff


class SuperuserMixin(UserPassesTestMixin):
    """
    Mixin allows you to require a user with `is_superuser` set to True.
    """
    raise_exception = True

    def test_func(self):
        return self.request.user.is_superuser


class OwnerMixin(UserPassesTestMixin):
    owner_kwargs = 'username'
    raise_exception = True

    def test_func(self):
        return self.request.user.user.username == self.kwargs.get(self.owner_kwargs)


def test_user_staff(user):
    """Test if the connected user is part of staff."""
    return user.is_staff


def test_user_superuser(user):
    """Test if the connected user is a superuser."""
    return user.is_superuser


def test_user_own_page(user, kwargs, field_to_test):
    """Test if the user logged in owned the page asked to be accessed."""
    return user.get_username() == kwargs.get(field_to_test) 


def test_access_private_page(user, kwargs, field_to_test):
    """Fusion of all the tests defined above."""
    return test_user_staff(user) or \
            test_user_superuser(user) or \
            test_user_own_page(user, kwargs, field_to_test)

class OwnerOrStaffMixin(UserPassesTestMixin):
    """Mixin that check if the user logged in has the rights to view the page."""
    permission_denied_message = "You do not have the right to view this page."            # from AccessMixin
    raise_exception = True

    def test_func(self):
        return test_access_private_page(self.request.user, self.kwargs, 'username')
