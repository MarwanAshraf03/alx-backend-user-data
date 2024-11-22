#!/usr/bin/env python3
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from user import User, Base


# Example database engine (e.g., SQLite)
engine = create_engine("sqlite:///example.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create a new User
new_user = User(email="example@example.com", hashed_password="hashed_password")
session.add(new_user)
session.commit()

print(new_user.id)  # This will now show the generated ID