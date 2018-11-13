from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from operator import attrgetter
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, Menu, Ingredient, CopyShredder
from .forms import MenuForm, ItemForm


def menu_list(request):
    # all_menus = Menu.objects.values('season', 'expiration_date', 'items', 'pk')
    # Why are we sending items to this template?
    menus = []
    all_menus = Menu.objects.values('season', 'expiration_date', 'pk')  # items m2m field was obstructing proper iteration.
    # values() call prevents m2m field from populating anyway.
    for menu in all_menus:
        # print(menu['pk'])
        if menu['expiration_date']:
            mitem = Menu.objects.get(pk=menu['pk']) # .values() gives a Menu object has no attribute values exception.
            menu['items'] = mitem.items
            if menu['expiration_date'] >= timezone.now():
                menus.append(menu)

    # menus = sorted(menus, key=attrgetter('expiration_date'))
    # menus = set(menus)
    return render(
        request,
        'menu/list_all_current_menus.html',
        {'menus': menus}
    )


def item_list(request):
    items = Item.objects.values(
        'name',
        'description',
        'created_date',
        'pk'
    )
    return render(
        request,
        'menu/item_list.html',
        {'items': items}
    )


def menu_detail(request, pk):
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try: 
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(data=request.POST)
        if form.is_valid():
            # menu = form.save(commit=False)
            # menu.created_date = timezone.now()
            # menu.save()
            menu = form.save()
            return redirect('menu:menu_detail', pk=menu.pk)
    # else:
    #    form = MenuForm(request.POST)
    return render(request, 'menu/add_menu.html', {'form': form})


def edit_menu(request, pk):
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
            # menu = form.save()
            return redirect('menu:item_detail', pk=item.pk)

    return render(request, 'menu/item_edit.html', {
        'item': item,
        'form': form
        }
    )