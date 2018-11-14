import unittest
import datetime

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from . import views
from .models import Menu, Item, Ingredient


def pregame(tci):
    """Setup function that can be repeated for all test cases."""
    tci.sugar = Ingredient.objects.create(name="Sugar")
    tci.spice = Ingredient.objects.create(name="Spice")
    tci.enice = Ingredient.objects.create(name="Everything Nice")
    tci.chemx = Ingredient.objects.create(name="Chemical X")

    tci.user = User.objects.create_user(
        'ProUtonium',
        'secretingredient@townsville.com',
        'dadgoals4ever'
    )

    tci.blossom = Item(
        name="Blossom",
        description="lead element",
        chef=User.objects.get(username='ProUtonium'),
        standard=True,
        ingredients=(
            tci.sugar,
            tci.spice,
            tci.enice,
            tci.chemx
        )
    )
    tci.blossom.save(commit=False)
    tci.blossom.save_m2m()
    tci.blossom.save()
    
    tci.bubbles = Item.objects.create(
        name="Bubbles",
        description="joy laughter element",
        chef=User.objects.filter(id=1),
        standard=False,
        ingredients=(
            tci.sugar,
            tci.enice,
            tci.chemx
        )
    )
    tci.buttercup = Item.objects.create(
        name="Buttercup",
        description="tough fights element",
        chef=User.objects.filter(id=1),
        standard=True,
        ingredients=(  #  Need save_m2m()
            tci.spice,
            tci.enice,
            tci.chemx
        )
    )
        
    tci.ppg = Menu.objects.create(
        season="Powerpuff",
        items=(
            tci.blossom,
            tci.bubbles,
            tci.buttercup
        ),
        expiration_date=datetime.datetime(2050, 1, 1, 1, 1, 1, 1)
    )
        
    tci.leaderless = Menu.objects.create(
        season="Leaderless PPG",
        items=(
            tci.bubbles,
            tci.buttercup
        ),
        expiration_date=datetime.datetime(2060, 1, 1, 1, 1, 1, 1)
    )
        
    tci.lonely = Menu.objects.create(
        season="Lone PPG",
        items=(
            tci.bubbles
        ),
        expiration_date=datetime.datetime(1983, 1, 1, 1, 1, 1, 1)
    )


class ModelTests(TestCase):
    def setUp(self):
        pregame(self)

    
class ViewTests(TestCase):
    def setUp(self):
        pregame(self)

    def test_menu_list_view(self):
        pass
        # resp = self.client.get('/menu/')
        # self.assertEqual(resp.status_code, 200)