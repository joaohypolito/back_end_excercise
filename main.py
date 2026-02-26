from contextlib import asynccontextmanager
from datetime import datetime, timezone
from random import randint
from typing import Annotated, Any, Generic, TypeVar
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, create_engine, Session, select, Field

# Modelo e esquema de banco de dados: representa a tabela de campanhas
# no SQLite usando SQLModel (Pydantic + SQLAlchemy) para mapear os campos
# e garantir validação/serialização automática nas respostas da API.
class Campaign(SQLModel, table=True):
    campaign_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    date: datetime | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=True, index=True)

class CampaignCreate(SQLModel):
    name: str
    date: datetime | None

# Configuração do banco: arquivo SQLite local usado pela aplicação.
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Parâmetros extras do driver SQLite (necessário para uso em apps async).
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependência de sessão com FastAPI: abre uma sessão por requisição e
# garante o fechamento automático após o uso.
def get_session():
    with Session(engine) as session:
        yield session

# Alias de tipo para injeção de dependência, deixando as rotas mais legíveis.
SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
# Ciclo de vida da aplicação: executa lógica de inicialização/encerramento.
# Aqui é usado para criar as tabelas e realizar uma seed inicial de dados
# de forma idempotente (só insere se o banco ainda estiver vazio).
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

# Wrapper genérico de resposta: define um envelope padrão {"data": ...}
# parametrizado pelo tipo T, garantindo consistência nas respostas JSON
# e reaproveitamento do mesmo formato em múltiplos endpoints.
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

@app.put(f"/campaigns/{id}", response_model=Response[Campaign])
async def update_campaign(id: int, campaign: CampaignCreate, session: SessionDep):
    data = session.get(Campaign, id)
    
    if not data:
        raise HTTPException(status_code=404)
    
    data.name = campaign.name
    data.due_date = campaign.due_date
    session.add(data)
    session.commit()
    session.refresh()
    
    return {"data": data}

@app.delete(f"/campaigns/{id}", status_code=204)
async def delete_campaign(id: int, session: SessionDep):
    data = session.get(Campaign, id)
    
    if not data:
        raise HTTPException(status_code=404)
    
    session.delete(data)
    session.commit()
