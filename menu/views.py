from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from operator import attrgetter
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, Menu, Ingredient, CopyShredder
from .forms import MenuForm


def shred_copies():
    """Delete all database duplicates."""
    print('**SHREDDER ACTIVATED**')
    lastSeenId = float('-Inf')
    menus = Menu.objects.all().order_by('id')
    menus = list(menus)
    print('Checking menus.')
    for menu in menus:
        if menu.id == lastSeenId:
            print("{}'s doppleganger is outta here!".format(menu.season))
            # We aren't getting to this block?
            menu.delete()
        else:
            lastSeenId = menu.id
            # This block runs and does indeed select menus.

    lastSeenId = float('-Inf')
    items = Item.objects.all().order_by('id')
    print('Checking items.')
    for item in items:
        if item.id == lastSeenId:
            item.delete()
        else:
            lastSeenId = item.id

    lastSeenId = float('-Inf')
    ingredients = Ingredient.objects.all().order_by('id')
    print('Checking ingredients.')
    for ingredient in ingredients:
        if ingredient.id == lastSeenId:
            ingredient.delete()
        else:
            lastSeenId = ingredient.id

    # lastSeenId = float('-Inf')
    # cshredders = CopyShredder.objects.all().order_by('id')
    # for cshredder in cshredders:
    #    if cshredder.id == lastSeenId:
    #        cshredder.delete()
    #    else:
    #        lastSeenId = cshredder.id


def menu_list(request):
    # Use get_or_create to make bool object that tells views whether or not to check db for duplicates.
    # After duplicates have been purged, flip switch.
    # shred_cue, _ = CopyShredder.objects.get_or_create(state=True)
    # if shred_cue.state:  # If we had to create this obj, there are copies to purge.
    #    print('*Calling shredder function.*')
    #    shred_copies()
    #    print('*disarming shredder*')
    #    shred_cue.state = False
    #    # Line 59 isn't working as desired?
    #    # Which is fine since while troubleshooting the shred_copies function.
    #    # When shred_copies works, add explicit '== True' to line 59?

    # If shredder won't work, add .distinct() to all_menus query.
    # .distinct() is not hiding duplicates?
    all_menus = Menu.objects.distinct().values('season', 'expiration_date', 'pk')
    menus = []
    for menu in all_menus:
        if menu['expiration_date']:
            if menu['expiration_date'] >= timezone.now():
                menus.append(menu)

    # menus = sorted(menus, key=attrgetter('expiration_date'))
    # menus = set(menus)
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


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
    # items = Item.objects.all().values('name')
    # form = MenuForm()
    form = MenuForm(instance=menu)
    if request.method == "POST":
        form = MenuForm(
            request.POST,
            instance=menu
        )
        if form.is_valid():
            menu.save()
            # menu = form.save()
            return HttpResponseRedirect(reverse('menu:menu_detail', pk=menu.pk))
    #    menu.season = request.POST.get('season', '')
    #    menu.expiration_date = datetime.strptime(request.POST.get('expiration_date', ''), '%m/%d/%Y')
    #    menu.items = request.POST.get('items', '')
    #    menu.save()

    return render(request, 'menu/change_menu.html', {
        'menu': menu,
        # 'items': items,
        }
    )
