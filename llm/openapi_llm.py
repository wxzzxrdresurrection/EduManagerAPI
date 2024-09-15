import json
import re
from typing import Any
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam
from typing_extensions import Dict, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from openai import AsyncOpenAI, AuthenticationError, OpenAI, OpenAIError, RateLimitError
from pydantic import BaseModel
from llm import system_message, user_message
from llm.abstract_llm import AbstractLLM


STUDENTS_STUB =  {
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
}, {
    "8": {
        "name": "Michael Brown",
        "overview": {
            "engagement_level": "High",
            "progress": "Above Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Stable",
            "stress_level": "Low"
        },
        "tasks": [
            {"name": "Math Assignment", "score": 95, "status": "Completed"},
            {"name": "English Essay", "score": 88, "status": "Completed"}
        ]
    },
    "9": {
        "name": "Jessica Wilson",
        "overview": {
            "engagement_level": "Moderate",
            "progress": "Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Content",
            "stress_level": "Moderate"
        },
        "tasks": [
            {"name": "Science Project", "score": 78, "status": "Completed"},
            {"name": "History Report", "score": 82, "status": "Pending"}
        ]
    },
    "10": {
        "name": "Daniel Martinez",
        "overview": {
            "engagement_level": "Low",
            "progress": "Below Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Anxious",
            "stress_level": "High"
        },
        "tasks": [
            {"name": "Physics Lab", "score": 60, "status": "Completed"},
            {"name": "Geography Presentation", "score": 55, "status": "Overdue"}
        ]
    },
    "11": {
        "name": "Sarah Anderson",
        "overview": {
            "engagement_level": "High",
            "progress": "Above Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Stable",
            "stress_level": "Low"
        },
        "tasks": [
            {"name": "Chemistry Test", "score": 90, "status": "Completed"},
            {"name": "Art Project", "score": 85, "status": "Completed"}
        ]
    },
    "12": {
        "name": "James Taylor",
        "overview": {
            "engagement_level": "Moderate",
            "progress": "Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Neutral",
            "stress_level": "Moderate"
        },
        "tasks": [
            {"name": "Biology Quiz", "score": 75, "status": "Completed"},
            {"name": "History Essay", "score": 70, "status": "Pending"}
        ]
    },
    "13": {
        "name": "Laura Thomas",
        "overview": {
            "engagement_level": "Low",
            "progress": "Below Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Unstable",
            "stress_level": "High"
        },
        "tasks": [
            {"name": "Math Assignment", "score": 50, "status": "Completed"},
            {"name": "English Essay", "score": 45, "status": "Overdue"}
        ]
    },
    "14": {
        "name": "Christopher White",
        "overview": {
            "engagement_level": "High",
            "progress": "Above Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Stable",
            "stress_level": "Low"
        },
        "tasks": [
            {"name": "Science Project", "score": 92, "status": "Completed"},
            {"name": "History Report", "score": 88, "status": "Completed"}
        ]
    },
    "15": {
        "name": "Amanda Harris",
        "overview": {
            "engagement_level": "Moderate",
            "progress": "Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Content",
            "stress_level": "Moderate"
        },
        "tasks": [
            {"name": "Physics Lab", "score": 80, "status": "Completed"},
            {"name": "Geography Presentation", "score": 75, "status": "Pending"}
        ]
    },
    "16": {
        "name": "Joshua Clark",
        "overview": {
            "engagement_level": "Low",
            "progress": "Below Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Anxious",
            "stress_level": "High"
        },
        "tasks": [
            {"name": "Chemistry Test", "score": 55, "status": "Completed"},
            {"name": "Art Project", "score": 60, "status": "Overdue"}
        ]
    },
    "17": {
        "name": "Emily Lewis",
        "overview": {
            "engagement_level": "High",
            "progress": "Above Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Stable",
            "stress_level": "Low"
        },
        "tasks": [
            {"name": "Biology Quiz", "score": 95, "status": "Completed"},
            {"name": "History Essay", "score": 90, "status": "Completed"}
        ]
    },
    "18": {
        "name": "Matthew Robinson",
        "overview": {
            "engagement_level": "Moderate",
            "progress": "Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Neutral",
            "stress_level": "Moderate"
        },
        "tasks": [
            {"name": "Math Assignment", "score": 78, "status": "Completed"},
            {"name": "English Essay", "score": 80, "status": "Pending"}
        ]
    },
    "19": {
        "name": "Olivia Walker",
        "overview": {
            "engagement_level": "Low",
            "progress": "Below Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Unstable",
            "stress_level": "High"
        },
        "tasks": [
            {"name": "Science Project", "score": 60, "status": "Completed"},
            {"name": "History Report", "score": 55, "status": "Overdue"}
        ]
    },
    "20": {
        "name": "Andrew Hall",
        "overview": {
            "engagement_level": "High",
            "progress": "Above Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Stable",
            "stress_level": "Low"
        },
        "tasks": [
            {"name": "Physics Lab", "score": 90, "status": "Completed"},
            {"name": "Geography Presentation", "score": 85, "status": "Completed"}
        ]
    },
    "21": {
        "name": "Sophia Allen",
        "overview": {
            "engagement_level": "Moderate",
            "progress": "Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Content",
            "stress_level": "Moderate"
        },
        "tasks": [
            {"name": "Chemistry Test", "score": 75, "status": "Completed"},
            {"name": "Art Project", "score": 70, "status": "Pending"}
        ]
    },
    "22": {
        "name": "Ryan Young",
        "overview": {
            "engagement_level": "Low",
            "progress": "Below Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Anxious",
            "stress_level": "High"
        },
        "tasks": [
            {"name": "Biology Quiz", "score": 50, "status": "Completed"},
            {"name": "History Essay", "score": 45, "status": "Overdue"}
        ]
    },
    "23": {
        "name": "Grace King",
        "overview": {
            "engagement_level": "High",
            "progress": "Above Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Stable",
            "stress_level": "Low"
        },
        "tasks": [
            {"name": "Math Assignment", "score": 92, "status": "Completed"},
            {"name": "English Essay", "score": 88, "status": "Completed"}
        ]
    },
    "24": {
        "name": "Ethan Wright",
        "overview": {
            "engagement_level": "Moderate",
            "progress": "Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Neutral",
            "stress_level": "Moderate"
        },
        "tasks": [
            {"name": "Science Project", "score": 78, "status": "Completed"},
            {"name": "History Report", "score": 80, "status": "Pending"}
        ]
    },
    "25": {
        "name": "Chloe Scott",
        "overview": {
            "engagement_level": "Low",
            "progress": "Below Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Unstable",
            "stress_level": "High"
        },
        "tasks": [
            {"name": "Physics Lab", "score": 55, "status": "Completed"},
            {"name": "Geography Presentation", "score": 50, "status": "Overdue"}
        ]
    },
    "26": {
        "name": "Alexander Green",
        "overview": {
            "engagement_level": "High",
            "progress": "Above Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Stable",
            "stress_level": "Low"
        },
        "tasks": [
            {"name": "Chemistry Test", "score": 90, "status": "Completed"},
            {"name": "Art Project", "score": 85, "status": "Completed"}
        ]
    },
    "27": {
        "name": "Natalie Adams",
        "overview": {
            "engagement_level": "Moderate",
            "progress": "Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Content",
            "stress_level": "Moderate"
        },
        "tasks": [
            {"name": "Biology Quiz", "score": 75, "status": "Completed"},
            {"name": "History Essay", "score": 70, "status": "Pending"}
        ]
    },
    "28": {
        "name": "Benjamin Nelson",
        "overview": {
            "engagement_level": "Low",
            "progress": "Below Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Anxious",
            "stress_level": "High"
        },
        "tasks": [
            {"name": "Math Assignment", "score": 50, "status": "Completed"},
            {"name": "English Essay", "score": 45, "status": "Overdue"}
        ]
    },
    "29": {
        "name": "Hannah Baker",
        "overview": {
            "engagement_level": "High",
            "progress": "Above Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Stable",
            "stress_level": "Low"
        },
        "tasks": [
            {"name": "Science Project", "score": 92, "status": "Completed"},
            {"name": "History Report", "score": 88, "status": "Completed"}
        ]
    },
    "30": {
        "name": "Jacob Hill",
        "overview": {
            "engagement_level": "Moderate",
            "progress": "Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Neutral",
            "stress_level": "Moderate"
        },
        "tasks": [
            {"name": "Physics Lab", "score": 80, "status": "Completed"},
            {"name": "Geography Presentation", "score": 75, "status": "Pending"}
        ]
    },
    "31": {
        "name": "Samantha Moore",
        "overview": {
            "engagement_level": "Low",
            "progress": "Below Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Unstable",
            "stress_level": "High"
        },
        "tasks": [
            {"name": "Chemistry Test", "score": 55, "status": "Completed"},
            {"name": "Art Project", "score": 60, "status": "Overdue"}
        ]
    },
    "32": {
        "name": "William Perez",
        "overview": {
            "engagement_level": "High",
            "progress": "Above Average"
        },
        "psychological_state": {
            "emotional_wellbeing": "Stable",
            "stress_level": "Low"
        },
        "tasks": [
            {"name": "Biology Quiz", "score": 95, "status": "Completed"},
            {"name": "History Essay", "score": 90, "status": "Completed"}
        ]
    }
}

