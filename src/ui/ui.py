import os
import pickle

from tkinter import *
from tkinter import ttk
from datetime import datetime

from src.functionality import app
from src.functionality import user
from src.functionality import data_io

import tkinter.simpledialog

sys.modules['user'] = user


class BudgetApp(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.content_frame = Frame(self)
        self.content_frame.pack(side=RIGHT)

        self.menu_frame = Frame(self)
        self.menu_frame.pack(side=LEFT, anchor=N, expand=YES)

        self.pages = {}
        self.app = app.App()

        self.load()

    def load(self):
        for F in (OverviewPage, ExpensePage, NewUserProfilePage):
            frame = F(self.content_frame, self)
            self.pages[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        dirs = [d for d in os.listdir('../../data') if os.path.isdir(os.path.join('../../data', d))]
        if len(dirs) > 0:
            if len(dirs) == 1:
                print("one profile, loading it")
                data_file = open("../../data/" + dirs[0] + "/user_data", "rb")
                self.app.app_user = pickle.load(data_file)
                data_file.close()
                print(repr(self.app.app_user))
            else:
                print("multiple profiles, choose")

            self.app.user_expense_data = data_io.get_user_expenses_data(self.app.app_user.name)
            self.app.user_budget_data = data_io.get_user_budget_settings(self.app.app_user.name)
            self.app.budget_performance_data = data_io.get_budget_performance_data(self.app.app_user.name)

            self.load_content_page(OverviewPage)
        else:
            print("create new profile")
            self.load_content_page(NewUserProfilePage)

        overview_button = Button(self.menu_frame, text="Overview", command=lambda: self.load_content_page(OverviewPage), width=12)
        overview_button.pack(side=TOP)

        expense_button = Button(self.menu_frame, text="Add Expense", command=lambda: self.load_content_page(ExpensePage), width=12)
        expense_button.pack(side=TOP)

    def load_content_page(self, page):
        to_load = self.pages[page]
        to_load.tkraise()


class OverviewPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Label(self, text="Overview page").pack()
        self.controller = controller


class ExpensePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Label(self, text="Expense page").pack()


class NewUserProfilePage(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)

        title_frame = Frame(self)
        title_frame.grid(row=0)
        Label(title_frame, text="Create a New User", font='bold').grid(row=0)

        content_frame = Frame(self)
        content_frame.grid(row=1)
        content_frame.config(bd=5)
        Label(content_frame, text="User Name:").grid(row=0, column=0, sticky=E)
        self.user_name_entry = Entry(content_frame)
        self.user_name_entry.grid(row=0, column=1)
        self.user_name_error = Label(content_frame, text="Invalid input", fg="red")

        Label(content_frame, text="Income Type:").grid(row=1, column=0, sticky=E)
        self.income_type = ttk.Combobox(content_frame, state="readonly", values=("Salary", "Hourly"))
        self.income_type.current(0)
        self.income_type.grid(row=1, column=1)
        self.income_type.bind("<<ComboboxSelected>>", self.income_type_change)

        self.salary_label = Label(content_frame, text="Annual Salary:")
        self.salary_entry = Entry(content_frame)
        self.salary_label.grid(row=2, column=0, sticky=E)
        self.salary_entry.grid(row=2, column=1)
        self.salary_error = Label(content_frame, text="Invalid input", fg="red")

        self.wage_label = Label(content_frame, text="Hourly Wage:")
        self.wage_entry = Entry(content_frame)
        self.wage_error = Label(content_frame, text="Invalid input", fg="red")
        self.hours_label = Label(content_frame, text="Average Hours Worked per Week:")
        self.hours_entry = Entry(content_frame)
        self.hours_error = Label(content_frame, text="Invalid input", fg="red")
        self.weeks_label = Label(content_frame, text="Expected Annual Work Weeks:")
        self.weeks_entry = Entry(content_frame)
        self.weeks_error = Label(content_frame, text="Invalid input", fg="red")

        Label(content_frame, text="Expected Additional Income:").grid(row=5, column=0, sticky=E)
        self.additional_income_entry = Entry(content_frame)
        self.additional_income_entry.grid(row=5, column=1)
        self.additional_income_error = Label(content_frame, text="Invalid input", fg="red")
        Label(content_frame, text="401k Contribution Percentage:").grid(row=6, column=0, sticky=E)
        self.retirement_entry = Entry(content_frame)
        self.retirement_entry.grid(row=6, column=1)
        self.retirement_error = Label(content_frame, text="Invalid input", fg="red")
        Label(content_frame, text="Annual HSA Contribution:").grid(row=7, column=0, sticky=E)
        self.hsa_entry = Entry(content_frame)
        self.hsa_entry.grid(row=7, column=1)
        self.hsa_error = Label(content_frame, text="Invalid input", fg="red")
        Label(content_frame, text="Tax Filing Status:").grid(row=8, column=0, sticky=E)
        filing_choices = ['single', 'married', 'married separately', 'head of household']
        self.tax_entry = ttk.Combobox(content_frame, state="readonly", values=filing_choices)
        self.tax_entry.current(0)
        self.tax_entry.grid(row=8, column=1)
        Label(content_frame, text="Home State:").grid(row=9, column=0, sticky=E)
        state_array = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
        self.state_entry = ttk.Combobox(content_frame, state="readonly", values=state_array)
        self.state_entry.current(0)
        self.state_entry.grid(row=9, column=1)

        button_frame = Frame(self)
        button_frame.grid(row=2)
        Button(button_frame, text="Submit", command=lambda: self.submit()).pack()

    def submit(self):
        print("Submit pressed")
        if self.valid_input():
            self.controller.app.create_user_profile(self.user_name_entry.get())
            salary = 0
            if self.income_type.get() == "Salary":
                salary = float(self.salary_entry.get())
            else:
                salary = self.controller.app.calculate_hourly_to_salary(float(self.wage_entry.get()), int(self.hours_entry.get()), int(self.weeks_entry.get()))
            post_tax_funds = self.controller.app.calculate_post_tax_funds(datetime.today().year, self.state_entry.get(), self.tax_entry.get(), salary, float(self.additional_income_entry.get()), float(self.retirement_entry.get()), float(self.hsa_entry.get()))
            self.controller.app.app_user = user.User(self.user_name_entry.get(), salary, float(self.additional_income_entry.get()), self.state_entry.get(), self.tax_entry.get(), post_tax_funds["annual"], post_tax_funds["monthly"])
            user_pickle_file = open("../../data/" + self.user_name_entry.get() + "/user_data", "wb")
            pickle.dump(self.controller.app.app_user, user_pickle_file)
            BudgetApp.load_content_page(self.controller, OverviewPage)

    def income_type_change(self, event):
        print("Income type changed")
        self.salary_label.grid_forget()
        self.salary_entry.grid_forget()
        self.wage_label.grid_forget()
        self.wage_entry.grid_forget()
        self.hours_label.grid_forget()
        self.hours_entry.grid_forget()
        self.weeks_label.grid_forget()
        self.weeks_entry.grid_forget()
        self.salary_error.grid_forget()
        self.wage_error.grid_forget()
        self.hours_error.grid_forget()
        self.weeks_error.grid_forget()

        if self.income_type.get() == "Salary":
            self.salary_label.grid(row=2, column=0, sticky=E)
            self.salary_entry.grid(row=2, column=1)
        else:
            self.wage_label.grid(row=2, column=0, sticky=E)
            self.wage_entry.grid(row=2, column=1)
            self.hours_label.grid(row=3, column=0, sticky=E)
            self.hours_entry.grid(row=3, column=1)
            self.weeks_label.grid(row=4, column=0, sticky=E)
            self.weeks_entry.grid(row=4, column=1)

    def valid_input(self):
        is_valid = True

        self.user_name_error.grid_forget()
        self.salary_error.grid_forget()
        self.wage_error.grid_forget()
        self.hours_error.grid_forget()
        self.weeks_error.grid_forget()
        self.additional_income_error.grid_forget()
        self.retirement_error.grid_forget()
        self.hsa_error.grid_forget()

        '''User Name'''
        if self.user_name_entry.get() == "":
            self.user_name_error.grid(row=0, column=3)
            is_valid = False

        '''Annual Salary'''
        if self.income_type.get() == "Salary":
            try:
                float(self.salary_entry.get())
            except ValueError:
                self.salary_error.grid(row=2, column=3)
                is_valid = False
        else:
            try:
                float(self.wage_entry.get())
            except ValueError:
                self.wage_error.grid(row=2, column=3)
                is_valid = False
            try:
                int(self.hours_entry.get())
            except ValueError:
                self.hours_error.grid(row=3, column=3)
                is_valid = False
            try:
                int(self.weeks_entry.get())
            except ValueError:
                self.weeks_error.grid(row=4, column=3)
                is_valid = False

        '''Additional income'''
        try:
            float(self.additional_income_entry.get())
        except ValueError:
            self.additional_income_error.grid(row=5, column=3)
            is_valid = False

        '''retirement contribution'''
        try:
            converted = float(self.retirement_entry.get())
            if converted < 0 or converted > 100:
                raise ValueError("Must be a percentage value between 0 and 100")
        except ValueError:
            self.retirement_error.grid(row=6, column=3)
            is_valid = False

        '''hsa contribution'''
        try:
            float(self.hsa_entry.get())
        except ValueError:
            self.hsa_error.grid(row=7, column=3)
            is_valid = False

        return is_valid


root = Tk()
root.title("BudgetBro")
application = BudgetApp(root)
application.mainloop()

