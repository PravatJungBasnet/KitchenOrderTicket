from rest_framework import serializers
from .models import Tables, Menu, Order, Billing, Category


class BaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not hasattr(self.Meta, "serialize_fields"):
            return representation

        serialize_fields = self.Meta.serialize_fields
        for field, serializer_class in serialize_fields.items():
            if not hasattr(instance, field):
                continue

            field_value = getattr(instance, field)
            if field_value is None:
                continue

            if hasattr(field_value, "all") and callable(field_value.all):
                # for o2m or m2m relation
                representation[field] = serializer_class(
                    field_value.all(), many=True, context=self.context
                ).data
            else:
                representation[field] = serializer_class(
                    field_value, context=self.context
                ).data

        return representation


class TableSerializer(BaseSerializer):
    class Meta:
        model = Tables
        fields = ["id", "number", "is_occupied"]


class CategoryBriefSerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "category", "name", "price", "image", "is_available"]
        serialize_fields = {
            "category": CategoryBriefSerializer,
        }


class TableBriefSerializer(BaseSerializer):
    class Meta:
        model = Tables
        fields = ["id", "number"]


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class MenuBriefSerializer(BaseSerializer):
    class Meta:
        model = Menu
        fields = ["id", "category", "name", "price"]
        serialize_fields = {
            "category": CategoryBriefSerializer,
        }


class OrderSerializer(BaseSerializer):
    class Meta:
        model = Order
        fields = ["id", "menu", "table", "quantity", "status", "total_amount"]
        serialize_fields = {
            "table": TableBriefSerializer,
            "menu": MenuBriefSerializer,
        }


class OrderBriefSerializer(BaseSerializer):
    class Meta:
        model = Order
        fields = ["id", "total_amount"]


class BillingSerializer(BaseSerializer):
    class Meta:
        model = Billing
        fields = ["id", "order", "status", "timestamp"]
        serializer_field = {"order": OrderBriefSerializer}


"""class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderList
        fields=["id","table","order","quantity","total_amount"] """
