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
        try:
            self.homeWin.withdraw()
        except:
            self.secondWin.withdraw()
        self.mainWin.deiconify()

    def win2up(self):
        try:
            self.homeWin.withdraw()
        except:
            self.mainWin.withdraw()
        self.secondWin.deiconify()
        
    def homeWinup(self):
        try:
            self.selectWin.withdraw()
        except:
            self.secondWin.withdraw()
            self.mainWin.withdraw()
        self.homeWin.deiconify()

    def homeWinupp(self):
        self.sttWin.withdraw()
        self.homeWin.deiconify()


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
        self.Homepage()
        self.cs=self.db.cursor()
        self.u=self.eU.get()
        self.p=self.eP.get()
        try:
            self.sqL=""" SELECT Password FROM ReservationUser
                          WHERE Username=%s
                      """
            self.cs.execute(self.sqL,self.u)
            self.dataL=self.cs.fetchall()
            if self.p==self.dataL[0][0] and len(self.p)!=0:
                messagebox.showinfo("", "Logged in!")
                self.homeWinup()
                
                
            else:
                messagebox.showerror("ERROR", "Urecognizable username/password combination")
                return None
        except:
            messagebox.showerror("ERROR", "Urecognizable username/password combination")
            return None
        self.cs.close()

        
    def Homepage(self):
        self.homeWin = Toplevel()
        self.cr=StringVar()
        self.homeWin.title("Room Reservation Homepage")
        Label(self.homeWin,text="Welcome to GT Room Reservation System!",relief="raised").grid(row=0,column=1,columnspan=3,sticky=EW)
        Label(self.homeWin,text=" ").grid(row=1,column=0,sticky=EW)
        Label(self.homeWin,text="Current Reservations").grid(row=2,column=0,sticky=E)
        Entry(self.homeWin,textvariable=self.cr,state="readonly",width=50).grid(row=2,column=1,columnspan=4)
        Label(self.homeWin,text=" ").grid(row=3,column=0,sticky=EW)
        Label(self.homeWin,text=" ").grid(row=4,column=0,sticky=EW)
        Label(self.homeWin,text="Make New Reservations:").grid(row=5,column=0)
        self.fDay=Frame(self.homeWin,bd=1,relief=SUNKEN)
        self.fTime=Frame(self.homeWin,bd=1,relief=SUNKEN)
        self.fBldg=Frame(self.homeWin,bd=1,relief=SUNKEN)
        self.fFlr=Frame(self.homeWin,bd=1,relief=SUNKEN)
        self.fRoom=Frame(self.homeWin,bd=1,relief=SUNKEN)
        self.fDay.grid(row=6,column=0)
        self.fTime.grid(row=6,column=1)
        self.fBldg.grid(row=6,column=2)
        self.fFlr.grid(row=6,column=3)
        self.fRoom.grid(row=6,column=4)
        Label(self.homeWin,text=" ").grid(row=7,column=0,sticky=EW)

        Button(self.homeWin,text="Cancel All Reservation",command=self.cancelReservation).grid(row=8, column=0, sticky=EW)
        Button(self.homeWin,text="Check Available Options",command=self.availableReservations).grid(row=8, column=1, columnspan=2,sticky=EW)
        Button(self.homeWin,text="Stats",command=self.stats).grid(row=8, column=3, sticky=EW)
        Button(self.homeWin,text="Logout",command=self.win1up).grid(row=8, column=4, sticky=EW)

        
        Label(self.fDay,text="Day Choices").pack()
        Label(self.fTime,text="Time Choices").pack()
        Label(self.fBldg,text="Building Choices").pack()
        Label(self.fFlr,text="Floor Choices").pack()
        Label(self.fRoom,text="Room Choices").grid(row=0,column=0,columnspan=2)

        self.iv1 = IntVar()
        self.iv2 = IntVar()
        self.iv3 = IntVar()
        self.iv4 = IntVar()
        self.iv5 = IntVar()
        
        Radiobutton(self.fDay, text="Monday", variable=self.iv1, value=1).pack(anchor="w")
        Radiobutton(self.fDay, text="Tuesday", variable=self.iv1,value=2).pack(anchor="w")
        Radiobutton(self.fDay, text="Wednesday", variable=self.iv1,value=3).pack(anchor="w")
        Radiobutton(self.fDay, text="Thursday", variable=self.iv1,value=4).pack(anchor="w")
        Radiobutton(self.fDay, text="Friday", variable=self.iv1,value=5).pack(anchor="w")

        Radiobutton(self.fTime, text="Morning", variable=self.iv2, value=1).pack(anchor="w")
        Radiobutton(self.fTime, text="Afternoon", variable=self.iv2,value=2).pack(anchor="w")
        Radiobutton(self.fTime, text="Evening", variable=self.iv2,value=3).pack(anchor="w")
        Radiobutton(self.fTime, text="Night", variable=self.iv2,value=4).pack(anchor="w")

        Radiobutton(self.fBldg, text="CULC", variable=self.iv3, value=1).pack()
        Radiobutton(self.fBldg, text="Klaus", variable=self.iv3,value=2).pack()

        Radiobutton(self.fFlr, text="1", variable=self.iv4, value=1).pack()
        Radiobutton(self.fFlr, text="2", variable=self.iv4,value=2).pack()
        Radiobutton(self.fFlr, text="3", variable=self.iv4,value=3).pack()
        Radiobutton(self.fFlr, text="4", variable=self.iv4,value=4).pack()

        Radiobutton(self.fRoom, text="1", variable=self.iv5, value=1).grid(row=1, column=0)
        Radiobutton(self.fRoom, text="2", variable=self.iv5,value=2).grid(row=2, column=0)
        Radiobutton(self.fRoom, text="3", variable=self.iv5,value=3).grid(row=3, column=0)
        Radiobutton(self.fRoom, text="4", variable=self.iv5,value=4).grid(row=4, column=0)
        Radiobutton(self.fRoom, text="5", variable=self.iv5, value=5).grid(row=5, column=0)
        Radiobutton(self.fRoom, text="6", variable=self.iv5,value=6).grid(row=1, column=1)
        Radiobutton(self.fRoom, text="7", variable=self.iv5,value=7).grid(row=2, column=1)
        Radiobutton(self.fRoom, text="8", variable=self.iv5,value=8).grid(row=3, column=1)
        Radiobutton(self.fRoom, text="9", variable=self.iv5, value=9).grid(row=4, column=1)
        Radiobutton(self.fRoom, text="10", variable=self.iv5,value=10).grid(row=5, column=1)
        self.us=self.eU.get()
        self.cr2=StringVar()

        try:
            self.csr=self.db.cursor()
            self.sqlQ="""SELECT * FROM RoomReservations WHERE ReservedBy=%s"""
            self.csr.execute(self.sqlQ,self.us)
            self.dataQ=self.csr.fetchall()
            self.rec1=self.dataQ[0]
            self.cr.set("Room "+str(self.rec1[2])+" on "+self.rec1[0]+" floor "+str(self.rec1[1])+" is reserved for "+self.rec1[3]+" at "+str(self.rec1[4])+" hours")
            if len(self.dataQ)>1:
                Entry(self.homeWin,textvariable=self.cr2,state="readonly",width=50).grid(row=3,column=1,columnspan=4)
                self.rec2=self.dataQ[1]
                self.cr2.set("Room "+str(self.rec2[2])+" on "+self.rec2[0]+" floor "+str(self.rec2[1])+" is reserved for "+self.rec2[3]+" at "+str(self.rec2[4])+" hours")       
            
        except:
            self.cr.set("No Reservations")
            

        self.homeWin.withdraw()
        self.homeWin.protocol("WM_DELETE_WINDOW", self.endProgram)
        self.csr.close()




    def cancelReservation(self):
        self.C=self.db.cursor()
        self.sqln=""" SELECT NumberOfReservations FROM ReservationUser WHERE Username=%s
                   """
        self.sqll="""UPDATE ReservationUser SET NumberOfReservations=%s WHERE Username=%s
                """
        self.C.execute(self.sqln,self.us)
        self.datan=self.C.fetchall()
        self.rN=self.datan[0][0]
        if self.rN==0:
            messagebox.showerror("Error", "You have no reservation to delete")
            return None
        else:
            self.C.execute(self.sqll,(0,self.us))
        self.sqlD="""DELETE FROM RoomReservations WHERE ReservedBy=%s
                """
        self.C.execute(self.sqlD,self.us)

        self.db.commit()
        messagebox.showinfo("Cancellation Completion", "Congratulations!You have cancelled you previous reservation.")
        try:
            self.cr.set("NO Reservation")
            self.cr2.set(" ")
        except:
            pass
            
        self.C.close()

    def availableReservations(self):
        self.dayN=self.iv1.get()
        self.timeN=self.iv2.get()
        self.bldgN=self.iv3.get()
        self.flrN=self.iv4.get()
        self.roomN=self.iv5.get()
        if self.dayN==0 or self.timeN==0 or self.bldgN==0 or self.flrN==0 or self.roomN==0:
            messagebox.showerror("Search Failure", "Please choose a valid option from each category")
            return None
        self.dayL=[0,"Monday","Tuesday","Wednesday","Thursday","Friday"]
        self.timeL=[0,["08:00","09:00","10:00","11:00"],["12:00","13:00","14:00","15:00"],["16:00","17:00","18:00","19:00"],["20:00","21:00","22:00","23:00"]]
        self.bldgL=[0,"CULC","Klaus"]
        self.flrL=[0,1,2,3,4]
        self.roomL=[0,1,2,3,4,5,6,7,8,9,10]
        
        
        self.day=self.dayL[self.dayN]
        self.time=self.timeL[self.timeN]
        self.bldg=self.bldgL[self.bldgN]
        self.flr=self.flrL[self.flrN]
        self.room=self.roomL[self.roomN]

        self.csor=self.db.cursor()
        self.sqlC="""SELECT Time FROM RoomReservations WHERE Building=%s AND Floor=%s AND RoomNo=%s AND Day=%s"""
        self.csor.execute(self.sqlC,(self.bldg,self.flr,self.room,self.day))
        self.dataC=self.csor.fetchall()

        
        self.tList=[]
        self.okList=[]
        for t in self.dataC:
            self.tList.append(t[0])
        for t in self.time:
            if t not in self.tList:
                self.okList.append(t)
        if len(self.okList)==0:
            messagebox.showerror("Search Failure", "Sorry!But this room is unavailable for the selected day and time")
            return None

        self.C1=self.db.cursor()
        self.sqlnn=""" SELECT NumberOfReservations FROM ReservationUser WHERE Username=%s

                   """
        self.C1.execute(self.sqlnn,self.us)
        self.datann=self.C1.fetchall()
        self.rNN=self.datann[0][0]
        
        
        if self.rNN>=2:
            messagebox.showerror("Error", "You can only make 2 reservations per week. Try again next week")
            return None
        self.homeWin.withdraw()
        self.selectWin=Toplevel()
        self.selectWin.title("Available Rooms")
        Label(self.selectWin,text=" ").grid(row=0,column=0)

        Label(self.selectWin,text="Building",bd=1,relief="raised").grid(row=1,column=0)
        Label(self.selectWin,text="Floor",bd=1,relief="raised").grid(row=1,column=1)
        Label(self.selectWin,text="Room",bd=1,relief="raised").grid(row=1,column=2)
        Label(self.selectWin,text="Day",bd=1,relief="raised").grid(row=1,column=3)
        Label(self.selectWin,text="Time",bd=1,relief="raised").grid(row=1,column=4)
        Label(self.selectWin,text="Select",bd=1,relief="raised").grid(row=1,column=5)
        
        self.iv=IntVar()
        for i in self.okList:
            pos=self.okList.index(i)+2
            Label(self.selectWin,text=self.bldg).grid(row=pos,column=0)
            Label(self.selectWin,text=str(self.flr)).grid(row=pos,column=1)
            Label(self.selectWin,text=str(self.room)).grid(row=pos,column=2)
            Label(self.selectWin,text=self.day).grid(row=pos,column=3)
            Label(self.selectWin,text=i).grid(row=pos,column=4)
            Radiobutton(self.selectWin, text="", variable=self.iv, value=pos-1).grid(row=pos,column=5)
            

        Button(self.selectWin,text="Submit Reservation",command=self.makeReservation).grid(row=6,column=3,columnspan=2,sticky=EW)
        Button(self.selectWin,text="cancel",command=self.homeWinup).grid(row=6,column=5,sticky=EW)

        self.C1.close()
        self.selectWin.protocol("WM_DELETE_WINDOW", self.endProgram)
       
        
        
        
        
    def makeReservation(self):
        self.chooseT=self.okList[self.iv.get()-1]
        if self.chooseT==0:
            messagebox.showerror("Error", "Please select a time or cancel.")

        self.cc=self.db.cursor()
        
        self.sqlU="""INSERT INTO RoomReservations(Building,Floor,RoomNo,Day,Time,ReservedBy)
                      VALUES(%s,%s,%s,%s,%s,%s)
                """
        self.sqlA=""" SELECT NumberOfReservations FROM ReservationUser WHERE Username=%s
                   """
        
        self.cc.execute(self.sqlA,self.us)
        self.dataA=self.cc.fetchall()
        self.resnum=self.dataA[0][0]
        self.newNum=self.resnum+1
        
        self.cc.execute(self.sqlU,(self.bldg,self.flr,self.room,self.day,self.chooseT,self.us))
        

        self.sqlR="""UPDATE ReservationUser SET NumberOfReservations=%s WHERE Username=%s
                """

        self.cc.execute(self.sqlR,(self.newNum,self.us))
        
        self.db.commit()
        
        messagebox.showinfo("Reservation Completion", "Congratulations! You have reserved your room. Click OK to go back to Homepage.")
        
        self.homeWinup()

        try:
            self.csr1=self.db.cursor()
            self.sqlQ1="""SELECT * FROM RoomReservations WHERE ReservedBy=%s"""
            self.csr1.execute(self.sqlQ1,self.us)
            self.dataQ1=self.csr1.fetchall()
            self.rec11=self.dataQ1[0]
            self.cr.set("Room "+str(self.rec11[2])+" on "+self.rec11[0]+" floor "+str(self.rec11[1])+" is reserved for "+self.rec11[3]+" at "+str(self.rec11[4])+" hours")
            if len(self.dataQ1)>1:
                Entry(self.homeWin,textvariable=self.cr2,state="readonly",width=50).grid(row=3,column=1,columnspan=4)
                self.rec21=self.dataQ1[1]
                self.cr2.set("Room "+str(self.rec21[2])+" on "+self.rec21[0]+" floor "+str(self.rec21[1])+" is reserved for "+self.rec21[3]+" at "+str(self.rec21[4])+" hours")
                
            
        except:
            self.cr.set("No Reservations")

        self.cc.close()
        
        
        
            
    def stats(self):
        self.homeWin.withdraw()
        self.sttWin=Toplevel()
        self.sttWin.title("Statistics")
        self.en1=StringVar()
        self.en2=StringVar()
        Label(self.sttWin,text=" ").grid(row=0,column=0)
        Label(self.sttWin,text="The average number of reservations per person is:").grid(row=1,column=0,sticky=E)
        Label(self.sttWin,text="The busiest buiding").grid(row=2,column=0,sticky=E)
        Entry(self.sttWin,textvariable=self.en1,state="readonly",width=50).grid(row=1,column=1,columnspan=2)
        Entry(self.sttWin,textvariable=self.en2,state="readonly",width=50).grid(row=2,column=1,columnspan=2)
        Button(self.sttWin,text="Back",command=self.homeWinupp).grid(row=3,column=2,sticky=EW)


        self.curs=self.db.cursor()
        self.sqlrNum="""SELECT * FROM RoomReservations"""
        self.rNum=self.curs.execute(self.sqlrNum)

        self.sqlpNum="""SELECT * FROM ReservationUser"""
        self.pNum=self.curs.execute(self.sqlpNum)

        self.avg=self.rNum/self.pNum
        self.en1.set(self.avg)

        self.sqlCULC=""" SELECT * FROM RoomReservations WHERE Building="CULC" """
        self.CULC=self.curs.execute(self.sqlCULC)
        self.Klaus=self.rNum-self.CULC
        self.str=""
        if self.CULC > self.Klaus:
            self.str="CULC is more busy with "+str(self.CULC)+" reservations so far"
        elif self.Klaus > self.CULC:
            self.str="Klaus is more busy with "+str(self.Klaus)+" reservations so far"
        else:
            self.str="Both are busy with"++str(self.Klaus)+" reservations so far"
        self.en2.set(self.str)
        self.curs.close()

        self.sttWin.protocol("WM_DELETE_WINDOW", self.endProgram)



        
        


w=Tk()
w.title("Login")
app=database(w)
w.mainloop()


