import unittest
import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from django.utils import timezone
from . import views
from .models import Menu, Item, Ingredient
from .forms import MenuForm, ItemForm, v_err


class Pregame(object):
    def setUp(self):
        """Setup function that can be repeated for all test cases.
        
        Creates sample Menu, Item, Ingredient and User objects.
        Creates sample context dictionaries for certain Menu and Item objects.
        """
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
        self.blossom.save()
        self.blossom.ingredients = (
            self.sugar,
            self.spice,
            self.enice,
            self.chemx
        )
        self.blossom.save()

        self.bubbles = Item(
            name="Bubbles",
            description="joy laughter element",
            chef=User.objects.get(username='ProUtonium'),
            standard=False,
        )
        self.bubbles.save()
        self.bubbles.ingredients = (
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
        self.buttercup.ingredients = (
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
            expiration_date=datetime.datetime(
                2050, 1, 1, 1, 1, 1, 1, tzinfo=(pst)
            ),
        )
        self.ppg.save()
        self.ppg.items = (
            self.blossom,
            self.bubbles,
            self.buttercup
        )
        self.ppg.save()

        self.leaderless = Menu(
            season="Leaderless PPG",
            expiration_date=datetime.datetime(
                2060, 1, 1, 1, 1, 1, 1, tzinfo=(pst)
            )
        )
        self.leaderless.save()
        self.leaderless.items = (
            self.bubbles,
            self.buttercup
        )
        self.leaderless.save()

        self.lonely = Menu(
            season="Lone PPG",
            expiration_date=datetime.datetime(
                1983, 1, 1, 1, 1, 1, 1, tzinfo=(pst)
            )
        )
        self.lonely.save()
        self.lonely.items = (
            self.bubbles,
        )
        self.lonely.save()


class MenuModelTests(Pregame, TestCase):
    """Menu app model tests."""
    def test_menu_creation(self):
        '''A sample menu object is created successfully.'''
        self.assertEqual(self.ppg.season, 'Powerpuff')
        self.assertLessEqual(self.lonely.expiration_date, timezone.now())

    def test_item_creation(self):
        '''A sample item object is created successfully.'''
        self.assertEqual(self.blossom.name, 'Blossom')
        self.assertEqual(self.buttercup.description, 'tough fights element')
        self.assertLessEqual(self.bubbles.created_date, timezone.now())


class MenuViewTests(Pregame, TestCase):
    """Menu app view tests."""
    def test_menu_list_view(self):
        '''Tests menu list view.
        
        The response gets a 200 status code.
        The correct template is used.
        Expected sample menus are found in the context.
        An unexpected sample menu is not found in the context.
        '''
        resp = self.client.get('/menu/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertIn(self.ppg, resp.context['menus'])
        self.assertIn(self.leaderless, resp.context['menus'])
        self.assertNotIn(self.lonely, resp.context['menus'])

    def test_item_list_view(self):
        '''Tests item list view.
        
        The response gets a 200 status code.
        The correct template is used.
        An expected sample item is found in the context.
        An unexpected sample item is not found in the context.
        '''
        resp = self.client.get('/menu/item/list/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_list.html')
        self.assertNotIn(self.item1, resp.context['items'])
        self.assertIn(self.item2, resp.context['items'])

    def test_menu_detail_view(self):
        '''Tests menu detail view.
        
        The response gets a 200 status code.
        The correct template is used.
        The expected sample menu is found in the context.
        An unexpected sample menu is not found in the context.
        '''
        resp = self.client.get('/menu/1/detail/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertEqual(self.ppg, resp.context['menu'])
        self.assertNotEqual(self.lonely, resp.context['menu'])

    def test_item_detail_view(self):
        '''Tests item detail view.
        
        The response gets a 200 status code.
        The correct template is used.
        The expected sample item is found in the context.
        An unexpected sample item is not found in the context.
        '''
        resp = self.client.get('/menu/item/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/detail_item.html')
        self.assertEqual(self.blossom, resp.context['item'])
        self.assertNotEqual(self.bubbles, resp.context['item'])

    def test_add_edit_menu_view(self):
        '''Tests add/edit menu view.
        
        Both responses get a 200 status code.
        Both responses use correct template.
        MenuForm instance and heading text are in context.
        '''
        resp = self.client.get('/menu/edit/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/change_menu.html')
        self.assertEqual('Edit Menu', resp.context['heading'])
        self.assertIsInstance(resp.context['form'], MenuForm)
        resp = self.client.get('/menu/edit/new/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/change_menu.html')
        self.assertEqual('New Menu', resp.context['heading'])
        self.assertIsInstance(resp.context['form'], MenuForm)

    def test_item_edit_view(self):
        '''Tests item edit view.
        
        The response gets a 200 status code.
        The correct template is used.
        The expected sample item is the context.
        The template is sent an ItemForm instance.
        '''
        resp = self.client.get('/menu/item/1/change/')
        self.assertTemplateUsed(resp, 'menu/item_edit.html')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.blossom, resp.context['item'])
        self.assertIsInstance(resp.context['form'], ItemForm)


class MenuFormTests(Pregame, TestCase):
    """Menu app form tests."""
    def test_menu_form(self):
        """Tests valid menu form.
        
        Creates a form with sample form data.
        Checks that form is valid.
        """
        form_data = {
            'season': self.ppg.season,
            'items': [
                self.blossom.id,
                self.buttercup.id,
                self.bubbles.id
            ],
            'created_date': self.ppg.created_date,
            'expiration_date': self.ppg.expiration_date
        }
        mf = MenuForm(data=form_data)
        self.assertTrue(mf.is_valid())

    def test_menu_form_invalid_season(self):
        """Tests invalid menu form.
        
        Creates a form with sample form data.
        Season string has fewer than 4 characters; is not valid.
        """
        form_data = {
            'season': 'sp',
            'items': [
                self.blossom.id,
                self.buttercup.id,
                self.bubbles.id
            ],
            'created_date': self.ppg.created_date,
            'expiration_date': self.ppg.expiration_date
        }
        mf = MenuForm(data=form_data)
        self.assertFalse(mf.is_valid())

    def test_item_form(self):
        """Tests valid item form.
        
        Creates a form with sample form data.
        Form is valid.
        """
        form_data = {
            'name': self.blossom.name,
            'description': self.blossom.description,
            'chef': self.blossom.chef,
            'standard': self.blossom.standard,
            'ingredients': [
                self.sugar.id,
                self.spice.id,
                self.enice.id,
                self.chemx.id
            ]
        }
        item_form = ItemForm(data=form_data)
        self.assertTrue(item_form.is_valid)

    def test_item_form_invalid_name(self):
        """Call is_valid on an ItemForm with a short name str."""
        form_data = {
            'name': 'bub',
            'description': self.bubbles.description,
            'chef': self.bubbles.chef,
            'ingredients': [
                self.sugar.id,
                self.enice.id
            ]
        }
        item_form = ItemForm(data=form_data)
        item_form.is_valid()
        self.assertFalse(item_form.is_valid())

    def test_v_err_helper(self):
        '''All keys in error_messages dict raise ValidationErrors.'''
        self.assertRaises(ValidationError, v_err, 'no_season')
        self.assertRaises(ValidationError, v_err, 'no_items')
        self.assertRaises(ValidationError, v_err, 'no_name')
        self.assertRaises(ValidationError, v_err, 'no_desc')
        self.assertRaises(ValidationError, v_err, 'no_chef')
        self.assertRaises(ValidationError, v_err, 'no_ing')
        self.assertRaises(ValidationError, v_err, 'elapsed')
