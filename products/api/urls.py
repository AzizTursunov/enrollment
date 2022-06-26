from django.urls import path

from .views import (
    ShopUnitImport, ShopUnitDestroy,
    ShopUnitDetail, ShopUnitSales
)

urlpatterns = [
    path('imports/', ShopUnitImport.as_view()),
    path('delete/<str:pk>', ShopUnitDestroy.as_view()),
    path('nodes/<str:pk>', ShopUnitDetail.as_view()),
    path('sales/', ShopUnitSales.as_view()),

]
