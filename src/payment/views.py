from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from .forms import ShippingForm
from .models import ShippingAddress, Order, OrderItem
#Login Required
from django.contrib.auth.mixins import LoginRequiredMixin

from Cart.cart import Cart

@login_required(login_url="two_factor:login")
def paymentsuccessview(request):

    # Empty the cart after payment
    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]

    return render(request, "payment/payment_success.html")

class PaymentFailedView(LoginRequiredMixin, TemplateView):
    login_url = "two_factor:login"
    template_name = "payment/payment_failed.html"

class CheckoutView(LoginRequiredMixin, UpdateView):
    login_url = "two_factor:login"
    success_url = reverse_lazy('payment-success')
    template_name = "payment/checkout.html"
    form_class = ShippingForm
    model = ShippingAddress

    def get_object(self, queryset=None):
        return ShippingAddress.objects.get_or_create(user=self.request.user)[0]

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return JsonResponse({'error': True}, status=400)

def complet_order(request):
    if request.POST.get("action") == "post":
        name = request.POST.get("name")
        email = request.POST.get("email")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zipcode = request.POST.get("zipcode")
        #shipping_adrress : allow us to make the recap informations about the user
        shipping_address = (address1 + "\n" + address2 + "\n" + city + "\n" + state + "\n" + zipcode + "\n")

        #shopping cart information
        cart = Cart(request)
        total_cost = cart.get_total()

        if request.user.is_authenticated:
            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost,
                                         user=request.user)
            #We create one object per item
            for item in cart:
                OrderItem.objects.create(order_id=order, product=item["product"], quantity=item["qty"],
                                         price=item["price"], user=request.user)

        # This part is not necessary for my case because i've protected the checkout view, and if the user arrived
        # at this level, he is automaticly connected
        else:
            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost)
            #We create one object per item
            for item in cart:
                OrderItem.objects.create(order_id=order, product=item["product"], quantity=item["qty"],
                                         price=item["price"])

        order_succes = True
        response = JsonResponse({"success":order_succes})
        return response