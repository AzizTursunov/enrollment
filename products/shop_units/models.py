from django.db import models


class ShopUnit(models.Model):
    """Создание модели ShopUnit"""

    class ShopUnitType(models.TextChoices):
        """Вспомогательный класс для выбора типа объекта."""

        OFFER = 'OFFER', 'OFFER'
        CATEGORY = 'CATEGORY', 'CATEGORY'

    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    parentId = models.UUIDField(blank=True, default=None, null=True)
    type = models.CharField(choices=ShopUnitType.choices, max_length=8)
    price = models.PositiveIntegerField(blank=True, null=True)
