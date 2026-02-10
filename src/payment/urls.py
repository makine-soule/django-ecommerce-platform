from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("payment-success/", views.paymentsuccessview, name="payment-success"),
    path("payment-failed/", views.PaymentFailedView.as_view(), name="payment-failed"),
    path("complete-order/", views.complet_order, name="complete-order"),
]