import data_io
import requests

user_expense_data = None
user_budget_data = None


def setup():
    global user_expense_data
    global user_budget_data
    user_expense_data = data_io.get_user_expenses_data()
    user_budget_data = data_io.get_user_budget_settings()


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


def update_expense_data():
    data_io.store_data("../../data/user_expenses.json", user_expense_data)


def fetch_tax_information(year, gross_income, state, filing_status):
    year = str(year)
    gross_income = str(gross_income)
    api_key_file = open("../../data/taxee_api.txt", "r")
    api_key = api_key_file.read()
    api_key_file.close()
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'state': state,
        'filing_status': filing_status,
        'pay_rate': gross_income
    }
    response = requests.post('https://taxee.io/api/v2/calculate/' + year, headers=headers, data=data)
    if response.status_code == 200:
        return response.text
    else:
        return None


def calculate_hourly_gross_income(wage, avg_hours, expected_weeks):
    return wage*avg_hours*expected_weeks;


def update_budget_data():
    data_io.store_data("../../data/user_data.json", user_budget_data)


setup()
display_home_view()

# print(fetch_tax_information(2019, 50000, "NC", "single"))
# add_new_expense("gas", "2019", "1", {"location": "Shell", "amount": 4.20})
# remove_expense("other", "2018", "2", 0)
# edit_expense("gas", "2019", "1", 1, {"location":"BP", "amount":4.20})
# print(user_expense_data)
