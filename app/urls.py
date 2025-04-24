from app.views import (
    BrandDetailView,
    BrandListView,
    CollectionDetailView,
    CollectionListView,
    ProductDetailView,
    ProductListView,
)
from django.urls import path

app_name = "app"

urlpatterns = [
    path("collection/", CollectionListView.as_view(), name="collection_list"),
    path("collection/<int:pk>", CollectionDetailView.as_view(), name="collection_detail"),
    path("brand/", BrandListView.as_view(), name="brand_list"),
    path("brand/<int:pk>", BrandDetailView.as_view(), name="brand_detail"),
    path("product/", ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product_detail"),
]
