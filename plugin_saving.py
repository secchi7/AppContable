import tkinter as tk
from tkinter import ttk,messagebox
import os
import os.path
import sqlite3
import requests
from datetime import datetime

class NewSaving(tk.Toplevel):
    in_use=False

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=300,height=300)
        self.title("Ahorros")

        ######Llama al usuario
        f=open("usuario_actual.txt","r",encoding="utf8")
        self.user_current=str(f.read())
        f.close()

        ######TIPO
        self.tag_type_movimiento=ttk.Label(
            self,
            text="Tipo:"    
        )
        self.tag_type_movimiento.place(x=10,y=10)
        self.list_type_movimiento=ttk.Combobox(
            self,
            state="readonly",
            values=["Acción","Bono", "Cedear", "Dolar", "Oro"]
        )
        self.list_type_movimiento.place(x=150,y=10)

        ######ESPECIE
        self.tag_name=ttk.Label(
            self,
            text="Especie:"
        )
        self.tag_name.place(x=10,y=40)
        self.box_name=ttk.Entry(
            self
            )
        self.box_name.place(x=150,y=40)

        ######CANTIDAD
        self.tag_amount=ttk.Label(
            self,
            text="Cantidad:"
        )
        self.tag_amount.place(x=10,y=70)
        self.box_amount=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validate_entry_numeros), "%S")
            )
        self.box_amount.place(x=150,y=70,width=142 ,height=20)        

        ######FECHA
        self.tag_date_saving=ttk.Label(
            self,
            text="Fecha (aaaa-mm-dd):"
        )
        self.tag_date_saving.place(x=10,y=190)
        self.box_date_saving=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validate_date), "%P")
        )
        self.box_date_saving.place(x=150,y=190,width=142,height=20)

        self.btn_add=ttk.Button(
            self,
            text="Agregar",
            command=self.add_new_saving
        )
        self.btn_add.place(x=10,y=270)
        self.btn_close=tk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )
        self.btn_close.place(x=210,y=270)
        self.__class__.in_use=True


    def add_new_saving(self):
        
        type=self.list_type_movimiento.get()
        name=self.check_empty(self.box_name.get())
        amount=self.check_empty(self.box_amount.get())
        # importe=self.verificar_vacio(self.caja_nuevo_gasto.get())
        # forma_pago=self.lista_forma_pago.get()
        # cuotas=self.lista_cantidad_cuotas.get()
        date_saving=self.box_date_saving.get()

        self.box_name.delete(0,tk.END)
        self.box_amount.delete(0,tk.END)
        # self.lista_tipo_gasto.delete(0,tk.END) ESTO NO FUNCIONA BUSCAR SOLUCIÓN
        self.box_date_saving.delete(0,tk.END)
        if name==False or amount==False or date_saving==None:
            pass

        else:
            conn=sqlite3.connect(f'{self.user_current}.db')
            cursor=conn.cursor()
            cursor.execute("INSERT INTO ahorros VALUES (?, ?, ?, ?)", (type, name, amount,date_saving))
            conn.commit()
            conn.close()

    def validate_entry_numeros(self,texto):
        return texto.isdecimal()

    def validate_date(self,date):
        if len(date)>10:
            return False
        chequeo=[]
        for i, letter in enumerate(date):
            if i in (4,7):
                chequeo.append(letter=="-")
            else:
                chequeo.append(letter.isdecimal())
        return all(chequeo)

    def check_empty(self,data):
        data_check=data
        if data_check=="":
            messagebox.showwarning(
                title="Advertencia",
                message="Por favor ingrese un monto en pesos."
            )
            return False
        else:
            return data_check

    def destroy(self):
        self.__class__.in_use=False
        return super().destroy()

#################################################################################

