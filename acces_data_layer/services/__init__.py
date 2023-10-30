from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/speaker_verification', echo=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
