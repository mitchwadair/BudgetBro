import os

from tkinter import *
from src.functionality import app
from src.functionality import user
from src.functionality import data_io


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
        dirs = [d for d in os.listdir('../../data') if os.path.isdir(os.path.join('../../data', d))]
        

        for F in (OverviewPage, ExpensePage):
            frame = F(self.content_frame, self)
            self.pages[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.load_content_page(OverviewPage)

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


root = Tk()
application = BudgetApp(root)
application.mainloop()

