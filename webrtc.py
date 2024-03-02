# Import necessary modules
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Serve static files (e.g., HTML, CSS, JS) from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Use Jinja2 for HTML templates
templates = Jinja2Templates(directory="templates")

# HTML template for the video chat
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# WebSocket connection for WebRTC signaling
class VideoChatWebSocket(WebSocket):
    async def on_connect(self, websocket):
        await websocket.accept()

    async def on_receive(self, websocket, data):
        await websocket.send_text(f"Message text was: {data}")

# WebSocket endpoint for video chat
@app.websocket("/ws")
async def video_chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
