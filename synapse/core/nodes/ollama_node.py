import ollama
from typing import Optional, List, Dict, Any

class OllamaNode:
    def __init__(self, model: str = "llama3", host: str = "http://localhost:11434"):
        self.model = model
        self.client = ollama.AsyncClient(host=host)

    async def generate(self, prompt: str, images: Optional[List[str]] = None) -> str:
        """
        Generates a response from the Ollama model.
        Can handle multimodal input (images) if provided.
        """
        response = await self.client.generate(
            model=self.model,
            prompt=prompt,
            images=images or []
        )
        return response.get("response", "")

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Handles a chat conversation with the Ollama model.
        """
        response = await self.client.chat(
            model=self.model,
            messages=messages
        )
        return response.get("message", {}).get("content", "")
