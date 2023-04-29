import sqlite3
import tkinter as tk
from tkinter import ttk

def window(result):
    win=tk.Tk()
    win.geometry('400x280')
    win.title("Table test")
    trv = ttk.Treeview(win,selectmode='browse')
    trv.grid(row=1,column=1,padx=20,pady=20)
    trv["columns"] =('1','2','3','4')
    trv["show"]='headings'
    trv.column('1',width='120',anchor='c')
    trv.column('2',width='130',anchor='c')
    trv.column('3',width='150',anchor='w')
    trv.column('4',width='30',anchor='w')

    trv.heading('1',text='site')
    trv.heading('2',text='username')
    trv.heading('3',text='password')
    trv.heading('4',text='ID')

    for dt in result:
        trv.insert('','end',iid=dt[0],values=(dt[0],dt[1],dt[2],dt[3]))
    win.mainloop()

def create(data):
    #conectarse a la base de datos
    conexion=connect()
    #crear el cursor
    cursor=conexion.cursor()
    #Crear una tabla
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {data[0]}( {data[1]} );""")
    #Guardar cambios
    conexion.commit()
    disconnect(conexion)

def search(command):
    #conectarse a la base de datos
    conexion=connect()
    #create the cursor
    cur=conexion.cursor()
    try:
        #Run command
        cur.execute(command)

        rows = cur.fetchall()
        #window(rows)
        for r in rows:
            print(r[0],",")

    except Exception as e:
        print(f"--ERROR:{e}")
    disconnect(conexion)

def execute(command):
    try:
        conexion=connect()
        cursor=conexion.cursor()
        cursor.execute(command)
        conexion.commit()
        disconnect(conexion)
    except Exception as e:
        print(f"--Error:{e}")
def description ():
    try:
        search("SELECT tbl_name FROM SQLITE_SCHEMA")
    except Exception as e:
        print(f"--Error:{e}")
def connect():
    #Conexión
    conexion = sqlite3.connect('testbd.db')
    return conexion

def disconnect(conexion):
    conexion.close()

if __name__ == '__main__':
    print("Tables available:")
    description()
    
    while True:
        com=input("[]->")

        if com=='help':
            print("\n'search'=seach data in database\n'run'=run command\ncreate=Create table\n'q'=quit")
        
        elif com=='search':
            com=input("[S]->")
            search(com)
        elif com=='run':
            com=input("[R]->")
            execute(com)
        elif com=='create':
            data=[input("[C-name]->"),input("[C-command]->")]
            create(data)
        elif com=='q':
            break
        