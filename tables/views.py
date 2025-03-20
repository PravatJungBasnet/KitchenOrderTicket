from .models import Tables, Menu, Order, Category, OrderItem
from .serilaizers import (
    TableSerializer,
    MenuSerializer,
    OrderSerializer,
    CategorySerializer,
    OrderItemSerializer,
)
from rest_framework.viewsets import ModelViewSet
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
