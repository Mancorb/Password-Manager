from tkinter import *
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import sqlite3
import numpy as np
import base64
from hashlib import md5
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Encription_Factory():
    def __init__(self):
        self.word = ""

    def encryptMain(self):
        """Encrypts a word with matrix multiplication

        Args:
            word (string): word to encrypt

        Returns:
            string: encrypted result
        """
        options = list("1234567890-=!@#$%^&*()_+qwertyuiop[]asdfghjkl;zxcvbnm,./QWERTYUIOP{|}ASDFGHJKL:ZXCVBNM<>?`~")
        res = ""
        while len(res) < len(self.word):
            C = self._obtainC(self.word,len(options))
            for i in C:
                res +=options[i] 

        return str(res)
    def _obtainC (self,n):
        """Returns the encrypted result of a word's character
        Args:
            word (String): letter to encrypt
        Return:
            string: encrypted letter

        """
        K = self._obtainK(P)
        P = self._obtainP(self.word)
        C = np.array(np.matmul(K,P))
        for i in range (len(C)):
            C[i]= (C[i]% n)

        return C
    def _obtainK(self,P):
        """Generate the K matrix, the number of cols must be equal to n which is the number of letters in P."

        Args:
            P (string): string value of P

        Returns:
            K matrix.
        """
        n = len(P)
        K = [] #store the matrix
        temp = [] # row of matrix
        switch= False

        counter = 2
        for row in range(n):
            for column in range(n):
                temp.append(int((P[row]/counter)*100))

                if switch:
                    counter -= 1.5
                else:
                    counter += 1.5
            K.append(temp)
            temp = []
            switch = not switch

        return np.array(K)
    def _obtainP(self):
        """Convert a word into ASCII value

        Args:
            word (string): Word to convert

        Returns:
            list: Converted values.
        """
        word = [self.word]
        P = [ord(ele) for sub in word for ele in sub]
        return P

    def getHashVal(self,text):
        """Returns hash value of a string

        Args:
            text (String): text to convert to hash

        Returns:
            String: string of hash object decrypted from byte form
        """
        return md5(bytes(text, 'utf-8')).hexdigest()

    #create an encription key
    def keyCreator(self,pswd):
        """Creates encription and decription key based on user input

        Args:
            pswd (String): user input of the password
        """
        password = pswd.encode()  # Convert to type bytes
        salt = self.getHashVal(pswd)
        salt = salt.encode()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))  # variable key will now have the value of a url safe base64 encoded key.
    
    #encript text with key
    def encryptor(self,key,text):
        """Encrypts the input text with the key using cryptography Fernet

        Args:
            key (bytes): key to encript the text
            text (String): Text to encript

        Returns:
            String: Encripted version of the text
        """
        f = Fernet(key)
        return f.encrypt(text.encode()).decode("utf-8")
    
    #decript text with key 
    def decryptor(key,target):
        """Decrypts the input text with the key using cryptography Fernet

        Args:
            key (bytes): key to encript the text
            text (String): Text to Decript

        Returns:
            String: Decripted version of the text
        """
        f = Fernet(key)
        return f.decrypt(target).decode("utf-8") 


    #The frame where all the content of the program will be placed

class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.encryption_obj = Encription_Factory()

        custom_font = ctk.CTkFont()
        

        #Create a ancor the tab in the top left corner
        self.TabSection = ctk.CTkTabview(self,
                                         anchor="nw",
                                         segmented_button_fg_color="#242732")
        
        self.TabSection.pack(fill = "both", expand = 1) # make it fill the screen
        self.TabSection._segmented_button.configure(text_color="white", fg_color = "grey", font = custom_font)

        #Declare the tabs
        self.search_Tab = self.TabSection.add("Search")
        self.register_Tab = self.TabSection.add("Add new")

        #content of the search tab
        


