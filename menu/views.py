from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.db.models import Q, Count
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from operator import attrgetter
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, Menu, Ingredient
from .forms import MenuForm, ItemForm


def menu_list(request):
    """Display a list of all non-expired menus."""
    menus = Menu.objects.filter(
        expiration_date__gte=timezone.now()
    ).prefetch_related(
        'items'
    )
    return render(
        request,
        'menu/list_all_current_menus.html',
        {
            'menus': menus
        }
    )


def item_list(request):
    """Display a list of the items."""
    items = Item.objects.filter(
        standard=False
    ).values(
        'name',
        'description',
        'created_date',
        'id'
    )
    return render(
        request,
        'menu/item_list.html',
        {'items': items}
    )


def menu_detail(request, pk):
    """Display a given menu in more detail."""
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    """Display a given item in greater detail."""
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    """Create a new row in the Menu model."""
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(data=request.POST)
        if form.is_valid():
            menu = form.save()
            return redirect('menu:menu_detail', pk=menu.pk)

    return render(request, 'menu/add_menu.html', {'form': form})


def edit_menu(request, pk):
    """Edit a menu."""
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)
    if request.method == "POST":
        form = MenuForm(
            request.POST,
            instance=menu
        )
        if form.is_valid():
            menu = form.save(commit=False)
            form.save_m2m()
            menu.save()
            return redirect('menu:menu_detail', pk=menu.pk)

    return render(request, 'menu/change_menu.html', {
        'menu': menu,
        'form': form
        }
    )


def item_edit(request, pk):
    """Edit an item."""
    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(instance=item)
    if request.method == "POST":
        form = ItemForm(
            request.POST,
            instance=item
        )
        if form.is_valid():
            item = form.save(commit=False)
            form.save_m2m()
            item.save()
            return redirect('menu:item_detail', pk=item.pk)

    return render(request, 'menu/item_edit.html', {
        'item': item,
        'form': form
        }
    )
