import tkinter as tk
from tkinter import ttk,messagebox
import os
import os.path
import sqlite3
from datetime import datetime

class NewSpend(tk.Toplevel):
    in_use=False

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=300,height=300)
        self.title("Nuevo Gasto")

        ######Llama al usuario
        conn=sqlite3.connect('main.db')
        cursor=conn.cursor()
        cursor.execute(f"SELECT nombre FROM usuarioActual")
        self.user_current=cursor.fetchone()[0]

        ######TIPO
        self.tag_type_movimiento=ttk.Label(
            self,
            text="Tipo:"    
        )
        # self.tag_type_movimiento.place(x=10,y=10)
        # self.list_type_movimiento=ttk.Combobox(
        #     self,
        #     state="readonly",
        #     values=["Ahorro","Gasto","Ingreso"]
        # )
        # self.list_type_movimiento.place(x=150,y=10)

        ######CATEGORÍA
        self.tag_category=ttk.Label(
            self,
            text="Categoría:"
        )
        self.tag_category.place(x=10,y=40)
        self.list_category=ttk.Combobox(
            self,
            state="readonly",
            values=["Acciones" , "Bazar","Dolares", "Electrodomésticos","Electrónica","Farmacia", "Librería", "Oro", "Ropa","Servicios","Servicios Públicos","Supermercado", "Verdulería","Viático"]
        )
        self.list_category.place(x=150,y=40)

        ######DESCRIPCIÓN
        self.tag_overview_spend=ttk.Label(
            self,
            text="Descripción:"
        )
        self.tag_overview_spend.place(x=10,y=70)
        self.box_overview_spend=ttk.Entry(self)
        self.box_overview_spend.place(x=150,y=70,width=142 ,height=20)        

        ######IMPORTE
        self.tag_new_spend=ttk.Label(
            self,
            text="Importe en pesos:"
        )
        self.tag_new_spend.place(x=10,y=100)
        self.box_new_spend=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validate_entry_numbers), "%S")
        )
        self.box_new_spend.place(x=150,y=100,width=142,height=20)

        ######FORMA DE PAGO
        self.tag_way_pay=ttk.Label(
            self,
            text="Forma de pago:"
        )
        self.tag_way_pay.place(x=10,y=130)
        self.list_way_pay=ttk.Combobox(
            self,
            state="readonly",
            values=["Efectivo","Tarjeta de Crédito","Tarjeta de Débito"]
        )
        self.list_way_pay.place(x=150,y=130)

        ######CUOTAS
        self.tag_amount_installments=ttk.Label(
            self,
            text="Cantidad de cuotas:"    
        )
        self.tag_amount_installments.place(x=10,y=160)
        self.list_amount_installments=ttk.Combobox(
            self,
            state="readonly",
            values=["1","3","6","9","12","18","24","30"]
        )
        self.list_amount_installments.place(x=150,y=160)

        ######FECHA
        self.tag_date_spend=ttk.Label(
            self,
            text="Fecha (aaaa-mm-dd):"
        )
        self.tag_date_spend.place(x=10,y=190)
        self.box_date_spend=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validate_date), "%P")
        )
        self.box_date_spend.place(x=150,y=190,width=142,height=20)

        self.btn_add=ttk.Button(
            self,
            text="Agregar",
            command=self.add_new_spend
        )
        self.btn_add.place(x=10,y=270)
        self.btn_close=tk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )
        self.btn_close.place(x=210,y=270)
        self.__class__.in_use=True


    def add_new_spend(self):
        
        # type=self.list_type_movimiento.get()
        type="Gasto"
        category=self.list_category.get()
        overview=self.check_empty(self.box_overview_spend.get())
        if overview!=False:

            amount=float(self.check_empty(self.box_new_spend.get()))
            if amount!=False:
                way_pay=self.list_way_pay.get()
                installments=int(self.list_amount_installments.get())
                date_spend=self.check_date(self.box_date_spend.get())
                if date_spend!=None:

                    amount_installments=round(amount/installments,0)

                    self.box_overview_spend.delete(0,tk.END)
                    self.box_new_spend.delete(0,tk.END)
                    # self.list_type_spend.delete(0,tk.END) ESTO NO FUNCIONA BUSCAR SOLUCIÓN
                    self.box_date_spend.delete(0,tk.END)

        # if overview==False or amount==False or date_spend==None:
        #     pass

        # else:
                    installment=0
                    year_1=int(date_spend[0:1])
                    year_2=int(date_spend[1:2])
                    year_3=int(date_spend[2:3])
                    year_4=int(date_spend[3:4])

                    month_1=int(date_spend[5:6])
                    month_2=int(date_spend[6:7])

                    day=date_spend[8:10]

                    while installment < installments:
                        installment+=1
                        if month_1==0 and month_2<9:
                            date_spend=(f'{year_1}{year_2}{year_3}{year_4}-{month_1}{month_2}-{day}')
                            month_2=month_2+1

                        elif month_1==0 and month_2==9:
                            date_spend=(f'{year_1}{year_2}{year_3}{year_4}-{month_1}{month_2}-{day}')
                            month_1=1
                            month_2=0
                            
                        
                        elif month_1==1 and month_2<2:
                            date_spend=(f'{year_1}{year_2}{year_3}{year_4}-{month_1}{month_2}-{day}')
                            month_2=month_2+1
                            
                        
                        elif month_1==1 and month_2==2:
                            if year_4<9:
                                date_spend=(f'{year_1}{year_2}{year_3}{year_4}-{month_1}{month_2}-{day}')
                                year_4=year_4+1
                                month_1=0
                                month_2=1
                                    

                            elif year_3<9:
                                date_spend=(f'{year_1}{year_2}{year_3}{year_4}-{month_1}{month_2}-{day}')
                                year_3=year_3+1
                                year_4=0
                                month_1=0
                                month_2=1
                                
                            elif year_2<9:
                                date_spend=(f'{year_1}{year_2}{year_3}{year_4}-{month_1}{month_2}-{day}')
                                year_2=year_2+1
                                year_3=0
                                year_4=0
                                month_1=0
                                month_2=1
                                
                            elif year_1<9:
                                date_spend=(f'{year_1}{year_2}{year_3}{year_4}-{month_1}{month_2}-{day}')
                                year_1=year_1+1
                                year_2=0
                                year_3=0
                                year_4=0
                                month_1=0
                                month_2=1
                                

                        conn=sqlite3.connect('main.db')
                        cursor=conn.cursor()
                        cursor.execute(f"SELECT id FROM usuarios WHERE nombre=?",[f"{self.user_current}"])
                        id_user=cursor.fetchone()[0]
                        cursor.execute("INSERT INTO gastos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (type, category, overview, amount_installments,way_pay,installment,installments,date_spend, id_user))
                        conn.commit()
                        conn.close()

    def validate_entry_numbers(self,text):
        return text.isdecimal()

    def validate_date(self,date):
        if len(date)>10:
            return False
        check=[]
        for i, letter in enumerate(date):
            if i in (4,7):
                check.append(letter=="-")
            else:
                check.append(letter.isdecimal())
        return all(check)


    def check_date(self,date):
        date_check=date
        try:
            datetime.strptime(date_check, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning(
            title="Advertencia",
            message="Por favor ingrese una fecha correcta del tipo 'aaaa-mm-dd'"
        )
        else:
            return date_check


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

#########################################################################################

class SpendMonthly(tk.Toplevel):
    in_use=False
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=800,height=800)
        self.title("Gastos Mensuales")
        
        self.table_spend=ttk.Treeview(self,
            columns=("descripcion","importe", "fp","cuota", "cuotas","fecha"),
            show="headings"
        )
        self.table_spend.heading("descripcion", text="Descripción")
        self.table_spend.heading("importe",text="importe")
        self.table_spend.heading("fp", text="Forma de pago")
        self.table_spend.heading("cuota",text="Cuota")
        self.table_spend.heading("cuotas",text="Cuotas")
        self.table_spend.heading("fecha",text="Fecha")

        self.table_spend.column("descripcion",width=50)
        self.table_spend.column("importe",width=50)
        self.table_spend.column("fp",width=70)
        self.table_spend.column("cuota",width=25)
        self.table_spend.column("cuotas",width=25)
        self.table_spend.column("fecha",width=50)

        self.table_spend.place(x=10,y=45,width=750,height=550)


        self.tag_year=ttk.Label(
            self,
            text="Año:"
        )
        self.tag_year.place(x=10,y=10)
        self.box_year=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validate_entry_year), "%P")
        )
        self.box_year.place(x=50,y=10)

        self.tag_month=ttk.Label(
            self,
            text="Mes:"
        )
        self.tag_month.place(x=200,y=10)
        self.list_months=ttk.Combobox(
            self,
            state="readonline",
            values=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio" ,"Agosto" ,"Septiembre" ,"Octubre" ,"Noviembre" ,"Diciembre"]
        )
        self.list_months.place(x=240,y=10)

        self.btn_display_month=ttk.Button(
            self,
            text="Mostrar",
            command=self.display_spend_month
        )
        self.btn_display_month.place(x=400,y=8)

        self.btn_close=ttk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )
        self.btn_close.place(x=500,y=770)
        self.__class__.in_use=True


    def display_spend_month(self):
        month=self.list_months.get()
        months={"Enero":"01","Febrero":"02","Marzo":"03","Abril":"04","Mayo":"05","Junio":"06","Julio":"07" ,"Agosto":"08" ,"Septiembre":"09" ,"Octubre":"10" ,"Noviembre":"11" ,"Diciembre":"12"}
        month_display=months[month]

        ######Llama al usuario
        conn=sqlite3.connect('main.db')
        cursor=conn.cursor()
        cursor.execute(f"SELECT usuarioId FROM usuarioActual")
        self.userId_current=cursor.fetchone()[0]
        
        conn=sqlite3.connect('main.db')
        
        cursor=conn.cursor()
        cursor.execute(f"SELECT descripcion, importe, formadepago, cuota, cantidadCuotas, fecha FROM gastos WHERE usuarioId={self.userId_current} AND tipo='Gasto' AND strftime('%m', fecha)='{month_display}' ORDER BY fecha")
        spend_monthly=cursor.fetchall()      
        self.table_spend.delete(*self.table_spend.get_children())
        for spend in spend_monthly:
            
            overview=spend[0]
            amount=f'$ {spend[1]}'
            waytopay=spend[2]
            installment=spend[3]
            installments=spend[4]
            date=spend[5]
            self.table_spend.insert("",tk.END,values=(overview, amount, waytopay, installment, installments, date))

        conn.close()

    def validate_entry_year(self,text):
        if text=="":
            return True
        else:        
            if len(text)>4:
                return False
            return text.isdecimal()

    def destroy(self):
        self.__class__.in_use=False
        return super().destroy()