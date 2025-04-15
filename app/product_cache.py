from app.base_cache import BaseCache
from app.models import Product


class ProductCache(BaseCache):
    cache_key = "product_cache"

    @classmethod
    def load_data(cls):
        """Fetch data from DB and store it in cache."""
        data = {}
        products = Product.objects.all()
        for p in products:
            data[p.pk] = p
        cls.set_data(cls.cache_key, data)
        return data

    @classmethod
    def get_products(cls):
        """Retrieve from cache if available, otherwise load from DB."""
        data = cls.get_data(cls.cache_key)
        if data is None:
            data = cls.load_data()
        return data
