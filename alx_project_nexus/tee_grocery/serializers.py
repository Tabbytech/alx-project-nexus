from rest_framework import serializers
from .models import Product, Category, Cart, CartItem, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(help_text="Name of the product category")
    description = serializers.CharField(help_text="Description of the category")

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(help_text="Name of the product")
    description = serializers.CharField(help_text="Detailed description of the product")
    price = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the product in KES")
    created_at = serializers.DateTimeField(read_only=True, help_text="Timestamp when the product was added")

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, help_text="Detailed product information")
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True,
        help_text="ID of the product to add to cart"
    )
    subtotal = serializers.SerializerMethodField(help_text="Subtotal for this item (price × quantity)")

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity", "subtotal"]
        read_only_fields = ["id", "product", "subtotal"]

    def get_subtotal(self, obj):
        return obj.subtotal()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, help_text="List of items in the cart")
    total_price = serializers.SerializerMethodField(help_text="Total price of all items in the cart")

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total_price"]
        read_only_fields = ["id", "user", "items", "total_price"]

    def get_total_price(self, obj):
        return obj.total_price()


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, help_text="Product details for this order item")

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]
        read_only_fields = ["id", "product", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, help_text="List of items included in the order")

    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "total_price", "items"]
        read_only_fields = ["id", "user", "created_at", "total_price", "items"]