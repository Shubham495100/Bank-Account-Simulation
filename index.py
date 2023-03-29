from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

win=Tk()
win.state("zoome")
win.resizable(width=False,height=False)
win.configure(bg="blue")

con=sql.connect(database='bank.sqlite')
cur=con.cursor()
try:
    cur.execute("create table user(acn integer primary key autoincrement,name text,pass text,bal integer,mob text)")
    con.commit()
except Exception as e:
    print(e)
con.close()


title=Label(win,text="Bank Account simulation",font=('arial',60,'underline','bold'),bg="blue")
title.pack()

def login_frame():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.20,relwidth=1,relheight=.80)

    def forgot_click():
        frm.destroy()
        forgot_frame()

    def open_click():
        frm.destroy()
        open_form()
    
    def reset():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()

    def login():
        acn=e_acn.get()
        p=e_pass.get()
        if(len(acn)==0 or len(p)==0):
            messagebox.showerror("Validation","Please fill both fields!")
        elif(acn.isdigit()==False):
            messagebox.showerror("Validation","Account No must be Numeric!")
        else:
            con=sql.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from user where acn=? and pass=?",(acn,p))
            global loginrow
            loginrow=cur.fetchone()  #fetchone--> for only read one row
            if loginrow==None:
                messagebox.showerror('login',f"invalid username/password")
            else:
                frm.destroy()
                welcome_frame()
    lbl_acn=Label(frm,text="Account No",font=('arial',20,'bold'),bg='pink')
    lbl_acn.place(relx=.2,rely=.2)

    lbl_pass=Label(frm,text="Password",font=('arial',20,'bold'),bg='pink')
    lbl_pass.place(relx=.2,rely=.37)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=2)
    e_acn.place(relx=.35,rely=.2)
    e_acn.focus()

    e_pass=Entry(frm,font=('arial',20,'bold'),bd=2,show="*")
    e_pass.place(relx=.35,rely=.37)

    b_login=Button(frm,command=login,text="LOGIN",font=('arial',10,'bold'),bg='green')
    b_login.place(relx=.30,rely=.50,relwidth=.1,relheight=.05)

    b_reset=Button(frm,command=reset,text='RESET',font=('arial',10,'bold'),bg='orange')
    b_reset.place(relx=.50,rely=.50,relwidth=.1,relheight=.05)

    b_open=Button(frm,command=open_click,text='open account',font=('arial',10,'bold'),bg='light green')
    b_open.place(relx=.30,rely=.60,relwidth=.1,relheight=.05)

    b_fp=Button(frm,command=forgot_click,text='FORGOT PASSWORD',font=('arial',10,'bold'),bg='red')
    b_fp.place(relx=.50,rely=.60,relwidth=.1,relheight=.05)


def forgot_frame():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.20,relwidth=1,relheight=.8)

    def back_key():
        frm.destroy()
        login_frame()
    
    def reset():
        e_acn.delete(0,"end")
        e_mob.delete(0,"end")
        e_acn.focus()

    def recover():
        a=e_acn.get()
        m=e_mob.get()
        con=sql.connect(database='bank.sqlite')
        cur=con.cursor()
        cur.execute("select pass from user where acn=? and mob=?",(a,m))
        row=cur.fetchone()
        if row==None:
            messagebox.showerror("Recover!","Invalid account number/password")
        else:
            messagebox.showinfo("recover!",f"your pass:{row[0]}")
            frm.destroy
            login_frame()

    b_back=Button(frm,command=back_key,text='<--  BACK',font=('arial',10),bg='green')
    b_back.place(relx=.05,rely=.1,relheight=.05,relwidth=.1)

    lbl_acn=Label(frm,text='Account No',font=('arial',20,'bold'),bg='pink')
    lbl_acn.place(relx=.2,rely=.3)

    lbl_mob=Label(frm,text='Phone NO.',font=('arial',20,'bold'),bg='pink')
    lbl_mob.place(relx=.2,rely=.4)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=2)
    e_acn.place(relx=.4,rely=.3)

    e_mob=Entry(frm,font=('arial',20,'bold'),bd=2)
    e_mob.place(relx=.4,rely=.4)

    b_recover=Button(frm,command=recover,text='RECOVER',font=('arial',12,'bold'),bg='orange')
    b_recover.place(relx=.4,rely=.5)

    b_reset=Button(frm,command=reset,text='RESET',font=('arial',12,'bold'),bg='yellow')
    b_reset.place(relx=.5,rely=.5)


