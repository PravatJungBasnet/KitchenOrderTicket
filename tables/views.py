from rest_framework.response import Response
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


"""@extend_schema(tags=["Billing"])
class BillingView(APIView):
    def get(self, request, table_id):
        try:
            table = Tables.objects.get(id=table_id)
        except Tables.DoesNotExist:
            return Response(
                {"message": "Table not found"}, status=status.HTTP_404_NOT_FOUND
            )

        billing = Billing.objects.get(table=table, status=PaymentStatus.PENDING)
        return Response(
            {"table_id": table.id, "total_bill": billing.order.total_amount}
        ) """
