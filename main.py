from contextlib import asynccontextmanager
from datetime import datetime, timezone
from random import randint
from typing import Annotated, Any, Generic, TypeVar
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, create_engine, Session, select, Field

class Campaign(SQLModel, table=True):
    campaign_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    date: datetime | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=True, index=True)

class CampaignCreate(SQLModel):
    name: str
    date: datetime | None

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan (app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        has_any_campaign = session.exec(select(Campaign).limit(1)).first() is not None
        if not has_any_campaign:
            now = datetime.now(timezone.utc)
            session.add_all(
                [
                    Campaign(name="Summer Launch", date=now),
                    Campaign(name="Black Friday", date=now),
                ]
            )
            session.commit()
    yield

app = FastAPI(root_path="/api/v1", lifespan=lifespan)

T = TypeVar("T")
class ApiResponse(BaseModel, Generic[T]):
    data: T

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/campaigns", response_model=ApiResponse[list[Campaign]])
async def read_campaings(session: SessionDep):
    data = session.exec(select(Campaign)).all()

    return {"data": data}

@app.get("/campaigns/{id}", response_model=ApiResponse[Campaign])
async def read_campaign(id: int, session: SessionDep):
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404)
    
    return {"data": data}

@app.post("/campaigns", status_code=201, response_model=ApiResponse[CampaignCreate])
async def create_campaign(campaign: CampaignCreate, session: SessionDep):
    db_campaign = Campaign.model_validate(campaign)
    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)

    return{"data": campaign}

# @app.put(f"/campaigns/{id}")
# async def update_campaign(id: int,body: dict[str, Any]):
#     for i, campaign in enumerate(data):
#         if campaign.get["campaign_id"] == id:
#             updated : Any = {
#                 "campaign_id": id,
#                 "name": body.get("name"),
#                 "due_date": body.get("due_date"),
#                 "created_at": campaign.get["created_at"],
#             },

#             data[i] = updated

#             return {"campaign": updated, "message": "Campaign updated!"}
#     raise HTTPException(status_code=404, detail="Campaign not found")

# @app.delete(f"/campaigns/{id}")
# async def delete_campaign(id: int,body: dict[str, Any]):
#     for i, campaign in enumerate(data):
#         if campaign.get["campaign_id"] == id:
#             data.pop(i)

#             return Response(status_code=204)
#     raise HTTPException(status_code=404, detail="Campaign not found")

