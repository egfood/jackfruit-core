from rest_framework.exceptions import NotAcceptable


class HasNoActiveDelivery(NotAcceptable):
    default_detail = 'Active delivery not found.'
    default_code = 'has_no_active_delivery'
