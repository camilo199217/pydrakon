from sqlmodel import Session, SQLModel, create_engine
from sandbox.settings import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
