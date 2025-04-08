from rest_framework import serializers
from app.models import Collection, Brand, Product, Supplier
from app.embedding import EmbeddingVector


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['collection_id', 'collection_name', 'collection_description', 'active']
        read_only_fields = ['collection_id']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_id', 'brand_name', 'brand_description', 'active']
        read_only_fields = ['brand_id']


class ProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(required=False)
    product_description = serializers.CharField(required=False)
    distance = serializers.FloatField(required=False)
    product_description_vector = serializers.ListField(required=False, write_only=True)
    active = serializers.BooleanField(required=False)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), required=False)
    collections = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all(), many=True, required=False)
    suppliers = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), many=True, required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def validate_product_name(self, value):
        # Make sure product_name is always provided when creating a new Product (POST request)
        if not value and not self.instance:  # This means it's a create (no instance exists)
            raise serializers.ValidationError("Product name is required for product creation.")
        return value

    def create(self, validated_data):
        validated_data['product_description_vector'] = EmbeddingVector().create_embedding_vector(
            input_text=validated_data.get('product_description'))
        collections = validated_data.pop("collections", [])
        suppliers = validated_data.pop("suppliers", [])
        product = Product.objects.create(**validated_data)
        # Assign brand if provided
        if collections:
            product.collections.set(collections)
        if suppliers:
            product.suppliers.set(suppliers)

        return product

    def update(self, instance, validated_data):
        instance.product_name = validated_data.get("product_name", instance.product_name)
        instance.active = validated_data.get("active", instance.active)
        instance.brand = validated_data.get("brand", instance.brand)

        if "product_description" in validated_data:
            description_vector = EmbeddingVector().create_embedding_vector(input_text=validated_data.get('product_description'))
            instance.product_description_vector = description_vector

        instance.save()

        # Handle many-to-many updates separately
        if "collections" in validated_data:
            instance.collections.set(validated_data["collections"])
        if "suppliers" in validated_data:
            instance.suppliers.set(validated_data["suppliers"])

        return instance
