from django.urls import path
from . import views
from .views import cart_view, add_to_cart, remove_from_cart, clear_cart

urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.item_list, name='item_list'),
    path('info/', views.info, name='info'),
    path("cart/", cart_view, name="cart_view"),
    path("cart/add/<int:item_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/clear/", clear_cart, name="clear_cart"),
]



