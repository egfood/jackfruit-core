from rest_framework import serializers

class CurrentBuyerProfileDefault(serializers.CurrentUserDefault):
    def __call__(self, serializer_field):
        buyer = super().__call__(serializer_field)
        return buyer.profile