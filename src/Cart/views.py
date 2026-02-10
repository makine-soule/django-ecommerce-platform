from django.views.generic import TemplateView
from .cart import Cart
from Store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

#Login Required
from django.contrib.auth.mixins import LoginRequiredMixin


class CartSummaryView(TemplateView):
    template_name = "Cart/cart-summary.html"  # Chemin vers votre template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj = Cart(self.request)
        context['cart'] = cart_obj
        return context

def CartAdd(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_quantity"))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_qty=product_qty)
        cart_quantity = cart.__len__()
        response = JsonResponse({"qty": cart_quantity})
        return response

def CartUpdate(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_quantity"))
        cart.update(product=product_id, qty=product_qty)
        cart_quantity = cart.__len__() # nous permet d'avoir le nombre d'éléments restant dans le cadis
        cart_total = cart.get_total() # nous permet d'avoir le prix total restant
        response = JsonResponse({"qty": cart_quantity, "total": cart_total})
        return response


def CartDelete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get("product_id"))
        cart.delete(product=product_id)
        cart_quantity = cart.__len__() # nous permet d'avoir le nombre d'éléments restant dans le cadis
        cart_total = cart.get_total() # nous permet d'avoir le prix total restant
        response = JsonResponse({"qty": cart_quantity, "total": cart_total})
        return response