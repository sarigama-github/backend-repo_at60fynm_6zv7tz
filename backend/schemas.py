from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime

# Each model corresponds to a MongoDB collection named after the class in lowercase
# e.g., class Booking -> collection "booking"

class MenuItem(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str  # e.g., "Food", "Drinks"
    image_url: Optional[HttpUrl] = None
    is_featured: bool = False

class Event(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    image_url: Optional[HttpUrl] = None
    is_recurring: bool = False
    tags: List[str] = []

class GalleryItem(BaseModel):
    title: Optional[str] = None
    image_url: HttpUrl
    category: Optional[str] = None  # e.g., "Food", "Bar", "Interior"

class Booking(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    date: datetime
    guests: int = Field(ge=1, le=20)
    notes: Optional[str] = None

class OpeningHours(BaseModel):
    day: str  # e.g., "Monday"
    open: str  # "12:00"
    close: str  # "23:00"
    kitchen_close: Optional[str] = None
