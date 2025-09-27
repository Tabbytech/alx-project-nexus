from rest_framework import viewsets, filters, status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from django.db import transaction
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
)
from rest_framework.permissions import IsAuthenticated


@extend_schema(tags=["Categories"])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(tags=["Products"])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]


@extend_schema(tags=["Cart"], responses={200: CartSerializer})
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


@extend_schema(
    tags=["Cart"],
    request=CartItemSerializer,
    responses={201: CartSerializer, 400: OpenApiResponse(description="Invalid input")},
)
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data["product"]
            quantity = serializer.validated_data.get("quantity", 1)
            item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            item.quantity = item.quantity + quantity if not created else quantity
            item.save()
            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Cart"],
    parameters=[OpenApiParameter(name="pk", description="CartItem ID", required=True, type=int)],
    responses={200: CartSerializer, 404: OpenApiResponse(description="Item not found")},
)
class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        try:
            item = cart.items.get(pk=pk)
            item.delete()
            return Response(CartSerializer(cart).data)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=["Checkout"], request=OrderSerializer, responses={201: OrderSerializer})
class CheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart or not cart.items.exists():
            raise ValueError("Cart is empty")

        order = serializer.save(user=user, total_price=0)
        total = sum(
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            ).price * item.quantity
            for item in cart.items.all()
        )

        order.total_price = total
        order.save()
        cart.items.all().delete()
        