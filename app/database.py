from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
from bson import ObjectId
from fastapi import HTTPException

from app.config import MONGO_URL, MONGO_DB


_client: Optional[AsyncIOMotorClient] = None


def get_db_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        if not MONGO_URL or "<user>" in MONGO_URL or "<password>" in MONGO_URL or "<cluster>" in MONGO_URL:
            print("AVISO: MONGO_URL não definida ou contém placeholders. Usando cliente MongoDB local para testes.")
            _client = AsyncIOMotorClient("mongodb://localhost:27017") # Conexão local de fallback
        else:
            _client = AsyncIOMotorClient(MONGO_URL)


    return _client


def get_db():
    client = get_db_client()
    return client[MONGO_DB]




def to_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de mensagem inválido.")

