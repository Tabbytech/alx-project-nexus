from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    CategoryViewSet,
    CartView,
    AddToCartView,
    RemoveFromCartView,
    CheckoutView,
    
)

# Router for viewsets
router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet)

# Combine router URLs with custom API endpoints
urlpatterns = router.urls + [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/", AddToCartView.as_view(), name="cart-add"),
    path("cart/remove/<int:pk>/", RemoveFromCartView.as_view(), name="cart-remove"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
   ]
