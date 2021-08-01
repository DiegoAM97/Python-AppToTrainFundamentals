from tkinter import *
from tkinter import messagebox
import pymysql

root = Tk()
root.title("Beta survey")

selected=False
nameValue = StringVar()
lastNameValue = StringVar()
gender= IntVar()
lenguageCsharp = IntVar()
lenguageR = IntVar()
lenguageJava = IntVar()
lenguageJS = IntVar()
lenguageP = IntVar()

#------------------METHODS------------------

def version():
    messagebox.showinfo("Version","The app is in beta phase")

def exit():
    root.destroy()

def toggleGender():

    global selected

    if gender.get() == 1:
        selected = True
        return "Male"

    elif gender.get() == 2:
        selected = True
        return "Female"


def toggleLanguage():
    text = [0,0,0,0,0]
    if lenguageCsharp.get() == 1:
        text[0] = 1
    if lenguageR.get() == 1:
        text[1] = 1
    if lenguageJava.get() == 1:
        text[2] = 1
    if lenguageP.get() == 1:
        text[3] = 1
    if lenguageJS.get() == 1:
        text[4] = 1
    return text


def send():

    global selected

    if selected and len(nameValue.get())>0 and len(lastNameValue.get())>0:

        try:
            insertTable()
            messagebox.showinfo("Yay!","Thanks for participating")
            resetValues()
        except:
            messagebox.showwarning("Database","The table doesn't exist")

    else:
        messagebox.showwarning("Error","Name, last name and gender is required")


def resetValues():
    nameValue.set("")
    lastNameValue.set("")
    gender.set(0)
    lenguageCsharp.set(0)
    lenguageR.set(0)
    lenguageJava.set(0)
    lenguageJS.set(0)
    lenguageP.set(0)


#------------------DATABASE RELATED METHODS------------------

def conectDB():
    try:
        createDatabase()
        createTable()
        messagebox.showinfo("Database","The database has been created correctly")

    except:
        messagebox.showwarning("Database","The database already exists")

def createDatabase():
    connection = pymysql.connect(host="localhost", port=3306, user="root", password="root", charset="utf8")
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE SurveyAppDatabase")
    connection.close()

def createTable():
    connection = pymysql.connect(host="localhost", port=3306, user="root", password="root", db="SurveyAppDatabase", charset="utf8")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE Survey(
                                ID INTEGER AUTO_INCREMENT PRIMARY KEY,
                                Name VARCHAR(50),
                                LastName VARCHAR(50),
                                Gender VARCHAR(10),
                                Csharp BOOLEAN,
                                R BOOLEAN,
                                Java BOOLEAN,
                                Python BOOLEAN,
                                JavaScript BOOLEAN
                    )""")
    connection.close()

def insertTable():
    connection = pymysql.connect(host="localhost", port=3306, user="root", password="root", db="SurveyAppDatabase", charset="utf8")
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO 
                    Survey (Name, LastName, Gender, Csharp, R, Java, Python, JavaScript) 
                    VALUES(
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )""" , (nameValue.get(), lastNameValue.get(), toggleGender(), toggleLanguage()[0],
                    toggleLanguage()[1], toggleLanguage()[2], toggleLanguage()[3], toggleLanguage()[4])
                    )
    connection.commit()
    connection.close()

#------------------INTERFACE------------------

frame = Frame(root, width=400, height=600)
frame.pack()

image = PhotoImage(file=r"Python.png").subsample(12, 12)

titulo = Label(frame, text="Survey developed with: ")
titulo.grid(row=0, column=0, pady=10, padx=10)


Label(frame, image=image).grid(row=0, column=2)

name = Label(frame, text="Name:")
name.grid(row=1, column=0, pady=10, padx=10, sticky=W)
lastName = Label(frame, text="Last name:")
lastName.grid(row=2, column=0, pady=10, padx=10, sticky=W)
gen = Label(frame, text="Gender:")
gen.grid(row=3, column=0, pady=10, padx=10, sticky=W)
knowledge = Label(frame, text="Knowledge:")
knowledge.grid(row=4, column=0, pady=10, padx=10, sticky=W)

nameE = Entry(frame, textvariable=nameValue)
nameE.grid(row=1, column=1, pady=10, padx=10)
lastNameE = Entry(frame, textvariable=lastNameValue)
lastNameE.grid(row=2, column=1, pady=10, padx=10)

Radiobutton(frame, text="Male", variable=gender, value=1, command=toggleGender).grid(row=3, column=1, sticky=W)
Radiobutton(frame, text="Female", variable=gender, value=2, command=toggleGender).grid(row=3, column=2, sticky=W)

Checkbutton(frame, text="C#", variable=lenguageCsharp, onvalue=1, offvalue=0, command=toggleLanguage).grid(row=4, column=1, sticky=W)
Checkbutton(frame, text="R", variable=lenguageR, onvalue=1, offvalue=0, command=toggleLanguage).grid(row=4, column=2, sticky=W)
Checkbutton(frame, text="Java", variable=lenguageJava, onvalue=1, offvalue=0, command=toggleLanguage).grid(row=4, column=3, sticky=W)
Checkbutton(frame, text="Python", variable=lenguageP, onvalue=1, offvalue=0, command=toggleLanguage).grid(row=5, column=1, sticky=W)
Checkbutton(frame, text="Javascript", variable=lenguageJS, onvalue=1, offvalue=0, command=toggleLanguage).grid(row=5, column=2, sticky=W)

button = Button(frame, text="Submit", width=20, command=lambda:send())
button.grid(row=6,column=1)
button.config(bg="gray", fg="black")

#------------------MENU INTERFACE------------------

menubar = Menu(root)
root.config(menu=menubar)

app = Menu(menubar, tearoff=0)
options = Menu(menubar, tearoff=0)
help = Menu(menubar, tearoff=0)

menubar.add_cascade(label="Database", menu=app)
menubar.add_cascade(label="Edit", menu=options)
menubar.add_cascade(label="Help", menu=help)

app.add_command(label="Conect", command=lambda:conectDB())
app.add_separator()
app.add_command(label="This does nothing")
options.add_command(label="Exit", command=lambda:exit())
help.add_command(label="Version", command=lambda:version())

root.resizable(width=False, height=False)
root.mainloop()
