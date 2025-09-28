from typing import List, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, HTTPException, status
from datetime import datetime, timezone

from app.database import get_db, to_object_id
from app.models import MessageIn, MessageOut, Message
from app.ws_manager import manager

router = APIRouter()


@router.get("/rooms/{room}/messages", response_model=List[MessageOut])
async def get_messages(
    room: str,
    limit: int = Query(20, ge=1, le=100),
    before_id: Optional[str] = Query(None, description="ID da mensagem para buscar mensagens anteriores."),
):
    query = {"room": room}
    if before_id:
        query["_id"] = {"$lt": to_object_id(before_id)}

    cursor = get_db()["messages"].find(query).sort("created_at", -1).limit(limit)
    docs = [MessageOut.parse_obj(d) async for d in cursor]
    docs.reverse()
    return docs


@router.post("/rooms/{room}/messages", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def post_message(
    room: str,
    message_in: MessageIn,
):
    if not message_in.content.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mensagem não pode ser vazia.")

    message_data = Message(
        room=room,
        username=message_in.username,
        content=message_in.content,
        created_at=datetime.now(timezone.utc)
    )
    
    res = await get_db()["messages"].insert_one(message_data.dict(by_alias=True, exclude_none=True))
    message_data.id = str(res.inserted_id)
    
    await manager.broadcast(room, {"type": "message", "item": MessageOut.parse_obj(message_data.dict(by_alias=True)).dict(by_alias=True)})
    
    return MessageOut.parse_obj(message_data.model_dump(by_alias=True))


@router.websocket("/ws/{room}")
async def ws_room(websocket: WebSocket, room: str):
    await manager.connect(room, websocket)
    try:
        cursor = get_db()["messages"].find({"room": room}).sort("created_at", -1).limit(20)
        items = [MessageOut.parse_obj(d) async for d in cursor]
        items.reverse()
        await websocket.send_json({"type": "history", "items": [item.dict(by_alias=True) for item in items]})

        while True:
            payload = await websocket.receive_json()
            message_in = MessageIn(username=payload.get("username", "anon"), content=payload.get("content", ""))
            
            if not message_in.content.strip():
                continue

            message_data = Message(
                room=room,
                username=message_in.username,
                content=message_in.content,
                created_at=datetime.now(timezone.utc)
            )
            
            res = await get_db()["messages"].insert_one(message_data.dict(by_alias=True, exclude_none=True))
            message_data.id = str(res.inserted_id)
            
            await manager.broadcast(room, {"type": "message", "item": MessageOut.parse_obj(message_data.dict(by_alias=True)).model_dump(by_alias=True)})

    except WebSocketDisconnect:
        manager.disconnect(room, websocket)
    except Exception as e:
        print(f"Erro no WebSocket: {e}")
        manager.disconnect(room, websocket)

