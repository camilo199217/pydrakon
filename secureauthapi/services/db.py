from fastapi import Request
from sqlmodel import Session


def get_session(request: Request):
    engine = request.app.state.secureauthapi_engine
    return Session(engine)
