from attrs import define
import json

@define
class Flower:
    name: str
    count: int
    cost: int
    id: int = 0


class FlowersRepository:
    flowers: list[Flower]

    def __init__(self):
        self.flowers = []
        self.id = 1

    def add_flower(self, flower : Flower) -> bool:
        self.flowers.append(flower)
        return True

    def create_flower(self, name, count, cost):
        self.id += 1
        flower = Flower(name=name, count=count, cost=cost, id=self.id)
        return flower
    def get_all_flowers(self) -> list[Flower]:
        return self.flowers 
    
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
    
    def change_cnt(self, id, how_much):
        for i in range(len(self.get_all_flowers())):
            if self.flowers[i].id == id:
                self.flowers[i].count = max(0, self.flowers[i].count - how_much)
                
    def get_flower(self, id) -> Flower:
        for i in range(len(self.flowers)):
            if self.flowers[i].id == id:
                return self.flowers[i]
        return None

    