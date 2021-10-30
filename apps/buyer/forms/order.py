from django import forms

from apps.store.models.order import FoodOrder


class BuyerFoodOrderForm(forms.ModelForm):
    class Meta:
        model = FoodOrder
        fields = ('payment_type', 'location')