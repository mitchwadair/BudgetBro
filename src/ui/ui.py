import os
import pickle

from tkinter import *
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
        self.menu_frame.pack(side=LEFT)

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
        overview_button.grid(row=0, column=0)

        expense_button = Button(self.menu_frame, text="Add Expense", command=lambda: self.load_content_page(ExpensePage), width=12)
        expense_button.grid(row=1, column=0)

    def load_content_page(self, page):
        to_load = self.pages[page]
        to_load.tkraise()


class OverviewPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Label(self, text="Overview page").pack()


class ExpensePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Label(self, text="Expense page").pack()


class NewUserProfilePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        title_frame = Frame(self)
        title_frame.grid(row=0)
        Label(title_frame, text="Create a New User").grid(row=0)

        content_frame = Frame(self)
        content_frame.grid(row=1)
        Label(content_frame, text="User Name:").grid(row=0, column=0, sticky=E)
        user_name_entry = Entry(content_frame)
        user_name_entry.grid(row=0, column=1)
        Label(content_frame, text="Annual Salary:").grid(row=1, column=0, sticky=E)
        salary_entry = Entry(content_frame)
        salary_entry.grid(row=1, column=1)
        Label(content_frame, text="Expected Additional Income:").grid(row=2, column=0, sticky=E)
        additional_income_entry = Entry(content_frame)
        additional_income_entry.grid(row=2, column=1)
        Label(content_frame, text="Tax Filing Status:").grid(row=3, column=0, sticky=E)
        tax_entry = Entry(content_frame)
        tax_entry.grid(row=3, column=1)
        Label(content_frame, text="Home State:").grid(row=4, column=0, sticky=E)
        state_entry = Entry(content_frame)
        state_entry.grid(row=4, column=1)


root = Tk()
root.title("BudgetBro")
application = BudgetApp(root)
application.mainloop()

