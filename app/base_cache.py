from typing import Optional

from django.core.cache import cache
from django.db.models.query import QuerySet


class BaseCache(object):
    queryset: Optional[QuerySet] = None
    cache_key: str = ""
    ttl = 43200

    @classmethod
    def get_query_set(cls) -> Optional[QuerySet]:
        return cls.queryset

    @classmethod
    def set_data(cls, key: str, data):
        cls.queryset = data
        cache.set(key, data, cls.ttl)

    @classmethod
    def get_data(cls, key: str) -> Optional[QuerySet]:
        if cls.queryset:
            return cls.get_query_set()
        return cache.get(key)
