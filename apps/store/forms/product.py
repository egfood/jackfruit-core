from django import forms

from apps.store.models import FoodProduct


class FoodProductForm(forms.ModelForm):
    class Meta:
        model = FoodProduct
        exclude = ['farmer']
