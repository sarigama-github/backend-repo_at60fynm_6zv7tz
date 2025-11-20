import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic.json import pydantic_encoder

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client = AsyncIOMotorClient(DATABASE_URL)
db = _client[DATABASE_NAME]


def _collection_name(raw: str) -> str:
    # Ensure collection names are safe and lowercase
    return raw.lower()


async def create_document(collection_name: str, data: Dict[str, Any]) -> str:
    col = db[_collection_name(collection_name)]
    payload = dict(data)
    now = datetime.utcnow()
    if "created_at" not in payload:
        payload["created_at"] = now
    payload["updated_at"] = now
    # Ensure JSON serializable
    for k, v in list(payload.items()):
        if hasattr(v, "model_dump"):
            payload[k] = v.model_dump()
    res = await col.insert_one(payload)
    return str(res.inserted_id)


async def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
    col = db[_collection_name(collection_name)]
    cursor = col.find(filter_dict or {}).limit(limit)
    docs: List[Dict[str, Any]] = []
    async for d in cursor:
        d.pop("_id", None)
        docs.append(d)
    return docs
