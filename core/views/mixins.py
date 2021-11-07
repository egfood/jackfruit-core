from collections import Iterable

from django.core.paginator import Paginator


class PaginationMixin:
    def get_paginate_page_and_subjects(self, pagination_objects, objects_per_page: int = 10):
        if not isinstance(pagination_objects, Iterable):
            raise TypeError('A "pagination_objects" attribute is of invalid type.')

        if pagination_objects:

            # pagination_objects must be forced converted onto any ordered type for yield consistent results of pagination
            if not isinstance(pagination_objects, list):
                consistent_pagination_objects = list(pagination_objects)
            else:
                consistent_pagination_objects = pagination_objects

            page_number = self.request.GET.get('page')
            paginator = Paginator(consistent_pagination_objects, objects_per_page)
            return paginator.get_page(page_number), paginator.get_page(page_number).object_list
        else:
            return None, pagination_objects
