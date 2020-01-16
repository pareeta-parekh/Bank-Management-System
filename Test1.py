import re
import pymongo
from tkinter import *
import os

root = Tk()
root.geometry('500x600')

root.title("Bank Registration Form")
root.config(bg="#c4d7d7")

Label(text="Registration Details", bg="#0481af",fg='white', width="300", height="2", font=("Calibri BOLD", 20)).pack()

name = StringVar()
phno = StringVar()
email = StringVar()
acctype = StringVar()
password = StringVar()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["Bank_details"]
cust = mydb["Customer_Details"]
#acc = mydb["Account_details"]
c_id = 0

def clearAll():
    name.set('')
    phno.set('')
    email.set('')
    acctype.set('')
    password.set('')

def auto():
    global c_id
    ans = cust.find().sort("_id",-1).limit(1)
    for i in ans:
        id = i["_id"]
        c_id = id + 1
        #print(i["_id"])
    cust_name = name.get()
    cust_phNo = phno.get()
    cust_email = email.get()
   # cust_accType = acctype.get()
    cust_pass = password.get()
    count = 0
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, cust_email)):
        print("Valid Email")
        for i in cust.find():
            #print("here for loop")
            if i["Email Id"] == cust_email:
                print("Use different Id")
                count = count + 1
    else:
        print("Invalid Email")

    if count == 0:
        #print("hiiiiiiii")
        data = {"_id": c_id, "Name": cust_name, "PhoNo": cust_phNo, "Email Id": cust_email, "Password": cust_pass, "Balance": 0}
        x = cust.insert_one(data)
        clearAll()




def delete_cust():
    cust_name = name.get()
    cust_pass = password.get()
    countDel = 1

    for i in cust.find():
        if i["Name"] == cust_name and i["Password"] == cust_pass:
            cust.delete_one({"Name": cust_name, "Password": cust_pass})
            clearAll()
        else:
            countDel = 0

    if countDel == 0:
        print("Invalid Login!")



nameUP = StringVar()
phnoUP = StringVar()
passwordUP = StringVar()

def update_cust():

    label_1 = Label(root, text="Name", width=20, bg="#c4d7d7", fg="#003399", font="Helvetica 13 bold").place(x=500,y=145)
    entry_1 = Entry(root, textvar=nameUP).place(x=730, y=145)

    label_2 = Label(root, text="PhNo", width=20, bg="#c4d7d7", fg="#003399", font="Helvetica 13 bold").place(x=500,y=200)
    entry_2 = Entry(root, textvar=phnoUP).place(x=730, y=200)

    label_5 = Label(root, text="Password", width=20, bg="#c4d7d7", fg="#003399", font="Helvetica 13 bold").place(x=500,y=245)
    entry_5 = Entry(root, textvar=passwordUP, show='*').place(x=730, y=245)

    buttonUpdateOk = Button(root, text="OK", bg='#057094', fg='white', width=30, command=okUpdate).place(x=600, y=350)

def okUpdate():

    cust_name = name.get()
    cust_pass = password.get()
    if cust_name == "" or cust_pass == "":
        print("error")
        root.destroy()

    for i in cust.find({"Name": cust_name, "Password": cust_pass}, {"_id": 0}):
        if i["Name"] == cust_name and i["Password"] == cust_pass:

            upName = nameUP.get()
            upPhno = phnoUP.get()
            upPassword = passwordUP.get()

            oldValue = ({"Name": cust_name, "Password": cust_pass})
            newValue = ({"$set": {"Name": upName, "PhoNo": upPhno, "Password": upPassword}})
            cust.update_one(oldValue, newValue)
        else:
            print("Error!")
    clearAll()

def showBal():
    root.destroy()
    os.system("python Test2.py")
    #exec(open('Test2.py').read())
    #mainloop(exit())

    clearAll()

def showClients():
    for i in cust.find():
        print(i)



label_1 = Label(root, text="Name", width=20,bg="#c4d7d7",fg="#003399",font="Helvetica 13 bold").place(x=40, y=145)
entry_1 = Entry(root, textvar=name).place(x=280, y=145)

label_2 = Label(root, text="PhNo", width=20, bg="#c4d7d7",fg="#003399",font="Helvetica 13 bold").place(x=40, y=200)
entry_2 = Entry(root, textvar=phno).place(x=280, y=200)

label_3 = Label(root, text="Email Id", width=20,bg="#c4d7d7",fg="#003399",font="Helvetica 13 bold").place(x=40, y=255)
entry_3 = Entry(root, textvar=email).place(x=280, y=255)

label_5 = Label(root, text="Password", width=20,bg="#c4d7d7",fg="#003399",font="Helvetica 13 bold").place(x=40, y=315)
entry_5 = Entry(root, textvar=password, show='*').place(x=280, y=315)

buttonAdd= Button(root, text="ADD", bg='#057094', fg='white',command=auto, width=15).place(x=50, y=400)
buttonDelete= Button(root, text="DELETE", bg='#057094', fg='white',command=delete_cust,width=15).place(x=200, y=400)
buttonUpdate= Button(root, text="UPDATE", bg='#057094', fg='white',width=15, command=update_cust).place(x=350, y=400)
buttonshow= Button(root, text="SHOW CLIENTS", bg='#057094', fg='white',width=30, command=showClients).place(x=120, y=470)
buttonBal = Button(root, text="SHOW BAL.", bg='#057094', fg='white',width=30,command=showBal).place(x=120, y=540)

root.mainloop()