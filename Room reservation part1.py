from tkinter import *
import pymysql
import urllib.request
import string

class database:
    def __init__(self,w):
        self.mainWin=w
        self.LoginPage(self.mainWin)
        self.Register()
        self.db=self.Connect()
        
        

    def LoginPage(self,w):
        self.url = "http://singhose.marc.gatech.edu/cranewebpage/images/georgia-tech.gif"
        response = urllib.request.urlopen(self.url)
        myPicture = response.read()
        import base64
        b64_data = base64.encodebytes(myPicture)
        self.photo = PhotoImage(data=b64_data)
        self.eU=StringVar()
        self.eP=StringVar()
        Label(self.mainWin,image=self.photo).grid(row=0,column=0,columnspan=5,sticky=EW)
        Label(self.mainWin,text="Username").grid(row=1,column=0,sticky=E)
        Label(self.mainWin,text="Password").grid(row=2,column=0,sticky=E)
        Entry(self.mainWin,textvariable=self.eU,width=30).grid(row=1,column=1,columnspan=3)
        Entry(self.mainWin,textvariable=self.eP,width=30).grid(row=2,column=1,columnspan=3)
        Button(self.mainWin,text="Rigister",command=self.win2up).grid(row=3,column=2,sticky=EW)
        Button(self.mainWin,text="Login",command=self.LoginCheck).grid(row=3,column=3,sticky=EW)
        Button(self.mainWin,text="Exit",command=self.endProgram).grid(row=3,column=4,sticky=EW)

    def Register(self):
        self.eLa=StringVar()
        self.eUs=StringVar()
        self.ePa=StringVar()
        self.eCP=StringVar()
        self.secondWin = Toplevel()
        self.secondWin.title("Room Reservation New User Registration")
        Label(self.secondWin,image=self.photo).grid(row=0,column=0,columnspan=4,sticky=EW)
        Label(self.secondWin,text="Last Name").grid(row=1,column=0,sticky=W)
        Label(self.secondWin,text="Username").grid(row=2,column=0,sticky=W)
        Label(self.secondWin,text="Password").grid(row=3,column=0,sticky=W)
        Label(self.secondWin,text="Confirm Password").grid(row=4,column=0,sticky=E)
        Entry(self.secondWin,textvariable=self.eLa,width=30).grid(row=1,column=1,columnspan=2)
        Entry(self.secondWin,textvariable=self.eUs,width=30).grid(row=2,column=1,columnspan=2)
        Entry(self.secondWin,textvariable=self.ePa,width=30).grid(row=3,column=1,columnspan=2)
        Entry(self.secondWin,textvariable=self.eCP,width=30).grid(row=4,column=1,columnspan=2)
        Button(self.secondWin,text="Cancel",command=self.win1up).grid(row=5,column=2,sticky=EW)
        Button(self.secondWin,text="Register",command=self.RegisterNew).grid(row=5,column=3,sticky=EW)
        self.secondWin.withdraw()
        self.secondWin.protocol("WM_DELETE_WINDOW", self.endProgram)


    def Connect(self):
        try:
            db = pymysql.connect(
                host="academic-mysql.cc.gatech.edu",
                user="yyao71",   passwd = "gLpo7jCE",
                db="cs2316db")
            return db
        except:
            messagebox.showerror("ERROR", "Please check your Internet Connection!")
            return None


    def endProgram(self):
        self.mainWin.destroy()

    def win1up(self):
        self.secondWin.withdraw()
        self.mainWin.deiconify()

    def win2up(self):
        self.mainWin.withdraw()
        self.secondWin.deiconify()


    def RegisterNew(self):
        self.lastName=self.eLa.get()
        self.userName=self.eUs.get()
        self.password=self.ePa.get()
        self.password2=self.eCP.get()
        if len(self.userName)==0 or len(self.password)==0:
            messagebox.showerror("ERROR", "Username&password needed.")
            return None
        if len(self.userName)> 15:
            messagebox.showerror("ERROR", "Maximum username length: 15 characters.")
            return None
        
        if self.password != self.password2:
            messagebox.showerror("ERROR", "Passwords don't match.Try again.")
            return None
        
        self.countN=0
        self.countL=0
        for char in self.password:
            if char in "0123456789":
                self.countN=self.countN+1
            if char in string.ascii_uppercase:
                self.countL=self.countL+1
        if self.countN==0 or self.countL==0:
            messagebox.showerror("ERROR", "Please include as least one letter and one number in your password. Try again.")
            return None
        self.c = self.db.cursor()
        self.sql = """SELECT Username FROM ReservationUser"""
        self.c.execute(self.sql)
        self.data = self.c.fetchall()
        self.userList=[]
        for item in self.data:
            itemN=""
            for char in item:
                itemN=itemN+char.lower()
            self.userList.append(itemN)
        
        self.username=""
        for char in self.userName:
           self.username=self.username+char.lower()
        if self.username in self.userList:
            print("yes")
            messagebox.showerror("ERROR", "Username already exists, use another one.")
            return None
        self.sql2="""INSERT INTO ReservationUser(Username,Password,LastName)
                      VALUES(%s,%s,%s)
                   """
        self.c.execute(self.sql2,(self.userName,self.password,self.lastName))
        self.db.commit()
        self.c.close()
        messagebox.showinfo("", "Registered")
        self.win1up()
        

    def LoginCheck(self):
        self.cs=self.db.cursor()
        self.u=self.eU.get()
        self.p=self.eP.get()
        try:
            self.sqL=""" SELECT Password FROM ReservationUser
                          WHERE Username=%s
                      """
            self.cs.execute(self.sqL,self.u)
            self.dataL=self.cs.fetchall()
            if self.p==self.dataL[0][0]:
                messagebox.showinfo("", "Logged in!")
                self.db.close()
                self.endProgram()
                
            else:
                messagebox.showerror("ERROR", "Urecognizable username/password combination")
                return None
        except:
            messagebox.showerror("ERROR", "Urecognizable username/password combination")
            return None


w=Tk()
w.title("Login")
app=database(w)
w.mainloop()


