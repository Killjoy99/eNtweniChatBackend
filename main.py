from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import secrets
import json
from datetime import datetime

from models import Base, User, Message
from database import get_session

app = FastAPI()


@app.get("/")
def index():
    return HTMLResponse(open("index.html").read())

@app.get("about/")
def about():
    return HTMLResponse(open("about.html").read())

@app.websocket("/chat")
async def eNtweniChatAppEndpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        try:
            data = await websocket.receive_json()
            
            if "action" in data:
                if data["action"] == "register":
                    await register_new_user(websocket, data)
                elif data["action"] == "get_new_messages":
                    last_received_message_id = data.get("last_received_message_id")
                    new_messages = await get_new_messages(data["phone_number"], last_received_message_id)
                    if new_messages:
                        await websocket.send_json(new_messages)
                elif data["action"] == "get_user_messages":
                    messages = await get_user_messages(data["phone_number"])
                    if messages:
                        await websocket.send_json(messages)
                    else:
                        await websocket.send_json({"data": "No new messages found"})
                elif data["action"] == "send_message":
                    await send_message(data["message"])
            else:
                await websocket.send_text("No command found.")
        except WebSocketDisconnect:
            websocket.close()

async def register_new_user(websocket, data):
    session = next(get_session())
    phone_number = data.get("phone_number")

    user = session.query(User).filter(User.phone_number == phone_number).first()
    if user:
        await websocket.send_json({"status": "failed", "message": "Phone number already registered."})
    else:
        new_user = User(phone_number=phone_number, is_registered=True)
        session.add(new_user)
        session.commit()
        await websocket.send_json({"status": "success", "message": "You have been registered successfully."})

    session.close()

# store user messages in the database
async def send_message(data):
    sender = data.get("sender")
    receiver = data.get("receiver")
    content = data.get("content")
    
    session = next(get_session())
    print(sender)
    # check if the user is registered
    user  = session.query(User).filter(User.phone_number == sender, User.is_registered == True).first()
    
    if user:
        message = Message(content=content, sender=sender, receiver=receiver)
        session.add(message)
        session.commit()
        session.close()
    else:
        session.close()
        raise Exception("User is not registered or is unauthorised.")
    
async def get_user_messages(phone_number):
    session = next(get_session())
    user = session.query(User).filter(User.phone_number == phone_number).first()
    
    if user:
        messages = session.query(Message).filter(Message.receiver == user.phone_number).all()
        # Mark messages as read
        for message in messages:
            message.read = True
        session.commit()
        # Serialize messages to JSON format
        serialized_messages = []
        for message in messages:
            serialized_message = {
                "id": message.id,
                "sender": message.sender,
                "receiver": message.receiver,
                "read": message.read,
                "content": message.content,
                "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
            serialized_messages.append(serialized_message)
        
        session.close()
        return serialized_messages
    else:
        session.close()
        return None

async def get_new_messages(phone_number, last_received_message_id):
    session = next(get_session())
    new_messages = session.query(Message).filter(Message.receiver == phone_number, Message.id > last_received_message_id, Message.read == False).all()
    # if there are new messages, mark them as read and return
    if new_messages:
        for message in new_messages:
            message.read = True
    session.commit()
    # Serialize messages to JSON format
    serialized_messages = []
    for message in new_messages:
        serialized_message = {
            "id": message.id,
            "sender": message.sender,
            "receiver": message.receiver,
            "content": message.content,
            "read": message.read,
            "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        serialized_messages.append(serialized_message)
        
    session.close()
    return serialized_messages if new_messages else None

async def generate_auth_token(phone_number):
    token = secrets.token_urlsafe(16)
    return token


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
