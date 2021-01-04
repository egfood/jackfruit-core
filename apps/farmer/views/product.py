from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from apps.farmer.forms.product import AddProductForm
from apps.store.forms.product import FoodProductForm
from apps.store.models import FoodProduct
from core.models import GreenUser


class AddProductView(CreateView):
    template_name = "farmer/pages/add_product.html"
    model = FoodProduct
    fields = ('name', 'description', 'price', 'min_weight', 'weight_per_price', 'packaging', 'is_visible')

    def post(self, request, *args, **kwargs):
        f = FoodProductForm(request.POST)
        if f.is_valid():
            new_product = f.save(commit=False)
            new_product.supplier_id = GreenUser.objects.get(id=self.request.user.id)
            new_product.save()
            messages.success(request, f'Продукт {new_product.name} успешно создан.')
        else:
            return render(request, self.template_name, {'form': f})

        return redirect(reverse('farmer:main_page'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_home_url'] = reverse('farmer:main_page')
        context['user'] = self.request.user
        return context


class DeleteProductView(DeleteView):
    model = FoodProduct
    success_url = reverse_lazy('farmer:main_page')
    template_name = 'farmer/pages/delete_product.html'


class UpdateProductView(UpdateView):
    model = FoodProduct
    template_name = 'farmer/pages/update_product.html'
    form_class = AddProductForm
    success_url = reverse_lazy('farmer:main_page')
