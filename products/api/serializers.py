from rest_framework import serializers
from shop_units.models import ShopUnit


class ShopUnitListSerializer(serializers.ListSerializer):
    """Вспомогательный сериализатор для создания списка объектов."""

    def create(self, validated_data):
        """Метод для создания списка объектов."""
        res = []
        for item in validated_data:
            type = item.pop('type')
            shop, created = ShopUnit.objects.update_or_create(
                id=item.pop('id'),
                defaults=item
            )
            if created:
                shop.type = type
                shop.save()
            res.append(shop)
        return res

    def validate(self, attrs):
        """Проверка входных данных."""
        # Проверяем, что в одном запросе нет элементов с одинаковым id
        id_list = [item['id'] for item in attrs]
        unique_id_list = set(id_list)
        if len(id_list) != len(unique_id_list):
            raise serializers.ValidationError()

        # Проверям, что родителем товара/категории не является категория
        cats = [item.id for item in ShopUnit.objects.filter(type='CATEGORY')]
        cats.extend(
            [item['id'] for item in attrs if item['type'] == 'CATEGORY']
            )
        cats = set(cats)
        for item in attrs:
            parentId = item.get('parentId')
            if parentId is None or parentId in cats:
                continue
            raise serializers.ValidationError()

        return attrs


class ShopUnitImportSerializer(serializers.ModelSerializer):
    """Сериализатор для создания списка объектов для POST-запроса."""
    class Meta:
        list_serializer_class = ShopUnitListSerializer
        model = ShopUnit
        fields = ('id', 'name', 'parentId', 'price', 'type', 'date')
        extra_kwargs = {
            'id': {'validators': []}
        }

    def validate_price(self, value):
        """Валидация цены товара."""
        if value < 0:
            raise serializers.ValidationError()
        return value


class ShopUnitNodeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ShopUnit для GET-запроса."""

    children = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = ShopUnit
        fields = (
            'id', 'name', 'parentId', 'price',
            'type', 'date', 'children'
        )

    def get_children(self, obj):
        """Получение дочерних элементов объекта."""
        if obj.type == 'OFFER':
            return None
        children = ShopUnit.objects.filter(parentId=obj.id)
        children_list = [
            ShopUnitNodeSerializer(item).data for item in children
        ]
        return children_list

    def get_price(self, obj):
        """Получение цены объекта."""
        if obj.type == 'OFFER':
            return obj.price
        children = ShopUnit.objects.filter(parentId=obj.id)
        children_prices = [
            ShopUnitNodeSerializer(item).data['price'] for item in children
        ]
        return sum(children_prices) // len(children_prices)

    def to_representation(self, obj):
        """Удаление поля cheldren у товаров."""
        ret = super(ShopUnitNodeSerializer, self).to_representation(obj)
        if ret['children'] is None:
            ret.pop('children')
        return ret
