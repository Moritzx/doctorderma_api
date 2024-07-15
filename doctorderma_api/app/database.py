"""
This file contains the code for connecting and interacting with the local PostgreSQL database.
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# replace with your own PostgreSQL database URL
DATABASE_URL = "postgresql://postgres:apricot@localhost:5432/arxiv_db"

# sqlalchemy engine for connecting to database
engine = create_engine(DATABASE_URL)

# session to interact with database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()   # needed for defining models (tables)


# create a table for arxiv papers with columns id, title, summary and link
class ArxivPaper(Base):
    __tablename__ = "arxiv_papers"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    summary = Column(Text)
    link = Column(String)


# create a table for logging query_start_time and query_end_time for each query
class QueryLog(Base):
    __tablename__ = "query_logs"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    query_start_time = Column(DateTime, default=datetime.utcnow)
    query_end_time = Column(DateTime)


# initialize database
def init_db():
    Base.metadata.create_all(bind=engine)
