from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ShopUnitImport, ShopUnitDestroy, ShopUnitDetail, ShopUnitSales

urlpatterns = [
    path('v1/imports/', ShopUnitImport.as_view()),
    path('v1/delete/<str:pk>', ShopUnitDestroy.as_view()),
    path('v1/nodes/<str:pk>', ShopUnitDetail.as_view()),
    path('v1/sales/', ShopUnitSales.as_view()),

]
