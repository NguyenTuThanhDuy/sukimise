from django.db import models
from django.db.models import F, Q
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchQuery
from pgvector.django import CosineDistance
from pgvector.django.vector import VectorField
from pgvector.django.indexes import HnswIndex

# Create your models here.
N_DIM = 512


class Audit(models.Model):
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BrandManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Brand(Audit):
    brand_id = models.AutoField(primary_key=True, help_text="brand id")
    brand_name = models.CharField(unique=True, max_length=100)
    brand_description = models.TextField()
    active = models.BooleanField(default=True)

    objects = BrandManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.brand_name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        db_table = "ms_app_brand"
        ordering = ["brand_id", "brand_name"]
        default_manager_name = "all_objects"
        indexes = [
            GinIndex(
                name="brand_name_gin_idx",
                fields=["brand_name", "brand_description"],
            )
        ]


class CollectionManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Collection(Audit):
    collection_id = models.AutoField(primary_key=True, help_text="collection id")
    collection_name = models.CharField(unique=True, max_length=100)
    collection_description = models.CharField(max_length=256)
    active = models.BooleanField(default=True)

    objects = CollectionManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.collection_name

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
        db_table = "ms_app_collection"
        ordering = ["collection_id", "collection_name"]
        default_manager_name = "all_objects"
        indexes = [
            GinIndex(
                name="collection_name_gin_idx",
                fields=["collection_name", "collection_description"],
            )
        ]


class SupplierManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Supplier(Audit):
    supplier_id = models.AutoField(primary_key=True, help_text="supplier id")
    supplier_name = models.CharField(unique=True, max_length=100)
    supplier_description = models.CharField(max_length=256)
    active = models.BooleanField(default=True)

    objects = SupplierManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.supplier_name

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        db_table = "ms_app_supplier"
        ordering = ["supplier_id", "supplier_name"]
        default_manager_name = "all_objects"
        indexes = [
            GinIndex(
                name="supplier_name_gin_idx",
                fields=["supplier_name", "supplier_description"],
            )
        ]


class ProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Product(Audit):
    product_id = models.AutoField(primary_key=True, help_text="product id")
    product_name = models.CharField(unique=True, max_length=100)
    product_description = models.TextField()
    product_description_vector = VectorField(dimensions=N_DIM)
    collections = models.ManyToManyField(Collection, through="ProductCollection")
    suppliers = models.ManyToManyField(Supplier, through="ProductSupplier")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    active = models.BooleanField(default=True)

    objects = ProductManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.product_name

    @classmethod
    def search_product_description_embedding(self, embedding: list[float], text_query: str):
        columns = ["product_id", "product_name"]
        columns_with_alias = {"product_desc": F("product_description")}
        products_with_description = Product.objects.values("product_id").annotate(
            distance=CosineDistance("product_description_vector", embedding),
            search=SearchVector("product_description")
        ).filter(
            Q(search=SearchQuery(text_query)) | Q(distance__lt=0.4)
        ).values(*columns, **columns_with_alias)
        return products_with_description

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "ms_app_product"
        ordering = ["product_id", "product_name"]
        default_manager_name = "all_objects"
        indexes = [
            HnswIndex(
                name="product_vector_idx",
                fields=["product_description_vector"],
                m=32,
                ef_construction=100,
                opclasses=["vector_cosine_ops"]
            ),
            GinIndex(
                name="product_name_gin_idx",
                fields=["product_name", "product_description"],
            )
        ]


class ProductCollection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product.product_name} {self.collection.collection_name}"

    class Meta:
        db_table = "ms_app_product_collection"


class ProductSupplier(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product.product_name} {self.supplier.supplier_name}"

    class Meta:
        db_table = "ms_app_product_supplier"
