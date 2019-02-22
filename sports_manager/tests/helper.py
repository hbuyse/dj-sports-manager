#! /usr/bin/env python
# coding=utf-8

"""Generate objects."""

# Standard library
from datetime import date, datetime, timedelta

# Django
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Current django project
from sports_manager.models import Category, Gymnasium, Player, Team, TimeSlot


def create_gymnasium():
    """Create a gymnasium."""
    gymnasium_info = {
        'name': "Toto",
        'address': "Toto",
        'city': "Toto",
        'zip_code': 12345,
        'phone': "0100000000",
        'surface': "48",
        'capacity': "2",
    }

    gymnasium = Gymnasium.objects.create(**gymnasium_info)

    return gymnasium_info, gymnasium


def create_category():
    """Create a Category object and save it in the DB."""
    category_info = {
        'name': 'Hello World',
        'min_age': 18,
        'summary': 'TODO',
        'description': '# TODO'
    }
    category_info['slug'] = slugify(category_info['name'])

    category = Category.objects.create(**category_info)

    return category_info, category


def create_team():
    """Create a Team object and save it in the DB."""
    team_info = {
        'name': 'Hello World Team',
        'level': 'GOL',
        'sex': 'MI',
        'url': 'http://example.com',
        'description': '# TODO',
        'recruitment': True,
    }
    category = create_category()[1]

    team_info['slug'] = slugify(team_info['name'])
    team_info['category'] = category
    team = Team.objects.create(**team_info)

    return team_info, team


def create_time_slot(team=None):
    """Create a TimeSlot object and save it in the DB."""
    time_slot_info = {
        'type': TimeSlot.PRACTICE,
        'day': TimeSlot.MONDAY,
        'start': datetime.strptime('20:00:00', '%H:%M:%S'),
        'end': datetime.strptime('22:30:00', '%H:%M:%S'),
    }
    if team is None:
        team = create_team()[1]
    gymnasium = create_gymnasium()[1]

    time_slot_info['team'] = team
    time_slot_info['gymnasium'] = gymnasium
    time_slot = TimeSlot.objects.create(**time_slot_info)

    return time_slot_info, time_slot


def create_player(owner):
    """Create a Player object and save it into the DB."""
    player_info = {
        'owner': owner,
        'first_name': "Toto",
        'last_name': "Tata",
        'sex': "MA",
        'birthday': date.today() - timedelta(weeks=10*52)
    }

    player = Player.objects.create(**player_info)

    return player_info, player


def create_user(username='toto', staff=False, superuser=False):
    """Create a standard, staff or super user."""
    user_info = {
        'username': username,
        'password': "hello-world",
        'first_name': "Toto",
        'last_name': "Tata",
        'is_staff': True if staff or superuser else False,
        'email': 'toto@example.com',
    }

    if superuser:
        user = get_user_model().objects.create_superuser(**user_info)
    else:
        user = get_user_model().objects.create_user(**user_info)

    return user_info, user
