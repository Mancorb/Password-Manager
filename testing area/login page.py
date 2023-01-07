from tkinter import ttk
from tkinter import *

root=Tk()
root.title("Password Manager")
root.geometry("500x500")
root.resizable(False, False)
#esthetics Font
font_title=("Bebas_Neue",35,"bold")
font_normal=("Bebas_Neue",19)
#colors
background_color="#92c1f5"
buttonColor="#1992b6"
root ['bg']= background_color

textColor= "#242424"
inputColor= "#ffffff"

main_pass=StringVar()

titulo=Label(text="Login",bg = background_color,fg = textColor,font = font_title)#main title
titulo.place(x=180, y=70)


user_label=Label(text="Password", fg=textColor, bg = background_color, font=font_normal)
user_label.place(x=190,y=220)

site_entry = Entry(textvariable=main_pass,bg=inputColor)#web site info
site_entry.place(x=120,y=260, height=30, width=260)

create_password_button = Button(text="Enter", width="10", height="1",
                                command=None,
                                bg=inputColor,font="Bebas_Neue 19 bold")
create_password_button.place(x=165,y=360)

root.mainloop()

print (main_pass)