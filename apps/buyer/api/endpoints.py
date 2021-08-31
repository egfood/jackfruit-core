from core.api.basic_endpoint import ProfileEndpoint
from .serializers import BuyerProfileSerializer
from ..models.profile import BuyerProfile


class BuyerProfileEndpoint(ProfileEndpoint):
    serializer_class = BuyerProfileSerializer
    profile_class = BuyerProfile
