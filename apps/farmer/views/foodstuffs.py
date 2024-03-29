from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from apps.farmer.forms.product import AddFarmerProductForm
from core.views.mixins import PaginationMixin
from .base import FarmerBasePagesView
from ..models.product import FarmerProduct


class FarmerFoodstuffsPageView(FarmerBasePagesView, PaginationMixin):
    template_name = "farmer/pages/farmer-foodstuffs.html"

    def post(self, request, *args, **kwargs):
        form = AddFarmerProductForm(data=request.POST, farmer=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('farmer:foodstuffs'))
        else:
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = FarmerProduct.objects.filter(farmer=self.request.user.profile)
        context['form'] = AddFarmerProductForm()
        context['page'], context['product_list'] = self.get_paginate_page_and_subjects(product_list, settings.COUNT_OF_FOODSTUFF_ITEMS_PER_PAGE)
        return context
