from django import forms

from apps.store.models import FoodProduct


class AddProductForm(forms.ModelForm):
    class Meta:
        model = FoodProduct
        fields = '__all__'
