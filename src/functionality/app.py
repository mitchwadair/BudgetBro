import data_io
import user

import requests
import json
import os
import datetime
import pickle

user_expense_data = None
user_budget_data = None

app_user = None


def setup():
    global user_expense_data
    global user_budget_data
    global app_user
    user_expense_data = data_io.get_user_expenses_data()
    user_budget_data = data_io.get_user_budget_settings()
    dirs = [d for d in os.listdir('../../data') if os.path.isdir(os.path.join('../../data', d))]
    if len(dirs) == 0:
        print("No users stored. Prompt to create one")
        app_user = create_user_profile()
        data_file = open("../../data/" + app_user.name + "/user_data", "wb")
        pickle.dump(app_user, data_file)
        data_file.close()
        print(repr(app_user))
    elif len(dirs) == 1:
        print("One user found, loading their data")
        data_file = open("../../data/" + dirs[0] + "/user_data", "rb")
        app_user = pickle.load(data_file)
        data_file.close()
        print(repr(app_user))
    else:
        print("More than one user found.  Prompt for use choice")


def create_user_profile():
    print("Enter your profile name:")
    name = input()
    print("Enter your salary:")
    salary = int(input())
    print("Enter expected additional income:")
    additional_inc = float(input())
    print("Enter your home state:")
    state = input()
    print("Enter your tax filing status:")
    filing_status = input()
    print("Enter your 401k contribution percentage")
    ret_cont = float(input()) / 100
    print("Enter your annual Health Savings Account contribution:")
    hsa_cont = int(input())

    year = datetime.datetime.today().year
    post_tax = calculate_post_tax_funds(year, state, filing_status, salary, additional_inc, ret_cont, hsa_cont)
    os.mkdir("../../data/" + name)

    return user.User(name, salary, additional_inc, state, filing_status, post_tax["annual"], post_tax["monthly"], None)


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


def calculate_post_tax_funds(year, state, filing_status, salary, additional_inc, retirement_cont, hsa_cont):
    gross_income = (salary + additional_inc) - (salary*retirement_cont) - hsa_cont
    tax_info = json.loads(fetch_tax_information(year, gross_income, state, filing_status))["annual"]
    post_tax_funds = gross_income - (tax_info["fica"]["amount"] + tax_info["federal"]["amount"] + tax_info["state"]["amount"])
    post_tax_funds_by_month = post_tax_funds / 12
    return {'annual': post_tax_funds, 'monthly': post_tax_funds_by_month}


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


def calculate_hourly_to_salary(wage, avg_hours, expected_weeks):
    return wage*avg_hours*expected_weeks


def update_budget_data():
    data_io.store_data("../../data/user_data.json", user_budget_data)


setup()
display_home_view()

# print(calculate_post_tax_funds(2019, "NC", "single", 100000, .19, 3100))
# add_new_expense("gas", "2019", "1", {"location": "Shell", "amount": 4.20})
# remove_expense("gas", "2019", "1", 0)
# edit_expense("gas", "2019", "1", 1, {"location":"BP", "amount":4.20})
# print(user_expense_data)
