import os
from fastapi import FastAPI, Request
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from dotenv import load_dotenv

from llm.openapi_llm import OpenAPILLM

load_dotenv()

app = FastAPI()


templates = Jinja2Templates(directory="templates")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("API key is not set")

llm = OpenAPILLM(api_key=api_key)


@app.get("/")
async def root():
    return {"message": "Hello Worldss"}

@app.get("/test/ws", response_class=HTMLResponse)
async def test_ws(request: Request):
    return templates.TemplateResponse("test_ws.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    context = "Welcome! Here's an overview of your students: [Your students' overview here]"
    await websocket.send_text(json.dumps({"type": "context", "content": context}))

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("APP_URL", "localhost"), port=8000)
