from attrs import define
import jwt

@define
class User:
    email: str
    name : str
    surname : str
    password : str
    id: int = 0

class UsersRepository:
    users: list[User]

    def __init__(self):
        self.users = []
        self.new_id = 0
    
    def add_user(self, user):
        self.users.append(user)
        return True
    
    def create_user(self, email, name, surname, password) -> User:
        self.new_id += 1
        user = User(email=email, name=name, surname=surname, id=self.new_id, password=password)
        return user
    
    def get_user_by_email(self, email) -> User:
        for i in range(len(self.users)):
            if self.users[i].email == email:
                return self.users[i]
        return None
    
    def encode_email(self, email):
        key = "Ramazan_the_best"
        algorithm = "HS256"
        shifr_email = jwt.encode(payload={"email" : email}, key=key, algorithm=algorithm)
        return shifr_email

    def decode_token(self, token) -> str:
        key = "Ramazan_the_best"
        algorithm = "HS256"
        email = jwt.decode(jwt=token, key=key, algorithms=algorithm)
        return email