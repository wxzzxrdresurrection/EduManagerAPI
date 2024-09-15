from abc import ABC, abstractmethod
from typing import Any, Dict
from typing_extensions import List
from pydantic import BaseModel
from fastapi import WebSocket

class AbstractLLM(ABC):
    @abstractmethod
    async def generate_response(self, messages: List[dict], websocket: WebSocket, extra_context: List[str] = []):
        """Generates a response from the LLM based on the given prompt and context."""
        pass
