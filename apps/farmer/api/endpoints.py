from core.api.basic_endpoint import ProfileEndpoint
from .serializers import FarmerProfileSerializer
from ..models.profile import FarmerProfile


class FarmerProfileEndpoint(ProfileEndpoint):
    serializer_class = FarmerProfileSerializer
    profile_class = FarmerProfile
