from contextlib import asynccontextmanager
from typing import Annotated
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.db import get_db, init_db, make_engine, make_session_factory, ping_db


def create_app(settings: Optional[Settings] = None) -> FastAPI:
    settings = settings or get_settings()
    engine = make_engine(settings.database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        init_db(engine)
        yield

    app = FastAPI(title="DocuMind", lifespan=lifespan)
    app.state.SessionLocal = make_session_factory(engine)

    def db_session(request: Request):
        yield from get_db(request.app.state.SessionLocal)

    @app.get("/health")
    def health(session: Annotated[Session, Depends(db_session)]):
        try:
            ping_db(session)
        except SQLAlchemyError as exc:
            raise HTTPException(status_code=503, detail="database unavailable") from exc
        return {"status": "ok", "database": "ok"}

    return app


app = create_app()
