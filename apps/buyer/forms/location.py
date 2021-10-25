from django import forms

from apps.store.models.location import Location


class BuyerLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ('office_name', 'location_type', 'city_district', 'sort_key', 'user')