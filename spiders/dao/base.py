# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqldb://tutturu:1@localhost/indexing_schema')

Session = sessionmaker(bind=engine)

Base = declarative_base()