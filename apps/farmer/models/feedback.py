from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .profile import FarmerProfile
from apps.store.models.order_item import FoodOrderItem
from core.models import FoodAbstract


class FarmerFeedback(FoodAbstract):
    class Meta:
        verbose_name = "Отзывы на фермера"
        verbose_name_plural = "Отзывы на фермеров"

    order_item = models.ForeignKey(FoodOrderItem, on_delete=models.SET_NULL, null=True, related_name="farmer_feedback")
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="farmer_feedback")
    rating = models.IntegerField("Оценка", validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.CharField("Отзыв", max_length=2000, blank=True, default="")