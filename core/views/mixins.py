from django.core.paginator import Paginator


class PaginationMixin:
    def get_paginate_page_and_subjects(self, pagination_objects, objects_per_page: int = 10):
        if pagination_objects:
            page_number = self.request.GET.get('page')
            paginator = Paginator(pagination_objects, objects_per_page)
            return paginator.get_page(page_number), paginator.object_list
        else:
            return None, pagination_objects
