from django import forms

from apps.store.models import FoodOfficeOrderItem, FoodHomeOrderItem, FoodOfficeOrder, FoodHomeOrder, HomeLocation


class FoodOfficeOrderForm(forms.ModelForm):
    class Meta:
        model = FoodOfficeOrder
        fields = ('office',)


class FoodHomeLocationForm(forms.ModelForm):
    class Meta:
        model = HomeLocation
        fields = (
        'city_type', 'city_value', 'city_district', 'street_type', 'street_value', 'building', 'porch', 'floor',
        'room',)


class FoodOfficeOrderItemForm(forms.ModelForm):
    class Meta:
        model = FoodOfficeOrderItem
        fields = ('product', 'value')

    selected_product_name = None


class FoodHomeOrderItemForm(forms.ModelForm):
    class Meta:
        model = FoodHomeOrderItem
        fields = ('product', 'value')

    selected_product_name = None
