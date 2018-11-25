from django.db import models
from django.utils import timezone


class Menu(models.Model):
    '''The Menu model.
    
    Fields:
        season: str of more than 4 but less than 21 characters.
        items: an m2m field of Item objects.
        created_date: timezone.now called when menu is created.
        expiration_date: a DateTimeField for when the menu expires.
    '''
    season = models.CharField(max_length=20)
    items = models.ManyToManyField(
        'Item',
        related_name='items'
    )
    created_date = models.DateTimeField(
        default=timezone.now
    )
    expiration_date = models.DateTimeField(
        blank=True, null=True
    )

    def __str__(self):
        return self.season

    class Meta:
        ordering = ('-expiration_date',)


class Item(models.Model):
    '''The Item model.
    
    Fields:
        name: CharField of more than 4 characters but less than 201.
        description: TextField to describe the item.
        chef: a ForeignKey field linking to the creator of the item.
        created_date: a timezone.now call for when the item is created.
        standard: a boolean marked True if an item is available year-round.
        ingredients: an m2m field of Ingredient objects.
    '''
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(
        default=timezone.now
    )
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name="ingredients"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Ingredient(models.Model):
    '''The Ingredient model.
    
    Fields:
        name: a CharField of less than 200 characters.
    '''
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
