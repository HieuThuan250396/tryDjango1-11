from django import forms
from .models import Item
from restaurants.models import RestaurantLocation

class ItemForm(forms.ModelForm):
    """Form definition for Item."""

    class Meta:
        """Meta definition for Itemform."""

        model = Item
        fields = ['restaurant', 'name', 'contents', 'excludes','public']
    def __init__(self, user=None, *args, **kwargs):
        # print(kwargs.pop('user'))
        print(user)
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['restaurant'].queryset = RestaurantLocation.objects.filter(owner = user) #.exclude(item__isnull = False)