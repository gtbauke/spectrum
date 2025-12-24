from sqlmodel import create_engine

from config import Config

engine = create_engine(url=Config.DATABASE_URL, echo=True)
