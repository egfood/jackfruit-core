from django import forms

from apps.store.models import RootProduct


class RootProductForm(forms.ModelForm):
    class Meta:
        model = RootProduct
        exclude = ['farmer']
