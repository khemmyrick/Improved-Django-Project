import re
import datetime

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _
from . import models


def v_err(flaw):
    """Raise validation error with the proper error message.
    
    Args:
        flaw: a str indicating which error message should display.
    Dict contains possible error messages.
    Raises: ValidationError.
    """
    error_messages = {
        'no_season': _(
            "Season must contain at least 4 alphanumeric characters."
        ),
        'no_items': _(
            "Menu must contain at least 1 item."
        ),
        'no_name': _(
            "Name field must contain at least 4 alphanumeric characters."
        ),
        'no_desc': _(
            "Description must contain at least 10 characters."
        ),
        'no_chef': _(
            "Item must belong to a chef."
        ),
        'no_ing': _(
            "Item must contain at least 1 ingredient."
        ),
        'elapsed': _(
            "This date has elapsed."
        )
    }
    raise forms.ValidationError(
        error_messages[flaw],
        code=flaw,
    )


class MenuForm(forms.ModelForm):
    """Create or edit a Menu."""

    def __init__(self, *args, **kwargs):
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

    class Meta:
        model = models.Menu
        fields = (
            'season',
            'items',
            'expiration_date'
        )
        exclude = [
            'created_date',
        ]

    def clean_season(self):
        """Season field needs at least 4 alphanumeric characters.
        
        Else: raise ValidationError.
        """
        season = self.cleaned_data['season']
        if not re.match(r'[\w{4}\s*]+', season) or len(season) < 4:
            v_err('no_season')
        return season

    def clean_items(self):
        """Items field needs at least 1 item.
        
        Else: raise ValidationError.
        """
        items = self.cleaned_data['items']
        if len(items) < 1:
            v_err('no_items')
        return items

    def clean_expiration_date(self):
        """Expiration date must be later than current date.
        
        Else: raise ValidationError.
        """
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date.date() <= datetime.date.today():
            v_err('elapsed')
        return expiration_date


class ItemForm(forms.ModelForm):
    """Create or edit an Item."""

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields["ingredients"].widget = forms.widgets.SelectMultiple()
        self.fields["ingredients"].queryset = models.Ingredient.objects.all()

    class Meta:
        model = models.Item
        fields = (
            'name',
            'description',
            'ingredients',
            'standard'
        )
        exclude = [
            'created_date',
        ]

    def clean_name(self):
        """Name field is a str of at least 4 alphanumeric characters.
        
        Else: raise ValidationError.
        """
        name = self.cleaned_data['name']
        if not re.match(r'[\w{4}\s*]+', name) or len(name) < 4:
            v_err('no_name')
        return name

    def clean_description(self):
        """Description field is a str of at least 10 characters.
        
        Else: raise ValidationError.
        """
        description = self.cleaned_data['description']
        if not re.match(r'[\w{4}\s*]+', description) or len(description) < 10:
            v_err('no_desc')
        return description

    def clean_ingredients(self):
        """Ingredient field needs at least 1 ingredient.
        
        Else: raise ValidationError.
        """
        ingredients = self.cleaned_data['ingredients']
        if len(ingredients) < 1:
            v_err('no_ing')
        return ingredients

    def clean_chef(self):
        """Chef field needs at least 1 chef.
        
        Else: raise ValidationError.
        """
        chef = self.cleaned_data['chef']
        if len(chef) < 1:
            v_err('no_chef')
        return chef
