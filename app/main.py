from fastapi import Cookie, FastAPI, Form, Request, Response, templating
from fastapi.responses import RedirectResponse
from flowers_repository import Flower, FlowersRepository
from purchases_repository import Purchase, PurchasesRepository
from users_repository import User, UsersRepository


app = FastAPI()
templates = templating.Jinja2Templates("../templates")


flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository()



@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup")
def signup(request : Request):
    return templates.TemplateResponse(
        "details/signup.html",
        {
            "request" : request
        }
    )

@app.get("/main_page")
def main_page(
    request: Request
):
    return templates.TemplateResponse(
        "details/main.html",
        {
            "request" : request
        }
    )

@app.post("/signup")
def signup_save(
    request : Request,
    email : str = Form(),
    name : str = Form(), 
    surname : str = Form(), 
    password : str = Form()
    ):
    user = users_repository.create_user(
        name=name,
        surname=surname,
        email=email,
        password=password
    )
    users_repository.add_user(user)
    return RedirectResponse(
        "/login",
        status_code=303
    )
    
@app.get("/login")
def login(request : Request):
    resp = templates.TemplateResponse(
        "details/login.html",
        {
            "request" : request
        }
    )
    return resp
    
@app.post("/login")
def login(
    request : Request,
    response : Response,
    email : str = Form(),
    password : str = Form()
    ):
    tmp = users_repository.get_user_by_email(email)
    if tmp != None and tmp.password == password:
        shifr_email = users_repository.encode_email(email)
        a = RedirectResponse("/main_page", status_code=303)
        a.set_cookie("token", shifr_email)
        return a
    another_ans = Response("Error")
    another_ans.status_code = 404
    return another_ans

@app.get("/flowers/add")
def add_flowers(
    request : Request,
    token : str = Cookie(default="")
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(email["email"])
    if user != None:
        return templates.TemplateResponse(
            "details/add_flower.html",
            {
                "request" : request,
            }
        )
    another_ans = Response("Error")
    another_ans.status_code = 404
    return another_ans

@app.get("/profile")
def profile(
    request : Request,
    token : str = Cookie(default="")
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(email["email"])
    if user != None:
        return templates.TemplateResponse(
            "details/profile.html",
            {
                "request" : request,
                "user" : user
            }
        )
    another_ans = Response("Error")
    another_ans.status_code = 404
    return another_ans


@app.post("/flowers/add")
def add_flowers(
    request : Request,
    name : str = Form(),
    count : str = Form(),
    cost : str = Form()
):
    count = int(count)
    cost = int(cost)
    flower = flowers_repository.create_flower(name=name, count=count, cost=cost)
    flowers_repository.add_flower(flower)
    return RedirectResponse(
        "/flowers/add",
        status_code=303
    )
    
@app.get("/shop")
def shop(
    request : Request,
    page : int = 1,
    limit : int = 3
):
    flowers = flowers_repository.get_all_flowers()
    start_interval = (page - 1) * limit
    max_page = len(flowers) // limit
    if len(flowers) % limit != 0:
        max_page += 1
    return templates.TemplateResponse(
        "details/shop.html",
        {
            "request" : request,
            "flowers" : flowers[start_interval : start_interval + limit],
            "next_page" : page + 1,
            "prev_page" : page - 1,
            "max_page" : max_page
        }
    )

@app.post("/cart/items")
def cart_items(
    request : Request,
    id : int = Form(),
    how_much : int = Form(),
    cart : str = Cookie(default="[]"),
    page : int = 1
):
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
    ans = RedirectResponse(
        f"/shop?page={page}",
        status_code=303
    )
    ans.set_cookie("cart", json_str)
    return ans

@app.get("/cart/items")
def cart_items(
    request : Request,
    cart : str = Cookie(default="[]"),
    page : int = 1,
    limit : int = 3
):
    list_flowers = flowers_repository.get_python_code(cart)
    start_interval = (page - 1) * limit
    max_page = len(list_flowers) // limit
    if len(list_flowers) % limit != 0:
        max_page += 1
    return templates.TemplateResponse(
        "details/cart.html",
        {
            "request" : request,
            "flowers_class" : flowers_repository,
            "list_flowers" : list_flowers[start_interval : start_interval + limit],
            "next_page" : page + 1,
            "prev_page" : page - 1,
            "max_page" : max_page
        }
    )
    
@app.post("/purchased")
def purchased(
    request : Request,
    cart : str = Cookie(default="[]"),
    token : str = Cookie(default="")
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(email["email"])
    list_flowers = flowers_repository.get_python_code(cart)
    purchases_repository.add_purchase(list_flowers, user.id)
    ans = RedirectResponse(
        "/purchased",
        status_code=303
    )
    ans.set_cookie("cart", "[]")
    return ans

@app.get("/purchased")
def purchased(
    request : Request,
    token : str = Cookie(default=""),
    page : int = 1,
    limit : int = 3
):
    email = users_repository.decode_token(token)
    user = users_repository.get_user_by_email(email["email"])
    list_purch = purchases_repository.get_user_purchases(user.id)

    start_interval = (page - 1) * limit
    max_page = len(list_purch) // limit
    if len(list_purch) % limit != 0:
        max_page += 1
    return templates.TemplateResponse(
        "details/purchased.html",
        {
            "request" : request,
            "flowers_class" : flowers_repository,
            "list_flowers" : list_purch[start_interval : start_interval + limit],
            "next_page" : page + 1,
            "prev_page" : page - 1,
            "max_page" : max_page
        }
    )