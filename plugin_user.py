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
        
        if os.path.isfile("usuarios.txt")==True:
            f=open("usuarios.txt","r",encoding="utf8")
            users=f.read().split("\n")[:-1]
            f.close()

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
        f=open("usuario_actual.txt","w",encoding="utf8")
        f.write(user_selected)

        f.close()

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
            command=self.create_base_data
        )
        self.btn_add_user.place(x=10,y=70)

        self.btn_close.place(x=190,y=70)

        # Indicar que está en uso luego de crearse
        self.__class__.in_use=True


    def create_base_data(self):
        user=self.box_new_user.get()
        if user.strip()=="":
            messagebox.showwarning(
                title="Advertencia",
                message="Por favor agregue un nombre de usuario válido."
            )

        else:
            f=open("usuario_actual.txt","w",encoding="utf8")
            f.write(user)
            f.close()

            f=open("usuarios.txt","a",encoding="utf8")
            f.write(f'{user}\n')
            f.close()
       
            conn=sqlite3.connect(f'{user}.db')
            cursor=conn.cursor()
            
            self.callback(self.box_new_user.get())


            try:
                cursor.execute("CREATE TABLE gastos (tipo TEXT, categoría TEXT, descripcion TEXT,importe FLOAT, formadepago TEXT, cuota INT, cantidadCuotas INT, fecha DATE)")
            except sqlite3.OperationalError:
                # silenciar la excepción
                pass
            try:
                cursor.execute("CREATE TABLE ahorros (tipo TEXT, especie TEXT, cantidad INT, fecha DATE)")
            except sqlite3.OperationalError:
                # silenciar la excepción
                pass

            conn.close()
            

    def destroy(self):
        self.__class__.in_use=False
        return super().destroy()