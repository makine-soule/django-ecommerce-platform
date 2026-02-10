from django.urls import path
from . import views

urlpatterns = [
    path("", views.CartSummaryView.as_view(), name="cart-summary"),
    path("add/", views.CartAdd, name="cart-add"),
    path("delete/", views.CartDelete, name="cart-delete"),
    path("update/", views.CartUpdate, name="cart-update"),

]