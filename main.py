from typing import List

from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)


class ChatUser(Base):
    __tablename__ = "chat_users"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace * with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id in self.connections:
            self.connections[user_id].append(websocket)
        else:
            self.connections[user_id] = [websocket]

    def disconnect(self, user_id: int, websocket: WebSocket):
        self.connections[user_id].remove(websocket)
        if not self.connections[user_id]:
            del self.connections[user_id]

    async def send_personal_message(self, user_id: int, message: str):
        if user_id in self.connections:
            for connection in self.connections[user_id]:
                await connection.send_text(message)

    async def broadcast(self, message: str):
        for connection_list in self.connections.values():
            for connection in connection_list:
                await connection.send_text(message)


manager = ConnectionManager()


# WebSocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: int, websocket: WebSocket):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(user_id, data)
    except WebSocketDisconnect as e:
        manager.disconnect(user_id, websocket)
        await manager.broadcast(f"User {user_id} left the chat")


# Routes implementation
@app.get("/chat-app/chats")
def get_user_chats(user_id: int = Depends(get_db)):
    user_chats = user_id.query(Chat).all()
    return user_chats


@app.get("/chat-app/chats/users")
def get_available_users(user_id: int = Depends(get_db)):
    available_users = user_id.query(User).all()
    return available_users


@app.post("/chat-app/chats/c/{receiver_id}")
def create_or_get_one_on_one_chat(
    user_id: int, receiver_id: int, db: Session = Depends(get_db)
):
    # Implement logic to create or get a one-on-one chat
    pass


@app.delete("/chat-app/chats/remove/{chat_id}")
def delete_one_on_one_chat(chat_id: int, db: Session = Depends(get_db)):
    # Implement logic to delete a one-on-one chat
    pass


@app.post("/chat-app/chats/group")
def create_group_chat(
    user_id: int,
    participants: List[int],
    group_name: str,
    db: Session = Depends(get_db),
):
    # Implement logic to create a group chat
    pass


@app.get("/chat-app/chats/group/{chat_id}")
def get_group_chat_details(chat_id: int, db: Session = Depends(get_db)):
    # Implement logic to get group chat details
    pass


@app.delete("/chat-app/chats/group/{chat_id}")
def delete_group_chat(chat_id: int, db: Session = Depends(get_db)):
    # Implement logic to delete a group chat
    pass


@app.patch("/chat-app/chats/group/{chat_id}")
def update_group_chat_name(chat_id: int, new_name: str, db: Session = Depends(get_db)):
    # Implement logic to update group chat name
    pass


@app.post(
    "/chat-app/chats/group/{chat_id}/{participant_id}"
)
def add_participant_to_group(
    chat_id: int, participant_id: int, db: Session = Depends(get_db)
):
    # Implement logic to add a participant to a group chat
    pass


@app.delete(
    "/chat-app/chats/group/{chat_id}/{participant_id}"
)
def remove_participant_from_group(
    chat_id: int, participant_id: int, db: Session = Depends(get_db)
):
    # Implement logic to remove a participant from a group chat
    pass


@app.delete("/chat-app/chats/leave/group/{chat_id}")
def leave_group_chat(chat_id: int, db: Session = Depends(get_db)):
    # Implement logic to leave a group chat
    pass


@app.get("/chat-app/messages/{chat_id}")
def get_all_messages(chat_id: int, db: Session = Depends(get_db)):
    # Implement logic to get all messages for a chat
    pass


@app.post("/chat-app/messages/{chat_id}")
def send_message(
    chat_id: int, sender_id: int, message: str, db: Session = Depends(get_db)
):
    # Implement logic to send a message to a chat
    pass
