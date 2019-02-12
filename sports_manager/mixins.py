# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class StaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin allows you to require a user with `is_staff` set to True.
    """
    raise_exception = True

    def test_func(self):
        return self.request.is_staff


class SuperuserMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin allows you to require a user with `is_superuser` set to True.
    """
    raise_exception = True

    def test_func(self):
        return self.request.is_superuser


class OwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    owner_kwargs = 'username'
    raise_exception = True

    def test_func(self):
        return self.request.user.username == self.kwargs.get(self.owner_kwargs)