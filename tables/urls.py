from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TableViewSet, MenuViewSet, OrderViewSet, BillingView

router = DefaultRouter()
app_name = "tables"
router.register("menu", MenuViewSet, basename="menu")
router.register("order", OrderViewSet, basename="order")
router.register("", TableViewSet, basename="tables")


urlpatterns = [
    path("<int:table_id>/", BillingView.as_view(), name="billing"),
    path("", include(router.urls)),
]
