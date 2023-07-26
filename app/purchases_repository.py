from attrs import define
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship
from .database import Base
from pydantic import BaseModel
from .flowers_repository import FlowersRepository

flower_repo = FlowersRepository()
class Purchase(Base):
    __tablename__ = "purchases"
    user_id = Column(Integer, primary_key = True)
    flowers = Column(String, default = "[]")
    # owner = relationship("Users", back_populates = "purchases")

class PurchasesRepository:
    def get_user_purchases(self, db : Session, user_id : int):
        purchases = db.query(Purchase).filter(Purchase.user_id == user_id).first()
        return purchases
    
    def add_purchase(self, db : Session, cart : str, user_id : int):
        old_cart = self.get_user_purchases(db, user_id)
        if old_cart != None:
            old_cart_code = flower_repo.get_python_code(old_cart.flowers)
            cart_code = flower_repo.get_python_code(cart)
            old_cart_code += cart_code
            old_cart_json = flower_repo.get_json_str(old_cart_code)
            old_cart.flowers = old_cart_json
            db.commit()
        else:
            purch = Purchase(user_id = user_id, flowers = cart)
            db.add(purch)
            db.commit()
            
            
        
        