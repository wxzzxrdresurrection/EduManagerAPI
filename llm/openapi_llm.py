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
            system_message(
                """Eres un asistente psicológico virtual diseñado para ayudar a los profesores a comprender y apoyar el bienestar emocional y el desempeño académico de sus estudiantes. 
                Tu objetivo principal es analizar los datos proporcionados sobre los estudiantes, identificar posibles áreas de preocupación y ofrecer recomendaciones prácticas y basadas en evidencia para mejorar su experiencia educativa."""
            ),
            system_message(
                """Examina cuidadosamente los datos proporcionados sobre cada estudiante, incluyendo su historial académico, desempeño en tareas, observaciones del profesor, resultados de encuestas y cualquier otra información relevante. 
                Identifica patrones y tendencias en los datos que puedan indicar fortalezas, debilidades, áreas de mejora o posibles problemas emocionales. 
                Considera el contexto de la clase, el tamaño del grupo, la dinámica del aula y otros factores que puedan influir en el bienestar y el aprendizaje de los estudiantes."""
            ),
            system_message(
                """Brinda recomendaciones claras, específicas y accionables que los profesores puedan implementar en el aula. 
                Prioriza las estrategias basadas en evidencia y las mejores prácticas en psicología educativa y apoyo emocional. 
                Adapta tus recomendaciones al nivel educativo, la edad de los estudiantes y el contexto específico de la clase. 
                Si detectas posibles problemas emocionales o de comportamiento, sugiere intervenciones tempranas y recursos de apoyo adecuados."""
            ),
            system_message(
                """Utiliza un lenguaje claro, conciso y comprensible para los profesores. 
                Evita jerga técnica o términos psicológicos complejos que puedan resultar confusos. 
                Sé empático y comprensivo en tus respuestas, reconociendo los desafíos que enfrentan los profesores en el aula. 
                Si no tienes suficiente información para proporcionar una recomendación específica, sugiere al profesor que recopile más datos o busque apoyo adicional de un profesional de la salud mental."""
            ),
            system_message(
                """Recuerda que no eres un terapeuta o consejero, y no debes diagnosticar ni tratar problemas de salud mental. 
                Tus recomendaciones deben centrarse en estrategias educativas y de apoyo en el aula."""
            ),
            system_message(
                """
                Recomienda metodos de aprendizaje si es que se necesita, ademas si existe un alunmo con estadisticas negativas, recomienda tratar ese caso
                """
            ),
            system_message(
                """Prioriza la claridad y la precisión en tus respuestas. Asegúrate de que todas las palabras estén completas y correctamente escritas.
                """
            ),
            system_message(
                """Agrega un '*' al final de cada palabra, para tener una forma de darme cuenta que completaste la palabra 
                """
            ),
            

            system_message("There are 30 students in the class"),
            system_message(str(
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
                            {"name": "History Report", "score": 94, "status": "Overdue"}
                        ]
                    },
                    "3": {
                        "name": "Alice Carter",
                        "overview": {
                            "engagement_level": "High",
                            "progress": "Above Average"
                        },
                        "psychological_state": {
                            "emotional_wellbeing": "Stable",
                            "stress_level": "Low"
                        },
                        "tasks": [
                            {"name": "Math Assignment", "score": 85, "status": "Completed"},
                            {"name": "English Essay", "score": 90, "status": "Completed"}
                        ]
                    },
                    "4": {
                        "name": "David Lee",
                        "overview": {
                            "engagement_level": "Moderate",
                            "progress": "Average"
                        },
                        "psychological_state": {
                            "emotional_wellbeing": "Neutral",
                            "stress_level": "Moderate"
                        },
                        "tasks": [
                            {"name": "Physics Lab", "score": 75, "status": "Completed"},
                            {"name": "Geography Presentation", "score": None, "status": "Pending"}
                        ]
                    },
                    "5": {
                        "name": "Karen Thompson",
                        "overview": {
                            "engagement_level": "Low",
                            "progress": "Below Average"
                        },
                        "psychological_state": {
                            "emotional_wellbeing": "Anxious",
                            "stress_level": "High"
                        },
                        "tasks": [
                            {"name": "Chemistry Test", "score": 65, "status": "Completed"},
                            {"name": "Art Project", "score": 34, "status": "Overdue"}
                        ]
                    },
                    "6": {
                        "name": "John Smith",
                        "overview": {
                            "engagement_level": "High",
                            "progress": "Above Average"
                        },
                        "psychological_state": {
                            "emotional_wellbeing": "Stable",
                            "stress_level": "Low"
                        },
                        "tasks": [
                            {"name": "Biology Quiz", "score": 92, "status": "Completed"},
                            {"name": "History Essay", "score": 88, "status": "Completed"}
                        ]
                    },
                    "7": {
                        "name": "Emily Davis",
                        "overview": {
                            "engagement_level": "Moderate",
                            "progress": "Average"
                        },
                        "psychological_state": {
                            "emotional_wellbeing": "Content",
                            "stress_level": "Moderate"
                        },
                        "tasks": [
                            {"name": "Music Theory", "score": 80, "status": "Completed"},
                            {"name": "Physical Education", "score": 93, "status": "Pending"}
                        ]
                    }
                }   
                            
            )),

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
            acumulador = ""
            async for chunk in stream:
                contenido = chunk.choices[0].delta.content
                if contenido is not None:
                    acumulador += contenido
                    if contenido.endswith('*'):
                        await websocket.send_text(acumulador)
                        acumulador = ""  # Reiniciamos el acumulador una vez enviado
            if acumulador:
                await websocket.send_text(acumulador)

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
