from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _
from . import models  # Menu, Item, Ingredient, model methods etc

def v_err(flaw):
    """Raise various validation errors."""
    error_messages = {
        'non_season': _(
            "Season must contain name of a season: "
            "Summer, spring, winter or fall."
        ),
        'lc_letters': _("Password must contain a lowercase letter."),
        'uc_letters': _("Password must contain a capital letters."),
        'no_num': _("Password must contain a numerical digit."),
        'symbols': _("Password must contain a non-alphanumeric symbol."),
        'password_mismatch': _("The two password fields didn't match."),
        'pw_short': _("Password must contain at least 14 characters."),
        'bio_short': _("Bio must contain at least 10 characters."),
        'bio_empty':_("Bio must contain non-whitespace."),
        'password_incorrect': _("The password is incorrect."),
        'triplets': _("New password same as old password."),
        'email_mismatch': _("The two email fields didn't match."),
        'not_email': _("This is not a valid email address.")
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

    def __init__ (self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields["items"].widget = forms.widgets.SelectMultiple()
        self.fields["items"].queryset = models.Item.objects.all()
        self.fields["expiration_date"].widget = forms.SelectDateWidget(  # forms.DateField(
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

