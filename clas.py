class Users():

    def __init__(self):
        self.user_list = []

    def add_user(self, user):
        self.user_list.append(user)

    def __str__(self) -> str:
        list1 = ""
        for item in self.user_list:
            list1 = list1 + f'name = {item.name}' + " "
        return list1

class User():

    def __init__(self, name):
        self.name = name




user_1 = User("Ann")
user_2 = User("Sasha")

user_list = Users()
user_list.add_user(user_1)
user_list.add_user(user_2)
print(user_list)