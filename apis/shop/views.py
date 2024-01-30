from rest_framework import generics
from rest_framework.response import Response
from .models import Order, Product, OrderItem
from .serializers import OrderSerializer
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from apis.shop.serializers import ProductSerializer

class ProductsView(APIView, PageNumberPagination):
    def get(self, request):
        products = Product.objects.all()
        results = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        order_items_data = self.request.data.pop('order_items', [])

        order = serializer.save()

        for order_item_data in order_items_data:
            product_data = order_item_data.pop('product', {})
            product = Product.objects.get(pk=product_data['id'])
            product.stock -= order_item_data.get('quantity')
            product.save()
            OrderItem.objects.create(order=order, product=product, **order_item_data)

class CustomerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        customer_name = self.kwargs.get('customer_name', None)

        queryset = Order.objects.filter(customer_name=customer_name)
        return queryset