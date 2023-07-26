import jwt
from pydantic import BaseModel
from attrs import define
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship
from database import Base

class UserRequest(BaseModel):
    email: str
    name : str
    surname : str
    password : str

class UserResponse(BaseModel):
    email: str
    name : str
    surname : str
    id: int = 0
    
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    # purchases = relationship("Purchase", back_populates = "owner")

class UsersRepository:
    def create_user(self, db : Session, user : UserRequest) -> UserRequest:
        user = Users(email = user.email, name = user.name, surname = user.surname, password = user.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_user_by_email(self, db : Session,  email : str) -> Users:
        return db.query(Users).filter(Users.email == email).first()
        
    def encode_email(self, email) -> str:
        key = "Ramazan_the_best"
        algorithm = "HS256"
        shifr_email = jwt.encode(payload={"email" : email}, key=key, algorithm=algorithm)
        return shifr_email

    def decode_token(self, token) -> dict:
        key = "Ramazan_the_best"
        algorithm = "HS256"
        email = jwt.decode(jwt=token, key=key, algorithms=algorithm)
        return email
                                                                                                                                                                                                                                                                                                    