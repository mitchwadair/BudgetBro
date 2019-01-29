import json


def get_user_budget_settings():
    user_data_file = open("../../data/user_data.txt", "r")
    user_data = json.loads(user_data_file.read())
    user_data_file.close()
    return user_data


def get_user_expenses_data():
    user_expenses_file = open("../../data/user_expenses.txt", "r")
    user_expenses = json.loads(user_expenses_file.read())
    user_expenses_file.close()
    return user_expenses


#test that file i/o is working
#print(get_user_budget_settings()["salary"])
#print(get_user_expenses_data())
