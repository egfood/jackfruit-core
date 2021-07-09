from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .base import FarmerBasePagesView
from apps.farmer.forms.product import AddProductForm
from ..models import FarmerProduct


class FarmerFoodstuffsPageView(FarmerBasePagesView):
    template_name = "farmer/pages/farmer-foodstuffs.html"

    def post(self, request, *args, **kwargs):
        form = AddProductForm(data=request.POST, farmer=request.user)
        if form.is_valid():
            form.save()
            # return render(request, self.template_name, {'form': form})
            return HttpResponseRedirect(f"/farmer?view={self.request.GET['view']}&page={self.request.GET['page']}/")
        else:
            form = AddProductForm()
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = FarmerProduct.objects.filter(farmer=self.request.user)
        paginator = Paginator(product_list, 2)
        if 'page' in self.request.GET:
            page_num = self.request.GET['page']
        else:
            page_num = 1
        # #         # try:
        page = paginator.get_page(page_num)
        # a=kwargs['page']
        # if 'page' in self.kwargs:
        #     page_num = self.kwargs['page']
        # else:
        #     page_num = 1
        # page = paginator.get_page(page_num)
                # except EmptyPage:
                #     page = paginator.get_page(1)
                # c_pages = paginator.get_elided_page_range(page_num, on_each_side=1, on_ends=1)
        form = AddProductForm()
        context['product_list'] = product_list
        context['form'] = form
        context['view'] = self.request.GET.get('view', 'table')
        context['page'] = page
        return context