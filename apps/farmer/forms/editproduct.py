from django.forms import ModelForm

from apps.farmer.models.product import FarmerProduct


class EditProductForm(ModelForm):
    class Meta:
        model = FarmerProduct
        fields = ('weight', 'price')
        labels = {'weight': 'Собрано', 'price': 'Цена(1кг)'}