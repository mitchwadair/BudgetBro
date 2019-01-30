import data_io
import json

user_expense_data = None
user_budget_data = None


def setup():
    global user_expense_data
    global user_budget_data
    user_expense_data = data_io.get_user_expenses_data()
    user_budget_data = data_io.get_user_budget_settings()


def display_home_view():
    print("This will display the home view")


def add_new_expense(category, date, location, amount):
    if category in user_expense_data["categories"]:
        # add data to existing category
        if date in user_expense_data["categories"][category]:
            entries = len(user_expense_data["categories"][category][date])
            print(entries)
            user_expense_data["categories"][category][date][entries + 1] = {"location": location, "amount": amount}
        else:
            user_expense_data["categories"][category][date] = {1: {"location": location, "amount": amount}}
    else:
        # create new category and add data to it
        user_expense_data["categories"][category] = {date: {1: {"location": location, "amount": amount}}}


setup()
display_home_view()

add_new_expense("gas", "1-29-2019", "BP", 3.66)
add_new_expense("new", "1-29-2019", "place", 4.20)
add_new_expense("gas", "1-28-2019", "Shell", 40.69)

data_io.store_data("../../data/user_expenses.json", user_expense_data)
