from tkinter import *
import tkinter.messagebox
import base64
import sqlite3
from tkinter import ttk
from random import randint
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from hashlib import md5
from cryptography.fernet import Fernet


global MASTER_KEY
global background_color

#--------------------------------------------------------
#methods
#UNIVERSAL METHODS
#-------------------------------------------------------------
#Get a new ID for the registry
def getID(cur):
    """Creates a new ID for the registry

    Args:
        cur (SQL cursor object): Database cursor

    Returns:
        int: registry ID
    """
    cur.execute("SELECT id FROM List ORDER BY id;")
    id=cur.fetchall()
    try:
        id=str(id)
        temp=''
        specialChars ="[](),'"
        for specialChar in specialChars:
            id=id.replace(specialChar,'')
        if id=='':
            return 1

        for i in id:
            if i !=' ':
                temp=temp+i
            if i==' ':
                temp=''
        return int(temp)+1
    except Exception as e:
        tkinter.messagebox.showerror("Error",e)
#hide all frames
def HideAllFrames():
    """Hide all the other windows
    """
    add_password_frame.pack_forget()
    search_password_frame.pack_forget()
    verify_password_frame.pack_forget()
    modify_data_frame.pack_forget()
    delete_data_frame.pack_forget()
    create_password_frame.pack_forget()
    register_frame.pack_forget()
    login_frame.pack_forget()
#obtain hash of String
def getHashVal(text):
    """Returns hash value of a string

    Args:
        text (String): text to convert to hash

    Returns:
        String: string of hash object decrypted from byte form
    """
    return md5(bytes(text, 'utf-8')).hexdigest()
#create an encription key
def keyCreator(pswd):
    """Creates encription and decription key based on user input

    Args:
        pswd (String): user input of the password
    """
    password = pswd.encode()  # Convert to type bytes
    salt = getHashVal(pswd)
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
def encryptor(key,text):
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


#creates a conection with data base and returns conection and cursor.
def SQLcon():
    
    con = sqlite3.connect("testbd.db")
    cur = con.cursor()
    data = [con,cur]
    return data
#comitts changes and closes conection to SQL file
def SQLclose(data):
    data.commit()
    data.close()
#-------------------------------------------------------------

#ADD PASSWORD Methods
#-------------------------------------------------------------
#Open add password menu
def OpenAddMenu():
    """Hide all the pages and load the 'add password' page
    """
    HideAllFrames()
    add_password_frame.pack(fill='both', expand=1)
    AddMenuStructure()
#Struture code for the Add Password Menu
def AddMenuStructure():
    """Structure of add menu screen
    """
    backcol=background_color
    frcolor = "black"
    #title
    titulo=Label(add_password_frame,text="Add Password",bg = backcol,fg = frcolor,font = font_title)#main title
    titulo.place(x=80, y=25)

    #input variables
    add_site=StringVar()
    add_user=StringVar()
    add_pass=StringVar()

    #user inputs label
    add_site_label=Label(add_password_frame,text="Site:", bg=backcol, fg = frcolor,font = font_normal)
    add_site_label.place(x=30, y=130)

    add_user_label=Label(add_password_frame,text="Username:", bg=backcol, fg = frcolor,font = font_normal)
    add_user_label.place(x=30, y=200)

    add_pass_label=Label(add_password_frame,text="Password:", bg=backcol, fg = frcolor,font = font_normal)
    add_pass_label.place(x=30, y=270)

    #user inputs
    add_site_entry = Entry(add_password_frame,textvariable=add_site,bg="white", font="Bebas_Neue 12")#web site info
    add_site_entry.place(x=90,y=135, height=25, width=340)

    add_user_entry = Entry(add_password_frame,textvariable=add_user,bg="white", font="Bebas_Neue 12")#username info
    add_user_entry.place(x=160,y=205, height=25, width=270)

    add_pass_entry = Entry(add_password_frame,textvariable=add_pass,bg="white", font="Bebas_Neue 12")#username info
    add_pass_entry.place(x=155,y=275, height=25, width=275)

    #button
    create_password_button = Button(add_password_frame,text="Add Password", width="12", height="1", command=lambda:NoticeAddPas(add_user,add_site,add_pass,add_pass_entry,add_user_entry,add_site_entry), bg="white",font="Bebas_Neue 19 bold")
    create_password_button.place(x=160,y=350)
