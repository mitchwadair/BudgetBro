import data_io

user_expense_data = None
user_budget_data = None


def setup():
    global user_expense_data
    global user_budget_data
    user_expense_data = data_io.get_user_expenses_data()
    user_budget_data = data_io.get_user_budget_settings()


def update_expense_data():
    data_io.store_data("../../data/user_expenses.json", user_expense_data)


def update_budget_data():
    data_io.store_data("../../data/user_data.json", user_budget_data)


def display_home_view():
    print("This will display the home view")


def add_new_expense(category, year, month, data):
    if category in user_expense_data:
        # add data to existing category
        if year in user_expense_data[category]:
            if month in user_expense_data[category][year]:
                entries = len(user_expense_data[category][year][month])
                # print(entries)
                user_expense_data[category][year][month].insert(entries, data)
            else:
                user_expense_data[category][year][month] = [data]
        else:
            user_expense_data[category][year] = {month: [data]}
    else:
        # create new category and add data to it
        user_expense_data[category] = {year: {month: [data]}}
    update_expense_data()


def edit_expense(category, year, month, index, data):
    user_expense_data[category][year][month][index] = data
    update_expense_data()


def remove_expense(category, year, month, index):
    del user_expense_data[category][year][month][index]
    update_expense_data()


setup()
display_home_view()

# add_new_expense("gas", "2019", "1", {"location": "Shell", "amount": 4.20})
# remove_expense("other", "2018", "2", 0)
# edit_expense("gas", "2019", "1", 1, {"location":"BP", "amount":4.20})
# print(user_expense_data)
