# from django.contrib import messages
# from django.shortcuts import redirect, render
# from django.urls import reverse_lazy, reverse
# from django.views.generic import CreateView, UpdateView, DeleteView
#
# from apps.farmer.forms.product import AddFarmerProductForm
# from apps.store.forms.product import RootProductForm
# from apps.store.models import RootProduct
# from core.models import GreenUser
#
#
# class AddProductView(CreateView):
#     template_name = "farmer/pages/add_product.html"
#     model = RootProduct
#     fields = ('name', 'description', 'price', 'min_weight', 'quantity_per_price', 'packaging', 'is_visible')
#
#     def post(self, request, *args, **kwargs):
#         f = RootProductForm(request.POST)
#         if f.is_valid():
#             new_product = f.save(commit=False)
#             new_product.farmer = GreenUser.objects.get(id=self.request.user.id)
#             new_product.save()
#             messages.success(request, f'Продукт {new_product.name} успешно создан.')
#         else:
#             return render(request, self.template_name, {'form': f})
#
#         return redirect(reverse('farmer:main_page'))
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['app_home_url'] = reverse('farmer:main_page')
#         context['user'] = self.request.user
#         return context
#
#
# class DeleteProductView(DeleteView):
#     model = RootProduct
#     success_url = reverse_lazy('farmer:main_page')
#     template_name = 'farmer/pages/delete_product.html'
#
#
# class UpdateProductView(UpdateView):
#     model = RootProduct
#     template_name = 'farmer/pages/update_product.html'
#     form_class = AddFarmerProductForm
#     success_url = reverse_lazy('farmer:main_page')
