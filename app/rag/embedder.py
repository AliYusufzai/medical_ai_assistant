from google import genai
from google.genai import types

# "RETRIEVAL_DOCUMENT": Use this for texts you are storing inside a vector database (like your Qdrant setup).
# "RETRIEVAL_QUERY": Use this on incoming user search queries right before you query your database.
# "SEMANTIC_SIMILARITY": Use this if you are strictly doing raw pairwise comparisons (e.g., comparing two medical strings directly using cosine similarity).


class Embedder:
    def __init__(self) -> None:
        self.__client = genai.Client()

    async def embed_document(self, text: str) -> list[float]:
        response = await self.__client.aio.models.embed_content(
            model="text-embedding-004",
            contents=text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
        )

        if not response.embeddings or not response.embeddings[0].values:
            raise ValueError("Failed to generate document embedding")
         
        return list(response.embeddings[0].values)
    
    async def embed_query(self, text:str) -> list[float]:

        response = await self.__client.aio.models.embed_content(
            model="text-embedding-004",
            contents=text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
        )

        if not response.embeddings or not response.embeddings[0].values:
            raise ValueError("Failed to generate query embedding")
        
        return list(response.embeddings[0].values)

embedder = Embedder()