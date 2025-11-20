from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from schemas import MenuItem, Event, GalleryItem, Booking, OpeningHours
from database import db, create_document, get_documents

app = FastAPI(title="The Sycamore Inn API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
async def test():
    # Quick DB test - list collections
    try:
        collections = await db.list_collection_names()
        return {"status": "ok", "collections": collections}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Seed default content route (idempotent)
@app.post("/seed")
async def seed_content():
    # Add a few default menu items, events, gallery images, opening hours
    now = datetime.utcnow()
    sample_menu = [
        MenuItem(name="Sunday Roast", description="Roast beef, Yorkshire pudding, seasonal veg, rich gravy.", price=15.95, category="Food", image_url="https://images.unsplash.com/photo-1604908176997-431206b7b42f"),
        MenuItem(name="Fish & Chips", description="Beer-battered cod, thick-cut chips, mushy peas.", price=13.50, category="Food", image_url="https://images.unsplash.com/photo-1558036117-15d82a90b9b9"),
        MenuItem(name="Cask Ale Pint", description="Rotating selection of local bitters and ales.", price=4.80, category="Drinks", image_url="https://images.unsplash.com/photo-1541343672885-9be56236302a"),
    ]
    sample_events = [
        Event(title="Pub Quiz Night", description="Test your knowledge every Thursday 8pm.", date=now, is_recurring=True, tags=["quiz", "community"], image_url="https://images.unsplash.com/photo-1529400971008-f566de0e6dfc"),
        Event(title="Sunday Roast Special", description="Traditional roasts served all day Sunday.", date=now, is_recurring=True, tags=["food", "sunday"], image_url="https://images.unsplash.com/photo-1511690656952-34342bb7c2f2"),
    ]
    sample_gallery = [
        GalleryItem(title="The Bar", image_url="https://images.unsplash.com/photo-1541534401786-2077eed87a72", category="Bar"),
        GalleryItem(title="Cosy Corner", image_url="https://images.unsplash.com/photo-1512917774080-9991f1c4c750", category="Interior"),
        GalleryItem(title="Steak & Chips", image_url="https://images.unsplash.com/photo-1544025162-d76694265947", category="Food"),
    ]
    opening_hours = [
        OpeningHours(day="Monday", open="12:00", close="23:00", kitchen_close="21:00"),
        OpeningHours(day="Tuesday", open="12:00", close="23:00", kitchen_close="21:00"),
        OpeningHours(day="Wednesday", open="12:00", close="23:00", kitchen_close="21:00"),
        OpeningHours(day="Thursday", open="12:00", close="23:30", kitchen_close="21:30"),
        OpeningHours(day="Friday", open="12:00", close="00:00", kitchen_close="22:00"),
        OpeningHours(day="Saturday", open="11:00", close="00:00", kitchen_close="22:00"),
        OpeningHours(day="Sunday", open="11:00", close="22:30", kitchen_close="20:30"),
    ]

    # Insert if collections are empty
    for item in sample_menu:
        await create_document("menuitem", item.model_dump())
    for ev in sample_events:
        await create_document("event", ev.model_dump())
    for gi in sample_gallery:
        await create_document("galleryitem", gi.model_dump())
    for oh in opening_hours:
        await create_document("openinghours", oh.model_dump())

    return {"status": "seeded"}


# Public read endpoints
@app.get("/menu", response_model=List[MenuItem])
async def get_menu(category: Optional[str] = None):
    filter_dict = {"category": category} if category else {}
    docs = await get_documents("menuitem", filter_dict)
    # Convert price to float in case
    return [MenuItem(**d) for d in docs]


@app.get("/events", response_model=List[Event])
async def get_events():
    docs = await get_documents("event", {})
    return [Event(**d) for d in docs]


@app.get("/gallery", response_model=List[GalleryItem])
async def get_gallery():
    docs = await get_documents("galleryitem", {})
    return [GalleryItem(**d) for d in docs]


@app.get("/hours", response_model=List[OpeningHours])
async def get_hours():
    docs = await get_documents("openinghours", {})
    return [OpeningHours(**d) for d in docs]


# Booking endpoint
@app.post("/book")
async def create_booking(booking: Booking):
    await create_document("booking", booking.model_dump())
    return {"status": "received"}
