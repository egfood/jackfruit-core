from django import forms

from apps.farmer.models.product import FarmerProduct


class AddFarmerProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.farmer = kwargs.pop('farmer', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        farmer_product = super().save(commit=False)
        farmer_product.farmer = self.farmer
        if commit:
            farmer_product.save()
        return farmer_product

    class Meta:
        model = FarmerProduct
        exclude = ('farmer',)
