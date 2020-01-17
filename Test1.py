import re
from tkinter import messagebox as ms
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

def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = True

    if len(passwd) < 8:
        #print('length should be at least 6')
        ms.showerror("Error","length should be at least 6")
        val = False

    if len(passwd) > 20:
        #print('length should be not be greater than 20')
        ms.showerror("Error","length should be not be greater than 20")
        val = False

    if not any(char.isdigit() for char in passwd):
        #print('Password should have at least one numeral')
        ms.showerror("Error","Password should have at least one numeral")
        val = False

    if not any(char.isupper() for char in passwd):
        #print('Password should have at least one uppercase letter')
        ms.showerror("Error","Password should have at least one uppercase letter")
        val = False

    if not any(char.islower() for char in passwd):
        #print('Password should have at least one lowercase letter')
        ms.showerror("Error","Password should have at least one lowercase letter")
        val = False

    if not any(char in SpecialSym for char in passwd):
        #print('Password should have at least one of the symbols $@#')
        ms.showerror("Error","Password should have at least one of the symbols $@#")
        val = False
    if val:
        return val

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

    if count == 0:
        if cust_name != '' and cust_phNo != '' and cust_pass != '':
            if len(cust_phNo) == 10:
                if password_check(cust_pass):
                    data = {"_id": c_id, "Name": cust_name, "PhoNo": cust_phNo, "Email Id": cust_email, "Password": cust_pass, "Balance": 0, "is_delete": False}
                    x = cust.insert_one(data)
                    #print("Data Inserted!")
                    ms.showinfo("Info","Data Inserted!")
                    clearAll()
                else:
                    #print("Invalid Password")
                    ms.showerror("Error","Invalid Password")
            else:
                print(cust_phNo)
                #print("Phone Number should be of 10 Digits!")
                ms.showerror("Error","Phone Number should be of 10 Digits!")
        else:
            #print("Empty Fields Not allowed!!")
            ms.showerror("Error","Empty Fields Not allowed!!")
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, cust_email)):
        # print("Valid Email")
        for i in cust.find():
            # print("here for loop")
            if i["Email Id"] == cust_email:
                # print("Use different Id")
                ms.showerror("Error", "Use different Id")
                count = count + 1
    else:
        # print("Invalid Email")
        ms.showerror("Error", "Invalid Email")


def delete_cust():
    cust_name = name.get()
    cust_pass = password.get()
    countDel = 1
    is_delete = False

    for i in cust.find():
        if i["Name"] == cust_name and i["Password"] == cust_pass:
            #cust.delete_one({"Name": cust_name, "Password": cust_pass})
            oldValue = ({"Name": cust_name, "Password":cust_pass,"is_delete": False})
            newValue = ({"$set": {"is_delete": True}})
            cust.update_one(oldValue, newValue)
            print("Data Deleted!")
            #ms.showinfo("INFO","Data Deleted!")
            clearAll()
            countDel = 1
            break
        else:
            countDel = 0

    if countDel == 0:
        print("Invalid Login!")
        print(countDel)
        #ms.showerror("Error","Invalid Login In Delete!")



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
        #print("error")
        ms.showerror("Error","error")
        root.destroy()

    for i in cust.find({"Name": cust_name, "Password": cust_pass}, {"_id": 0}):
        if i["Name"] == cust_name and i["Password"] == cust_pass:

            upName = nameUP.get()
            upPhno = phnoUP.get()
            upPassword = passwordUP.get()

            oldValue = ({"Name": cust_name, "Password": cust_pass})
            newValue = ({"$set": {"Name": upName, "PhoNo": upPhno, "Password": upPassword}})
            cust.update_one(oldValue, newValue)
            #print("Data Updated!")
            ms.showinfo("INFO","Data Updated!")
        else:
            #print("Error!")
            ms.showerror("Error","Error!")
    clearAll()

def showBal():
    root.destroy()
    os.system("python Test2.py")
    #exec(open('Test2.py').read())
    #mainloop(exit())

    clearAll()

def showClients():
    for i in cust.find({"is_delete":False}):
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