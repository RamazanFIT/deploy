from fastapi import Cookie, FastAPI, Form, Request, Response, templating, HTTPException, Depends
from fastapi.responses import RedirectResponse
from .flowers_repository import Flowers, FlowersRepository, FlowerRequest
from .purchases_repository import Purchase, PurchasesRepository
from .users_repository import UserRequest, UsersRepository, UserResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.post("/signup", response_model=UserResponse)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
def signup_save(
    user : UserRequest,
    db : Session = Depends(get_db)
    ):
    user = users_repository.create_user(
        db, user
    )
    return user
    
@app.post("/login")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
def login(
    response : Response,
    username : str = Form(),
    password : str = Form(),
    db : Session = Depends(get_db)
    ):
    tmp = users_repository.get_user_by_email(db, username)
    if tmp != None and tmp.password == password:
        shifr_email = users_repository.encode_email(username)
        return {'access_token': shifr_email, 'type': 'bearer'}
    raise HTTPException(status_code=401, detail="Incorrect login or password")

@app.get("/profile", response_model=UserResponse)
def profile(
    token : str = Depends(oauth2_scheme),
    db : Session = Depends(get_db)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(db, email["email"])
    if user != None:
        return user
    raise HTTPException(status_code=401, detail="Not authorized")


@app.post("/flowers")
def add_flowers(
    flower : FlowerRequest,
    token : str = Depends(oauth2_scheme),
    db : Session = Depends(get_db)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(db, email["email"])
    if user != None:
        flower = flowers_repository.add_flower(db, flower)
        return {
            "flower_id" : flower.id
        }
    raise HTTPException(status_code=401, detail="Not authorized")
    
    
@app.get("/flowers")
def shop(
    token : str = Depends(oauth2_scheme),
    db : Session = Depends(get_db)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(db, email["email"])
    if user != None:
        flowers = flowers_repository.get_all_flowers(db=db)
        return flowers
    raise HTTPException(status_code=401, detail="Not authorized")
    
@app.delete("/flowers/{flower_id}")
def del_flower(
    flower_id : int,
    token : str = Depends(oauth2_scheme),
    db : Session = Depends(get_db)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(db, email["email"])
    if user != None:
        flowers_repository.delete_flower(db, flower_id)
        return {
            "deleted_flower_id" : flower_id
        }
    raise HTTPException(status_code=401, detail="Not authorized")

@app.patch("/flowers/{flower_id}")
def change_flower(
    flower_id : int,
    new_flower : FlowerRequest,
    token : str = Depends(oauth2_scheme),
    db : Session = Depends(get_db)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(db, email["email"])
    if user != None:
        flowers_repository.update_flower(db, flower_id, new_flower)
        return Response("Succeessfully updated")
        
    raise HTTPException(status_code=401, detail="Not authorized")
    

@app.post("/cart/items")
def cart_items(
    response : Response,
    id : int = Form(),
    how_much : int = Form(),
    cart : str = Cookie(default="[]"),
    token : str = Depends(oauth2_scheme),
    db : Session = Depends(get_db)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(db, email["email"])
    if user != None:
        some_dict = flowers_repository.create_dict(id, how_much)
        list_ = flowers_repository.get_python_code(cart)
        set_ = set()
        for i in list_:
            set_.add(i["id"])
        if id in set_:
            for i in range(len(list_)):
                if list_[i]["id"] == id:
                    list_[i]["how_much"] += how_much
        else:
            list_.append(some_dict)
        flowers_repository.change_cnt(db, id, how_much)
        json_str = flowers_repository.get_json_str(list_)
        ans = Response()
        ans.set_cookie("cart", json_str)
        return ans
    raise HTTPException(status_code=401, detail="Not authorized")

@app.get("/cart/items")
def cart_items(
    cart : str = Cookie(default="[]"),
    token : str = Depends(oauth2_scheme),
    db : Session = Depends(get_db)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(db, email["email"])
    if user != None:
        list_flowers = flowers_repository.get_python_code(cart)
        cartt = []
        total_cost = 0
        for i in list_flowers:
            cartt.append(
                {
                    "Name of Flower" : flowers_repository.get_flower(db, i["id"]).name,
                    "Count" : i["how_much"],
                    "Cost" : i["how_much"] * flowers_repository.get_flower(db, i["id"]).cost
                }
            )
            total_cost += cartt[-1]["Cost"]
        return [cartt, {"total_cost:" : total_cost}]
    raise HTTPException(status_code=401, detail="Not authorized")
    
@app.post("/purchased")
def purchased(
    response : Response,
    cart : str = Cookie(default="[]"),
    token : str = Depends(oauth2_scheme),
    db : Session = Depends(get_db)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(db, email["email"])
    purchases_repository.add_purchase(db, cart, user.id)
    ans = Response()
    ans.set_cookie("cart", "[]")
    return ans

@app.get("/purchased")
def purchased(
    request : Request,
    token : str = Depends(oauth2_scheme),
    db : Session = Depends(get_db)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(db, email["email"])
    list_purch = flowers_repository.get_python_code(purchases_repository.get_user_purchases(db, user.id).flowers)
    
    purch = []
    for i in list_purch:
        purch.append(
            {
                "Name of the Flower" : flowers_repository.get_flower(db, i["id"]).name,
                "Count" : i["how_much"],
                "Cost" : i["how_much"] * flowers_repository.get_flower(db, i["id"]).cost
            }
        )
    return purch
      