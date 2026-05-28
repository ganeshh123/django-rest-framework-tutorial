from rest_framework import serializers

from .models import Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price", "stock")

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Prce must be greater than 0.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2, coerce_to_string=False
    )
    product_subtotal = serializers.DecimalField(
        source="item_subtotal", max_digits=10, decimal_places=2, coerce_to_string=False
    )
    product_detail = serializers.SerializerMethodField()

    def get_product_detail(self, obj):
        product = obj.product
        return f"/products/{product.id}"

    class Meta:
        model = OrderItem
        fields = (
            "product_name",
            "product_detail",
            "product_price",
            "quantity",
            "product_subtotal",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj.user
        return f"[{user.id}] {user.username}"

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = ("order_id", "created_at", "user", "status", "items", "total_price")

class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
    
    