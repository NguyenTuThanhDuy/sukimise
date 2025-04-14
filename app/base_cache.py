from django.core.cache import cache
from django.db.models.query import QuerySet


class BaseCache:
    queryset = None
    cache_key = None
    ttl = 43200

    @classmethod
    def get_query_set(cls) -> QuerySet:
        return cls.queryset

    @classmethod
    def set_data(cls, key: str, data):
        cache.set(key, data, cls.ttl)

    @classmethod
    def get_data(cls, key: str) -> QuerySet:
        if cls.queryset:
            return cls.get_query_set()
        return cache.get(key)
