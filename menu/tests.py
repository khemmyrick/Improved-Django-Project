import unittest
import datetime
# import pytz

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from django.utils import timezone
from . import views
from .models import Menu, Item, Ingredient


class Pregame(object):
    def setUp(self):
        """Setup function that can be repeated for all test cases."""
        pst = datetime.timezone(-datetime.timedelta(hours=8))
        self.sugar = Ingredient.objects.create(name="Sugar")
        self.spice = Ingredient.objects.create(name="Spice")
        self.enice = Ingredient.objects.create(name="Everything Nice")
        self.chemx = Ingredient.objects.create(name="Chemical X")

        self.user = User.objects.create_user(
            'ProUtonium',
            'secretingredient@townsville.com',
            'dadgoals4ever'
        )

        self.blossom = Item(
            name="Blossom",
            description="lead element",
            chef=User.objects.get(username='ProUtonium'),
            standard=True
        )
        self.blossom.save()  # Must save instance before adding m2m field.
        self.blossom.ingredients=(
            self.sugar,
            self.spice,
            self.enice,
            self.chemx
        )
        # self.blossom.save_m2m()
        # save_m2m() and save(commit=True) seem to only work for forms?
        self.blossom.save()

        self.bubbles = Item(
            name="Bubbles",
            description="joy laughter element",
            chef=User.objects.get(username='ProUtonium'),
            standard=False,
        )
        self.bubbles.save()
        self.bubbles.ingredients=(
            self.sugar,
            self.enice,
            self.chemx
        )
        self.bubbles.save()

        self.buttercup = Item(
            name="Buttercup",
            description="tough fights element",
            chef=User.objects.get(username='ProUtonium'),
            standard=True
        )
        self.buttercup.save()
        self.buttercup.ingredients=(
            self.spice,
            self.enice,
            self.chemx
        )
        self.buttercup.save()

        self.item1 = {
            'name': self.blossom.name,
            'description': self.blossom.description,
            'created_date': self.blossom.created_date,
            'id': self.blossom.id
        }
        
        self.item2 = {
            'name': self.bubbles.name,
            'description': self.bubbles.description,
            'created_date': self.bubbles.created_date,
            'id': self.bubbles.id
        }

        self.ppg = Menu(
            season="Powerpuff",
            expiration_date=datetime.datetime(2050, 1, 1, 1, 1, 1, 1, tzinfo=(pst)),
        )
        self.ppg.save()
        self.ppg.items=(
            self.blossom,
            self.bubbles,
            self.buttercup
        )
        self.ppg.save()

        self.leaderless = Menu(
            season="Leaderless PPG",
            expiration_date=datetime.datetime(2060, 1, 1, 1, 1, 1, 1, tzinfo=(pst))
        )
        self.leaderless.save()
        self.leaderless.items=(
            self.bubbles,
            self.buttercup
        )
        self.leaderless.save()

        self.lonely = Menu(
            season="Lone PPG",
            expiration_date=datetime.datetime(1983, 1, 1, 1, 1, 1, 1, tzinfo=(pst))
        )
        self.lonely.save()
        self.lonely.items=(
            self.bubbles,
        )
        self.lonely.save()


class ModelTests(Pregame, TestCase):

    def test_menu_creation(self):
        self.assertEqual(self.ppg.season, 'Powerpuff')
        self.assertLessEqual(self.lonely.expiration_date, timezone.now())
        # self.assertIn(self.buttercup, self.leaderless.items.queryset)
        


class ViewTests(Pregame, TestCase):

    def test_menu_list_view(self):
        resp = self.client.get('/menu/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertIn(self.ppg, resp.context['menus'])
        self.assertIn(self.leaderless, resp.context['menus'])
        self.assertNotIn(self.lonely, resp.context['menus'])

    def test_item_list_view(self):
        resp = self.client.get('/menu/item/list/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_list.html')
        self.assertNotIn(self.item1, resp.context['items'])
        self.assertIn(self.item2, resp.context['items'])

    def test_menu_detail_view(self):
        resp = self.client.get('/menu/1/detail/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertEqual(self.ppg, resp.context['menu'])
        self.assertNotEqual(self.lonely, resp.context['menu'])

    def test_item_detail_view(self):
        resp = self.client.get('/menu/item/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/detail_item.html')
        self.assertEqual(self.blossom, resp.context['item'])
        self.assertNotEqual(self.bubbles, resp.context['item'])
