# from django.conf import settings
# from django.contrib import messages
# from django.forms import formset_factory, HiddenInput
# from django.shortcuts import get_object_or_404, render
#
# from apps.store.forms.order import FoodOfficeOrderItemForm, FoodHomeOrderItemForm, FoodOfficeOrderForm, \
#     FoodHomeLocationForm
# from apps.store.models import FoodDelivery, FoodProduct, FoodOfficeOrder, FoodOfficeOrderItem, FoodHomeOrderItem, \
#     FoodHomeOrder, OfficeLocation
# from .base import BuyerBasePagesView
#
#
# # TODO: Remove it after implementation order on one way
# class BuyerOfficeOrderByDeliveryView(BuyerBasePagesView):
#     template_name = 'buyer/pages/office_order.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['delivery'] = get_object_or_404(FoodDelivery, pk=kwargs['delivery_pk'])
#         initial_office = {}
#         orders_by_product_pk = {}
#         order = FoodOfficeOrder.objects.filter(user=self.request.user, delivery=context['delivery']).first()
#
#         if order:
#             order_items = FoodOfficeOrderItem.objects.filter(office_order=order)
#             orders_by_product_pk = {item.product.pk: item for item in order_items}
#             if order.office is not None:
#                 initial_office = {'office': order.office.pk}
#
#         products = FoodProduct.objects.filter(is_visible=True)
#         FoodOrderFormSet = formset_factory(FoodOfficeOrderItemForm, extra=0)
#         initial = []
#         for p in products:
#             current_order = orders_by_product_pk.get(p.pk, None)
#             order_value = None if current_order is None else current_order.value
#             initial.append({'product': p.pk, 'value': order_value})
#         order_formset = FoodOrderFormSet(initial=initial)
#         context['order_formset'] = self.__update_product_name_and_widget(order_formset)
#
#         context['office_order_form'] = FoodOfficeOrderForm(initial=initial_office)
#         context['is_order_creation'] = not bool(order)
#         context['order'] = order
#         context['shipping_cost'] = settings.SHIPPING_COST
#         return context
#
#     def post(self, request, *args, **kwargs):
#         delivery = get_object_or_404(FoodDelivery, pk=kwargs['delivery_pk'])
#         order, _ = FoodOfficeOrder.objects.get_or_create(delivery=delivery, user=request.user)
#         order.office = get_object_or_404(OfficeLocation, pk=request.POST['office'])
#         order.save()
#         order_items = FoodOfficeOrderItem.objects.filter(office_order=order)
#         orders_by_product_pk = {item.product.pk: item for item in order_items}
#         FoodOrderFormSet = formset_factory(FoodOfficeOrderItemForm)
#         formset = FoodOrderFormSet(request.POST)
#
#         order_items_for_creation = []
#         order_items_for_update = []
#         for form in formset:
#             if form.is_valid():
#                 saved_order = orders_by_product_pk.get(form.cleaned_data['product'].pk, False)
#                 if saved_order:
#                     saved_order.value = form.cleaned_data['value']
#                     order_items_for_update.append(saved_order)
#                 else:
#                     if form.cleaned_data['value']:
#                         new_order_item = FoodOfficeOrderItem(office_order=order, product=form.cleaned_data['product'],
#                                                              value=form.cleaned_data['value'])
#                         order_items_for_creation.append(new_order_item)
#
#         if order_items_for_update:
#             FoodOfficeOrderItem.objects.bulk_update(order_items_for_update, ['value'])
#         if order_items_for_creation:
#             FoodOfficeOrderItem.objects.bulk_create(order_items_for_creation)
#
#         if order_items_for_update:
#             messages.success(request, f'Данные заказа на доставку {delivery.short_name} успешно обновлены.')
#         elif order_items_for_creation:
#             messages.success(request, f'Заказ на доставку {delivery.short_name} успешно отправлен на обработку.\n'
#                                       f'Вы можете отредактировать ваш заказ на этой странице, '
#                                       f'зафиксировав изменения нажатием на кнопку "Изменить заказ".')
#
#         nearest_delivery = FoodDelivery.get_nearest_delivery()
#         nearest_delivery_pk = nearest_delivery.pk if nearest_delivery else None
#
#         context = super().get_context_data(**kwargs)
#         context.update({'order_formset': self.__update_product_name_and_widget(formset), 'delivery': delivery,
#                         'nearest_delivery_pk': nearest_delivery_pk, 'is_order_creation': False,
#                         'office_order_form': FoodOfficeOrderForm(initial={'office': order.office.pk}),
#                         'order': order, 'shipping_cost': settings.SHIPPING_COST})
#
#         return render(request, self.template_name, context)
#
#     def __update_product_name_and_widget(self, order_formset, products=None):
#         if products is None:
#             products = FoodProduct.objects.filter(is_visible=True)
#         i = 0
#         for form in order_formset:
#             form.selected_product_name = products[i]
#             form.fields['product'].widget = HiddenInput()
#             i += 1
#         return order_formset
#
#
# # TODO: Remove it after implementation order on one way
# class BuyerHomeOrderByDeliveryView(BuyerBasePagesView):
#     template_name = 'buyer/pages/home_order.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['delivery'] = get_object_or_404(FoodDelivery, pk=kwargs['delivery_pk'])
#         order = FoodHomeOrder.objects.filter(user=self.request.user, delivery=context['delivery']).first()
#         initial = []
#         orders_by_product_pk = {}
#
#         if order:
#             order_items = FoodHomeOrderItem.objects.filter(home_order=order)
#             orders_by_product_pk = {item.product.pk: item for item in order_items}
#             if order.home is not None:
#                 context['home_location_form'] = FoodHomeLocationForm(instance=order.home)
#         else:
#             context['home_location_form'] = FoodHomeLocationForm()
#
#         products = FoodProduct.objects.filter(is_visible=True)
#         FoodOrderFormSet = formset_factory(FoodHomeOrderItemForm, extra=0)
#         for p in products:
#             current_order = orders_by_product_pk.get(p.pk, None)
#             order_value = None if current_order is None else current_order.value
#             initial.append({'product': p.pk, 'value': order_value})
#         order_formset = FoodOrderFormSet(initial=initial)
#         context['order_formset'] = self.__update_product_name_and_widget(order_formset)
#
#         context['is_order_creation'] = not bool(order)
#         context['order'] = order
#         context['shipping_cost'] = settings.SHIPPING_COST
#         return context
#
#     def post(self, request, *args, **kwargs):
#         delivery = get_object_or_404(FoodDelivery, pk=kwargs['delivery_pk'])
#         order, _ = FoodHomeOrder.objects.get_or_create(delivery=delivery, user=request.user)
#         home_address_form = FoodHomeLocationForm(request.POST)
#         order.home = home_address_form.save()
#         order.save()
#         order_items = FoodHomeOrderItem.objects.filter(home_order=order)
#         orders_by_product_pk = {item.product.pk: item for item in order_items}
#         FoodOrderFormSet = formset_factory(FoodHomeOrderItemForm)
#         formset = FoodOrderFormSet(request.POST)
#
#         order_items_for_creation = []
#         order_items_for_update = []
#         for form in formset:
#             if form.is_valid():
#                 saved_order = orders_by_product_pk.get(form.cleaned_data['product'].pk, False)
#                 if saved_order:
#                     saved_order.value = form.cleaned_data['value']
#                     order_items_for_update.append(saved_order)
#                 else:
#                     if form.cleaned_data['value']:
#                         new_order_item = FoodHomeOrderItem(home_order=order, product=form.cleaned_data['product'],
#                                                            value=form.cleaned_data['value'])
#                         order_items_for_creation.append(new_order_item)
#
#         if order_items_for_update:
#             FoodHomeOrderItem.objects.bulk_update(order_items_for_update, ['value'])
#         if order_items_for_creation:
#             FoodHomeOrderItem.objects.bulk_create(order_items_for_creation)
#
#         if order_items_for_update:
#             messages.success(request, f'Данные заказа на доставку {delivery.short_name} успешно обновлены.')
#         elif order_items_for_creation:
#             messages.success(request, f'Заказ на доставку {delivery.short_name} успешно отправлен на обработку.\n'
#                                       f'Вы можете отредактировать ваш заказ на этой странице, '
#                                       f'зафиксировав изменения нажатием на кнопку "Изменить заказ".')
#
#         nearest_delivery = FoodDelivery.get_nearest_delivery()
#         nearest_delivery_pk = nearest_delivery.pk if nearest_delivery else None
#
#         context = super().get_context_data(**kwargs)
#         context.update({'order_formset': self.__update_product_name_and_widget(formset), 'delivery': delivery,
#                         'nearest_delivery_pk': nearest_delivery_pk, 'home_location_form': home_address_form,
#                         'is_order_creation': False, 'order': order, 'shipping_cost': settings.SHIPPING_COST})
#
#         return render(request, self.template_name, context)
#
#     def __update_product_name_and_widget(self, order_formset, products=None):
#         if products is None:
#             products = FoodProduct.objects.filter(is_visible=True)
#         i = 0
#         for form in order_formset:
#             form.selected_product_name = products[i]
#             form.fields['product'].widget = HiddenInput()
#             i += 1
#         return order_formset
