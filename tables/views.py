from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import OrderStatus, PaymentStatus, Tables, Menu, Order, Category, OrderItem
from .serilaizers import (
    TableSerializer,
    MenuSerializer,
    OrderSerializer,
    CategorySerializer,
    OrderItemSerializer,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Tables"])
class TableViewSet(ModelViewSet):
    queryset = Tables.objects.all()
    serializer_class = TableSerializer
    filterset_fields = ["number", "is_occupied"]
    search_fields = ["number", "is_occupied"]


@extend_schema(tags=["Menu"])
class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filterset_fields = ["name", "price"]
    search_fields = ["name", "price"]


@extend_schema(tags=["Order"])
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ["id", "status"]
    search_fields = ["id", "status"]

    @action(
        detail=False, methods=["get"], name="recently-order", url_path="recently-order"
    )
    def recently_order(self, request):
        order = Order.objects.order_by("-id").filter(
            payment_status=PaymentStatus.PENDING
        )[:10]
        serializer = self.get_serializer(order, many=True)
        return Response({"data": serializer.data})

    @action(
        detail=False, methods=["get"], name="order-history", url_path="order-history"
    )
    def order_history(self, request):
        order = (
            Order.objects.order_by("-timestamp")
            .filter(payment_status=PaymentStatus.PAID, status=OrderStatus.COMPLETED)
            .order_by("-timestamp")
        )
        serializer = self.get_serializer(order, many=True)
        return Response({"data": serializer.data})


@extend_schema(tags=["Category"])
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ["id", "name"]
    search_fields = ["id", "name"]


@extend_schema(tags=["OrderItem"])
class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


@extend_schema(tags=["Billing"])
class BillingView(APIView):
    def get(self, request, *args, **kwargs):
        table_id = kwargs.get("table_id")
        table = get_object_or_404(Tables, id=table_id)

        order = (
            Order.objects.order_by("-timestamp")
            .filter(
                table=table,
                payment_status=PaymentStatus.PAID,
                status=OrderStatus.COMPLETED,
            )
            .first()
        )

        if not order:
            return Response(
                {"message": "No completed and paid orders found for this table"},
                status=404,
            )

        # Fetch ordered items with quantity
        order_items = OrderItem.objects.filter(order=order).select_related("menu")

        invoice_items = []
        subtotal = 0

        for item in order_items:
            quantity = item.quantity
            unit_price = float(item.menu.price)
            total_price = unit_price * quantity

            invoice_items.append(
                {
                    "name": item.menu.name,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "total_price": total_price,
                }
            )

            subtotal += total_price

        invoice_data = {
            "invoice_id": f"INV-{order.id:06}",  # Example: INV-000013
            "date": order.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "table_number": order.table.number,
            "items": invoice_items,
            "total": round(subtotal, 2),
        }

        return Response(invoice_data)
