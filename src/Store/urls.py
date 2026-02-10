from django.urls import path
from . import views

urlpatterns = [
    path("", views.StoreView.as_view(), name="store"),
    path("product/<str:slug>/", views.ProductView.as_view(), name="product-info"),
    path("search/<str:category>/", views.StoreCategoryView.as_view(), name="store-category")
]
