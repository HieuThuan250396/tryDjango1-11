from django.db import models
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from .utils import unique_slug_generator
from .validator import validate_category
from django.core.urlresolvers import reverse
from django.db.models import Q

# Create your models here.

User = settings.AUTH_USER_MODEL

class RestaurantLocationQuerySet(models.query.QuerySet): # RestaurantLocation.objects.all().search(query) # RestaurantLocation.objects.filter(something).search
    def search(self, query):
        if query:
            query = query.strip()
            return self.filter(
                        Q(name__icontains=query)|
                        Q(item__name__icontains=query)|
                        Q(category__icontains=query)|
                        Q(location__icontains=query)|
                        Q(item__contents__icontains=query)
                    ).distinct()
        return self

class RestaurantLocationManager(models.Manager): # RestaurantLocation.objects.search()
    def get_queryset(self):
        return RestaurantLocationQuerySet(self.model, using=self._db)
    
    def search(self, query):
        return self.get_queryset().search(query)

class RestaurantLocation(models.Model):
    owner       = models.ForeignKey(User)
    name        = models.CharField(max_length=120)
    location    = models.CharField(max_length=120, null=True, blank=True)
    category    = models.CharField(max_length=120, null=True, blank=True, validators = [validate_category])
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    slug        = models.SlugField(null=True, blank=True)

    objects = RestaurantLocationManager()
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurants:detail', kwargs={'slug': self.slug})

    @property
    def title(self):
        return self.name


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.category = instance.category.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


# def rl_post_save_receiver(sender, instance, *args, **kwargs):
#     print("saved")
#     print(instance.timestamp)
#     if not instance.slug:
#         instance.slu = unique_slug_generator(instance)
#         instance.saved()
    

pre_save.connect(rl_pre_save_receiver, sender=RestaurantLocation)

# post_save.connect(rl_post_save_receiver, sender=RestaurantLocation)