class Login_Register_Frame(ctk.CTkToplevel):

    #TODO: add a way to close all the app if this page is closed by the user without loggin in
    # Current phase: Create Account Logic


    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.encryption_obj = Encription_Factory()

        self.geometry("420x570")
        self.grab_set()#Method to for the user to use this page and inactivate the other page

        #setup the variables
        self.title_font = ctk.CTkFont(family="@Adobe Gothic Std B",size= 45)
        self.text_font = ctk.CTkFont(family="Arial Rounded MT Bold", size = 12)
        self.button_font = ctk.CTkFont(family="Arial Rounded MT Bold", size = 20)
        self.disclaimer_font = ctk.CTkFont(family="Segoe UI Variable Display Semib", size = 13)
        self.username = ""
        self.background_color= '#242525'

        self.registerVerification()


    def registerVerification(self):
        """Verify if there is already a registered user in the sistem
        """
        command= "SELECT COUNT(username) FROM Authentification;"
        number_rows = self.execute(command,True)[0][0]

        if number_rows==0:
            self.runRegistration()

        else:
            self.runLogin()

    def execute(self,command, result = False):
        """Run SQL command in the database
        Args:
            connection (sqlite obj): object with connection to the sqlite DB
            command (string): sqlite command in string
        """
        #Create connection to database
        connection = sqlite3.connect('Archive.db')

        try:
            cursor=connection.cursor()
            cursor.execute(command)
            connection.commit()

            if result:
                results = cursor.fetchall()

        except Exception as e:
            CTkMessagebox(title="Error", message=e, icon="cancel")
        
        connection.close()

        if result:
            return results

    def runLogin(self):
        loginFrame = Frame(self,background =self.background_color)

        username = self.execute("SELECT username FROM Authentification;", True)[0][0]

        check_var = ctk.StringVar(value = "on")

        def checkbox_event():
            state = check_var.get()
            if state == "on":
                self.password_input.configure(show = "*")
            else:
                self.password_input.configure(show = "")

        #Set up page interior
        titleLabel = ctk.CTkLabel(self, text = "Login", font = self.title_font, justify="left")
        titleLabel.place(relx = 0.1, rely = 0.05,anchor = NW)

        username_Label = ctk.CTkLabel(master = self,
                                           text = username,
                                           font= self.title_font,
                                           justify = "center")
        
        self.password_input = ctk.CTkEntry(master = loginFrame,
                                            bg_color="transparent",
                                            text_color="orange",
                                            placeholder_text="Password", 
                                            placeholder_text_color="white", 
                                            border_width=1,
                                            border_color="orange",
                                            fg_color=self.background_color,
                                            width = loginFrame.winfo_screenmmwidth(),
                                            font = self.text_font,
                                            show = "*")
        
        checkbox = ctk.CTkCheckBox(master=loginFrame,
                                   text="Hide Password", 
                                   variable=check_var,
                                   command=lambda: checkbox_event(),
                                   onvalue="on",
                                   offvalue="off")
        
        login_Button = ctk.CTkButton(master = loginFrame,
                                     text="Login",
                                     text_color="white",
                                     fg_color="#fa820b", 
                                     font = self.button_font,
                                     hover_color = "#c56200",
                                     command=lambda: self.check_credencials())
        
        username_Label.place(relx = 0.1, rely = 0.2,anchor=NW)
        self.password_input.pack()
        checkbox.pack(side= "right")
        login_Button.pack(side = "bottom",pady = 20)
        loginFrame.pack(anchor = CENTER,expand = True, pady=20)
        

    def runRegistration(self):
        
        registerFrame = Frame(self,background =self.background_color)

        #Set up page interior
        self.titleLabel = ctk.CTkLabel(self, text = "Create\nAccount", font = self.title_font, justify="left")
        self.titleLabel.place(relx = 0.1, rely = 0.05,anchor = NW)

        self.disclaimerLabel = ctk.CTkLabel(master = registerFrame,
                                            text="Disclaimer: The password you use cannot be currently recovered. Thus we suggest a STRONG PASSWORD TO REMEMBER. A future version of this program may include a 'recover password feature'.",
                                            font= self.disclaimer_font,
                                            text_color="grey",
                                            wraplength=390
                                            )

        self.username_input = ctk.CTkEntry(master = registerFrame,
                                            bg_color="transparent",
                                            text_color="orange",
                                            placeholder_text="Username", 
                                            placeholder_text_color="white",
                                            border_width=1,
                                            border_color="orange",
                                            fg_color=self.background_color,
                                            width = registerFrame.winfo_screenmmwidth(),
                                            font = self.text_font
                                            )

        self.password_input = ctk.CTkEntry(master = registerFrame,
                                            bg_color="transparent",
                                            text_color="orange",
                                            placeholder_text="Password", 
                                            placeholder_text_color="white", 
                                            border_width=1,
                                            border_color="orange",
                                            fg_color=self.background_color,
                                            width = registerFrame.winfo_screenmmwidth(),
                                            font = self.text_font
                                            )

        self.Register_Button = ctk.CTkButton(master = registerFrame,
                                            text="Register",
                                            text_color="white",
                                            fg_color="#fa820b", 
                                            font = self.button_font,
                                            hover_color = "#c56200",
                                            command=lambda: self.procedure()
                                            )
        
        #pad x and y
        x = 100
        y = 20
        #ipad x and ipady of entries
        i_x = 2
        i_y = 2
        #ipad x and y if button
        b_x = 1
        b_y = 5
        ctk.CTkLabel(master = registerFrame, text = "").pack(pady = y*2)
        self.username_input.pack(side = "top", ipadx = i_x, ipady = i_y, padx = x, pady = y)

        self.password_input.pack(side = "top", ipadx = i_x, ipady = i_y, padx = x, pady = y)
        self.disclaimerLabel.pack(side = "top",padx=0, pady =0)

        self.Register_Button.pack(side = "top", ipadx = b_x, ipady = b_y, padx = x, pady = y+20)

        registerFrame.pack(anchor =CENTER, expand = True, pady=60)
    
    def procedure(self):

        def verifyInput(username, password):
            if not username or not password: 
                CTkMessagebox(title="Error Missing Input", message="Please fill in all the inputs", icon="cancel")
                #Mark the entries as red if they are missing and make them orange again if they have an input
                if not username:
                    self.username_input.configure({"border_color": "red"})
                else:
                    self.username_input.configure({"border_color": "orange"})

                if not password:
                    self.password_input.configure({"border_color": "red"})
                else:
                    self.password_input.configure({"border_color": "orange"})

                return False

            return True

        # get the imputs
        username = self.username_input.get()
        password = self.password_input.get()

        if verifyInput(username,password):
            self.register_in_DB(username,password)
            self.restore()

    def restore(self):
        """Gives control back to the main page of the program
        """
        self.grab_release()
        self.destroy()

    def register_in_DB(self, user, password):

        self.encryption_obj.text = password

        command = f"INSERT INTO Authentification VALUES('{user}','{self.encryption_obj.getHashVal(self.encryption_obj.encryptMain())}')"
        self.execute(command)
        



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)

        ctk.set_appearance_mode("dark")

        self.toplevel_window = None

        self.mainFrame = MainFrame(self)
        self.mainFrame.pack(fill = "both", expand = 1)


        self.open_login_toplevel()

        

    def open_login_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Login_Register_Frame(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it



app = App()
app.mainloop()