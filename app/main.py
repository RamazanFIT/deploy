from fastapi import Cookie, FastAPI, Form, Request, Response, templating, HTTPException, Depends
from fastapi.responses import RedirectResponse
from flowers_repository import Flower, FlowersRepository
from purchases_repository import Purchase, PurchasesRepository
from users_repository import User, UsersRepository
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository()


@app.post("/signup")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
def signup_save(
    user : User
    ):
    user = user.dict()
    user = users_repository.create_user(
        **user
    )
    users_repository.add_user(user)
    return user
    
@app.post("/login")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
def login(
    response : Response,
    username : str = Form(),
    password : str = Form()
    ):
    tmp = users_repository.get_user_by_email(username)
    if tmp != None and tmp.password == password:
        shifr_email = users_repository.encode_email(username)
        return {'access_token': shifr_email, 'type': 'bearer'}
    raise HTTPException(status_code=401, detail="Incorrect login or password")

@app.get("/profile")
def profile(
    token : str = Depends(oauth2_scheme)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(email["email"])
    if user != None:
        return user.dict()
    raise HTTPException(status_code=401, detail="Not authorized")


@app.post("/flowers")
def add_flowers(
    name : str = Form(),
    count : str = Form(),
    cost : str = Form(),
    token : str = Depends(oauth2_scheme)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(email["email"])
    if user != None:
        count = int(count)
        cost = int(cost)
        flower = flowers_repository.create_flower(name=name, count=count, cost=cost)
        flowers_repository.add_flower(flower)
        return {
            "flower_id" : flower.id
        }
    raise HTTPException(status_code=401, detail="Not authorized")
    
    
@app.get("/flowers")
def shop(
    token : str = Depends(oauth2_scheme)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(email["email"])
    if user != None:
        flowers = flowers_repository.get_all_flowers()
        # return flowers 
        flowerss = []
        for i in flowers:
            flowerss.append(flowers_repository.dict(i))
        return flowerss
        
    raise HTTPException(status_code=401, detail="Not authorized")
    
    
    

@app.post("/cart/items")
def cart_items(
    response : Response,
    id : int = Form(),
    how_much : int = Form(),
    cart : str = Cookie(default="[]"),
    token : str = Depends(oauth2_scheme)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(email["email"])
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
        flowers_repository.change_cnt(id, how_much)
        json_str = flowers_repository.get_json_str(list_)
        ans = Response()
        ans.set_cookie("cart", json_str)
        return ans
    raise HTTPException(status_code=401, detail="Not authorized")

@app.get("/cart/items")
def cart_items(
    request : Request,
    cart : str = Cookie(default="[]"),
    token : str = Depends(oauth2_scheme)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(email["email"])
    if user != None:
        list_flowers = flowers_repository.get_python_code(cart)
        cartt = []
        total_cost = 0
        for i in list_flowers:
            cartt.append(
                {
                    "Name of Flower" : flowers_repository.get_flower(i["id"]).name,
                    "Count" : i["how_much"],
                    "Cost" : i["how_much"] * flowers_repository.get_flower(i["id"]).cost
                }
            )
            total_cost += cartt[-1]["Cost"]
        return [cartt, {"total_cost:" : total_cost}]
    raise HTTPException(status_code=401, detail="Not authorized")
    
@app.post("/purchased")
def purchased(
    response : Response,
    cart : str = Cookie(default="[]"),
    token : str = Depends(oauth2_scheme)
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(email["email"])
    list_flowers = flowers_repository.get_python_code(cart)
    purchases_repository.add_purchase(list_flowers, user.id)
    ans = Response()
    ans.set_cookie("cart", "[]")
    return ans

@app.get("/purchased")
def purchased(
    request : Request,
    token : str = Depends(oauth2_scheme),
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(email["email"])
    list_purch = purchases_repository.get_user_purchases(user.id)
    
    purch = []
    for i in list_purch:
        purch.append(
            {
                "Name of the Flower" : flowers_repository.get_flower(i["id"]).name,
                "Count" : i["how_much"],
                "Cost" : i["how_much"] * flowers_repository.get_flower(i["id"]).cost
            }
        )
    return purch
      