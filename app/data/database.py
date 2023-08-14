from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Base

engine = create_engine('sqlite:///data//data.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
