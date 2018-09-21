#! /usr/bin/env python
# coding=utf-8

"""Generate objects."""

from dj_sports_manager.models import Category

from django.contrib.auth import get_user_model
from django.utils.text import slugify


def create_category():
    """Create a Category."""
    category_info = {
        'name': 'Hello World',
        'min_age': 18,
        'summary': 'TODO',
        'description': '# TODO'
    }
    category_info['slug'] = slugify(category_info['name'])
    category = Category.objects.create(**category_info)

    return category_info, category


def create_user(staff=False, superuser=False):
    """Create a standard, staff or super user."""
    user_info = {
        'username': "hbuyse",
        'password': "usermodel",
        'first_name': "Henri",
        'last_name': "Buyse",
        'is_staff': True if staff or superuser else False,
        'email': 'toto@example.com',
    }
    if superuser:
        user = get_user_model().objects.create_superuser(**user_info)
    else:
        user = get_user_model().objects.create_user(**user_info)

    return user_info, user