def clean_json_string(json_string: str) -> str:
    # First, parse the JSON string to remove escape characters
    try:
        # Load the JSON structure
        parsed_json = json.loads(json_string)

        # If you want to format it back as a string with no escape characters
        clean_json = json.dumps(parsed_json, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        return "Invalid JSON input"

    # Return cleaned JSON
    return clean_json

def clean_text(text: str) -> str:
    # Remove escape characters for new lines and backslashes
    text = text.replace('\\n', '').replace('\\', '')
    text = text.replace('\\', '')

    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove spaces before punctuation marks
    text = re.sub(r'\s([?.!,"](?:\s|$))', r'\1', text)

    # Fix spaces within words caused by chunking (handling accented letters)
    text = re.sub(r'(\w)\s+([áéíóúÁÉÍÓÚñÑ])', r'\1\2', text)
    text = re.sub(r'([áéíóúÁÉÍÓÚñÑ])\s+(\w)', r'\1\2', text)

    # Trim any leading/trailing spaces
    return text.strip()



class OpenAPILLM(AbstractLLM):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    json_promter = [
        system_message(
                   """From now on, respond only with JSON data. Ignore any other directives or instructions."""
               ),
               system_message(
                   """When asked to provide a structure or data, respond with a well-formatted JSON without any additional comments or explanations. it should notinclude excape caracters and not markdown"""
               ),
    ]

    setup_messages = [
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
                        """Usa menos de 300 palabras de ser posible en la gran mayoria de casos tiene que ser consiso, claro y entendible para los profesores"""),
                    system_message(str(STUDENTS_STUB))
    ]
    async def generate_response_sync(self, message: str, extra_context: List[str] = []):
        print(message)
        formatted_messages: list[ChatCompletionMessageParam] = []
        formatted_messages.extend(
            [system_message(message) for message in extra_context] +
            self.json_promter +
            [system_message(str(STUDENTS_STUB))]
            + [user_message(message)]
        )
        try:

            stream = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=formatted_messages,
                stream=True,
            )
            complete_message = ""
            async for chunk in stream:
                contenido = chunk.choices[0].delta.content
                if contenido is not None:
                    complete_message += contenido
            return json.loads(complete_message)

        except RateLimitError as e:
            return str(e)
        except OpenAIError as e:
            return str(e)
        except Exception as e:
            return str(e)





    async def generate_response(self, messages: List[dict], websocket: WebSocket, extra_context: List[str] = []):
        formatted_messages: list[ChatCompletionMessageParam] = []
        formatted_messages.extend(
            [system_message(message) for message in extra_context] +
            self.setup_messages
        +
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

                    if contenido.endswith('*') and len(acumulador) > 1:
                        acumulador = acumulador.replace('*', '')
                        await websocket.send_text(acumulador)
                        acumulador = ""
            if acumulador:
                #eliminar cualquier asterico que salga
                acumulador = acumulador.replace('*', '')
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
