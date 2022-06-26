from django.forms import ValidationError
from rest_framework import status, generics
from rest_framework.response import Response
from shop_units.models import ShopUnit
from .serializers import ShopUnitNodeSerializer, ShopUnitImportSerializer
from .errors import VALIDATION_FAILED, NOT_FOUND_ERROR
from collections import deque
import datetime


class ShopUnitImport(generics.ListCreateAPIView):
    """Generic View для создания/обновления списка товаров/категорий."""

    queryset = ShopUnit.objects.all()
    serializer_class = ShopUnitImportSerializer

    def create(self, request):
        """Создание/обновление списка с добавлением даты обновления."""
        items = request.data['items']
        date = request.data['updateDate']
        for item in items:
            item['date'] = date
        serializer = self.get_serializer(
            data=items,
            many=True)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(
                status=status.HTTP_200_OK,
                headers=headers
            )
        return Response(
            VALIDATION_FAILED,
            status=status.HTTP_400_BAD_REQUEST
        )


class ShopUnitDestroy(generics.DestroyAPIView):
    """Generic View для удаления категории/товара."""

    queryset = ShopUnit.objects.all()
    serializer_class = ShopUnitNodeSerializer

    def destroy(self, request, *args, **kwargs):
        """Удаление товара или категории с дочерними элементами."""
        item_id = kwargs.get('pk')
        try:
            item = ShopUnit.objects.get(id=item_id)
        except ShopUnit.DoesNotExist:
            return Response(
                NOT_FOUND_ERROR,
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError:
            return Response(
                VALIDATION_FAILED,
                status=status.HTTP_400_BAD_REQUEST
            )
        if item.type == 'CATEGORY':
            children = deque(ShopUnit.objects.filter(parentId=item_id))
            while children:
                child = children.pop()
                children.extendleft(ShopUnit.objects.filter(parentId=child.id))
                child.delete()
        return super().destroy(request, *args, **kwargs)


class ShopUnitDetail(generics.RetrieveAPIView):
    """Generic View для получения информации о товаре/категории."""

    queryset = ShopUnit.objects.all()
    serializer_class = ShopUnitNodeSerializer

    def retrieve(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        try:
            item = ShopUnit.objects.get(id=item_id)
        except ShopUnit.DoesNotExist:
            return Response(
                NOT_FOUND_ERROR,
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError:
            return Response(
                VALIDATION_FAILED,
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().retrieve(request, *args, **kwargs)


class ShopUnitSales(generics.ListAPIView):
    """Generic View для получения списка товаров,
    цена которых была обновлена за последние 24 часа.
    """

    serializer_class = ShopUnitNodeSerializer

    def get_queryset(self):
        print(self)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        queryset = ShopUnit.objects.filter(
            date__gte=date,
            type='OFFER'
        )
        return queryset
