from ui import MainWindow
from tkinter import Tk, Label, Entry, Button

# Login details checker function
def login():
   username = txtUsername.get().strip()
   password = txtPassword.get().strip()

   if username != "Admin":
       lblInfo.config(text="Incorrect Username")
   elif password != "Admin123":
       lblInfo.config(text="Incorrect Password")
   else:
       window.destroy()

       main = MainWindow()
       main.run()

# Login window
window = Tk()
window.title("Login")
window.geometry("500x500")

infoText = "Welcome, please input username and password.\n"
lblInfo = Label(text=infoText)
lblInfo.pack()

lblUser = Label(text="Username")
lblUser.pack()

txtUsername = Entry(background="#dddddd", width=10)
txtUsername.pack()

lblPass = Label(text="Password")
lblPass.pack()

txtPassword = Entry(background="#dddddd", width=10, show="•")
txtPassword.pack()

btnLogin = Button(text="Login", command=login)
btnLogin.pack()

window.mainloop()
