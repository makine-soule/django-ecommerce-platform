from .cart import Cart

#Returns default session data from class Cart
def cart(request):
    return {"cart" : Cart(request)}