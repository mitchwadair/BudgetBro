import json


def get_user_budget_settings():
    try:
        user_data_file = open("../../data/user_data.json", "r")
    except FileNotFoundError:
        print("User data file not found.")
        return None
    else:
        user_data = json.loads(user_data_file.read())
        user_data_file.close()
        return user_data


def get_user_expenses_data():
    try:
        user_expenses_file = open("../../data/user_expenses.json", "r")
    except FileNotFoundError:
        print("User expenses file not found.")
        return None
    else:
        user_expenses = json.loads(user_expenses_file.read())
        user_expenses_file.close()
        return user_expenses


def store_data(file_path, data):
    to_write = json.dumps(data);
    data_file = open(file_path, "w")
    data_file.write(to_write)


#test that file i/o is working
#print(get_user_budget_settings())
#print(get_user_expenses_data())
#store_data("../../data/user_expenses.json", get_user_expenses_data())

