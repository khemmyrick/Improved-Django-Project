import random
import string

from django import template

from django.shortcuts import get_object_or_404

from menu.models import Menu


register = template.Library()


@register.filter('underspace')
def underspace(attr_string):
    """Replace spaces with underscores."""
    return attr_string.replace('_', ' ')


@register.inclusion_tag('menu/chef_nav.html', takes_context=True)
def nav_chefs_list(context):
    """Returns a dictionary of chefs to display in layout."""
    chef_list = User.objects.all().order_by('name')
    return {'chef_list': chef_list,
            'chef': context['chef']}


@register.inclusion_tag('menu/letters.html', takes_context=True)
def abc_list(context):
    """Return a list of letters for first letter search."""
    alpha_search = []
    for char in string.ascii_uppercase:
        alpha_search.append(char)
    return {'alpha_search': alpha_search,
            'target_letter': context['target_letter']}
