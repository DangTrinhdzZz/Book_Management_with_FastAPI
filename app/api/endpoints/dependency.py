#mỗi lần muốn sử dụng database thì phải import cái này vào
from typing import Generator
from app.database.session import sessionLocal

def get_db() -> Generator:
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()