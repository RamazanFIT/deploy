from attrs import define


@define
class Purchase:
    flowers : list = []
    user_id: int = 0


class PurchasesRepository:
    purchases: list[Purchase]

    def __init__(self):
        self.purchases = []

    def get_user_purchases(self, user_id) -> list[dict]:
        for i in range(len(self.purchases)):
            if user_id == self.purchases[i].user_id:
                return self.purchases[i].flowers
        return []
    
    def create_purchase(self, user_id, flowers):
        purch = Purchase(flowers=flowers, user_id=user_id)
        return purch
    
    def add_purchase(self, list_, user_id):
        # Не использовать коммент; Это для дальнейшего улучшения пригодится
        # .....................................................................................
        # get_purchases = self.get_user_purchases(user_id)
        # set_ = set()
        # for i in list_:
        #     set_.add(i["id"])
        # additional_list = []
        # for i in range(len(get_purchases)):
        #     if get_purchases[i]["id"] in set_:
        #         for j in range(len(list_)):
        #             if list_[j]['id'] == get_purchases[i]['id']:
        #                 get_purchases[i]["how_much"] += list_[j]["how_much"]
        #     else:
        #         additional_list.append(get_purchases[i])
        # get_purchases += additional_list
        # for i in range(len(self.purchases)):
        #     if self.purchases[i] == user_id:
        #         self.purchases[i].flowers = get_purchases
        #.....................................................................................
        flag = True
        for i in self.purchases:
            if i.user_id == user_id:
                flag = False
        if flag:
            self.purchases.append(self.create_purchase(user_id, list_))
        else:
            for i in range(len(self.purchases)):
                if self.purchases[i].user_id == user_id:
                    self.purchases[i].flowers += list_
        