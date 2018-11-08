from models import Menu, Item, Ingredient


def shred_copies():
    lastSeenId = float('-Inf')
    menus = Menu.objects.all().order_by('id')
    for menu in menus:
        if menu.id == lastSeenId:
            menu.delete()
        else:
            lastSeenId = menu.id

    lastSeenId = float('-Inf')
    items = Item.objects.all().order_by('id')
    for item in items:
        if item.id == lastSeenId:
            item.delete()
        else:
            lastSeenId = item.id

    lastSeenId = float('-Inf')
    ingredients = Ingredient.objects.all().order_by('id')
    for ingredient in ingredients:
        if ingredient.id == lastSeenId:
            ingredient.delete()
        else:
            lastSeenId = ingredient.id
