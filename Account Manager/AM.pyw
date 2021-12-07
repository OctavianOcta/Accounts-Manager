from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter.font as tkFont

from PIL import ImageTk, Image

import json
from cryptography.fernet import Fernet
import ast

import win32gui, win32con

hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide , win32con.SW_HIDE)


FILENAME = "accounts.csv"


root = ThemedTk(theme="equilux")


class App:
    
    def __init__(self,decrypted_data3):
        self.account = {}
        self.acc_lis = decrypted_data3
        self.mini_frame = Frame()
        self.acc = {}
        
        self.fontStyle = tkFont.Font(family="Lucida Grande", size=14)
        
        root.title("Account Manager")
        root.geometry("800x600")
        root.grid_rowconfigure(0, weight=1)
        root.rowconfigure(1,weight=1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        
        # keeps place of the root so i can expend it all the way with the colors
        
        root3 = ttk.Frame(root)
        root3.pack(anchor=N, fill=BOTH, expand=True )
        
        
        
        # root2 has all the contents
        root2 = ttk.LabelFrame(root)
        root2.place(in_ = root3, anchor = "c", relx = .5, rely = .5)
       
        
        home_display = ttk.Frame(root2, width=800, height=540)
        home_display.grid(row= 0, column= 0, columnspan=3)

        self.frame = home_display
        
        add_menu = ttk.Frame(root2, width=800, height=540)
        search_menu = ttk.Frame(root2, width=800, height=540)
        remove_menu = ttk.Frame(root2, width=800, height=540)

        add = ttk.Button(root2, text="Add an account", command= lambda: self.addMenu(add_menu))
        search = ttk.Button(root2, text="Search for an account",command= lambda: self.searchMenu(search_menu))
        remove = ttk.Button(root2, text="Remove an account", command= lambda: self.removeMenu(remove_menu))

        add.grid(row=1,column=0,pady= 20)
        search.grid(row=1, column=1,pady=20)
        remove.grid(row=1, column=2,pady=20)

    def print_b(self):
        print(self.acc_lis)
    
    
    def return_data(self):
        return self.acc_lis    
    
    def raise_frame(self,frame2):
        self.frame.grid_forget()
        self.mini_frame.place_forget()
        frame2.columnconfigure(0, weight=1)
        frame2.columnconfigure(1, weight=3)
        frame2.grid(row=0,column = 0, columnspan= 3)

        frame2.grid_propagate(0)
        self.frame = frame2

    def getting_info(self,web_e,email_e,nick_e,pwd_e):
        self.account['website'] = web_e.get()
        self.account['email'] = email_e.get()
        self.account['nickname'] = nick_e.get()
        self.account['password'] = pwd_e.get()
        
        web_e.delete(0,END)
        email_e.delete(0,END)
        nick_e.delete(0,END)
        pwd_e.delete(0,END)
    
        self.append_data()
    
    def append_data(self):
 
        acc = {}
        acc['website'] = self.account['website']
        acc['email'] = self.account['email']
        acc['nickname'] = self.account['nickname']
        acc['password'] = self.account['password']
        self.acc_lis.append(acc)
        

        
    def addMenu(self,frame2):
        self.raise_frame(frame2)
        frame3 = ttk.Frame(frame2)
        frame3.place(in_=frame2, anchor="c", relx=.5, rely=.5)

        website = ttk.Label(frame3, text="Website: ", )
        web_e = ttk.Entry(frame3,width=35)
        
        email = ttk.Label(frame3, text="Email: ")
        email_e = ttk.Entry(frame3,width=35)
        
        nickname = ttk.Label(frame3, text="Nickname: ")
        nick_e = ttk.Entry(frame3,width=35)
        
        password = ttk.Label(frame3, text="Password: ")
        pwd_e = ttk.Entry(frame3,width=35)
        
        website.grid(row=0,column=0,pady=15)
        web_e.grid(row=0,column=1)
        
        email.grid(row=1,column=0,pady=15)
        email_e.grid(row=1,column=1)
        
        nickname.grid(row=2,column=0,pady=15)
        nick_e.grid(row=2,column=1)
        
        password.grid(row=3,column=0,pady=15)
        pwd_e.grid(row=3,column=1)

        
        submit = ttk.Button(frame3, text="Submit",command= lambda: self.getting_info(web_e,email_e,nick_e,pwd_e))
        
        #check = ttk.Button(frame3,text="check", command=self.print_b)
        #check.grid(row=4, column=0)
        submit.grid(row=4,column=1,sticky = "E",padx=20,pady=20)
        
        web_e.delete(0,END)
        email_e.delete(0,END)
        nick_e.delete(0,END)
        pwd_e.delete(0,END)
        

    def searchMenu(self,frame2):
        self.raise_frame(frame2)
        frame3 = ttk.Frame(frame2,width=800, height=500)
        frame3.place(in_=frame2, anchor="c", relx=.5, rely=.5)
        

        search_by = ttk.Label(frame3, text="Type in the name of the website that you need the account for.")
        search = ttk.Entry(frame3,width=35)
        self.mini_frame = frame3
        srcb = ttk.Button(frame3, text="Search", command= lambda: self.get_account(search, self.mini_frame))
        search_by.grid(row= 0, column= 0,columnspan=2)
        search.grid(row=1, column=0, pady= 25,columnspan=2)
        srcb.grid(row=2, column=0, pady=50,columnspan=2)
        
        search.delete(0,END)
        
    
        
    def get_account(self,search,frame):
        web_n = search.get()
        
        self.account_searching(web_n, frame)
    
    def account_searching(self,search_option_value, frame, value = 'website'):
  
        counter = 0
            
        for acc in self.acc_lis:
            if acc[value].lower().strip() == search_option_value.lower().strip():
                #print("")
                #title_label = Label(frame, text="The account that you are searching for is:")
                
                web = ttk.Label(frame, text="Website: " )
                text = str(acc['website'])
                web_inf = ttk.Label(frame, text = text)
                
                email = ttk.Label(frame,text="Email: ")
                text = str(acc["email"])
                email_inf = ttk.Label(frame,text= text)
                
                nick = ttk.Label(frame, text = "Nickname: ")
                text = str(acc['nickname'])
                nick_inf = ttk.Label(frame, text = text)
                
                pwd = ttk.Label(frame, text= "Password: ")
                text = str(acc['password'])
                pwd_info = ttk.Label(frame, text= text)

                #title_label.grid(row=3, column=0)
                
                web.grid(row= 4, column = 0)
                web_inf.grid(row=4, column=1)
                
                email.grid(row=5, column=0)
                email_inf.grid(row=5, column=1)
                
                nick.grid(row=6, column=0)
                nick_inf.grid(row=6, column=1)
                
                pwd.grid(row=7, column=0)
                pwd_info.grid(row=7, column=1)
                
                self.acc = acc
                break
                        
            else:
                counter += 1
                
        if counter == len(self.acc_lis):
            
            l1 = ttk.Label(frame, text = "We couldn't find your account." ,padx=20)
            l2 = ttk.Label(frame, text= "You can (re)add the account into the 'Add' section.",padx=20)
            l1.grid(row=4, column=0)
            l2.grid(row=5, column=0)
    
    def account_deleted(self,frame2,upframe,dnframe):
        upframe.grid_forget()
        dnframe.grid_forget()
        self.raise_frame(frame2)
        self.raise_frame(frame2)
        
        frame = ttk.Frame(frame2)
        frame.place(in_=frame2, anchor="c", relx=.5, rely=.5)
        
        acc_deleted = ttk.Label(frame, text="Your account has been deleted.", font= self.fontStyle)
        acc_deleted.pack()
    
    def removeMenu(self,frame2):
        
        self.raise_frame(frame2)
        frame = ttk.Frame(frame2)
        frame.place(in_=frame2, anchor="c", relx=.5, rely=.5)
        frame.config( width=800, height=500)
         
        l1 = ttk.Label(frame, text = "Search for an account first.")
        l1.pack()
        
        if bool(self.acc):
            l1.pack_forget()
            
            upframe = ttk.Frame(frame)
            upframe.grid(row=0, column=0,pady=160,sticky="N")
            
            dnframe = ttk.Frame(frame)
            dnframe.grid(row=1, column=0,pady= 100,sticky="S")
            
            web = ttk.Label(upframe, text="Website: " , font = self.fontStyle)
            text = str(self.acc['website'])
            web_inf = ttk.Label(upframe, text = text, font = self.fontStyle)
                
            email = ttk.Label(upframe,text="Email: ", font = self.fontStyle)
            text = str(self.acc["email"])
            email_inf = ttk.Label(upframe,text= text, font = self.fontStyle)
                
            nick = ttk.Label(upframe, text = "Nickname: ", font = self.fontStyle)
            text = str(self.acc['nickname'])
            nick_inf = ttk.Label(upframe, text = text, font = self.fontStyle)
                
            pwd = ttk.Label(upframe, text= "Password: ", font = self.fontStyle)
            text = str(self.acc['password'])
            pwd_info = ttk.Label(upframe, text= text, font = self.fontStyle)

                #title_label.grid(row=3, column=0)
                
            web.grid(row= 1,column = 0,pady=5)
            web_inf.grid(row=1, column=1,padx=5)
                
            email.grid(row=2, column=0,pady=5)
            email_inf.grid(row=2, column=1,padx=5)
                
            nick.grid(row=3, column=0,pady=5)
            nick_inf.grid(row=3, column=1,padx=5)
                
            pwd.grid(row=4, column=0,pady=5)
            pwd_info.grid(row=4, column=1,padx=5)
            

            
            rusure = ttk.Label(dnframe, text= "Are you sure you want to delete the account?")
            delete = ttk.Button(dnframe, text="Delete", command= lambda: self.deleteAcc(frame2,upframe,dnframe))
            
            rusure.grid(row= 0, column=0)
            delete.grid(row=0, column=1)
            
            
        

    
    def deleteAcc(self,frame2,upframe,dnframe):
        
        for i in range(len(self.acc_lis)):
            if self.acc == self.acc_lis[i]:
                del self.acc_lis[i]
                #print(self.acc_lis)
                break
            
        self.acc = {}
        
        self.account_deleted(frame2,upframe,dnframe)
        
        
        
        
    def submit_button_pressed(self,web_e,email_e,nick_e,pwd_e,acc_lis):
        self.getting_info(web_e,email_e,nick_e,pwd_e)
        acc_lis = self.append_data(acc_lis,)
        
    
    
    


def getting_key():
       
        with open('test_key.key','rb') as file:
            key = file.read()       
        
        return key

def decrypting(key):
        
        
        with open(FILENAME, "rb") as encrypted_file:
            encrypted = encrypted_file.read()
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted)

        return decrypted_data

def bytes_to_dict(decrypted_data):
        
        decrypted_data2 = decrypted_data.decode("UTF-8")
        decrypted_data3 = ast.literal_eval(decrypted_data2)
        
        return decrypted_data3

def creating_a_list_with_all_the_accounts(decrypted_data3):
        
        acc_lis = decrypted_data3["accounts"]
        
        

def dict_to_bytes(data):
    
    user_encode_data = json.dumps(data).encode('utf-8')
    return user_encode_data

def encrypting(key,data):
    
  
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

 
    with open(FILENAME,'wb') as f:
        f.write(encrypted)


key = getting_key()
decrypted_data = decrypting(key)
decrypted_data3 = bytes_to_dict(decrypted_data)
#print(decrypted_data3)
ap = App(decrypted_data3)
root.mainloop()
data = ap.return_data()
user_encode_data = dict_to_bytes(data)
encrypting(key,user_encode_data)
