import json
import os


def get_user_budget_settings(name):
    if os.path.exists("../../data"):
        try:
            user_data_file = open("../../data/" + name + "/user_budget.json", "r")
        except FileNotFoundError:
            print("User data file not found.")
            return None
        else:
            user_data = json.loads(user_data_file.read())
            user_data_file.close()
            return user_data
    else:
        os.mkdir("../../data")
        get_user_budget_settings(name)


def get_user_expenses_data(name):
    if os.path.exists("../../data"):
        try:
            user_expenses_file = open("../../data/" + name + "/user_expenses.json", "r")
        except FileNotFoundError:
            print("User expenses file not found... Creating a new one.")
            store_data("../../data/" + name + "/user_expenses.json", {})
            get_user_expenses_data(name)
        else:
            user_expenses = json.loads(user_expenses_file.read())
            user_expenses_file.close()
            return user_expenses
    else:
        os.mkdir("../../data")
        get_user_expenses_data(name)


def get_budget_performance_data(name):
    if os.path.exists("../../data"):
        try:
            budget_performance_file = open("../../data/" + name + "/budget_performance.json", "r")
        except FileNotFoundError:
            print("User expense performance file not found... Creating a new one.")
            store_data("../../data/" + name + "/budget_performance.json", {})
            get_budget_performance_data(name)
        else:
            budget_performance = json.loads(budget_performance_file.read())
            budget_performance_file.close()
            return budget_performance
    else:
        os.mkdir("../../data")
        get_budget_performance_data(name)


def store_data(file_path, data):
    to_write = json.dumps(data, indent=2);
    data_file = open(file_path, "w")
    data_file.write(to_write)
    data_file.close()


#test that file i/o is working
#print(get_user_budget_settings())
#print(get_user_expenses_data())
#store_data("../../data/user_expenses.json", get_user_expenses_data())