#Check if all the inputs are valid and gives notification
def NoticeAddPas(user_info,site_info,pass_info,add_pass_entry,add_user_entry,add_site_entry):
    """Checks if the user made correct input to add a new password

    Args:
        user_info (Tkinter input info): username input content
        site_info (Tkinter input info): website input info
        pass_info (Tkinter input info): password input info
        add_pass_entry (Tkinter Entry): object control of password entry
        add_user_entry (Tkinter Entry): object control of username entry
        add_site_entry (Tkinter Entry): object control of website entry
    """
    user_info=user_info.get()
    site_info=site_info.get()
    pass_info=pass_info.get()
    if site_info=="" or user_info=="" or pass_info=="":
        tkinter.messagebox.showerror("Error",f"Please fill in all the data")
    else:
        add_pass_entry.delete(0, END)
        add_user_entry.delete(0, END)
        add_site_entry.delete(0, END)
        CommitComfirm(site_info,user_info,pass_info)
#Notify User data has been saved ---INCOMPLETE---
def CommitComfirm(site_data, user_data, pass_data):
    """Make a commitment in the databse with the input info values

    Args:
        site_data (String): data of the website
        user_data (String): Username
        pass_data (String): Password
    """
    password = encryptor(MASTER_KEY,pass_data)
    try:
        con,cur = SQLcon()
        id=getID(cur)

        cur.execute(f"INSERT INTO list VALUES('{site_data}','{user_data}','{password}',{id})")
        SQLclose(con)
        tkinter.messagebox.showinfo("Registry created",f"Data:\nSite: {site_data}\nUser: {user_data}\nPass: {pass_data}\nClick ok to continue")
    except Exception as e:
        tkinter.messagebox.showerror("ERROR",f"{e}")
    ReturnToAdd()
#Closes the screen and open the add password menu
def ReturnToAdd():
    """Closes the screen and open the add password menu
    """
    HideAllFrames()
    OpenAddMenu()
#-------------------------------------------------------------

#SEARCH PASSWORDS Methods
#-------------------------------------------------------------
#Open search password menu
def OpenSearchMenu():
    """Open search password menu
    """
    HideAllFrames()
    search_password_frame.pack(fill='both', expand=1)
    OpenSearchMenuStructure()
#Structure of the Search menu
def OpenSearchMenuStructure():
    """Setup the 'Search Menu' page
    """
    backcol="white"
    titulo=Label(search_password_frame,text="Search Password",bg = backcol,fg = "black",font = font_title)
    titulo.place(x=10, y=5)

    #input variables
    query=StringVar()
    currentvar=StringVar()

    #List of options
    options=['Site','User']

    #user inputs
    searcher = Entry(search_password_frame,textvariable=query,
                        bg=backcol, font="Bebas_Neue 12")#web site info

    searcher.place(x=10,y=70, height=30, width=300)

    #Dropbox
    filterinfo=OptionMenu(search_password_frame ,currentvar,options[0],options[1])
    
    #Set the current option
    currentvar.set(options[0])
  
    filterinfo.place(x=310,y=70, width=70, height=30)

    #button
    searchB= Button(search_password_frame,text="Search",
                    command=lambda:refresh(query.get(),
                    currentvar.get(),infotable), font="Bebas_Neue 12")
    searchB.place(x=380,y=70,width=70, height=30)

    #Remove selected
    deleteB= Button(search_password_frame,text="Delete",
                    command=lambda:openDeleteMenu(infotable.selection()),
                    font="Bebas_Neue 12")
    deleteB.place(x=400,y=440,width=70)
    #Copy selected
    copyB= Button(search_password_frame,text="Copy Selected",
                    command=lambda:copyRow(infotable.selection()),
                    font="Bebas_Neue 12")
    copyB.place(x=40,y=440, width=160)
    #Edit selected
    editB= Button(search_password_frame,text="Edit",
                    command=lambda:updateRow(infotable.selection()),
                    font="Bebas_Neue 12")
    editB.place(x=300,y=440,width=90)

    #table
    infotable=ttk.Treeview(search_password_frame, columns=(1,2,3), show="headings", height=5)
    infotable.column(1,width=30, anchor="c")
    infotable.column(2,width=210, anchor="c")
    infotable.column(3,width=230, anchor="c")
    infotable.heading(1,text="ID")
    infotable.heading(2,text="Web Site")
    infotable.heading(3,text="User name / email")
    infotable.place(x=10, y=120, height=300)

    sub=Label(search_password_frame,text="Options",bg = backcol,fg = "black",font = font_normal)
    sub.place(x=10, y=400)

    #----------------------------------------------------------------

    #menu config
    menubar= Menu(root)
    root.config(menu=menubar)

    #create menu item
    CreateMenu=Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Create", menu=CreateMenu)
    CreateMenu.add_command(label="Create Password", command=OpenCreateMenu)
    CreateMenu.add_separator()
    CreateMenu.add_command(label="Add Password", command=OpenAddMenu)

    #Search menu
    menubar.add_cascade(label="Search", command=OpenSearchMenu)

