from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from restaurants.models import RestaurantLocation
# Create your models here.

class Item(models.Model):
    #assosiations
    user        = models.ForeignKey(settings.AUTH_USER_MODEL)
    restaurant  = models.ForeignKey(RestaurantLocation)
    #items stuff
    name        = models.CharField(max_length=120)
    contents    = models.TextField(help_text='Seperate each item by comma')
    excludes    = models.TextField(blank=True, null=True, help_text='Seperate each item by comma')
    public      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-timestamp'] #item.objects.all()

    def __str__(self):
        return self.name

    def get_contents(self):
        return self.contents.split(",")
    
    def get_excludes(self):
        return self.excludes.split(",")

    def get_absolute_url(self):
        return reverse('menus:detail', kwargs={'pk': self.pk})