def open_form():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.2,relheight=.8,relwidth=1)

    def back_key():
        frm.destroy()
        login_frame()

    def submit():
        n=e_name.get()
        p=e_pass.get()
        m=e_phone.get()
        b=1000

        con=sql.connect(database='bank.sqlite')
        cur=con.cursor()
        cur.execute('insert into user(name,pass,bal,mob) values(?,?,?,?)',(n,p,b,m))
        con.commit()

        cur.execute("select max(acn) from user")

        acn=cur.fetchone()[0]
        con.close()
        messagebox.showinfo("Register",f"Account open with Account No.:{acn}")
        frm.destroy()
        login_frame()

    b_back=Button(frm,command=back_key,text='BACK',font=('arial',20,'bold'),bg='green')
    b_back.place(relx=.05,rely=.1,relwidth=.1,relheight=.05)

    l_name=Label(frm,text='Full Name',font=('arial',20,'bold'),bg='pink')
    l_name.place(relx=.2,rely=.3)

    e_name=Entry(frm,font=("arial",20,'bold'),bd=2)
    e_name.place(relx=.4,rely=.3)
    e_name.focus()

    l_phone=Label(frm,text="Phone Number",font=('arial',20,'bold'),bg='pink')
    l_phone.place(relx=.2,rely=.4)

    e_phone=Entry(frm,font=('arial',20,'bold'),bd=2)
    e_phone.place(relx=.4,rely=.4)

    l_pass=Label(frm,text="Password",font=('arial',20,'bold'),bg='pink')
    l_pass.place(relx=.2,rely=.5)

    e_pass=Entry(frm,font=('arial',20,'bold'),show='@',bd=2)
    e_pass.place(relx=.4,rely=.5)  

    b_submit=Button(frm,command=submit,text='SUBMIT',font=('arial',20,'bold'),bg='orange')
    b_submit.place(relx=.5,rely=.7,relwidth=.1,relheight=.05)

