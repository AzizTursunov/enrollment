from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ShopUnitImport, ShopUnitDestroy, ShopUnitDetail, ShopUnitSales

urlpatterns = [
    path('imports/', ShopUnitImport.as_view()),
    path('delete/<str:pk>', ShopUnitDestroy.as_view()),
    path('nodes/<str:pk>', ShopUnitDetail.as_view()),
    path('sales/', ShopUnitSales.as_view()),

]
