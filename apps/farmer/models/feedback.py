from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.store.models.order_item import FoodOrderItem
from core.models import FoodAbstract


class FarmerFeedback(FoodAbstract):
    class Meta:
        verbose_name = "Отзывы на фермера"
        verbose_name_plural = "Отзывы на фермеров"

    order_item = models.OneToOneField(FoodOrderItem, on_delete=models.SET_NULL,
                                      null=True, related_name="farmer_feedback")
    rating = models.IntegerField("Оценка", validators=[MinValueValidator(1), MaxValueValidator(5)],
                                 blank=True, null=True)
    feedback = models.TextField("Отзыв", blank=True, default="")

    def __str__(self):
        return f"Отзыв на [{self.order_item}]"
