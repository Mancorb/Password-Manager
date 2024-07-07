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

    def encryptMain(self, word):
        """Encrypts a word with matrix multiplication

        Args:
            word (string): word to encrypt

        Returns:
            string: encrypted result
        """
        options = list("1234567890-=!@#$%^&*()_+qwertyuiop[]asdfghjkl;zxcvbnm,./QWERTYUIOP{|}ASDFGHJKL:ZXCVBNM<>?`~")
        res = ""
        while len(res) < len(word):
            C = self._obtainC(word,len(options))
            for i in C:
                res +=options[i] 

        return str(res)


    def _obtainC (self,word,n):
        """Returns the encrypted result of a word's character
            Args:
                word (String): letter to encrypt
            Return:
                string: encrypted letter
        """
        P = self._obtainP(word)
        K = self._obtainK(P)
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

        
    def _obtainP(self,word):
        """Convert a word into ASCII value

        Args:
            word (string): Word to convert

        Returns:
            list: Converted values.
        """
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
        search_background_color = '#242525'
        """
        Order: 
        Title
        Search bar  | Search button | usr/site
        Results Table
        |Website  Username  Edit icon  copy icon|
        """
        #Title text:
        search_frame = Frame(self.search_Tab,background=search_background_color)

        search_title_Label = ctk.CTkLabel(self.search_Tab,text="Search Passwords", justify= "left")
        search_title_Label.place(relx = 0.1, rely = 0.05,anchor = NW)
        


