from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi_pagination import add_pagination

from config import ORIGINS
from src.config import DEBUG
from src.database.db_config import get_session
from src.on_start.create_default_admin import create_admin_user
from src.auth.router import router as auth_router


@asynccontextmanager
async def lifespan(app1: FastAPI):
    if DEBUG:
        async for db_session in get_session():
            await create_admin_user(db_session)
            await db_session.flush()
            await db_session.commit()
    yield

app = FastAPI(
    root_path="/api",  # This should match your API base URL
    openapi_url="/openapi.json",
    title="moscow_bt",
    version="1.0.0",
    openapi_version="3.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

add_pagination(app)
