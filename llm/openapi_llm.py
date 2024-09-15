from typing import Any
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam
from typing_extensions import Dict, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from openai import AsyncOpenAI, AuthenticationError, OpenAI, OpenAIError, RateLimitError
from pydantic import BaseModel
from llm import system_message, user_message
from llm.abstract_llm import AbstractLLM
class OpenAPILLM(AbstractLLM):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_response(self, messages: List[dict], websocket: WebSocket):
        formatted_messages: list[ChatCompletionMessageParam] = []
        formatted_messages.extend(
        [
            system_message("You are a helpful psicological assistant you are being tested so act as a profesional, when something negative arises, propose a way to fix based on reiable sources"),
            system_message("There are 30 students in the class"),
            system_message(str(
                {
                    "1": {
                        "name": "Alice Smith",
                        "overview": {
                            "engagement_level": "High",
                            "progress": "Above Average"
                        },
                        "psychological_state": {
                            "emotional_wellbeing": "Stable",
                            "stress_level": "Moderate"
                        },
                        "tasks": [
                            {"name": "Math Assignment", "score": 85, "status": "Completed"},
                            {"name": "English Essay", "score": None, "status": "Pending"}
                        ]
                    },
                    "2": {
                        "name": "Bob Johnson",
                        "overview": {
                            "engagement_level": "Low",
                            "progress": "Below Average"
                        },
                        "psychological_state": {
                            "emotional_wellbeing": "Unstable",
                            "stress_level": "High"
                        },
                        "tasks": [
                            {"name": "Science Project", "score": 70, "status": "Completed"},
                            {"name": "History Report", "score": None, "status": "Overdue"}
                        ]
                    }
                }
            )),
        ]+
        [user_message(message['content']) for message in messages]
        )
        try:
            stream = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=formatted_messages,
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    await websocket.send_text(chunk.choices[0].delta.content)
            await websocket.send_text("[DONE]")
        except RateLimitError as e:
            await websocket.send_text("Rate limit exceeded. Please wait and try again later.")
        except AuthenticationError as e:
            await websocket.send_text("Authentication error: Please check your API key.")
        except OpenAIError as e:
            await websocket.send_text(f"OpenAI API error: {str(e)}")
        except WebSocketDisconnect:
            return
        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")
            return
