import datetime


# This is the customer class that stores all the customer data and has some helpful methods
class Customer:

    def __init__(self, num, name, dates, prod):
        self.__num = num
        self.__name = name
        self.__last_send_date = datetime.datetime(2000, 1, 1)

        self.__dates = []
        if isinstance(dates, str):
            self.__dates.append(dates)
        else:
            self.__dates = dates

        self.__products = {}
        if prod in self.__products.keys():
            self.__products[prod] += 1
        else:
            self.__products[prod] = 1

    def add_product(self, pname, pquant):
        if pname in self.__products.keys():
            self.__products[pname] += int(pquant)
        else:
            self.__products[pname] = int(pquant)

    def add_date(self, d):
        if d not in self.__dates:
            self.__dates.append(d)

    def get_num(self):
        return self.__num

    def get_name(self):
        return self.__name

    def get_prods(self):
        l = []
        for p in self.__products.keys():
            l.append([p, self.__products[p]])
        l.sort(key=lambda x: x[1])
        return l

    def get_dates(self):
        return self.__dates

    # get_usual_days finds the three most common days that the customer comes to the store. It outputs them in a
    # string formatted as "day:number of visits, day:number of visits, day:number of visits"
    def get_usual_days(self):
        DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
        l = {}

        for d in self.__dates:
            w = d.split("/")
            day = DAYS[datetime.datetime(2000 + int(w[1]), int(w[0]), int(w[2])).weekday()]
            if day in l.keys():
                l[day] += 1
            else:
                l[day] = 1

        daysList = list(l.keys())
        daysList.sort(key=lambda x: l[x])

        j = 3
        if len(daysList) <= 3:
            j = len(daysList)

        s = ""
        for i in range(j):
            s += f'{daysList[i]}:{l[daysList[i]]} '

        return s[:-1]

    # returns last date that the customer was sent a message
    def get_last_date(self):
        return self.__last_send_date

    # updates the last date that the customer was sent a message
    def set_last_date(self, date):
        self.__last_send_date = date

    # outputs a string with the most important data of the customer for display in the GUI
    def to_string(self):
        prods = self.get_prods()[:3]
        pStr = ""
        for p in prods:
            pStr += f'{p[0]}:{p[1]} | '
        pStr = pStr[:-3]

        return f'{self.__num}\t{self.__name}\t{pStr}\t{self.get_usual_days()}\t'

    # Outputs a string containing all of the customer's data for storage in a text file
    def to_long_string(self):
        return f'{self.__num},{self.__name},{self.get_prods()},{self.__dates}'
