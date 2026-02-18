import datetime
import random
from typing import Any
from fastapi import FastAPI, HTTPException, Request, Response

app = FastAPI(root_path="/api/v1")

data : Any = [
    {
        "campaign_id": 1,
        "name": "Summer Lunch",
        "due_date": datetime.now(),
        "created_at": datetime.now(),
    },
    {
        "campaign_id": 2,
        "name": "Black Friday",
        "due_date": datetime.now(),
        "created_at": datetime.now(),
    },
    {
        "campaign_id": 3,
        "name": "Valentine's Day",
        "due_date": datetime.now(),
        "created_at": datetime.now(),
    },
]

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/campaigns")
async def read_campaings():
    return {"campaigns": data}

@app.get("/campaigns/{id}")
async def read_campaign(id: int):
    for campaign in data:
        if campaign["campaign_id"] == id:
            return {"campaign": campaign}
        raise HTTPException(status_code=404, detail="Campaign not found")

@app.post("/campaigns", status_code=201)
async def create_campaign(body: dict[str, Any]):
    new : Any = {
        "campaign_id": random.randint(3, 100),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": datetime.now(),
    },

    data.append(new)

    return {"campaign": new, "message": "Created!"}

@app.put(f"/campaigns/{id}")
async def update_campaign(id: int,body: dict[str, Any]):
    for i, campaign in enumerate(data):
        if campaign.get["campaign_id"] == id:
            updated : Any = {
                "campaign_id": id,
                "name": body.get("name"),
                "due_date": body.get("due_date"),
                "created_at": campaign.get["created_at"],
            },

            data[i] = updated

            return {"campaign": updated, "message": "Campaign updated!"}
    raise HTTPException(status_code=404, detail="Campaign not found")

@app.delete(f"/campaigns/{id}")
async def delete_campaign(id: int,body: dict[str, Any]):
    for i, campaign in enumerate(data):
        if campaign.get["campaign_id"] == id:
            data.pop(i)

            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Campaign not found")
