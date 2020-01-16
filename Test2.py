try:
    import pymongo
    from tkinter import *

    showmain = Tk()
    showmain.geometry('500x600')

    showmain.title("Bank Registration Form")
    showmain.config(bg="#c4d7d7")

    name = StringVar()
    password = StringVar()
    addRs = StringVar()

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["Bank_details"]
    cust = mydb["Customer_Details"]

    def clearAll():
        name.set('')
        password.set('')
        addRs.set('')

    def addbal():
        cname = name.get()
        cpass = password.get()
        cbal = addRs.get()
        addbalRs = int(cbal)
        ansAmt = 0

        ans = cust.find({"Name": cname, "Password": cpass})
        for x in ans:
            bal = int(x["Balance"])
            ansAmt = bal + addbalRs
            #print("UR BAL IS :{}".format(ansAmt))
        ans = cust.find_one_and_update({"Name": cname, "Password": cpass},{"$set":{"Balance":ansAmt}})
        label_add = Label(showmain, text="Amount Added!!", bg="#c4d7d7", fg="#003399", font="Helvetica 13 bold").place(x=150, y=450)
        clearAll()

    def delbal():
        print("in delete")
        cname = name.get()
        cpass = password.get()
        cbal = addRs.get()
        addbalRs = int(cbal)
        ansAmt = 0

        for x in cust.find({"Name": cname, "Password": cpass}):
            #print(x["Balance"])
            bal = int(x["Balance"])
            #print(type(bal))
            if bal == 0:
                print("You Cant Withdraw, ur bal is NULL")
                label_delete1 = Label(showmain, text="You Cant Withdraw, ur bal is NULL!!", bg="#c4d7d7", fg="#003399", font="Helvetica 13 bold").place(x=150, y=450)
            else:
                ans = cust.find({"Name": cname, "Password": cpass})
                for x in ans:
                    bal = int(x["Balance"])
                    if addbalRs >= bal :
                        print("You cant withdraw this amt, Choose lesser number")
                        label_delete2 = Label(showmain, text="You cant withdraw this amt, Choose lesser number!!", bg="#c4d7d7",fg="#003399", font="Helvetica 13 bold").place(x=150, y=450)
                    else:
                        ansAmt = bal - addbalRs
                        # print("UR BAL IS :{}".format(ansAmt))
                        ans = cust.find_one_and_update({"Name": cname, "Password": cpass}, {"$set": {"Balance": ansAmt}})
                        label_delete3 = Label(showmain, text="Amount Withdrawn!!", bg="#c4d7d7",fg="#003399", font="Helvetica 13 bold").place(x=150, y=450)

        clearAll()
    def showbal():
        cname = name.get()
        cpass = password.get()

        ans = cust.find({"Name": cname, "Password": cpass})

        for x in ans:
            print("UR BAL IS :", x["Balance"])
            #label_show = Label(showmain, text="Your Balance is: ", bg="#c4d7d7", fg="#003399",font="Helvetica 13 bold").place(x=190, y=450)
        clearAll()


    custNames = Label(showmain,text="Show Account Balance", bg="#0481af", fg='white', width="300", height="2",font=("Calibri BOLD", 20)).pack()

    label_1 = Label(showmain, text="Name", width=20, bg="#c4d7d7", fg="#003399", font="Helvetica 13 bold").place(x=40,y=145)
    entry_1 = Entry(showmain, textvar=name).place(x=280, y=145)

    label_5 = Label(showmain, text="Password", width=20, bg="#c4d7d7", fg="#003399", font="Helvetica 13 bold").place(x=40,y=205)
    entry_5 = Entry(showmain, textvar=password, show='*').place(x=280, y=205)

    label_6 = Label(showmain, text="Balance Amount", width=20, bg="#c4d7d7", fg="#003399", font="Helvetica 13 bold").place(x=40,y=265)
    entry_6 = Entry(showmain, textvar=addRs).place(x=280, y=265)

    buttonbalAdd = Button(showmain, text="ADD BALANCE", bg='#057094', fg='white',width=20, command=addbal).place(x=50, y=330)
    buttonbalWithdraw = Button(showmain, text="WIHDRAW MONEY", bg='#057094', fg='white',width=20, command=delbal).place(x=250, y=330)
    buttonbalSHow = Button(showmain, text="SHOW STATUS", bg='#057094', fg='white',width=20, command=showbal).place(x=150, y=390)

    showmain.mainloop()
except Exception as e:
    print("Exception : ", e)