class VindowSaving(tk.Toplevel):
    in_use=False

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=800,height=800)
        self.title("Ahorros")

        self.table_saving=ttk.Treeview(self,
            columns=("tipo","especie", "cantidad","cotización","precio_p" ,"precio_d"),
            show="headings"
        )
        self.table_saving.heading("tipo", text="Tipo")
        self.table_saving.heading("especie",text="Especie")
        self.table_saving.heading("cantidad",text="Cantidad")
        self.table_saving.heading("cotización",text="Cotización")
        self.table_saving.heading("precio_p", text="Precio en pesos")
        self.table_saving.heading("precio_d",text="Precio en dolares")

        self.table_saving.column("tipo",width=50)
        self.table_saving.column("especie",width=50)
        self.table_saving.column("cantidad",width=70)
        self.table_saving.column("cotización",width=70)
        self.table_saving.column("precio_p",width=25)
        self.table_saving.column("precio_d",width=25)

        self.table_saving.place(x=10,y=45,width=750,height=550)

        # Lee la base de datos
        f=open("usuario_actual.txt","r",encoding="utf8")
        user_current=str(f.read())
        f.close()
        
        conn=sqlite3.connect(f'{user_current}.db')
        
        cursor=conn.cursor()
        cursor.execute(f"SELECT tipo, especie, cantidad FROM ahorros ORDER BY especie")
        savings=cursor.fetchall()
        self.table_saving.delete(*self.table_saving.get_children())

        price_dollar=self.dollar()
        for saving in savings:
            
            type=saving[0]
            name=saving[1]
            amount=saving[2]
            quotation=self.api_iol(name)
            price_q=amount*quotation
            price_d=amount*price_dollar

            self.table_saving.insert("",tk.END,values=(type, name, amount, quotation,price_q,price_d))

        self.btn_close=ttk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )

        self.btn_close.place(x=400,y=770)
        # Indicar que está en uso luego de crearse
        self.__class__.in_use=True

    def dollar(self):
        r = requests.get("https://api-dolar-argentina.herokuapp.com/api/contadoliqui")

        if r.status_code==200:
            print("Petición exitosa.")
            content=r.json()
            dollar_CCL=float(content["compra"])
            return dollar_CCL

        else:
            print(r.status_code)
            dollar_CCL=0
            return dollar_CCL


    def api_iol(self,name):
        #################### SECCION POST ####################

        # Pido la fecha actual para compararla con la fecha del Token_Bearer
        date_current=datetime.now().replace(microsecond=0)

        f=open("Token_Bearer.txt","r",encoding="utf8")
        content=f.read().split("\n")
        date=content[1]
        f.close()

        date_formato=datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        minutes_difference= (date_current-date_formato).total_seconds()/60

        if minutes_difference<15:
            # "Estamos en tiempo menor a 15min, no hace falta renovar el token"
            f=open("Token_Bearer.txt","r",encoding="utf8")
            content=f.read().split("\n")
            Token_Bearer=content[0]
            f.close()

        elif minutes_difference<60 and minutes_difference>15:
            # "Estamos entre los 15 min y la 60 min de cuanto se solicito el token, es necesario usar el refresh"

            # Abro el txt para obtener el Token_Refresh
            url="https://api.invertironline.com/token"
            f=open("Token_Refresh.txt", "r", encoding="utf8")
            content=f.read().split("\n")
            Token_Refresh=content[0]
            f.close()

            #Abro el Token_Bearer para obtener la feche original y mantenerla en el txt, ya que tiene vigencia por 60min 
            f=open("Token_Refresh.txt", "r", encoding="utf8")
            content=f.read().split("\n")
            date_Bearer=content[1]
            f.close()

            information={
                "refresh_token":Token_Refresh,
                "grant_type":'refresh_token'
            }

            r = requests.post(url,data=information)

            if r.status_code==200:
                token=r.json()
                date=str(datetime.now().replace(microsecond=0))

                f=open("Token_Bearer.txt","w",encoding="utf8")
                f.write(token['access_token']+"\n")
                f.write(date_Bearer)
                f.close()

                f=open("Token_Refresh.txt","w",encoding="utf8")
                f.write(token['refresh_token']+"\n")
                f.write(date)
                f.close()

            else:
                print("Error de petición.")
                print(r.status_code)

        else:
            # "Se necesita volver a pedir el Token_Bearer"
            url="https://api.invertironline.com/token"

            f=open("User_Password.txt", "r", encoding="utf8")
            content=f.read().split("\n")
            user=content[0]
            password=content[1]
            f.close()

            information={
                "username":user,
                "password":password,
                "grant_type":'password'
            }

            r = requests.post(url,data=information)

            if r.status_code==200:
                token=r.json()
                date=str(datetime.now().replace(microsecond=0))

                f=open("Token_Bearer.txt","w",encoding="utf8")
                f.write(token['access_token']+"\n")
                f.write(date)
                f.close()

                f=open("Token_Refresh.txt","w",encoding="utf8")
                f.write(token['refresh_token']+"\n")
                f.write(date)
                f.close()

            else:
                print("Error de petición.")
                print(r.status_code)

        #################### SECCION GET ####################

        f=open("Token_Bearer.txt", "r", encoding="utf8")
        content=f.read().split("\n")
        Token_Bearer=content[0]
        f.close()

        market="bCBA"
        symbol=str(name)

        information={"Authorization": "Bearer "+Token_Bearer}

        r = requests.get(url=f"https://api.invertironline.com/api/v2/{market}/Titulos/{symbol}/CotizacionDetalle", headers=information)

        if r.status_code==200:
            security =r.json()
            price_name=security ["ultimoPrecio"]
            return  price_name

        else:
            print("Error de petición.")
            print(r.status_code)

        print("Fin del programa.")        

    def destroy(self):
        self.__class__.in_use=False
        return super().destroy()