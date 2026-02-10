from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from . import models


class StoreView(ListView):
    model = models.Product
    context_object_name = "products"
    template_name = "Store/store.html"

class StoreCategoryView(ListView):
    model = models.Product
    context_object_name = "products"
    template_name = "Store/store.html"

    def get_queryset(self):
        # Récupérer la catégorie spécifiée dans l'URL
        category_slug = self.kwargs['category']
        category = get_object_or_404(models.Category, slug=category_slug)

        # Filtrer les produits par catégorie
        queryset = super().get_queryset().filter(category=category)
        return queryset

class ProductView(DetailView):
    template_name = "Store/product.html"
    model = models.Product
    context_object_name = "product"

#Allows categories to be known in all templates
def categoriesview(request):
    categories_data = models.Category.objects.all()
    return {"categories":categories_data}

