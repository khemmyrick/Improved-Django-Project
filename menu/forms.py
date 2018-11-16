import re
import datetime

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _
from . import models  # Menu, Item, Ingredient, model methods etc

def v_err(flaw):
    """Raise various validation errors."""
    error_messages = {
        'no_season': _("Season must contain at least 4 alphanumeric characters."),
        'no_items': _("Menu must contain at least 1 item."),
        'no_name': _("Name field must contain at least 4 alphanumeric characters."),
        'no_desc': _("Description must contain at least 10 characters."),
        'no_chef': _("Item must belong to a chef."),
        'no_ing': _("Item must contain at least 1 ingredient."),
        'elapsed': _("This date has elapsed.")
    }
    raise forms.ValidationError(
        error_messages[flaw],
        code=flaw,
    )


class MenuForm(forms.ModelForm):

    class Meta:
        model = models.Menu
        fields = (
            'season',
            'items',
            'expiration_date'
        )
        exclude = ['created_date',]

    def clean_season(self):
        season = self.cleaned_data['season']
        if not re.match(r'[\w{4}\s*]+', season) or len(season) < 4:
            v_err('no_season')
        return season

    def clean_items(self):
        items = self.cleaned_data['items']
        if len(items) < 1:
            v_err('no_items')
        return items
        
    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date.date() <= datetime.date.today():
            v_err('elapsed')
        return expiration_date

    def __init__ (self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields["items"].widget = forms.widgets.SelectMultiple()
        self.fields["items"].queryset = models.Item.objects.all()
        self.fields["expiration_date"].widget = forms.SelectDateWidget(
            empty_label=(
                "Choose Year",
                "Choose Month",
                "Choose Day"
            ),
        )


class ItemForm(forms.ModelForm):

    class Meta:
        model = models.Item
        fields = (
            'name',
            'description',
            'ingredients',
            'standard'
        )
        exclude = ['created_date',]

    def __init__ (self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields["ingredients"].widget = forms.widgets.SelectMultiple()
        self.fields["ingredients"].queryset = models.Ingredient.objects.all()
        # self.fields["standard"].widget = forms.BooleanField()
        
    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'[\w{4}\s*]+', name) or len(name) < 4:
            v_err('no_name')
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 10:
            v_err('no_desc')
        return description
        
    def clean_ingredients(self):
        ingredients = self.cleaned_data['ingredients']
        if len(ingredients) < 1:
            v_err('no_ing')
        return ingredients

    def clean_chef(self):
        chef = self.cleaned_data['chef']
        if len(chef) < 1:
            v_err('no_chef')
        return chef
