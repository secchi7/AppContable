import tkinter as tk
from tkinter import ttk,messagebox
import os
import os.path
import sqlite3

class UserList(tk.Toplevel):
    in_use=False

    def __init__(self,*args,callback=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=300,height=100)
        self.callback=callback
        self.title("Usuario existente")

        self.btn_close=ttk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )

        self.tag_user_existing=ttk.Label(
            self,
            text="Usuario existente"
        )
        self.tag_user_existing.place(x=10,y=10)

        if os.path.isfile("main.db")==True:
            conn=sqlite3.connect('main.db')
            cursor=conn.cursor()
            cursor.execute(f"SELECT nombre FROM usuarios")
            users=cursor.fetchall()
            conn.close()

        else:
            users=[]
            messagebox.showwarning(
                title="Advertencia",
                message="No existe ningún usuario."
            )

        self.list_users=ttk.Combobox(
            self,
            state="readonly",
            values=users
        )
        self.list_users.place(x=150,y=10)

        self.btn_select_user=ttk.Button(
            self,
            text="Seleccionar Usuario",
            command=self.select_user
        )
        self.btn_select_user.place(x=10,y=70)

        self.btn_close.place(x=210,y=70)
        # Indicar que está en uso luego de crearse
        self.__class__.in_use=True


    def select_user(self):
        user_selected=self.list_users.get()
        conn=sqlite3.connect('main.db')
        cursor=conn.cursor()
        cursor.execute(f"SELECT id FROM usuarios WHERE nombre=?",[f"{user_selected}"])
        id_user=cursor.fetchone()[0]
        cursor.execute("UPDATE usuarioActual SET nombre=?, usuarioId=?", (f"{user_selected}",id_user))
        conn.commit()
        conn.close()

        self.callback(self.list_users.get())

        # Una vez que se seleccionó el usuario, cierra la ventana.
        self.__class__.in_use=False
        return super().destroy()
     
    def destroy(self):
        self.__class__.in_use=False
        return super().destroy()

class NewUser(tk.Toplevel):
    in_use=False

    def __init__(self,*args,callback=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.create_base_data()
        self.config(width=280,height=100)

        self.callback=callback

        self.title("Crear usuario")

        self.btn_close=ttk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )


        self.tag_new_user=ttk.Label(
            self,
            text="Nuevo usuario"
        )
        self.tag_new_user.place(x=10,y=10)

        self.box_new_user=ttk.Entry(self)
        self.box_new_user.place(x=120,y=10,width=150,height=25)


        self.btn_add_user=ttk.Button(
            self,
            text="Agregar usuario",
            command=self.create_user
        )
        self.btn_add_user.place(x=10,y=70)

        self.btn_close.place(x=190,y=70)

        # Indicar que está en uso luego de crearse
        self.__class__.in_use=True

    def create_base_data(self):
        try:
            conn=sqlite3.connect(f'main.db')
        except sqlite3.OperationalError:
            # silenciar la excepción
            pass

        cursor=conn.cursor()

        try:
            cursor.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT)")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("CREATE TABLE usuarioActual (nombre TEXT, usuarioId, FOREIGN KEY(usuarioId) REFERENCES usuarios(id))")
        except sqlite3.OperationalError:
            pass
        
        cursor.execute("INSERT INTO usuarioActual VALUES (?,?)", ["NULL","NUL"])

        try:
            cursor.execute("CREATE TABLE gastos (tipo TEXT, categoría TEXT, descripcion TEXT, importe FLOAT, formadepago TEXT, cuota INT, cantidadCuotas INT, fecha DATE, usuarioId, FOREIGN KEY(usuarioId) REFERENCES usuarioActual(usuarioId))")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("CREATE TABLE ahorros (tipo TEXT, especie TEXT, mercado TEXT, cantidad INT, fecha DATE, usuarioId, FOREIGN KEY(usuarioId) REFERENCES usuarioActual(usuarioId))")
        except sqlite3.OperationalError:
            pass
        
        conn.commit()
        conn.close()

    def create_user(self):
        user=self.box_new_user.get()
        if user.strip()=="":
            messagebox.showwarning(
                title="Advertencia",
                message="Por favor agregue un nombre de usuario válido."
            )

        else:
            conn=sqlite3.connect('main.db')
            cursor=conn.cursor()
            cursor.execute(f"SELECT nombre FROM usuarios WHERE nombre=?",[f"{user}"])
            consultation=cursor.fetchall()
            self.callback(self.box_new_user.get())

            if consultation==[]:
                cursor.execute("INSERT INTO usuarios(nombre) VALUES (?)", [f"{user}"])
                cursor.execute("UPDATE usuarioActual SET nombre=?, usuarioId=?", (f"{user}",cursor.lastrowid))
                conn.commit()
                conn.close()

            else:
                messagebox.showwarning(
                    title="Advertencia",
                    message="El usuario ya existe."
                )


    def destroy(self):
        self.__class__.in_use=False
        return super().destroy()