#Search button for the search table
def refresh(inputdata,type,table):
    """Search for the info the the database and returns the results on screen

    Args:
        inputdata (String): description of what to look for
        type (String): The name of the column to search in the table
        table (db object): object to control the database
    """
    for i in table.get_children():
        table.delete(i)
    try:
        if inputdata:
            sequence=f"SELECT * FROM list WHERE {type} LIKE '%{inputdata}%' ORDER BY id"
        else: sequence='SELECT * FROM list ORDER BY id'
        isrtDataInTbl(table,sequence)
    except Exception as e:
        tkinter.messagebox.showerror("Error",e)
        isrtDataInTbl(table)
#Inserts the obtained data from the DB into the TKinter table
def isrtDataInTbl(infotable,command=None):
    """Grab Query result and place it into the on screen table

    Args:
        infotable (_type_): _description_
        command (_type_, optional): _description_. Defaults to None.
    """
    if command:
        con,cur =SQLcon()
        #Run command
        cur.execute(command)
        rows = cur.fetchall()
        for dt in rows:
            infotable.insert('','end',iid=dt[3],values=(dt[3],dt[0],dt[1]))
        SQLclose(con)
    else:
        infotable.insert("",'end',text="L1",
                        values=('',"NONE","NONE",
                            "NONE"))
#Hide all screens and open the delete menu screen
def openDeleteMenu(cel):
    if cel:
        HideAllFrames()
        delete_data_frame.pack(fill='both',expand=1)
        cel=extractInfo(cel)
        DeleteMenuStructure(cel)
    else:tkinter.messagebox.showwarning("Warning","Nothing selected")
#Screen used to delete a registry
def DeleteMenuStructure(cel):
    backcol="red"
    #title
    titulo=Label(delete_data_frame,text="WARNING",bg = backcol,fg = "black",font = font_title)#main title
    titulo.place(x=140, y=15)
    
    text=Label(delete_data_frame,
                text="You are about to PERMANENTLY DELETE\nthis PASSWORD and all the related DATA!\nARE YOU SURE?",
                bg = backcol,fg = "black",font = 'Bebas_Neue 18 bold')
    text.place(x=10,y=120)

    #confirm Button
    ConfirmB=Button(delete_data_frame,text="YES", command=lambda:deleteRow(cel), font="Bebas_Neue 19 bold")
    ConfirmB.place(x=350,y=300,height=60, width=130)
    
    #deny Button
    DenyB=Button(delete_data_frame,text="NO",command=ReturnToSearch, font="Bebas_Neue 19 bold")
    DenyB.place (x=20,y=300,height=60, width=130)
#Deletes the selected row from the DB
def deleteRow(id):
    con,cur = SQLcon()
    try:
        cur.execute(f"DELETE FROM List WHERE id={id}")
        con.commit()
    except Exception as e:
        tkinter.messagebox.showerror("Error",e)
    con.close()
    ReturnToSearch()
#Copy the password of the selected Row
def copyRow(sel):
    try:
        root.clipboard_clear()
        con,cur = SQLcon()
        cur.execute(f'SELECT pass FROM List WHERE id = {sel[0]}')
        pswrd=cur.fetchone()
        pswrd=decryptor(MASTER_KEY,str(pswrd[0]))
        total=''
        for i in pswrd:
            if i!='(' and i!=')' and i != ',' and i != ' ' and i != '[' and i != ']':
                total=total+i
        root.clipboard_append(total)
        con.close()
    except Exception as e:
        tkinter.messagebox.showerror("Error","Nothing selected")
#Checks if any row is selected to modify
def updateRow(sel):
    try:
        id=extractInfo(sel[0])
        con,cur = SQLcon()
        data=['site','user','pass']
        counter=0
        for i in data:
            cur.execute(f"SELECT {i} FROM List WHERE id={id}")
            temp=cur.fetchone()
            data[counter]=extractInfo(temp)
            counter=counter+1
        openModifyMenu(data[1],data[0],data[2],id)

    except Exception as e:
        tkinter.messagebox.showwarning("Warning","Nothing selected")
        con.close()
    
    
