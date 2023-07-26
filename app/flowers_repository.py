from attrs import define
import json
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship
from .database import Base
from pydantic import BaseModel

class FlowerRequest(BaseModel):
    name : str | None = None
    count : int | None = None
    cost : int | None = None


class Flowers(Base):
    __tablename__ = "flowers"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    count = Column(Integer)
    cost = Column(Integer)


class FlowersRepository:

    def add_flower(self, db : Session, flower : FlowerRequest) -> Flowers:
        flower = Flowers(name = flower.name, count = flower.count, cost = flower.cost)
        db.add(flower)
        db.commit()
        db.refresh(flower)
        return flower

    def get_all_flowers(self, db : Session, skip : int = 0, limit : int = 100) -> Flowers:
        return db.query(Flowers).offset(skip).limit(limit).all()
    
    def delete_flower(self, db : Session, flower_id : int) -> None:
        flower = db.query(Flowers).filter(Flowers.id == flower_id).first()
        db.delete(flower)
        db.commit()
        return None
    
    def update_flower(self, db : Session, flower_id : int, new_flower : FlowerRequest) -> None:
        flower = self.get_flower(db, flower_id)
        if new_flower.name != None:
            flower.name = new_flower.name
        if new_flower.count != None:
            flower.count = new_flower.count
        if new_flower.cost != None:
            flower.cost = new_flower.cost
        db.commit()
        return None
            
    def create_dict(self, id, how_much) -> dict:
        some_dict = {
            "id" : id,
            "how_much" : how_much
        }
        return some_dict

    def get_python_code(self, json_str):
        list_ = json.loads(json_str)
        return list_
    
    def get_json_str(self, dict_):
        json_str = json.dumps(dict_)
        return json_str
    
    def change_cnt(self, db : Session, id : int, how_much : int):
        flower = self.get_flower(db, id)
        flower.count = max(0, flower.count - how_much)
        db.commit()
        
           
    def get_flower(self, db : Session, id : int) -> Flowers:
        flower = db.query(Flowers).filter(Flowers.id == id).first()
        return flower

    