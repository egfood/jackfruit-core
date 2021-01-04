from abc import ABC, abstractmethod

from django.http import HttpResponse
from django.utils import timezone


class CSVResponder:
    _response = None

    def __init__(self, selected_instance, unique_filename_part):
        self.selected_instance = selected_instance
        self.unique_part = unique_filename_part

    @property
    def csv_file_response(self):
        if self._response is None:
            self._response = HttpResponse(content_type="text/csv")
            self._response["Content-Disposition"] = f"attachment; filename={self._get_filename()}.csv"
        return self._response

    def _get_filename(self):
        return f"delivery_{self.selected_instance.pk}_{self.unique_part}_{timezone.now():%d-%m-%Y-%Hh-%Mm-%Ss}.csv"


class BasicCSVAssembler(ABC):

    def __init__(self, selected_instance):
        self.selected_instance = selected_instance
        self.responder = CSVResponder(self.selected_instance, self.unique_filename_part)

    @property
    @abstractmethod
    def unique_filename_part(self):
        pass

    @abstractmethod
    def build_csv_file(self):
        pass

    @abstractmethod
    def get_csv_data(self, instance):
        pass