class Login_Register_Frame(ctk.CTkToplevel):

    # root is "self"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encryption_obj = Encription_Factory()

        self.geometry("420x600")
        self.grab_set()#Method to for the user to use this page and inactivate the other page

        #setup the variables
        self.title_font = ctk.CTkFont(family="@Adobe Gothic Std B",size= 45, weight= "bold")
        self.text_font = ctk.CTkFont(family="Arial Rounded MT Bold", size = 12)
        self.button_font = ctk.CTkFont(family="Arial Rounded MT Bold", size = 20)
        self.disclaimer_font = ctk.CTkFont(family="Segoe UI Variable Display Semib", size = 13)
        self.username = ""
        self.background_color= '#242525'
        self.state = False #boolean to confirm registration or Login is successfull
        self.password = None

        self.protocol("WM_DELETE_WINDOW",self.close_procedure)

        self.registerVerification()


    def registerVerification(self):
        """Verify if there is already a registered user in the system
        """
        command= "SELECT COUNT(username) FROM Authentification;"
        number_rows = self.execute(command,True)[0][0]

        if number_rows==0:
            self.RunRegistration_Front()

        else:
            self.RunLogin_Front()


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


    def RunLogin_Front(self):
        loginFrame = Frame(self,background =self.background_color)

        username = self.execute("SELECT username FROM Authentification;", True)[0][0]

        check_var = ctk.StringVar(value = "on")


        def checkbox_event():
            """Checks the state of the checkbox, if it is 'on' then hide the input text, else show the input text
            """
            if check_var.get() == "on":
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
                                   offvalue="off",
                                   checkmark_color="orange",
                                   fg_color="grey",hover_color="white"
                                   )
        
        login_Button = ctk.CTkButton(master = self,
                                     text="Login",
                                     text_color="white",
                                     fg_color="#fa820b", 
                                     font = self.button_font,
                                     hover_color = "#c56200",
                                     command=lambda: self.login_procedure(),
                                     width = 120,
                                     height = 45)
        
        username_Label.place(relx = 0.1, rely = 0.2,anchor=NW)
        self.password_input.pack(pady=20, padx = 20)
        checkbox.pack(side= "right", padx = 15)
        
        loginFrame.pack(anchor = CENTER,expand = True, pady=200)
        login_Button.place(anchor = S,relx = 0.5, rely = 0.8)


    def login_procedure(self):
        
        self.password = self.password_input.get()

        if not self.password:
            CTkMessagebox(title="Error Missing Input", message="Please fill in the inputs", icon="cancel")
            self.password_input.configure({"border_color": "red"})

            return
        
        #Encrypt the password and check if it is the same as the one saved
        encrypted_pass = self.encryption_obj.getHashVal(self.encryption_obj.encryptMain(self.password))

        sql_com = "SELECT code FROM Authentification" 

        saved_pass = self.execute(command = sql_com, result= True)[0][0]

        # Check if its the same password as the one stored internally

        if saved_pass != encrypted_pass:
            hint_text = "Hint: " + self.execute("SELECT Hint FROM Authentification",True)[0][0]

            if len(hint_text)<7:
                hint_text = "Please try again"

            CTkMessagebox(title="Wrong password", message=hint_text, icon = "info")

            return
        
        else:
            self.restore()
        

    def RunRegistration_Front(self):
        
        registerFrame = Frame(self,background =self.background_color)

        #Set up page interior
        self.titleLabel = ctk.CTkLabel(self, text = "Create\nAccount", font = self.title_font, justify="left")
        self.titleLabel.place(relx = 0.1, rely = 0.05,anchor = NW)

        self.disclaimerLabel = ctk.CTkLabel(master = registerFrame,
                                            text="Disclaimer: The password you use cannot be currently recovered. Thus we suggest a STRONG PASSWORD TO REMEMBER.\nA future version of this program may include a 'recover password feature'.",
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

        self.hint_input = ctk.CTkEntry(master = registerFrame,
                                  bg_color="transparent",
                                  text_color="#ebd3b7",
                                  placeholder_text="Password hint",
                                  placeholder_text_color="#9c8d7c",
                                  border_width=1,
                                  border_color="#ebd3b7",
                                  fg_color=self.background_color,
                                  width = registerFrame.winfo_screenmmwidth(),
                                  font = self.text_font)

        self.Register_Button = ctk.CTkButton(master = registerFrame,
                                            text="Register",
                                            text_color="white",
                                            fg_color="#fa820b", 
                                            font = self.button_font,
                                            hover_color = "#c56200",
                                            command=lambda: self.register_Procedure()
                                            )
        
        #pad x and y
        x = 100
        y = 20
        #ipad x and ipady of entries
        i_x = 2
        i_y = 2
        #ipad x and y if button
        b_y = 10
        ctk.CTkLabel(master = registerFrame, text = "").pack(pady = y*2)
        self.username_input.pack(side = "top", ipadx = i_x, ipady = i_y, padx = x, pady = y)

        self.password_input.pack(side = "top", ipadx = i_x, ipady = i_y, padx = x, pady = y)

        self.hint_input.pack(side = "top", ipadx = i_x, ipady = i_y, padx = x, pady = y)

        self.disclaimerLabel.pack(side = "top",padx=0, pady =0)


        self.Register_Button.pack(side = "top", padx = x, pady = y, ipady = b_y)

        registerFrame.pack(anchor =CENTER, expand = True, pady=60)
    

    def register_Procedure(self):

        def verifyInput(username, password, hint):

            if not username or not password: 
                CTkMessagebox(title="Error: Missing Input", message="Please fill in all the inputs", icon="cancel")
                #Mark the entries as red if they are missing and make them orange again if they have an input
                if not username:
                    self.username_input.configure(border_color= "red")
                else:
                    self.username_input.configure(border_color= "orange")

                if not password:
                    self.password_input.configure(border_color = "red")
                else:
                    self.password_input.configure(border_color = "orange")

                return False

            if len(hint) > 149:
                CTkMessagebox(title="Error: Scace exeded", message="The hint has to be less than 150 characters long", icon="info")

                return False
            
            elif hint == password:
                CTkMessagebox(title="Error", message="The HINT can't be the SAME as the PASSWORD.", icon="info")
                return False

            return True

        # get the inputs
        username = self.username_input.get()
        self.password = self.password_input.get()
        hint = self.hint_input.get()

        if verifyInput(username,self.password,hint):
            self.register_in_DB(username,self.password,hint)
            self.restore()


    def restore(self):
        """Gives control back to the main page of the program
        """
        self.grab_release()
        #save input in the global variable
        master_password = self.password

        self.destroy()


    def register_in_DB(self, user, password, hint):

        if hint == None:
            hint = ""

        command = f"INSERT INTO Authentification VALUES('{user}','{self.encryption_obj.getHashVal(self.encryption_obj.encryptMain(password))}', '{hint}')"
        self.execute(command)

    def close_procedure(self):
        exit()


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

    


if __name__ == "__main__":
    #global password variable
    master_password=None
    app = App()
    app.mainloop()

"""
Notes:

Create a global password variable wich will be filled as soon as teh user puts in a correct login or registration
If the variable is still empty after closing the login or registration pages then close the entire app.

It is necesary to manipulate the exit funtion of tkinter
function logig:
obtain master password
if not masterpassword:
    clse the program using os (lookup the backdoor program in gitub)
"""