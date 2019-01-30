import data_io

user_expense_data = None
user_budget_data = None


def setup():
    global user_expense_data
    global user_budget_data
    user_expense_data = data_io.get_user_expenses_data()
    user_budget_data = data_io.get_user_budget_settings()


def display_home_view():
    print("This will display the home view")


def add_new_expense(category, year, month, location, amount):
    if category in user_expense_data["categories"]:
        # add data to existing category
        if year in user_expense_data["categories"][category]:
            if month in user_expense_data["categories"][category][year]:
                entries = len(user_expense_data["categories"][category][year][month])
                # print(entries)
                user_expense_data["categories"][category][year][month][entries + 1] = {"location": location, "amount": amount}
            else:
                user_expense_data["categories"][category][year][month] = {1: {"location": location, "amount": amount}}
        else:
            user_expense_data["categories"][category][year] = {month: {1: {"location": location, "amount": amount}}}
    else:
        # create new category and add data to it
        user_expense_data["categories"][category] = {year: {month: {1: {"location": location, "amount": amount}}}}


setup()
display_home_view()