#Hides all screens and shows the modify screen
def openModifyMenu(user,site, pswrd,id):
    HideAllFrames()
    modify_data_frame.pack(fill='both', expand=1)
    ModifyMenuStructure(user,site, pswrd,id)
#Structure of the Modify entry screen
def ModifyMenuStructure(user,site,pswrd,id):
    backcol="white"
    size=19
    #title
    titulo=Label(modify_data_frame,text="Modify",bg = backcol,fg = "black",font = font_title)#main title
    titulo.place(x=60, y=15)
    #variables
    InSite=StringVar()
    InSite.set(site)
    InUser=StringVar()
    InUser.set(user)
    InPwrd=StringVar()
    InPwrd.set(decryptor(MASTER_KEY,pswrd))
    #inputs to modify info
    OGsite=Label(modify_data_frame,text='Site:',bg = backcol,fg = "black",font= f'Bebas_Neue {size} bold')
    OGsite.place(x=20,y=90)
    NWsite=Entry(modify_data_frame,textvariable=InSite,font=font_normal)
    NWsite.place(x=20,y=130, width=370)

    OGuser=Label(modify_data_frame,text='User:',bg = backcol,fg = "black",font= f'Bebas_Neue {size} bold')
    OGuser.place(x=20,y=190)
    NWuser=Entry(modify_data_frame,textvariable=InUser,font=font_normal)
    NWuser.place(x=20,y=240, width=370)

    OGpwrd=Label(modify_data_frame,text='Password:',bg = backcol,fg = "black",font= f'Bebas_Neue {size} bold')
    OGpwrd.place(x=20,y=320)
    NWpass=Entry(modify_data_frame,textvariable=InPwrd,font='Bebas_Neue 10 bold')
    NWpass.place(x=20,y=370,width=370)
    
    #Change Button
    CancelB=Button(modify_data_frame,text="Cancel", command=ReturnToSearch, font="Bebas_Neue 19 bold")
    CancelB.place(x=20,y=410,height=60, width=130)
    #Apply Button
    ConfirmB=Button(modify_data_frame,text="Confirm",command=lambda:NoticeModification(InSite.get(), InUser.get(), InPwrd.get(), user,site, pswrd,id), font="Bebas_Neue 19 bold")
    ConfirmB.place(x=350,y=410,height=60, width=130)
#Notify the user that the data has been modified
def NoticeModification(site_data, user_data, pass_data,user,site, pswrd,id):
    warn=False
    if not site_data:
        site_data=site
        warn=True
    if not user_data:
        user_data=user
        warn=True
    if not pass_data:
        pass_data=decryptor(MASTER_KEY,pswrd)
        warn=True
    if warn: tkinter.messagebox.showwarning("Warning","The original information will be used to replace th empty input")
    con,cur = SQLcon()
    try:
        cur.execute(f"UPDATE List SET site='{site_data}',user='{user_data}',pass='{encryptor(MASTER_KEY,pass_data)}' WHERE id={id};")
        SQLclose(con)
        tkinter.messagebox.showinfo("UPDATED",'The database has been updated')
    except Exception as e:
        tkinter.messagebox.showerror("Error",e)
        con.close()
    OpenSearchMenu()
#Hides the current screen and shows the search screen again
def ReturnToSearch():
    HideAllFrames()
    OpenSearchMenu()
#delete any format symbols from the SQL result
def extractInfo(info):
    id=str(info)
    res=''
    for i in id:
        if i!='(' and i !=')' and i!=',' and i != "'":
            res=res+i
    return res
#-------------------------------------------------------------

#Create Password Page
def OpenCreateMenu():
    HideAllFrames()
    create_password_frame.pack(fill='both', expand=1)
    OpenCreateMenuStructure()

def OpenCreateMenuStructure():
    #variables
    site=StringVar()
    username=StringVar()
    textColor= "#242424"
    inputColor= "#ffffff" 

    #main page
    titulo=Label(create_password_frame,text="Create Password",bg = background_color,fg = textColor,font = font_title)#main title
    titulo.place(x=55, y=30)

    #user entries label
    site_label=Label(create_password_frame,text="Web Site:", fg=textColor, bg = background_color, font=font_normal)
    site_label.place(x=50,y=165)
    user_label=Label(create_password_frame,text="Username:", fg=textColor, bg = background_color, font=font_normal)
    user_label.place(x=40,y=255)
    #user entries
    site_entry = Entry(create_password_frame,textvariable=site,bg=inputColor, font="Bebas_Neue 12")#web site info
    user_entry = Entry(create_password_frame,textvariable=username,bg=inputColor, font="Bebas_Neue 19")#username
    site_entry.place(x=170,y=168, height=30, width=260)
    user_entry.place(x=170,y=260, height=30, width=260)

    #button for entry
    create_password_button = Button(create_password_frame,text="Create", width="10", height="1",
                                    command=lambda:Creator(site,username,site_entry,user_entry),
                                    bg=inputColor,font="Bebas_Neue 19 bold")
    create_password_button.place(x=175,y=360)
    

