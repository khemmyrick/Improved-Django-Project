from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Item, Menu
from .forms import MenuForm, ItemForm


def menu_list(request):
    """Display a list of all non-expired menu objects.

    Args:
        request: an HttpRequest object.
    Filters menus where expiration dates are greater than timezone.now().
    Prefetches related items to include in menus context.
    Returns: A template with context data for all relevant menus.
    """
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
    """Display a list of the items which aren't available year-round.

    Args: request
    Filters field values for items which aren't available year-round.
    Returns: A template with context data for all relevant items.
    """
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
    """Display the menu assigned to the id of <pk> in more detail.
    
    Args:
        request: an HttpRequest object.
        pk (int): The primary key of the desired menu object.
    Returns: A template populated with menu context data.
    """
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    """Display the item assigned to the id of <pk> in more detail.
    
    Args:
        request: an HttpRequest object.
        pk (int): The primary key of the desired item object.
    Returns: A template populated with item context data.
    """
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})


def add_edit_menu(request, pk=None):
    """Create a new menu or edit an existing menu.

    Args:
        request: an HttpRequest object.
    Keyword arg:
        pk (int): The primary key of the desired menu object.
    Returns: A template populated with form context data
        and one of two possible heading strings.
        After form data is entered and submitted,
        returns redirect to desired menu_detail view.
    """
    if pk:
        menu = get_object_or_404(Menu, pk=pk)
        heading = 'Edit Menu'
    else:
        menu = None
        heading = 'New Menu'

    if request.method == "POST":
        form = MenuForm(
            request.POST,
            instance=menu
        )
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()
            form.save_m2m()
            menu.save()
            return redirect('menu:menu_detail', pk=menu.pk)

    else:
        form = MenuForm(instance=menu)
    return render(request, 'menu/change_menu.html', {
        'form': form,
        'heading': heading
        }
    )


def item_edit(request, pk):
    """Edit an item.

    Args:
        request: an HttpRequest object.
        pk (int): The primary key of the desired item object.
    Returns: A template populated with item context data
        and a form prefilled with desired item fields.
        After form data is edited and resubmitted,
        returns redirect to item_detail view.
    """
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

    return render(
        request, 'menu/item_edit.html', {
            'item': item,
            'form': form
        }
    )
