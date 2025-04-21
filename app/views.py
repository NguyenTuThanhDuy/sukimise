import json
from django.http import Http404
from django.http.request import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.models import Collection, Brand, Product
from app.serializers import CollectionSerializer, BrandSerializer, ProductSerializer
from app.embedding import EmbeddingVector
from app.product_cache import ProductCache
from app.vector_search import ProductSearch


class CollectionListView(APIView):

    def get(self, request: HttpRequest, format=None):
        collections = Collection.objects.all()
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest, format=None):
        data = json.loads(request.body)
        serializer = CollectionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionDetailView(APIView):

    def get_active_object(self, pk: int):
        try:
            return Collection.objects.get(pk=pk)
        except Collection.DoesNotExist:
            raise Http404(f"Collection ID: {pk} does not exist")

    def get_all_type_object(self, pk: int):
        try:
            return Collection.all_objects.get(pk=pk)
        except Collection.DoesNotExist:
            raise Http404(f"Collection ID: {pk} does not exist")

    def get(self, request: HttpRequest, pk: int, format=None):
        collection = self.get_active_object(pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    def put(self, request: HttpRequest, pk: int, format=None):
        collection = self.get_all_type_object(pk)
        data = json.loads(request.body)
        serializer = CollectionSerializer(collection, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, pk: int, format=None):
        collection = self.get_all_type_object(pk)
        serializer = CollectionSerializer(collection, {"active": False})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class BrandListView(APIView):

    def get(self, request: HttpRequest, format=None):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest, format=None):
        data = json.loads(request.body)
        serializer = BrandSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BrandDetailView(APIView):

    def get_active_object(self, pk: int):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            raise Http404(f"Brand ID: {pk} does not exist")

    def get_all_type_object(self, pk: int):
        try:
            return Brand.all_objects.get(pk=pk)
        except Brand.DoesNotExist:
            raise Http404(f"Brand ID: {pk} does not exist")

    def get(self, request: HttpRequest, pk: int, format=None):
        brand = self.get_active_object(pk)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)

    def put(self, request: HttpRequest, pk: int, format=None):
        brand = self.get_all_type_object(pk)
        data = json.loads(request.body)
        serializer = BrandSerializer(brand, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, pk: int, format=None):
        brand = self.get_all_type_object(pk)
        serializer = BrandSerializer(brand, {"active": False})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class ProductListView(APIView):

    def get(self, request: HttpRequest):
        search_text = request.GET.get("search", "").strip()
        if search_text:
            products = ProductSearch.search_from_cached(
                ProductCache.get_products(),
                EmbeddingVector().create_embedding_vector(input_text=search_text),
            )
        else:
            products = ProductCache.get_products()

        serializer = ProductSerializer(products.values(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save()

            # Optional: Re-serialize to return full object (incl. nested if configured)
            response_serializer = ProductSerializer(product)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get_active_object(self, pk: int):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404(f"Product ID: {pk} does not exist")

    def get_all_type_object(self, pk: int):
        try:
            return Product.all_objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404(f"Product ID: {pk} does not exist")

    def get(self, request: HttpRequest, pk: int, format=None):
        product = self.get_active_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request: HttpRequest, pk: int, format=None):
        product = self.get_all_type_object(pk)
        data = json.loads(request.body)
        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, pk: int, format=None):
        product = self.get_all_type_object(pk)
        serializer = ProductSerializer(product, {"active": False})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