#CREATE PASSWORD Methods
#-------------------------------------------------------------
def Creator(site, username,entry_s,entry_u):
    NoticeCrtPas(site,username,CreatePass())
    entry_s.delete(0, END)
    entry_u.delete(0, END)

def CreatePass():
    lowerLetters=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    UpperLetters=['A', 'B', 'C', 'D', 'E', 'F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    symbols=['|','#','$','&','%','/','-','+','_']
    password=process(lowerLetters,UpperLetters,symbols)
    return password
#Process to generate the password
def process(lowerLetters,UpperLetters,symbols):
    final='' #Create empty string to store password
    for i in range(30):#Create a password with 30 characters
        key=randint(1,1000)#Chooses a number between 1 and 1000
        #first checks if the number can be devided by 2
        if (key%2)==0:
            #It will add a random character from a specific list of characters
            #depending if the "key" is greater of smaller then 500
            if key<=500:
                #uselower
                temp=lowerLetters[randint(0,len(lowerLetters)-1)] 
                #choose a character without overlapping ammount of characters available
            if key>500:
                #useupper
                temp=UpperLetters[randint(0,len(UpperLetters)-1)]
        else: #If it is not divisible by 2 it will do the same process but with different characters
            if key<=500:
                #useNumber
                temp=str(randint(0,10))
            if key>500:
                #useSymbol
                temp=symbols[randint(0,len(symbols)-1)]

        #Adds selected character to the final string
        final+=temp
    return final#returns the final string (the generated password)
#password created notification
def NoticeCrtPas(site,username,pswd):
    user_info=username.get()
    site_info=site.get()

    password = encryptor(MASTER_KEY,pswd)

    if site_info!="" or user_info!="":
        try:
            con,cur = SQLcon()
            id=getID(cur)
            cur.execute(f"INSERT INTO list VALUES('{site_info}','{user_info}','{password}',{id})")
            SQLclose(con)
            tkinter.messagebox.showinfo("Password created",f"Your password: has been\nadded to the data base")
            
        except Exception as e:
            tkinter.messagebox.showerror("Error",e)
            con.close()
    else:
        tkinter.messagebox.showerror("Error",f"Please fill in the site and user data")
#-------------------------------------------------------------
#REGISTER SCREEN
def openRegisterMenu():
    HideAllFrames()
    register_frame.pack(fill='both', expand=1)
    RegisterStructure()

def RegisterStructure():
    textColor= "#242424"
    inputColor= "#ffffff"

    main_pass=StringVar()

    titulo=Label(register_frame,text="Register",bg = background_color,fg = textColor,font = font_title)#main title
    titulo.place(x=180, y=70)


    user_label=Label(register_frame,text="Password", fg=textColor, bg = background_color, font=font_normal)
    user_label.place(x=190,y=220)

    pass_entry = Entry(register_frame,textvariable=main_pass,bg=inputColor)#web site info
    pass_entry.place(x=120,y=260, height=30, width=260)

    create_password_button = Button(register_frame,text="Enter", width="10", height="1",
                                    command=lambda: registerVerification(pass_entry),
                                    bg=inputColor,font=font_normal)
    create_password_button.place(x=165,y=360)

def registerVerification(p):
    """Check if the user has entered a valid passwrd, makes a hash, saves it in the database 
    under the 'auth' table and saves in a local variable the values written

    Args:
        p (tkinter input): Master password input
    """
    masterP = p.get()
    #verify if there was a valid input
    if masterP != "":

        con,cur = SQLcon() #create conection
        try:#insert values into the system
            cur.execute(f"INSERT INTO auth VALUES('{getHashVal(masterP)}')")

        except Exception as e:
            tkinter.messagebox.showerror("Error",e)

        SQLclose(con)
        global MASTER_KEY
        MASTER_KEY = keyCreator(masterP)

        OpenSearchMenu()

#-------------------------------------------------------------
#LOGIN SCREEN
def openLoginMenu():
    HideAllFrames()
    login_frame.pack(fill='both', expand=1)
    LoginStructure()

def LoginStructure():
    root.geometry("500x500")
    font_title=("Bebas_Neue",35,"bold")
    main_pass=StringVar()
    textColor= "#242424"
    inputColor= "#ffffff"

    titulo=Label(login_frame,text="Login",bg = background_color,fg = textColor,font = font_title)#main title
    titulo.place(x=180, y=70)


    user_label=Label(login_frame,text="Password", fg=textColor, bg = background_color, font=font_normal)
    user_label.place(x=190,y=220)

    site_entry = Entry(login_frame,textvariable=main_pass,bg=inputColor)#web site info
    site_entry.place(x=120,y=260, height=30, width=260)

    create_password_button = Button(login_frame,text="Enter", width="10", height="1",
                                    command=lambda: verifyPass(site_entry),
                                    bg=inputColor,font="Bebas_Neue 19 bold")
    create_password_button.place(x=165,y=360)

def verifyPass(p):
    inVal = p.get()


    if inVal!="":
        con,cur =SQLcon()
        try:
            cur.execute("SELECT ID FROM auth")
            res = cur.fetchall()
            res = res[0][0]
        except Exception as e:
            tkinter.messagebox.showerror("Error",e)
        
        SQLclose(con)

        if res == getHashVal(inVal):
            global MASTER_KEY
            MASTER_KEY = keyCreator(inVal)
            OpenSearchMenu()
        else:
            tkinter.messagebox.showwarning("Error","Incorrect password")
    else:
        tkinter.messagebox.showinfo("Warning","Please fill out the input to continue...")

#-------------------------------------------------------------
#if no password is established open register menu, else open login menu
def testForAuth():
    """Check if there is a registered master password to encript the data
    """
    #Open database
    con,cur = SQLcon()
    try:
        cur.execute("SELECT COUNT ('ID') FROM auth")
        res = cur.fetchone()[0]
        con.close()
        if res > 0:
            return True
        else: 
            return False
    except Exception as e:
        print("ERROR: ",e)
        con.close()
        return False
    

#root settings
root=Tk()
root.title("Password Manager")
root.geometry("300x100")
root.resizable(False, False)
root.iconbitmap("logo_icono.ico")
#esthetics Font
font_title=("Segoe UI",20,"bold")
font_normal=("Segoe UI",15)
#colors
background_color='white'
buttonColor="#1992b6"
masterP = ""
root ['bg']= background_color

textColor= "#242424"

loading_frame = Frame(root,width=300,heigh=100,bg=background_color)
loading_frame.pack(fill='both', expand=1)

titulo=Label(loading_frame,text="Loading",bg = background_color,fg = textColor,font = font_title)#main title
titulo.place(x=110, y=20)

bar = ttk.Progressbar(loading_frame, orient=HORIZONTAL,length=260,mode='determinate')
bar.place(x=20, y=60)

i = 0
j = False
res = False

def load():
    """Show progress bar on screen. It will go after 50% once the program verifies if there is a password or not to encript
    """
    global i,res,j
    if i<50 and not j:
        bar.after(13,load)
        bar["value"]=i
        i+=1
        return
    
    elif j and i<100:
        bar.after(5,load)
        bar["value"]=i
        i+=1
        return

    if i == 50:
        j = 1
        if testForAuth():
            res = True
        load()
    
    elif i == 100:
        root.geometry("500x500")
        loading_frame.pack_forget()
        if res:
            openLoginMenu()
        else:
            openRegisterMenu()

#----------------------------------------------------------------

#------------------------------------------------------------------
#creation of frames
#default frame is the "loading frame"
sizes = 500

login_frame = Frame(root,width=sizes, height=sizes, bg='white')
register_frame = Frame(root,width=sizes, height=sizes, bg='white')
add_password_frame= Frame(root,width=sizes, height=sizes, bg='white')
verify_password_frame= Frame(root,width=sizes, height=sizes, bg='white')
search_password_frame= Frame(root,width=sizes, height=sizes, bg='white')
modify_data_frame= Frame(root,width=sizes, height=sizes, bg='white')
delete_data_frame= Frame(root,width=sizes, height=sizes, bg='red')
create_password_frame = Frame(root,width=sizes, height=sizes, bg='white')
#------------------------------------------------------------------
load()
root.mainloop()