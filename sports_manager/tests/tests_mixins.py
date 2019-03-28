#! /usr/bin/env python
# coding=utf-8

# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse, Http404
from django.test import RequestFactory, TestCase
from django.views.generic import View

# Current django project
from sports_manager.mixins import OwnerMixin, OwnerOrStaffMixin, StaffMixin, SuperuserMixin
from sports_manager.tests.helper import UserHelper


class StaffMixinTest(TestCase):
    '''
    Tests StaffMixin like a boss
    '''

    class StaffMixinView(StaffMixin, View):

        def get(self, request, *args, **kwargs):
            return HttpResponse()

    def setUp(self):
        # Every test needs access to the request factory.
        self.request = RequestFactory().get('/rand')
        self.view = self.StaffMixinView

    def test_anonymous(self):
        self.request.user = AnonymousUser()
        
        with self.assertRaises(PermissionDenied):
            self.view.as_view()(self.request)

    def test_normal_user(self):
        user = UserHelper()
        self.request.user = user.object
        
        with self.assertRaises(PermissionDenied):
            self.view.as_view()(self.request)

    def test_staff_user(self):
        user = UserHelper(is_staff=True)
        self.request.user = user.object

        response = self.view.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_superuser_user(self):
        user = UserHelper(is_superuser=True)
        self.request.user = user.object

        response = self.view.as_view()(self.request)
        self.assertEqual(response.status_code, 200)


class SuperuserMixinTest(TestCase):
    '''
    Tests SuperuserMixin like a boss
    '''
    
    class SuperuserMixinView(SuperuserMixin, View):

        def get(self, request, *args, **kwargs):
            return HttpResponse()

    def setUp(self):
        # Every test needs access to the request factory.
        self.request = RequestFactory().get('/rand')
        self.view = self.SuperuserMixinView

    def test_anonymous(self):
        self.request.user = AnonymousUser()
        
        with self.assertRaises(PermissionDenied):
            self.view.as_view()(self.request)

    def test_normal_user(self):
        user = UserHelper()
        self.request.user = user.object
        
        with self.assertRaises(PermissionDenied):
            self.view.as_view()(self.request)

    def test_staff_user(self):
        user = UserHelper(is_staff=True)
        self.request.user = user.object
        
        with self.assertRaises(PermissionDenied):
            self.view.as_view()(self.request)

    def test_superuser_user(self):
        user = UserHelper(is_superuser=True)
        self.request.user = user.object
        response = self.view.as_view()(self.request)
        self.assertEqual(response.status_code, 200)


class OwnerMixinTest(TestCase):
    '''
    Tests OwnerMixin like a boss
    '''


    class OwnerMixinView(OwnerMixin, View):

        def get(self, request, *args, **kwargs):
            return HttpResponse()

    def setUp(self):
        # Every test needs access to the request factory.
        self.request = RequestFactory().get('/rand')
        self.view = self.OwnerMixinView

    def test_anonymous_user_not_valid(self):
        user = UserHelper()
        kwargs = {'username': user.object.get_username() + 'a'}
        self.request.user = AnonymousUser()

        with self.assertRaises(Http404):
            self.view.as_view()(self.request, **kwargs)

    def test_normal_user_is_not_owner(self):
        user = UserHelper()
        kwargs = {'username': user.object.get_username() + 'a'}
        self.request.user = user.object
        
        with self.assertRaises(Http404):
            self.view.as_view()(self.request, **kwargs)

    def test_normal_user_is_owner(self):
        user = UserHelper()
        kwargs = {'username': user.object.get_username()}
        self.request.user = user.object
        self.view.as_view()(self.request, **kwargs)

    def test_staff_user_is_not_owner(self):
        user = UserHelper(is_staff=True)
        kwargs = {'username': user.object.get_username() + 'a'}
        self.request.user = user.object
        
        with self.assertRaises(Http404):
            self.view.as_view()(self.request, **kwargs)

    def test_staff_user_is_owner(self):
        user = UserHelper(is_staff=True)
        kwargs = {'username': user.object.get_username()}
        self.request.user = user.object
        self.view.as_view()(self.request, **kwargs)

    def test_superuser_user_is_not_owner(self):
        user = UserHelper(is_superuser=True)
        kwargs = {'username': user.object.get_username() + 'a'}
        self.request.user = user.object
        
        with self.assertRaises(Http404):
            self.view.as_view()(self.request, **kwargs)

    def test_superuser_user_is_owner(self):
        user = UserHelper(is_superuser=True)
        kwargs = {'username': user.object.get_username()}
        self.request.user = user.object
        self.view.as_view()(self.request, **kwargs)


class OwnerOrStaffMixinTest(TestCase):
    '''
    Tests OwnerOrStaffMixin like a boss
    '''


    class OwnerOrStaffMixinView(OwnerOrStaffMixin, View):

        def get(self, request, *args, **kwargs):
            return HttpResponse()

    def setUp(self):
        # Every test needs access to the request factory.
        self.request = RequestFactory().get('/rand')
        self.view = self.OwnerOrStaffMixinView

    def test_anonymous(self):
        kwargs = {'username': 'hello'}
        self.request.user = AnonymousUser()

        with self.assertRaises(Http404):
            self.view.as_view()(self.request, **kwargs)

    def test_normal_user_is_not_owner(self):
        user = UserHelper()
        kwargs = {'username': user.object.get_username() + 'a'}
        self.request.user = user.object

        with self.assertRaises(Http404):
            self.view.as_view()(self.request, **kwargs)

    def test_normal_user_is_owner(self):
        user = UserHelper()
        kwargs = {'username': user.object.get_username()}
        self.request.user = user.object
        self.view.as_view()(self.request, **kwargs)

    def test_staff_user_is_not_owner(self):
        user = UserHelper(is_staff=True)
        kwargs = {'username': user.object.get_username() + 'a'}
        self.request.user = user.object

        with self.assertRaises(Http404):
            self.view.as_view()(self.request, **kwargs)

    def test_staff_user_is_owner(self):
        user = UserHelper(is_staff=True)
        kwargs = {'username': user.object.get_username()}
        self.request.user = user.object
        self.view.as_view()(self.request, **kwargs)

    def test_superuser_user_is_not_owner(self):
        user = UserHelper(is_superuser=True)
        kwargs = {'username': user.object.get_username() + 'a'}
        self.request.user = user.object
        
        with self.assertRaises(Http404):
            self.view.as_view()(self.request, **kwargs)

    def test_superuser_user_is_owner(self):
        user = UserHelper(is_superuser=True)
        kwargs = {'username': user.object.get_username()}
        self.request.user = user.object
        self.view.as_view()(self.request, **kwargs)
