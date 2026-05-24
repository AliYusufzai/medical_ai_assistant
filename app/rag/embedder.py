from google import genai
from google.genai import types
from app.core.config import config

# "RETRIEVAL_DOCUMENT": Use this for texts you are storing inside a vector database (like your Qdrant setup).
# "RETRIEVAL_QUERY": Use this on incoming user search queries right before you query your database.
# "SEMANTIC_SIMILARITY": Use this if you are strictly doing raw pairwise comparisons (e.g., comparing two medical strings directly using cosine similarity).


class Embedder:
    def __init__(self) -> None:
        self.__client = genai.Client(api_key=config.GEMINI_API_KEY)

    async def embed_document(self, text: str) -> list[float]:
        response = await self.__client.aio.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT", output_dimensionality=768),
        )

        if not response.embeddings or not response.embeddings[0].values:
            raise ValueError("Failed to generate document embedding")
         
        return list(response.embeddings[0].values)
    
    async def embed_query(self, text:str) -> list[float]:

        response = await self.__client.aio.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY", output_dimensionality=768),
        )

        if not response.embeddings or not response.embeddings[0].values:
            raise ValueError("Failed to generate query embedding")
        
        return list(response.embeddings[0].values)

embedder = Embedder()