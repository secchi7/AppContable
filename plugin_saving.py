import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox, constants
import os
import os.path
import sqlite3
import requests
from datetime import datetime
import json
from requests import Session
class NewSaving(tk.Toplevel):
    in_use=False

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=300,height=300)
        self.title("Ahorros")

        ######Llama al usuario
        conn=sqlite3.connect('main.db')
        cursor=conn.cursor()
        cursor.execute(f"SELECT nombre FROM usuarioActual")
        self.user_current=cursor.fetchone()[0]
        conn.close()
        ######TIPO
        self.tag_type_movimiento=ttk.Label(
            self,
            text="Tipo:"    
        )
        self.tag_type_movimiento.place(x=10,y=10)
        self.list_type_movimiento=ttk.Combobox(
            self,
            state="readonly",
            values=["Acción","Bono", "Cedear", "Cripto", "Dolar", "Oro"]
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
            values=["Lider","General", "Cedear","Cripto", "Dolar", "Oro"]
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
            # validate="key",
            # validatecommand=(self.register(self.validate_entry_numeros), "%S")
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
            conn=sqlite3.connect('main.db')
            cursor=conn.cursor()
            cursor.execute(f"SELECT id FROM usuarios WHERE nombre=?",[f"{self.user_current}"])
            id_user=cursor.fetchone()[0]
            cursor.execute("INSERT INTO ahorros VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (type_saving, name, market, amount,date_saving,"NULL","NULL", id_user))
            conn.commit()
            conn.close()

    # def validate_entry_numeros(self,texto):
    #     return texto.isdecimal()


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
        self.config(width=535,height=600)
        self.title("Ahorros")

        self.table_saving=ttk.Treeview(self,
            columns=("tipo","especie", "cantidad","cotización","precio_p" ,"precio_d"),
            show="headings", 
            height=18
        )
        
        self.table_saving.heading("tipo", text="Tipo")
        self.table_saving.heading("especie",text="Especie")
        self.table_saving.heading("cantidad",text="Cantidad")
        self.table_saving.heading("cotización",text="Cotización")
        self.table_saving.heading("precio_p", text="Precio en pesos")
        self.table_saving.heading("precio_d",text="Precio en dolares")

        self.table_saving.column("tipo", anchor=CENTER ,width=65)
        self.table_saving.column("especie", anchor=CENTER ,width=70)
        self.table_saving.column("cantidad", anchor=E ,width=80)
        self.table_saving.column("cotización", anchor=E ,width=100)
        self.table_saving.column("precio_p", anchor=E ,width=100)
        self.table_saving.column("precio_d", anchor=E ,width=100)

        self.table_saving.place(x=10,y=45)

        ######Llama al usuario
        conn=sqlite3.connect('main.db')
        cursor=conn.cursor()
        cursor.execute(f"SELECT usuarioId FROM usuarioActual")
        self.userId_current=cursor.fetchone()[0]
        #Actualiza la base de datos
        cursor.execute(f"SELECT especie, mercado FROM ahorros WHERE usuarioId={self.userId_current} GROUP BY especie")
        values_list=cursor.fetchall()
        cursor=conn.cursor()
        self.api_quotes(self.userId_current,values_list) 
        conn.close() # Cierro la consulta porque la funcion tambien necesita usar la base de datos para actualizar los precios

        # Consulto la cotización del dolar
        price_dollar=self.dollar()
        ######################################

        conn=sqlite3.connect('main.db')
        cursor=conn.cursor()
        cursor.execute(f"SELECT tipo, especie, mercado, SUM(cantidad), cotizacion FROM ahorros WHERE usuarioId={self.userId_current} GROUP BY especie")
        savings=cursor.fetchall()
        cursor=conn.cursor()
        
        price_tq=0
        cripto_q=0
        cripto_d=0
        dollar_q=0
        dollar_d=0
        shares_q=0
        shares_d=0


        # print("#######INICIO DEL FOR#######")
        for saving in savings:
            # print("############################")
            type_saving=saving[0]
            name=saving[1]
            if type_saving=="Cripto":
                amount=round(saving[3],3)
                price=round(saving[4]*price_dollar,0)
                price_q=round(amount*price_dollar,0)
                price_d=round(amount*saving[4],0)
                cripto_q=cripto_q+price_q
                cripto_d=cripto_d+price_d
                price_tq=price_tq+price_q

            elif type_saving=="Dolar":
                amount=round(saving[3],3)
                price=round(price_dollar,0)
                price_q=round(amount*price_dollar,0)
                price_d=round(amount,0)
                dollar_q=dollar_q+price_q
                dollar_d=dollar_d+price_d
                price_tq=price_tq+price_q

            else:
                amount=saving[3]
                price=saving[4]
                price_q=round(amount*price,0)
                price_d=round(price_q/price_dollar,0)
                shares_q=shares_q+price_q
                shares_d=shares_d+price_q
                price_tq=price_tq+price_q

            self.table_saving.insert("",tk.END,values=(type_saving, name, amount, price,price_q,price_d))
        # print("#######FIN DEL FOR#######")

        #Calculo los porcentajes 
        percentage_shares=round(shares_q/price_tq*100,0)
        percentage_dollar=round(dollar_q/price_tq*100,0)
        percentage_cryto=round(cripto_q/price_tq*100,0)

        price_td=round(price_tq/price_dollar,0)

        self.tag_percentage=ttk.Label(
            self,
            text=f"Porcentajes:"
        )
        self.tag_percentage.place(x=20, y=440)

        self.tag_percentage_shares=ttk.Label(
            self,
            text=f"     *    Acciones {percentage_shares}%"
        )
        self.tag_percentage_shares.place(x=20, y=460)

        self.tag_percentage_dollar=ttk.Label(
            self,
            text=f"     *    Dolares {percentage_dollar}%"
        )
        self.tag_percentage_dollar.place(x=20, y=480)

        self.tag_percentage_crypto=ttk.Label(
            self,
            text=f"     *    Criptos {percentage_cryto}%"
        )
        self.tag_percentage_crypto.place(x=20, y=500)

        self.tag_total_dollar=ttk.Label(
            self,
            text=f"Total en USD {price_td}"
        )
        self.tag_total_dollar.place(x=20, y=530)
        self.tag_total_pesos=ttk.Label(
            self,
            text=f"Total en $ {price_tq}"
        )
        self.tag_total_pesos.place(x=20, y=550)

        self.btn_close=ttk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )

        self.btn_close.place(x=440,y=570)
        # Indicar que está en uso luego de crearse
        self.__class__.in_use=True

    def dollar(self):
        date_consultation=datetime.now().replace(microsecond=0)
        userId=0
        res=self.check_time(userId)
        if res=="yes":
            url = "https://www.dolarsi.com/api/api.php"

            querystring = {"type":"valoresprincipales"}

            payload = ""
            headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "es-ES,es;q=0.9",
                "Connection": "keep-alive",
                "Cookie": "_ga=GA1.2.1513822857.1681762964; _gid=GA1.2.79098551.1681762964; _gat=1",
                "Referer": "https://www.dolarsi.com/func/conversor.php",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "sec-ch-ua": "^\^Chromium^^;v=^\^112^^, ^\^Google",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "^\^Windows^^"
            }

            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

            jsondata=json.loads(response.text)    
            
            price_name=jsondata[4]["casa"]["compra"]
            price_name=price_name.replace(".", "" )
            price_name=float(price_name.replace(",", "." ))
            conn=sqlite3.connect('main.db')
            cursor=conn.cursor()
            cursor.execute(f"UPDATE ahorros SET cotizacion=?, cotizacionFecha=? WHERE tipo='Dolar' ", (f"{price_name}", f"{date_consultation}"))
            conn.commit()
            conn.close()

            return price_name
        
        else:
            conn=sqlite3.connect('main.db')
            cursor=conn.cursor()
            cursor.execute(f"SELECT cotizacion FROM ahorros WHERE tipo='Dolar'")
            price_name=cursor.fetchone()[0]
            conn.close()
            return price_name

    def api_quotes(self,userId_current,values_list):
        date_consultation=datetime.now().replace(microsecond=0)
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
        res=self.check_time(userId_current)
        if res=="yes":
            leader=[]
            general=[]
            cedear=[]
            cryptoL=[]
            crypto="."

            for value in values_list:
                if value[1]=="Lider":
                    leader.append(value[0])
                elif value[1]=="General":                    
                    general.append(value[0])
                elif value[1]=="Cedear":
                    cedear.append(value[0])
                elif value[1]=="Cripto":
                    cryptoL.append(value[0])
                    crypto=f"{crypto},{value[0]}"
            
            crypto=crypto.replace(".,","")

            conn=sqlite3.connect('main.db')
            cursor=conn.cursor()

            if leader!=[]:
                url = "https://ws.bolsar.info/BYMA/view/lideres_v2.html"
                querystring = {"1":"1"}
                response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

                jsondata=json.loads(response.text)

                # creo un diccionario para buscar el código
                shares={}
                codes=jsondata.keys()  #creo una lista con las keys del diccionario

                for code in codes:
                    value=jsondata[code]["name"]
                    shares[value]=code

                for name in leader:
                    name=name.upper()
                    name=f"{name}_48hs"
                    if name in shares.keys():
                        code=shares[name]
                
                    d=jsondata[code]["description"]
                    d=d.strip()
                    lines=d.split("\n") 

                    for line in lines:
                        index1=line.find("<b>")
                        index2=line.find("</b>")
                        price_name=line[index1+3:index2]

                    price_name=price_name.replace(".", "" )
                    price_name=float(price_name.replace(",", "." ))
                    name=name.replace("_48hs","")
                    cursor.execute(f"UPDATE ahorros SET cotizacion=?, cotizacionFecha=? WHERE especie='{name}' AND usuarioId={userId_current} ", (f"{price_name}", f"{date_consultation}"))
                    conn.commit()

            if general!=[]:
                url = "https://ws.bolsar.info/BYMA/paneles_v2.php"
                querystring = {"1":"1","panel":"2","format":"json"}
                response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

                jsondata=json.loads(response.text)

                # creo un diccionario para buscar el código
                shares={}
                codes=jsondata.keys()  #creo una lista con las keys del diccionario

                for code in codes:
                    value=jsondata[code]["name"]
                    shares[value]=code


                for name in general:
                    name=name.upper()
                    name=f"{name}_48hs"
                    if name in shares.keys():
                        code=shares[name]
                
                    d=jsondata[code]["description"]
                    d=d.strip()
                    lines=d.split("\n") 

                    for line in lines:
                        index1=line.find("<b>")
                        index2=line.find("</b>")
                        price_name=line[index1+3:index2]
                    
                    price_name=price_name.replace(".", "" )
                    price_name=float(price_name.replace(",", "." ))
                    name=name.replace("_48hs","")
                    cursor.execute(f"UPDATE ahorros SET cotizacion=?, cotizacionFecha=? WHERE especie='{name}' AND usuarioId={userId_current} ", (f"{price_name}", f"{date_consultation}"))
                    conn.commit()

            if cedear!=[]:
                url = "https://ws.bolsar.info/BYMA/paneles_v2.php"
                querystring = {"1":"1","panel":"5","format":"json"}
                response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

                jsondata=json.loads(response.text)

                # creo un diccionario para buscar el código
                shares={}
                codes=jsondata.keys()  #creo una lista con las keys del diccionario

                for code in codes:
                    value=jsondata[code]["name"]
                    shares[value]=code


                for name in cedear:
                    name=name.upper()
                    name=f"{name}_48hs"
                    if name in shares.keys():
                        code=shares[name]
                
                    d=jsondata[code]["description"]
                    d=d.strip()
                    lines=d.split("\n") 

                    for line in lines:
                        index1=line.find("<b>")
                        index2=line.find("</b>")
                        price_name=line[index1+3:index2]
                    
                    price_name=price_name.replace(".", "" )
                    price_name=float(price_name.replace(",", "." ))
                    name=name.replace("_48hs","")
                    cursor.execute(f"UPDATE ahorros SET cotizacion=?, cotizacionFecha=? WHERE especie='{name}' AND usuarioId={userId_current} ", (f"{price_name}", f"{date_consultation}"))
                    conn.commit()
            if cryptoL!=[]:
                url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest' # Coinmarketcap API url

                parameters = { 'symbol': f"{crypto}", 'convert': 'USD' } # API parameters to pass in for retrieving specific cryptocurrency data
                headers = {
                    'Accepts': 'application/json',
                    'X-CMC_PRO_API_KEY': '97a2a702-4610-4a9d-8383-197036d851b3'
                } # Replace 'YOUR_API_KEY' with the API key you have recieved in the previous step

                session = Session()
                session.headers.update(headers)

                response = session.get(url, params=parameters)

                jsondata = json.loads(response.text)

                for name in cryptoL:
                    name=name.upper()
                    
                    price_name=float(jsondata["data"][f"{name}"]["quote"]["USD"]["price"])

                    cursor.execute(f"UPDATE ahorros SET cotizacion=?, cotizacionFecha=? WHERE especie='{name}' AND usuarioId={userId_current} ", (f"{price_name}", f"{date_consultation}"))
                    conn.commit()

            conn.close()

    def check_time(self,userId_current):
        #función que verifica la ultima vez que se realizo la consulta, para no exceder la cantidad de peticiones en las páginas que pido la información de la cotización.
        conn=sqlite3.connect('main.db')
        cursor=conn.cursor()
        cursor.execute(f"SELECT cotizacionFecha FROM ahorros WHERE usuarioId={userId_current}")
        date_price=cursor.fetchone()[0]
        conn.close()

        if date_price=="NULL":
            check="yes"
            return check

        else:
            date_price=datetime.strptime(date_price, "%Y-%m-%d %H:%M:%S")
            date_current=datetime.now().replace(microsecond=0)
            minutes_diferencia= (date_current-date_price).total_seconds()/60
            
            if minutes_diferencia<60:
                # "No hace falta volver a pedir la cotización."
                check="no"

                return check
            
            else:
                check="yes"
                return check

    def destroy(self):
        self.__class__.in_use=False
        return super().destroy()