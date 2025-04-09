from rest_framework import serializers
from app.models import Collection, Brand, Product, Supplier
from app.embedding import EmbeddingVector


from rest_framework import serializers
from .models import Collection, Brand, Supplier


class CollectionSerializer(serializers.ModelSerializer):
    collection_name = serializers.CharField(required=False, allow_blank=False)
    collection_description = serializers.CharField(required=False, allow_blank=False)

    class Meta:
        model = Collection
        fields = ['collection_id', 'collection_name', 'collection_description', 'active']
        read_only_fields = ['collection_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance is None:
            self.fields['collection_name'].required = True
            self.fields['collection_description'].required = True

    def update(self, instance: Collection, validated_data: dict):
        """
        If the field is not provided, keep the existing value.
        """
        collection_name = validated_data.get('collection_name', instance.collection_name)
        collection_description = validated_data.get('collection_description', instance.collection_description)
        active = validated_data.get('active', instance.active)

        instance.collection_name = collection_name
        instance.collection_description = collection_description
        instance.active = active

        instance.save()
        return instance

    def create(self, validated_data):
        return super().create(validated_data)


class BrandSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(required=False, allow_blank=False)
    brand_description = serializers.CharField(required=False, allow_blank=False)

    class Meta:
        model = Brand
        fields = ['brand_id', 'brand_name', 'brand_description', 'active']
        read_only_fields = ['brand_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance is None:
            self.fields['brand_name'].required = True
            self.fields['brand_description'].required = True

    def update(self, instance: Brand, validated_data: dict):
        """
        If the field is not provided, keep the existing value.
        """
        brand_name = validated_data.get('brand_name', instance.brand_name)
        brand_description = validated_data.get('brand_description', instance.brand_description)
        active = validated_data.get('active', instance.active)

        instance.brand_name = brand_name
        instance.brand_description = brand_description
        instance.active = active

        instance.save()
        return instance

    def create(self, validated_data):
        return super().create(validated_data)


class SupplierSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(required=False, allow_blank=False)
    supplier_description = serializers.CharField(required=False, allow_blank=False)

    class Meta:
        model = Supplier
        fields = ['supplier_id', 'supplier_name', 'supplier_description', 'active']
        read_only_fields = ['supplier_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance is None:
            self.fields['supplier_name'].required = True
            self.fields['supplier_description'].required = True

    def update(self, instance: Supplier, validated_data: dict):
        """
        If the field is not provided, keep the existing value.
        """
        supplier_name = validated_data.get('supplier_name', instance.supplier_name)
        supplier_description = validated_data.get('supplier_description', instance.supplier_description)
        active = validated_data.get('active', instance.active)

        instance.supplier_name = supplier_name
        instance.supplier_description = supplier_description
        instance.active = active

        instance.save()
        return instance

    def create(self, validated_data):
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(required=False, allow_blank=False)
    product_description = serializers.CharField(required=False, allow_blank=False)
    product_description_vector = serializers.ListField(required=False, write_only=True)
    active = serializers.BooleanField(required=False)
    brand = BrandSerializer(read_only=True)
    collections = CollectionSerializer(many=True, read_only=True)
    suppliers = SupplierSerializer(many=True, read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        write_only=True, source='brand', required=False)
    collection_ids = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(),
        many=True, write_only=True, source='collections', required=False)
    supplier_ids = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        many=True, write_only=True, source='suppliers', required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance is None:
            self.fields['product_name'].required = True
            self.fields['product_description'].required = True

    def create(self, validated_data: dict):
        validated_data['product_description_vector'] = EmbeddingVector().create_embedding_vector(
            input_text=validated_data.get('product_description'))
        collections = validated_data.pop("collections", [])
        suppliers = validated_data.pop("suppliers", [])
        product = Product.objects.create(**validated_data)

        if collections:
            product.collections.set(collections)
        if suppliers:
            product.suppliers.set(suppliers)

        return product

    def update(self, instance: Product, validated_data: dict):
        instance.product_name = validated_data.get("product_name", instance.product_name)
        instance.active = validated_data.get("active", instance.active)
        instance.brand = validated_data.get("brand", instance.brand)

        if "product_description" in validated_data:
            description_vector = EmbeddingVector().create_embedding_vector(input_text=validated_data.get('product_description'))
            instance.product_description_vector = description_vector
        else:
            instance.product_description_vector = validated_data.get(
                "product_description_vector", instance.product_description_vector
            )
        instance.product_description = validated_data.get("product_description", instance.product_description)

        instance.save()

        # Handle many-to-many updates separately
        if "collections" in validated_data:
            instance.collections.set(validated_data["collections"])
        if "suppliers" in validated_data:
            instance.suppliers.set(validated_data["suppliers"])

        return instance
