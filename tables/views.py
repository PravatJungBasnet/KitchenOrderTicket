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
            payment_status=PaymentStatus.PAID, status=OrderStatus.PENDING
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

    @action(
        detail=True,
        methods=["post"],
        url_path="add-items",
        serializer_class=OrderItemSerializer,
    )
    def add_items_to_order(self, request, pk=None):
        try:
            order = self.get_object()

            if order.status == OrderStatus.COMPLETED:
                return Response(
                    {"error": "Cannot modify a completed order"}, status=400
                )

            menu_items = request.data.get("menu_items")

            if menu_items is None:
                menu_id = request.data.get("menu")
                quantity = request.data.get("quantity")

                if menu_id is None and quantity is None:
                    return Response(
                        {"error": "Invalid payload. Provide either  menu and quantity"},
                        status=400,
                    )

                menu_items = [{"menu_id": menu_id, "quantity": quantity}]

            if not menu_items:
                return Response({"error": "No menu items provided"}, status=400)

            # Add items to the order
            added_items = []
            for item in menu_items:
                try:
                    menu = Menu.objects.get(id=item.get("menu_id"))

                    # Check if item already exists in order
                    existing_order_item = OrderItem.objects.filter(
                        order=order, menu=menu
                    ).first()

                    if existing_order_item:
                        # Update existing item quantity
                        existing_order_item.quantity += item["quantity"]
                        existing_order_item.save()
                        added_items.append(
                            {
                                "menu_id": menu.id,
                                "menu_name": menu.name,
                                "quantity": item["quantity"],
                                "status": "updated",
                            }
                        )
                    else:
                        added_items.append(
                            {
                                "menu_id": menu.id,
                                "menu_name": menu.name,
                                "quantity": item["quantity"],
                                "status": "added",
                            }
                        )

                except Menu.DoesNotExist:
                    return Response(
                        {"error": f"Menu item with ID {item.get('menu_id')} not found"},
                        status=404,
                    )

            return Response(
                {
                    "message": "Items added successfully",
                    "added_items": added_items,
                    "total_amount": order.total_amount,
                },
                status=200,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)


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
