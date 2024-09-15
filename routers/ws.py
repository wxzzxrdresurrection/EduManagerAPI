import os
from fastapi.requests import Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocket, WebSocketDisconnect
import json

from starlette.responses import HTMLResponse

from llm.openapi_llm import OpenAPILLM

ws_router = APIRouter()
templates = Jinja2Templates(directory="templates")
apiKey = os.getenv("OPENAI_API_KEY")
if apiKey is None:
    raise ValueError("OPENAI_API_KEY is not set")

llm = OpenAPILLM(api_key=apiKey)


@ws_router.get("/test", response_class=HTMLResponse)
async def test_ws(request: Request):
    url = os.getenv("APP_URL", "localhost")
    return templates.TemplateResponse("test_ws.html", {"request": request, "url": url})

@ws_router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    prompt = "Resumen destacable del aula, puedes mencionar rendimiento general, quien destaca para bien o para mal"
    context = {
        "type": "user",
        "content": prompt
    }
    await llm.generate_response([context], websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            message = json.loads(data)
            if message["type"] == "message":
                print(message["content"])
                await llm.generate_response(message["content"], websocket)
    except WebSocketDisconnect:
        print("Client disconnected")
