from django.urls import path
from . import views
from .views import OrderCreateView, CustomerOrderListView

urlpatterns = [
    path('products/', views.ProductsView.as_view(), name='products'),
    # need to define product details here for a single product
    path('order/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<str:customer_name>/', CustomerOrderListView.as_view(), name='customer_order_list'),
]