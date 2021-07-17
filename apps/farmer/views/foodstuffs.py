from django.core.paginator import Paginator
from django.shortcuts import render

from apps.farmer.forms.product import AddFarmerProductForm
from .base import FarmerBasePagesView
from ..models import FarmerProduct


class FarmerFoodstuffsPageView(FarmerBasePagesView):
    template_name = "farmer/pages/farmer-foodstuffs.html"

    def post(self, request, *args, **kwargs):
        form = AddFarmerProductForm(data=request.POST, farmer=request.user)
        if form.is_valid():
            form.save()
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = FarmerProduct.objects.filter(farmer=self.request.user)
        paginator = Paginator(product_list, 2)
        if 'page' in self.request.GET:
            page_num = self.request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        form = AddFarmerProductForm()
        context['product_list'] = product_list
        context['form'] = form
        context['page'] = page
        return context
