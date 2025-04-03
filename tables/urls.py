from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TableViewSet,
    MenuViewSet,
    OrderViewSet,
    CategoryViewSet,
    OrderItemViewSet,
    BillingView,
    MostSoldItemsDailyAPIView,
)

router = DefaultRouter()
app_name = "tables"
router.register("category", CategoryViewSet, basename="category")
router.register("menu", MenuViewSet, basename="menu")
router.register("order", OrderViewSet, basename="order")
router.register("order-items", OrderItemViewSet, basename="order-items")
router.register("", TableViewSet, basename="tables")


urlpatterns = [
    # path("<int:table_id>/", BillingView.as_view(), name="billing"),
    # path('order/<int:id>/update-order/', UpdateOrderView.as_view(), name='update-order'),
    path("daily/", MostSoldItemsDailyAPIView.as_view(), name="most-sold-items-daily"),
    path("billing/<int:table_id>/", BillingView.as_view(), name="billing"),
    path("", include(router.urls)),
]
