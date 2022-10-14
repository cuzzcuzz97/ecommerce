from django.urls import path, re_path
from . import views
from .views import (
    HomeView,
    ItemDetailView,
    OrderSummaryView,
    add_to_cart,
    increase_quantity,
    decrease_quantity,
    delete_item,
)
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product-detail'),
    path('product/<slug>/addtocart', add_to_cart, name='add-to-cart'),
    path('product/<slug>/increase_quantity', increase_quantity, name='increase_quantity'),
    path('product/<slug>/decrease_quantity', decrease_quantity, name='decrease_quantity'),
    path('product/<slug>/delete_item', delete_item, name='delete_item'),
    path('product/cart', OrderSummaryView.as_view(), name='order-summary'),
]