def welcome_frame():
    frm=Frame(win) 
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.2,relheight=1,relwidth=1)

    def back_key():
        frm.destroy()
        login_frame()
    
    def logout():
        frm.destroy()
        login_frame()
    
    def check_bal():
        frm=Frame(win)
        frm.configure(bg='pink')
        frm.place(relx=0,rely=.2,relwidth=1,relheight=.8)
        con=sql.connect(database='bank.sqlite')
        cur=con.cursor()
        cur.execute("select bal from user where acn=?",(loginrow[0],))
        bal=cur.fetchone()
        lbl_bal=Label(frm,text=f"available balance : {bal[0]}",font=('arial',20,'bold'),bg='pink')
        lbl_bal.place(relx=.4,rely=.4)

        def back_butt():
            frm.destroy()
            welcome_frame()

        b_back=Button(frm,command=back_butt,text='back',font=("arial",20,'bold'),bg='green')
        b_back.place(relx=.8,rely=.07,relwidth=.1,relheight=.05)
        


    
    welcome_lbl=Label(frm,text=f'welcome,{loginrow[1]}',font=('arial',20,'bold'),bg='pink')
    welcome_lbl.place(relx=.1,rely=.15)

    def deposit():
        frm=Frame(win)
        frm.configure(bg='pink')
        frm.place(relx=0,rely=.2,relwidth=1,relheight=.8)
        

        def back_butt():
            frm.destroy()
            welcome_frame()
        def final_deposit():
            amnt=int(e_amnt.get())
            con=sql.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("update user set bal=bal+? where acn=?",(amnt,loginrow[0]))
            con.commit()
            con.close()
            messagebox.showinfo("deposite",'amount deposited')
            frm.destroy()
            welcome_frame()


        b_back=Button(frm,command=back_butt,text='back',font=("arial",20,'bold'),bg='green')
        b_back.place(relx=.05,rely=.05,relwidth=.1,relheight=.05)


        lbl_amnt=Label(frm,text='Enter Amount:',font=('arial',20,'bold'),bg='pink')
        lbl_amnt.place(relx=.1,rely=.4)

        e_amnt=Entry(frm,font=("arial",20,'bold'),bd=2)
        e_amnt.place(relx=.3,rely=.4)

        b_deposit=Button(frm,command=final_deposit,text='Deposite',font=('arial',20,'bold'),bg='green')
        b_deposit.place(relx=.6,rely=.4)

    #transfer
    def transfer():
        frm=Frame(win)
        frm.configure(bg='pink')
        frm.place(relx=0,rely=.2,relwidth=1,relheight=.8)
        

        def back_butt():
            frm.destroy()
            welcome_frame()

        def final_transfer():
            amt=int(e_amnt.get())
            to=int(e_acn.get())


            con=sql.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select bal from user where acn=?",(loginrow[0],))
            bal=cur.fetchone()[0]
            con.close()

            con=sql.connect('bank.sqlite')
            cur=con.cursor()
            cur.execute("select * from user where acn=?",(to,))
            to_ac=cur.fetchone()[0]
            con.close()
            if to_ac==None:
                messagebox.showerror('enter account no')
            else:
                if bal>amt:
                    con=sql.connect(database='bank.sqlite')
                    cur=con.cursor()
                    cur.execute("update user set bal=bal-? where acn=?",(amt,loginrow[0]))
                    cur.execute('update user set bal=bal+? where acn=?',(amt,to))
                    con.commit()
                    con.close()
                    messagebox.showinfo("deposite!",'Amount Transfered')
                else:
                    messagebox.showwarning("insufficient balance")

        b_back=Button(frm,command=back_butt,text='back',font=("arial",20,'bold'),bg='green')
        b_back.place(relx=.05,rely=.05,relwidth=.1,relheight=.05)

        lbl_acn=Label(frm,text='Enter account no:',font=('arial',20,'bold'),bg='pink')
        lbl_acn.place(relx=.1,rely=.2)

        lbl_amnt=Label(frm,text='Enter Amount:',font=('arial',20,'bold'),bg='pink')
        lbl_amnt.place(relx=.1,rely=.4)

        e_acn=Entry(frm,font=("arial",20,'bold'),bd=2)
        e_acn.place(relx=.3,rely=.2)

        e_amnt=Entry(frm,font=("arial",20,'bold'),bd=2)
        e_amnt.place(relx=.3,rely=.4)

        b_transfer=Button(frm,command=final_transfer,text="Transfer",font=('arial',20,'bold'),bg='green')
        b_transfer.place(relx=.4,rely=.5)
        
    def withdraw():
        frm=Frame(win)
        frm.configure(bg='pink')
        frm.place(relx=0,rely=.2,relheight=.8,relwidth=1)

        def back_butt():
            frm.destroy()
            welcome_frame()

        def f_withdraw():
            amt=int(e_amnt.get())

            con=sql.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select bal from user where acn=?",(loginrow[0],))
            bal=cur.fetchone()[0]
            con.close()
            if(bal>amt):
                con=sql.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("update user set bal=bal-? where acn=?",(amt,loginrow[0]))
                con.commit()
                con.close()
                messagebox.showinfo('done')
            else:
                messagebox.showwarning('insufficient bal')


        b_back=Button(frm,command=back_butt,text='back',font=("arial",20,'bold'),bg='green')
        b_back.place(relx=.05,rely=.05,relwidth=.1,relheight=.05)


        lbl_amnt=Label(frm,text='enter amount to withdraw',font=('arial',20,'bold'),bg='pink')
        lbl_amnt.place(relx=.2,rely=.3)

        e_amnt=Entry(frm,font=('arial',20,'bold'),bd=2)
        e_amnt.place(relx=.45,rely=.3)

        b_withdraw=Button(frm,command=f_withdraw,text='withdraw',font=('arial',20,'bold'),bg='green')
        b_withdraw.place(relx=.6,rely=.6)
    
    b_back=Button(frm,command=back_key,text='back',font=("arial",20,'bold'),bg='green')
    b_back.place(relx=.05,rely=.05,relwidth=.1,relheight=.05)

    b_withdraw=Button(frm,command=check_bal,text='check balance',font=('arial',20,'bold'),bg='green')
    b_withdraw.place(relx=.2,rely=.3,relwidth=.2,relheight=.05)

    b_deposit=Button(frm,command=deposit,text='Deposit',font=('arial',20,'bold'),bg='green')
    b_deposit.place(relx=.2,rely=.4,relwidth=.2,relheight=.05)

    b_withdraw=Button(frm,command=withdraw,text='withdraw',font=('arial',20,'bold'),bg='green')
    b_withdraw.place(relx=.2,rely=.5,relwidth=.2,relheight=.05)
    
    b_withdraw=Button(frm,command=transfer,text='transfer',font=('arial',20,'bold'),bg='green')
    b_withdraw.place(relx=.2,rely=.6,relwidth=.2,relheight=.05)

    b_transfer=Button(frm,command=logout,text='logout',font=('arial',20,'bold'),bg='green')
    b_transfer.place(relx=.8,rely=.05,relwidth=.1,relheight=.05)
    
login_frame()
win.mainloop()
