import json


def get_user_budget_settings():
    try:
        user_data_file = open("../../data/user_data.txt", "r")
    except FileNotFoundError:
        print("User data file not found.")
        return None
    else:
        user_data = json.loads(user_data_file.read())
        user_data_file.close()
        return user_data


def get_user_expenses_data():
    try:
        user_expenses_file = open("../../data/user_expenses.txt", "r")
    except FileNotFoundError:
        print("User expenses file not found.")
        return None
    else:
        user_expenses = json.loads(user_expenses_file.read())
        user_expenses_file.close()
        return user_expenses


#test that file i/o is working
#print(get_user_budget_settings())
#print(get_user_expenses_data())
