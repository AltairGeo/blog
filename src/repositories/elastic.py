from typing import Dict, Any, List, Optional

from repositories.base import AbstractElasticRepo
from schemas.posts import FullPost
from utils.posts import calculation_offset


class ElasticRepo(AbstractElasticRepo):
    async def add_to_index(self, doc_id: int, document: Dict[str, Any]) -> bool:
        try:
            await self.es.index(index=self.index_name, id=str(doc_id), document=document)
            return True
        except Exception as e:
            print(e)
            return False

    async def remove_from_index(self, doc_id: int) -> bool:
        try:
            await self.es.delete(index=self.index_name, id=str(doc_id))
            return True
        except Exception as e:
            print(e)
            return False

    async def update_in_index(self, doc_id: int, update_fields: Dict[str, Any]) -> bool:
        try:
            await self.es.update(index=self.index_name, id=str(doc_id), doc=update_fields)
            return True
        except Exception as e:
            print(e)
            return False

    async def search_in_index(
            self,
            query: Dict[str, Any],
            sort: Optional[List[Dict[str, Any]]],
            page: int = 1,
    ) -> List[Dict[str, Any]]:
        try:
            offset = calculation_offset(page)
            result = await self.es.search(index=self.index_name, query=query, sort=sort, from_=offset, size=10)
            return result
        except Exception as e:
            print(e)
            return

    async def bulk_add_to_index(self, documents: List[FullPost]):
        try:
            bulk_actions = []
            documents = [i.to_elastic() for i in documents]

            for doc in documents:
                bulk_actions.append({
                    "index": {
                        "_index": self.index_name,
                        "_id": str(doc["id"]),
                    }
                })
                bulk_actions.append(doc)

            resp = await self.es.bulk(index=self.index_name, operations=bulk_actions)
            return resp
        except Exception as e:
            print(e)
            return {'err': str(e)}

    async def ping(self) -> bool:
        try:
            return await self.es.ping()
        except Exception as e:
            print(e)
            return False
