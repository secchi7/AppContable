import tkinter as tk
from tkinter import ttk,messagebox
import os
import os.path
import sqlite3
import requests
from datetime import datetime
import json

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

        ######MERCADO
        self.tag_market=ttk.Label(
            self,
            text="Mercado:"
        )
        self.tag_market.place(x=10,y=70)

        self.list_market=ttk.Combobox(
            self,
            state="readonly",
            values=["Lider","General", "Cedear", "Dolar", "Oro"]
        )
        self.list_market.place(x=150,y=70)

        ######CANTIDAD
        self.tag_amount=ttk.Label(
            self,
            text="Cantidad:"
        )
        self.tag_amount.place(x=10,y=100)
        self.box_amount=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validate_entry_numeros), "%S")
            )
        self.box_amount.place(x=150,y=100,width=142 ,height=20)        

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
        
        type_saving=self.list_type_movimiento.get()
        name=self.check_empty(self.box_name.get())
        market=self.list_market.get()
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
            cursor.execute("INSERT INTO ahorros VALUES (?, ?, ?, ?, ?)", (type_saving, name, market, amount,date_saving))
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
        cursor.execute(f"SELECT tipo, especie, mercado, SUM(cantidad) FROM ahorros GROUP BY especie")
        savings=cursor.fetchall()

        self.table_saving.delete(*self.table_saving.get_children())
        price_dollar=self.dollar()

        for saving in savings:
            
            type_saving=saving[0]
            name=saving[1]
            market=saving[2]
            amount=saving[3]
            price=float(self.api_bolsar(name,market))
            price_q=amount*price
            price_d=amount*price_dollar

            self.table_saving.insert("",tk.END,values=(type_saving, name, amount, price,price_q,price_d))

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

    def api_bolsar(self,name,market):
        name=name.upper()
        name=f"{name}_48hs"
        payload = ""
        headers = {
            "authority": "ws.bolsar.info",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "es-ES,es;q=0.9",
            "origin": "https://bolsar.info",
            "referer": "https://bolsar.info/",
            "sec-ch-ua": "^\^Chromium^^;v=^\^112^^, ^\^Google",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\^Windows^^",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }

        if market=="Lider":
            # url = "https://ws.bolsar.info/BYMA/view/lideres_v2.html"
            # querystring = {"1":"1"}
            # response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

            # jsondata=json.loads(response.text)
            with open('Market.json') as f:
                jsondata=json.load(f)


            # creo un diccionario para buscar el código
            accionesLideres={}
            codes=jsondata.keys()  #creo una lista con las keys del diccionario

            for code in codes:
                value=jsondata[code]["name"]
                accionesLideres[value]=code


            if name in accionesLideres.keys():
                code=accionesLideres[name]

            else:
                print("ERROR")
            
            datos=jsondata[code]["description"]
            datos=datos.strip()
            lineas=datos.split("\n") 

            for linea in lineas:
                indice1=linea.find("<b>")
                indice2=linea.find("</b>")
                price_name=linea[indice1+3:indice2]
            
            price_name=float(price_name.replace(",", "." ))
            return  price_name

        elif name=="Cedear":
            print("cedear")
            # code=cedears[name]
            # url = "https://ws.bolsar.info/BYMA/paneles_v2.php"
            # querystring = {"1":"1","panel":"5","format":"json"}
            # response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

            # jsondata=json.loads(response.text)

            # datos=jsondata[code]["description"]
            # datos=datos.strip()
            # lineas=datos.split("\n")

            # for linea in lineas:
            #     indice1=linea.find("<b>")
            #     indice2=linea.find("</b>")
            #     price_name=linea[indice1+3:indice2]
                
            # return  price_name

        else:
            print("ERROR")

    def destroy(self):
        self.__class__.in_use=False
        return super().destroy()