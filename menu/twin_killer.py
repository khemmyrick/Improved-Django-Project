from models import Menu, Item, Ingredient


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

# class CopyShredder(models.Model):
#    state = models.BooleanField(default=True)
## I originally set copyshredder as a model object. 
## This was so I could set its state, and have it know whether or not it had run.