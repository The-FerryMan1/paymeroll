from app.core.database import SessionLocal


def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
