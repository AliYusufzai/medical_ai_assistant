import fitz  # type: ignore
import asyncio
import uuid
from qdrant_client.models import PointStruct, ScoredPoint

from app.rag.embedder import embedder
from app.rag.vector_store import vector_store
from app.core.config import config

class Pipeline:
    def __init__(self):
        self.__embedder = embedder
        self.__vector_store = vector_store

    def extract_text(self, file_path: str) -> str:
        full_text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                page_text = page.get_text()  # type: ignore
                if isinstance(page_text, str):
                    full_text += page_text
        return full_text

    def chunk_text(self, text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
        chunks: list[str] = []
        start: int = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            if chunk.strip():
                chunks.append(chunk)
            start += chunk_size - chunk_overlap

        return chunks

    async def index_document(
        self, file_path: str, user_id: int, document_id: int
    ) -> None:
        text = self.extract_text(file_path)
        print(f"Extracted text length: {len(text)} characters")

        chunks = self.chunk_text(text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
        print(f"Total chunks: {len(chunks)}")

        coroutines = []
        for chunk in chunks:
            coroutines.append(self.__embedder.embed_document(chunk)) # type: ignore

        vectors: list[list[float]] = await asyncio.gather(*coroutines) # type: ignore

        points: list[PointStruct] = []
        for i, chunk in enumerate(chunks):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vectors[i],
                payload={
                    "text": chunk,
                    "user_id": user_id,
                    "document_id": document_id,
                    "chunk_index": i,
                },
            )
            points.append(point)

        await self.__vector_store.upsert(points)

    async def search(self, query: str, user_id: int, limit: int = 5) -> list[str]:
        query_vector: list[float] = await self.__embedder.embed_query(query)
        results: list[ScoredPoint] = await self.__vector_store.search( # type: ignore
            query_vector, user_id, limit
        )
        return [str(result.payload["text"]) for result in results if result.payload]


pipeline = Pipeline()
