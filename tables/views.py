from .models import Tables, Menu, Order
from .serilaizers import TableSerializer, MenuSerializer, OrderSerializer
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
