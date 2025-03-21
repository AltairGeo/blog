from abc import ABC, abstractmethod
from logging import warning
from typing import Dict, Any, Optional, List

from elasticsearch import AsyncElasticsearch


class AbstractRepo(ABC):
    @abstractmethod
    async def create(self):
        warning("DONT USE ABSTRACT REPOSITORY!")
        raise NotImplementedError

    @abstractmethod
    async def update(self):
        warning("DONT USE ABSTRACT REPOSITORY!")
        raise NotImplementedError

    @abstractmethod
    async def delete(self):
        warning("DONT USE ABSTRACT REPOSITORY!")
        raise NotImplementedError

    @abstractmethod
    async def find_one(self):
        warning("DONT USE ABSTRACT REPOSITORY!")
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        warning("DONT USE ABSTRACT REPOSITORY!")
        raise NotImplementedError


class AbstractElasticRepo(ABC):
    def __init__(self, es_client: AsyncElasticsearch, index_name: str):
        self.es = es_client
        self.index_name = index_name

    @abstractmethod
    async def add_to_index(self, doc_id: int, document: Dict[str, Any]) -> bool:
        warning("DONT USE ABSTRACT REPOSITORY!")
        raise NotImplementedError

    @abstractmethod
    async def remove_from_index(self, doc_id: int) -> bool:
        warning("DONT USE ABSTRACT REPOSITORY!")
        raise NotImplementedError

    @abstractmethod
    async def update_in_index(self, doc_id: int, update_fields: Dict[str, Any]) -> bool:
        warning("DONT USE ABSTRACT REPOSITORY!")
        raise NotImplementedError

    @abstractmethod
    async def search_in_index(
            self,
            query: Dict[str, Any],
            sort: Optional[List[Dict[str, any]]],
            page: int = 1,
    ) -> List[Dict[str, Any]]:
        warning("DONT USE ABSTRACT REPOSITORY!")
        raise NotImplementedError

    @abstractmethod
    async def bulk_add_to_index(self, documents: List[Dict[str, Any]]):
        raise NotImplementedError

    @abstractmethod
    async def ping(self) -> bool:
        raise NotImplementedError
