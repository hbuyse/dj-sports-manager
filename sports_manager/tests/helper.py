#! /usr/bin/env python
# coding=utf-8

"""Generate objects."""

# Standard library
import logging
import sys
from datetime import date, datetime, timedelta
from importlib import reload, import_module
from unittest import mock

# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db.models.base import ModelBase
from django.urls.base import clear_url_caches

# Current django project
from sports_manager.category.models import Category
from sports_manager.gymnasium.models import Gymnasium
from sports_manager.player.models import Player, MedicalCertificate, EmergencyContact
from sports_manager.team.models import Team, TimeSlot

logger = logging.getLogger(__name__)


class HelperAttributeNotConfigured(Exception):
    pass


class HelperAttributeImproperlyConfigured(Exception):
    pass


class Helper(object):

    defaults = {}
    iter_fields = list()
    model = None

    def __init__(self, *args, **kwargs):
        """Constructor.
        
        Set default first and then we update the defaults.
        """
        super().__init__()  # TypeError: object.__init__() takes no arguments

        # Set the default fields
        for k, v in self.get_defaults().items():
            setattr(self, k, v)
        
        # Overload the fields
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._object = None
    
    def __iter__(self):
        for key in self.get_iter_fields():
            if issubclass(type(getattr(self, key)), Helper):
                yield (key, getattr(self, key).object)
            else:
                yield (key, getattr(self, key))

    def get_defaults(self):
        if not getattr(self, "defaults"):
            raise HelperAttributeNotConfigured("'defaults' field not set. You have to set it.")
        elif not isinstance(self.defaults, dict):
            raise HelperAttributeImproperlyConfigured("'defaults' field has to be a dict.")
        return self.defaults
    
    def get_model(self):
        """."""
        if not getattr(self, "model"):
            raise HelperAttributeNotConfigured("'model' field not set. You have to set it.")
        elif not isinstance(self.model, ModelBase):
            raise HelperAttributeImproperlyConfigured("'model' field has to be a django.db.models.base.ModelBase.")
        return self.model
    
    def get_iter_fields(self):
        """."""
        if not getattr(self, "iter_fields"):
            raise HelperAttributeNotConfigured("'iter_fields' field not set. You have to set it.")
        elif not isinstance(self.iter_fields, (list, tuple)):
            raise HelperAttributeImproperlyConfigured("'iter_fields' field has to be a list or a tuple.")
        return self.iter_fields
    
    def create(self):
        self._object = self.get_model().objects.create(**dict(self))
    
    def destroy(self):
        self.get_model().objects.get(pk=self._object.pk).delete()
    
    def get(self, attr):
        if self._object is None:
            self.create()
        return getattr(self._object, attr)
    
    @property
    def datas_for_form(self):
        for key in self.get_iter_fields():
            if issubclass(type(getattr(self, key)), Helper):
                yield (key, getattr(self, key).get('pk'))
            else:
                yield (key, getattr(self, key))
    
    @property
    def object(self):
        if self._object is None:
            self.create()
        return self._object
    
    @property
    def pk(self):
        return self.get('pk')


class GymnasiumHelper(Helper):

    defaults = {
        'type': Gymnasium.GYMNASIUM_TYPE,
        'name': "Toto",
        'address': "Toto",
        'city': "Toto",
        'zip_code': "12345",
        'phone': "0100000000",
        'area': "48",
        'capacity': "2",
    }
    model = Gymnasium
    iter_fields = ['type', 'name', 'address', 'city', 'zip_code', 'phone', 'area', 'capacity']


class CategoryHelper(Helper):
    
    defaults = {
        'name': 'Hello World',
        'min_age': 18,
        'summary': 'TODO',
        'description': '# TODO',
        'img': mock.MagicMock(spec=File, name='file.png', size=1 << 20), # Mock of File 'file.png' with size 2MB
    }
    model = Category
    iter_fields = ['name', 'min_age', 'summary', 'description']


class TeamHelper(Helper):
    """Create a Team object and save it in the DB."""
    
    defaults = {
        'name': 'Hello World Team',
        'level': 'GOL',
        'sex': 'MI',
        'url': 'http://example.com',
        'description': '# TODO',
        'recruitment': True,
    }
    model = Team
    iter_fields = ['name', 'level', 'sex', 'url', 'description', 'recruitment', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = CategoryHelper()


class TimeSlotHelper(Helper):
    """Create a TimeSlot object and save it in the DB."""
    
    defaults = {
        'type': TimeSlot.PRACTICE,
        'day': TimeSlot.MONDAY,
        'start': datetime.strptime('20:00:00', '%H:%M:%S'),
        'end': datetime.strptime('22:30:00', '%H:%M:%S'),
    }
    model = TimeSlot
    iter_fields = ['type', 'day', 'start', 'end', 'team', 'gymnasium']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.team = TeamHelper() if 'team' not in kwargs else kwargs['team']
        self.gymnasium = GymnasiumHelper() if 'gymnasium' not in kwargs else kwargs['gymnasium']




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
    gymnasium = GymnasiumHelper()

    time_slot_info['team'] = team
    time_slot_info['gymnasium'] = gymnasium.object
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


def create_medical_certificate(player):
    """Create a MedicalCertificate object and save it into the DB."""
    mc_info = {
        'player': player,
        'file': mock.MagicMock(spec=File),
        'start': date.today(),
        'end': date.today() + timedelta(weeks=52),
        'validation': MedicalCertificate.IN_VALIDATION,
    }

    mc = MedicalCertificate.objects.create(**mc_info)

    return mc_info, mc


def create_emergency_contact(player):
    """Create a EmergencyContact object and save it into the DB."""
    ec_info = {
        'player': player,
        'first_name': "Toto",
        'last_name': "Tata",
        'phone': "MA",
    }

    ec = EmergencyContact.objects.create(**ec_info)

    return ec_info, ec


def create_user(username='toto', staff=False, superuser=False):
    """Create a standard, staff or super user."""
    user_info = {
        'username': username,
        'password': "hello-world",
        'first_name': "Toto",
        'last_name': "Tata",
        'is_staff': True if staff or superuser else False,  # Attention: Superuser must have is_staff=True.
        'email': 'toto@example.com',
    }

    if superuser:
        user = get_user_model().objects.create_superuser(**user_info)
    else:
        user = get_user_model().objects.create_user(**user_info)

    return user_info, user


def reload_urlconf(urlconf=None):
    clear_url_caches()
    if urlconf is None:
        urlconf = settings.ROOT_URLCONF
    if urlconf in sys.modules:
        reload(sys.modules[urlconf])
    else:
        import_module(urlconf)