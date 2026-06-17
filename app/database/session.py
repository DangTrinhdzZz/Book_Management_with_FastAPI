from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import setting


engine = create_engine(
    setting.SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} if setting.SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
                       )
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)