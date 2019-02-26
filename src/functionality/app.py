import data_io
from src.functionality import user

import requests
import json
import os
import datetime


class App:
    def __init__(self):
        self.user_expense_data = {}
        self.user_budget_data = {}
        self.budget_performance_data = {}
        self.app_user = user.User()

    @staticmethod
    def create_user_profile(name):
        os.mkdir("../../data/" + name)

    def add_new_expense(self, category, year, month, data):
        if category in self.user_expense_data:
            # add data to existing category
            if year in self.user_expense_data[category]:
                if month in self.user_expense_data[category][year]:
                    entries = len(self.user_expense_data[category][year][month])
                    # print(entries)
                    self.user_expense_data[category][year][month].insert(entries, data)
                else:
                    self.user_expense_data[category][year][month] = [data]
            else:
                self.user_expense_data[category][year] = {month: [data]}
        else:
            # create new category and add data to it
            self.user_expense_data[category] = {year: {month: [data]}}
        self.update_expense_data(self.app_user.name)

    def edit_expense(self, category, year, month, index, data):
        self.user_expense_data[category][year][month][index] = data
        self.update_expense_data(self.app_user.name)

    def remove_expense(self, category, year, month, index):
        del self.user_expense_data[category][year][month][index]
        self.update_expense_data(self.app_user.name)

    def update_expense_data(self, name):
        data_io.store_data("../../data/" + name + "/user_expenses.json", self.user_expense_data)

    @staticmethod
    def calculate_post_tax_funds(year, state, filing_status, salary, additional_inc, retirement_cont, hsa_cont):
        gross_income = (salary + additional_inc) - (salary*retirement_cont) - hsa_cont
        tax_info = json.loads(App.fetch_tax_information(year, gross_income, state, filing_status))["annual"]
        post_tax_funds = gross_income - (tax_info["fica"]["amount"] + tax_info["federal"]["amount"] + tax_info["state"]["amount"])
        post_tax_funds_by_month = post_tax_funds / 12
        return {'annual': post_tax_funds, 'monthly': post_tax_funds_by_month}

    @staticmethod
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

    @staticmethod
    def calculate_hourly_to_salary(wage, avg_hours, expected_weeks):
        return wage*avg_hours*expected_weeks

    def create_budget(self):
        current_year = datetime.datetime.today().year
        budget = {current_year: {1: {}}}
        self.user_budget_data = budget
        self.update_budget_data()

    def change_budget(self, year, month, category, amount):
        if year in self.user_budget_data:
            if month in self.user_budget_data[year]:
                if category is None:
                    self.user_budget_data[year][month] = "s"
                else:
                    self.user_budget_data[year][month][category] = amount
            else:
                if category is None:
                    self.user_budget_data[year][month] = "s"
                else:
                    self.user_budget_data[year][month] = {category: amount}
        else:
            if category is None:
                self.user_budget_data[year] = {month: "s"}
            else:
                self.user_budget_data[year] = {month: {category: amount}}
        self.update_budget_data()

    def update_budget_data(self):
        data_io.store_data("../../data/" + self.app_user.name + "/user_budget.json", self.user_budget_data)

    def calculate_budget_performance(self, year=None, month=None):
        if year is None or month is None:
            if self.budget_performance_data is None:
                self.budget_performance_data = {}
            for y in sorted(self.user_budget_data):
                if y not in self.budget_performance_data:
                    self.budget_performance_data[y] = {}
                    self.calculate_budget_performance()
                for m in sorted(self.user_budget_data[y]):
                    if m not in self.budget_performance_data[y]:
                        self.budget_performance_data[y][m] = {}
                        self.calculate_budget_performance()
                    self.calculate_budget_performance(y, m)
        else:
            year = str(year)
            month = str(month)
            for c in self.user_budget_data[year][month]:
                expenses_added = False
                if c in self.user_expense_data:
                    if year in self.user_expense_data[c]:
                        if month in self.user_expense_data[c][year]:
                            expense_sum = 0
                            for data in self.user_expense_data[c][year][month]:
                                expense_sum += data["amount"]
                            self.budget_performance_data[year][month][c] = {"budgeted": self.user_budget_data[year][month][c], "spent": expense_sum}
                            self.update_budget_performance_data()
                            expenses_added = True
                if not expenses_added:
                    self.budget_performance_data[year][month][c] = {"budgeted": self.user_budget_data[year][month][c], "spent": 0}
            self.update_budget_performance_data()

    def update_budget_performance_data(self):
        data_io.store_data("../../data/" + self.app_user.name + "/budget_performance.json", self.budget_performance_data)
