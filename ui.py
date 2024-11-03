from tkinter import Tk, Label, Text, Button, Frame, Listbox, END
import importcustomerdata
import datetime


# MainWindow is a class that contains the main GUI that powers the message sending, filtering, and displaying
class MainWindow:

    def __init__(self):
        self.window = Tk()

        self.customers = importcustomerdata.import_customer_data()
        self.sendList = self.customers.copy()

        self.window.title("Save'n'save Grocery Text Messaging Platform")
        self.window.geometry("1000x500")
        self.window.config(background="#bbbbbb")

        lblHeader = Label(text="Welcome")
        lblHeader.pack()

        frameMessage = Frame(self.window)
        frameMessage.pack()
        frameMessage.place(x=20, y=50)

        lblMessageTitle = Label(frameMessage, text="Message")
        lblMessageTitle.pack()

        self.txtMessage = Text(frameMessage, background="#dddddd", height=20, width=60)
        self.txtMessage.pack()

        lblInstructions = Label(frameMessage, text='''"{NAME}", "{First_NAME}", and "{LAST_NAME}", and "{CUSTOMER_NUMBER}"
           will be substituted for their corresponding values''')
        lblInstructions.pack()

        btnSend = Button(frameMessage, text="Send Message", command=self.send)
        btnSend.pack()

        frameList = Frame(self.window)
        frameList.pack()
        frameList.place(x=520, y=50)

        lblListTitle = Label(frameList, text="Customers")
        lblListTitle.pack()

        self.listCustomers = Listbox(frameList, width=46, height=18)
        for i, c in enumerate(self.customers):
            self.listCustomers.insert(i, c.to_string())
        self.listCustomers.pack(side="top")

        frameFilter = Frame(frameList, width=500)
        frameFilter.pack()

        self.txtSearch = Text(frameFilter, width=40, height=1, background="#eeeeee")
        self.txtSearch.pack(side="left")

        btnSearch = Button(frameFilter, text="Search", command=self.search)
        btnSearch.pack(side="right")

    # send() calculates the best send time (the day before the most common visit day at 8 pm)
    def send(self):

        DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
        now = datetime.datetime.now()
        today = now.weekday()

        # Iterates through each customer in the list
        for customer in self.sendList:
            baseMessage = self.txtMessage.get("1.0", END).strip()

            # finds the day of the week of the best send time
            day = customer.get_usual_days()[:3]
            sendDay = DAYS.index(day) - 1

            if sendDay == -1:
                sendDay = 6

            # Finding the number of days until the best send day so that the date of the best send day can be found
            daysUntilSend = sendDay - today

            if daysUntilSend < 1:
                daysUntilSend += 7

            # Accounting for the number of days in each month (if this is not done, sendDate could be Feb 30th for ex.)
            DAYS_IN_MONTHS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
            year = now.year
            month = now.month
            date = now.day + daysUntilSend

            if date > DAYS_IN_MONTHS[month - 1]:
                date -= DAYS_IN_MONTHS[month - 1]
                month += 1

            if month == 13:
                month = 1
                year += 1

            # Creating the actual datetime object with the best send date at 8 pm (hour 20)
            sendDate = datetime.datetime(year, month, date, hour=20)

            if (sendDate - customer.get_last_date()).days < 4:
                break

            custNum = customer.get_num()

            # Replacing all of the template text with the actual customer data
            message = baseMessage.replace("{NAME}", customer.get_name())
            message = message.replace("{FIRST_NAME}", customer.get_name().split(" ")[0])
            message = message.replace("{LAST_NAME}", customer.get_name().split(" ")[-1])
            message = message.replace("{CUSTOMER_NUMBER}", custNum)

            importcustomerdata.send_message(custNum, message, sendDate)
            customer.set_last_date(sendDate)

    # search() filters through all of the customers given inputted search queries
    def search(self):

        # Separates the input into queries separated by " + "
        queries = self.txtSearch.get("1.0", END).strip().split(" + ")
        self.listCustomers.delete(0, END)
        self.sendList = []

        # Iterates through each customer, and tests if each query applies to the customer
        for c in self.customers:
            for query in queries:
                if query.lower() in c.to_long_string().lower():
                    self.listCustomers.insert("end", c.to_string())
                    self.sendList.append(c)
                    break

    def run(self):
        self.window.mainloop()
