from customer import Customer
import linecache
from twilio.rest import Client


# import_customer_data() goes through the data formatted from the POS system and outputs a list of Customer objects
def import_customer_data():
    n = 1
    customers = {}
    while True:

        # Reading through each line in the file
        line = linecache.getline("CustData.csv", n)[:-1]
        if line == "":
            break
        l = line[:-1].split(",")

        # Separating each line into its elements (number, name, date, product purchased, quantity purchased)
        cnum = l[0]
        cname = l[1]
        date = l[2]
        prod = l[7]
        quant = l[8]

        # Places all of this data into a dict where the customer number is the key and the customer object is the values
        if cnum not in customers.keys():
            c = Customer(cnum, cname, date, prod)
            customers[cnum] = c

        else:
            customers[cnum].add_date(date)
            customers[cnum].add_product(prod, quant)

        n += 1

    # Writes the data into another file formated to store customers' data separately in each line
    with open("C.csv", "w") as o:
        l = list(customers.values())
        l.sort(key=lambda x: x.get_name())
        o.seek(0)
        for c in l:
            o.writelines(c.to_long_string() + "\n")

    # Returns just the values of the dict
    return list(customers.values())


# A recursive implementation of the binary search algorithm
def binary_search(l, low, high, name):
    if high >= low:
        mid = (high + low) // 2

        if l[mid].split(",")[1] == name:
            return mid
        elif l[mid].split(",")[1] > name:
            return binary_search(l, low, mid - 1, name)
        else:
            return binary_search(l, mid + 1, high, name)
    return -1


# Adds a customer to the formatted file
def add_customer(customer):
    with open("C.csv", "r") as c:
        d = c.readlines()
        index = 0
        while index < len(d) and d[index].split(",")[1] > customer.get_name():
            index += 1

    with open("C.csv", "w") as c:
        c.seek(index)
        c.write(customer.to_long_string())


# Deletes a customer from the formatted file
def delete_customer(customer):
    with open("test_data.csv", "r") as f:
        d = f.readlines()
        line_number = binary_search(d, 0, len(d), customer.get_name())

        del d[line_number]

    with open("test_data.csv", "w") as f:
        f.seek(0)
        for line in d:
            f.write(line)


# send_message() sends the actual message. For the purposes of examination, the code has been commented out and replaced
# with an output to console instead. The account ID and Token have also been omitted
def send_message(number, message, date):
    account_sid = '${{secrets.API_ID}}'
    auth_token = "${{secrets.API_KEY}}"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to='+63' + number,
        from_="+12058136754",
        body=message,
        send_at=date,
    )

    print(f'"{message}" sent to {number} on {date}')
