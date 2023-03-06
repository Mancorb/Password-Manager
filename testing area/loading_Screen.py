from tkinter import ttk
from tkinter import *

root=Tk()
root.title("Password Manager")
root.geometry("300x100")
root.resizable(False, False)
#esthetics Font
font_title=("Bebas_Neue",15,"bold")
#colors
background_color="#ffffff"

root ['bg']= background_color

textColor= "#242424"
inputColor= "#ffffff"

titulo=Label(text="Loading",bg = background_color,fg = textColor,font = font_title)#main title
titulo.place(x=110, y=20)

bar = ttk.Progressbar(root, orient=HORIZONTAL,length=260,mode='determinate')
bar.place(x=20, y=60)

i = 0
def load():
    global i
    if i<=50:
        bar.after(10,load)
        bar["value"]=i
        i+=1
    
load()
root.mainloop()