# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///links.db')

Session = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()

print 'Init'