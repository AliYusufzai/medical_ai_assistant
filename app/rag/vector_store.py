from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    ScoredPoint,
)

from app.core.config import config


class VectorStore:
    def __init__(self):
        self.__qdrantClient = AsyncQdrantClient(url=config.QDRANT_URL)

    async def ensure_collection_exists(self):
        collection_check = await self.__qdrantClient.collection_exists(
            config.QDRANT_COLLECTION
        )

        if not collection_check:
            await self.__qdrantClient.create_collection(
                config.QDRANT_COLLECTION,
                vectors_config=VectorParams(
                    size=config.VECTOR_SIZE, distance=Distance.COSINE
                ),
            )

    async def upsert(self, points: list[PointStruct]) -> None:
        await self.__qdrantClient.upsert(
            collection_name=config.QDRANT_COLLECTION,
            points=points,
        )

    async def search(
        self, query_vector: list[float], user_id: int, limit: int = 5
    ) -> list[ScoredPoint]:
        results: list[ScoredPoint] = await self.__qdrantClient.query_points(  # type: ignore
            collection_name=config.QDRANT_COLLECTION,
            query=query_vector,
            query_filter=Filter(
                must=[FieldCondition(key="user_id", match=MatchValue(value=user_id))]
            ),
            limit=limit,
        )
        return results.points  # type: ignore


vector_store = VectorStore()
