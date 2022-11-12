from atexit import register
from cgitb import text
import os
import os.path
import sqlite3
import tkinter as tk
from tkinter import ttk,messagebox
from base64 import b64decode


icono_chico_datos="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwABGUAAARlAAYDjddQAAAJJSURBVDhPY8AH5vip8349W+D770KGGFQIAzBBaazg//9/8X//Mm/6y/RXDyqEARihNBzM8FfX5eNhrFDW43YWVZASl9XXYfj/8/Wlv1+fXP/789UZ7tfn+hnDGP5ClaMaMM9f3YqX/+8eh2BWTm4RKQZWHlkGZm5phv+/PjP8/vwAjL/8ZeCRdL/0FaoF1Qv//v9v0DT6wsnB+Rfk/Me3zrxc8ev7H4Ynt972XDr85uSbF3/fQ5XCAVoYMGrxCkCE/v/5PfP4prvb/v35xyCrJjvbrOSYhWLMVSFk20EAxQDG/wxPv33jgLBZWBPUjMXMMEMJFaAawPSv8fZltj//GZgZGBmZVCz9VXI4eNgY/jF8PfT1qMuST3tUtKBK4QDFgKSNt7e9es5gd/7g/+1fPvz8BRUGOoJRnJmFK5qRkfv0x+0allBhMMDpwPnx8hwK8rKp9rH2k24evf6Kl/etGD//e4Z/f77t5fe44wJVhh6ICJC48OGPBxdfPQZZoWyqGnps05tPjCxcDP8ZmDShSsAAxYC5gar6OwqUz3/eo9f1dKWBK68wJzAVMTAcXnk2XFyek/f/P6Cv/v99BFUOBugJyVda8ecmKy82YAKSZWDhlmFg4ZFh+P3tI8P/748Yfn1++P/vzy9Bgt53N0C1oLrg7z/WUyys7BP+M7Bc/v//LzC5QsxnYWFi+Pfvz31gPIcgawYBnIH4dJMP17O7P2ONfc1mMPz5lcq4nGseY2PjP6g0cWBVmjH//9vVof/uVopDhdAAAwMAm23eqvMMP2oAAAAASUVORK5CYII="
icono_grande_datos="iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwABGUAAARlAAYDjddQAAAUvSURBVFhH1ZZdbFRFFMfPzNz96JZtt7Sl0EJpod22yEcfgBJtVfyoBFo+AkRIhD5IfJDoi8bogyEkPDQxiA/6gBAkiJCAEUTRlUpTIQYBpU1MGksVLBSh0O52v9rdu/fOeO7uLF/duyxFY/xlb869c+7MnDnzn3MX/muItONiT5N7wZLXn2opKitwCtXrUWbvPChdGUOlHReckL1CE5upYt8oBJ8rmx+KcQdwaO1aRoiRwUdKYua9P252lxMQ6yihi+0TlDmFJfZJrskuWl3/GDgL80ENXP5JD1/7hqtD1ym1XRyx6V0Fi84FZHdTHhjArjWzJhJVex8Eeal4hoXVLMiCorIcYFmFwKy5QK05QCwTQMTCoKvDwPHSo2hjAZ2rgfPRLL2xsL4nKIcbQ9ot2Nk0q5So+nlGSUvd88AaVligqNQGRLFh6Olix70RnAmuL9LCsSzZmBLTALZsAcqIfginmVH7eAimV0ZQdbr0/nOYBjCts6oJF1mXkxeD8qqwbL0Dqn6gv2coGB2NxZ9vXfVdvXj2r/CVbj+MhrR4WyaYb4GAZsMUlyUHE9JiIri+3SZyp53c9+u58DBmBplYWvSqx9NV2HGo77UvP+z/9tTRcOdAv/BBKO42xXQjdy+vOo3O+vlPqzB9pk+KzQXU4gw4uJJPFv+g7W52e1a+8cwL+aVTQNNizRb3tq9l94wxzQARkB2/oZa4ScaaOPsSQpLOcWMaACb8umFHR+xy7uQWEGfUbt8cvwORVuGZYJ4BKtoMO9AXAWrLN1rwSgTBge1Qf3lx/7SagqlMMZdRJtxJ5318uqQiR7WybrwtaVxvg1yXHzWQi8UHtYAXxSLELIZNFCIeC9/UI0Nd2si1dhTEQUfD91cSI6XHNPwNnt+xjPLVQsDwubYIrnqC9KQGVzKJUNZIFUerrnr/CHoqdvqOzHNJtylp8/fysd6zlNOFw4PQ0XFEw/Mdw03g0psaQhWjTCvElvsKy9bPDn41tUS6UmK6BfezZ0Vlg93BWqrns6Xl8yZPceSl+xb4Qag+0NSQMcEZ54/d9WRr6sgzDuAuyL417rIn11fPGroWfbe2cU4dtTohMHAL9NFbkGX3YZbwfBgBYCCEMNAjg6vylt88Kvvfw3gkLDZ+fvFy2epjxzvb/uxJruHGZe+FLz7o+u3kgQGIhNR4m4Ee9YLiLF8lH8fwSGeIYu/kR7FyQdnnaBbisfVfaA/i1kj9oYoJUaoSD2N5pAASJHeRRzcdM7774kbQGwHCsIBJULimFTNtAHtXVszEer/t5/eq2/wnqpcZi5GuOAlVyQopaOSTFZW1+EpFfrEDhDaSaMceqIiriYexKNKmRNPZ25jiTVYWBsZcz4Xaay/5vxPH+3pJYPCGPea9Hp3LuQCG73ae6N7AOWktnpnN5jY4jX9E8TGMgqWG+k/GH1Jwz4ruZ3dz1S4jgLpng1DqttxbCfHoMWtefAJiyYZIANWPkzISwOMYvH0KBOc3NTFUWbDUm/L/YUYawBTKu7vA45Ug4bNlWcFix4SSu4YkNIbRtJhNbpA+AAIdQoghUPLiFe72fj8IoeMvOig4We5q6vPI1pSkDQBV/Vk4xktG/OFlHBytGMVpjl8dVBhOkqKwoUqFrvq4NrKdU1eNa0l32skN0mogFUJsoZEzZ2Yo9nx3b1fozeonahYbGuDaaDuP+FqZve8UdXui8vV/l/3rZn/Ee94S4tJWwXvf2SGbH4qMRGiGYmMHMOmHsSIc5rq4IJv/TwD8DaeKBW/ao4INAAAAAElFTkSuQmCC"

class NuevoGasto(tk.Toplevel):
    en_uso=False

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=300,height=300)
        self.title("Nuevo Registro")

        ######Llama al usuario
        f=open("usuario_actual.txt","r",encoding="utf8")
        self.usuario_actual=str(f.read())
        f.close()

        ######TIPO
        self.etiqueta_tipo_movimiento=ttk.Label(
            self,
            text="Tipo:"    
        )
        self.etiqueta_tipo_movimiento.place(x=10,y=10)
        self.lista_tipo_movimiento=ttk.Combobox(
            self,
            state="readonly",
            values=["Ahorro","Gasto","Ingreso"]
        )
        self.lista_tipo_movimiento.place(x=150,y=10)

        ######CATEGORÍA
        self.etiqueta_categoria=ttk.Label(
            self,
            text="Categoría:"
        )
        self.etiqueta_categoria.place(x=10,y=40)
        self.lista_categoria=ttk.Combobox(
            self,
            state="readonly",
            values=["Acciones" , "Bazar","Dolares", "Electrodomésticos","Electrónica","Farmacia", "Librería", "Oro", "Ropa","Servicios","Servicios Públicos","Supermercado", "Verdulería","Viático"]
        )
        self.lista_categoria.place(x=150,y=40)

        ######DESCRIPCIÓN
        self.etiqueta_descripcion_gasto=ttk.Label(
            self,
            text="Descripción:"
        )
        self.etiqueta_descripcion_gasto.place(x=10,y=70)
        self.caja_descripcion_gasto=ttk.Entry(self)
        self.caja_descripcion_gasto.place(x=150,y=70,width=142 ,height=20)        

        ######IMPORTE
        self.etiqueta_nuevo_gasto=ttk.Label(
            self,
            text="Importe en pesos:"
        )
        self.etiqueta_nuevo_gasto.place(x=10,y=100)
        self.caja_nuevo_gasto=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validar_entrda_numeros), "%S")
        )
        self.caja_nuevo_gasto.place(x=150,y=100,width=142,height=20)

        ######FORMA DE PAGO
        self.etiqueta_forma_pago=ttk.Label(
            self,
            text="Forma de pago:"
        )
        self.etiqueta_forma_pago.place(x=10,y=130)
        self.lista_forma_pago=ttk.Combobox(
            self,
            state="readonly",
            values=["Efectivo","Tarjeta de Crédito","Tarjeta de Débito"]
        )
        self.lista_forma_pago.place(x=150,y=130)

        ######CUOTAS
        self.etiqueta_cantidad_cuotas=ttk.Label(
            self,
            text="Cantidad de cuotas:"    
        )
        self.etiqueta_cantidad_cuotas.place(x=10,y=160)
        self.lista_cantidad_cuotas=ttk.Combobox(
            self,
            state="readonly",
            values=["1","3","6","9","12","18","24","30"]
        )
        self.lista_cantidad_cuotas.place(x=150,y=160)

        ######FECHA
        self.etiqueta_fecha_gasto=ttk.Label(
            self,
            text="Fecha (aaaa-mm-dd):"
        )
        self.etiqueta_fecha_gasto.place(x=10,y=190)
        self.caja_fecha_gasto=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validar_fecha), "%P")
        )
        self.caja_fecha_gasto.place(x=150,y=190,width=142,height=20)

        self.boton_agregar=ttk.Button(
            self,
            text="Agregar",
            command=self.agregar_nuevo_gasto
        )
        self.boton_agregar.place(x=10,y=270)
        self.boton_cerrar=tk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )
        self.boton_cerrar.place(x=210,y=270)
        self.__class__.en_uso=True


    def agregar_nuevo_gasto(self):
        
        tipo=self.lista_tipo_movimiento.get()
        categoria=self.lista_categoria.get()
        descripcion=self.verificar_vacio(self.caja_descripcion_gasto.get())
        importe=self.verificar_vacio(self.caja_nuevo_gasto.get())
        forma_pago=self.lista_forma_pago.get()
        cuotas=self.lista_cantidad_cuotas.get()
        fecha_gasto=self.caja_fecha_gasto.get()

        self.caja_descripcion_gasto.delete(0,tk.END)
        self.caja_nuevo_gasto.delete(0,tk.END)
        # self.lista_tipo_gasto.delete(0,tk.END) ESTO NO FUNCIONA BUSCAR SOLUCIÓN
        self.caja_fecha_gasto.delete(0,tk.END)
        if descripcion==False or importe==False or fecha_gasto==None:
            pass

        else:
            cuota=0
            cuotas=int(cuotas)
            año_1=int(fecha_gasto[0:1])
            año_2=int(fecha_gasto[1:2])
            año_3=int(fecha_gasto[2:3])
            año_4=int(fecha_gasto[3:4])

            mes_1=int(fecha_gasto[5:6])
            mes_2=int(fecha_gasto[6:7])

            dia=fecha_gasto[8:10]

            while cuota < cuotas:
                cuota+=1
                if mes_1==0 and mes_2<9:
                    fecha_gasto=(f'{año_1}{año_2}{año_3}{año_4}-{mes_1}{mes_2}-{dia}')
                    mes_2=mes_2+1

                elif mes_1==0 and mes_2==9:
                    fecha_gasto=(f'{año_1}{año_2}{año_3}{año_4}-{mes_1}{mes_2}-{dia}')
                    mes_1=1
                    mes_2=0
                    
                
                elif mes_1==1 and mes_2<2:
                    fecha_gasto=(f'{año_1}{año_2}{año_3}{año_4}-{mes_1}{mes_2}-{dia}')
                    mes_2=mes_2+1
                    
                
                elif mes_1==1 and mes_2==2:
                    if año_4<9:
                        fecha_gasto=(f'{año_1}{año_2}{año_3}{año_4}-{mes_1}{mes_2}-{dia}')
                        año_4=año_4+1
                        mes_1=0
                        mes_2=1
                              

                    elif año_3<9:
                        fecha_gasto=(f'{año_1}{año_2}{año_3}{año_4}-{mes_1}{mes_2}-{dia}')
                        año_3=año_3+1
                        año_4=0
                        mes_1=0
                        mes_2=1
                        
                    elif año_2<9:
                        fecha_gasto=(f'{año_1}{año_2}{año_3}{año_4}-{mes_1}{mes_2}-{dia}')
                        año_2=año_2+1
                        año_3=0
                        año_4=0
                        mes_1=0
                        mes_2=1
                        
                    elif año_1<9:
                        fecha_gasto=(f'{año_1}{año_2}{año_3}{año_4}-{mes_1}{mes_2}-{dia}')
                        año_1=año_1+1
                        año_2=0
                        año_3=0
                        año_4=0
                        mes_1=0
                        mes_2=1
                        

                conn=sqlite3.connect(f'{self.usuario_actual}.db')
                cursor=conn.cursor()
                cursor.execute("INSERT INTO gastos VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (tipo, categoria, descripcion, importe,forma_pago,cuota,cuotas,fecha_gasto))
                conn.commit()
                conn.close()

    def validar_entrda_numeros(self,texto):
        return texto.isdecimal()

    def validar_fecha(self,fecha):
        if len(fecha)>10:
            return False
        chequeo=[]
        for i, letra in enumerate(fecha):
            if i in (4,7):
                chequeo.append(letra=="-")
            else:
                chequeo.append(letra.isdecimal())
        return all(chequeo)

    def verificar_vacio(self,dato):
        dato_verificar=dato
        if dato_verificar=="":
            messagebox.showwarning(
                title="Advertencia",
                message="Por favor ingrese un monto en pesos."
            )
            return False
        else:
            return dato_verificar

    def destroy(self):
        self.__class__.en_uso=False
        return super().destroy()

#########################################################################################

class VentanaAhorros(tk.Toplevel):
    en_uso=False

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=800,height=800)
        self.title("Ahorros")

        self.tabla_gasto=ttk.Treeview(self,
            columns=("tipo","especie", "cantidad","cotización","precio_p" ,"precio_d"),
            show="headings"
        )
        self.tabla_gasto.heading("tipo", text="Tipo")
        self.tabla_gasto.heading("especie",text="Especie")
        self.tabla_gasto.heading("cantidad",text="Cantidad")
        self.tabla_gasto.heading("cotización",text="Cotización")
        self.tabla_gasto.heading("precio_p", text="Precio en pesos")
        self.tabla_gasto.heading("precio_d",text="Precio en dolares")

        self.tabla_gasto.column("tipo",width=50)
        self.tabla_gasto.column("especie",width=50)
        self.tabla_gasto.column("cantidad",width=70)
        self.tabla_gasto.column("cotización",width=70)
        self.tabla_gasto.column("precio_p",width=25)
        self.tabla_gasto.column("precio_d",width=25)

        self.tabla_gasto.place(x=10,y=45,width=750,height=550)

        # Lee la base de datos
        f=open("usuario_actual.txt","r",encoding="utf8")
        usuario_actual=str(f.read())
        f.close()
        
        conn=sqlite3.connect(f'{usuario_actual}.db')
        
        cursor=conn.cursor()
        cursor.execute(f"SELECT tipo, especie, cantidad FROM ahorros ORDER BY especie")
        ahorros=cursor.fetchall()
        self.tabla_gasto.delete(*self.tabla_gasto.get_children())
        for ahorro in ahorros:
            
            tipo=ahorro[0]
            especie=ahorro[1]
            cantidad=ahorro[2]
            cotización=0
            precio_p=0
            precio_d=0

            self.tabla_gasto.insert("",tk.END,values=(tipo, especie, cantidad, cotización,precio_p,precio_d))

        self.boton_cerrar=ttk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )

        self.boton_cerrar.place(x=400,y=770)
        # Indicar que está en uso luego de crearse
        self.__class__.en_uso=True

    def destroy(self):
        self.__class__.en_uso=False
        return super().destroy()

#########################################################################################

class UsuarioExistente(tk.Toplevel):
    en_uso=False

    def __init__(self,*args,callback=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=300,height=100)
        self.callback=callback
        self.title("Usuario existente")

        self.boton_cerrar=ttk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )

        self.etiqueta_usuario_existente=ttk.Label(
            self,
            text="Usuario existente"
        )
        self.etiqueta_usuario_existente.place(x=10,y=10)
        
        if os.path.isfile("usuarios.txt")==True:
            f=open("usuarios.txt","r",encoding="utf8")
            usuarios=f.read().split("\n")[:-1]
            f.close()

        else:
            usuarios=[]
            messagebox.showwarning(
                title="Advertencia",
                message="No existe ningún usuario."
            )

        self.lista_usuarios=ttk.Combobox(
            self,
            state="readonly",
            values=usuarios
        )
        self.lista_usuarios.place(x=150,y=10)

        self.boton_seleccionar_usuario=ttk.Button(
            self,
            text="Seleccionar Usuario",
            command=self.seleccionar_usuario
        )
        self.boton_seleccionar_usuario.place(x=10,y=70)

        self.boton_cerrar.place(x=210,y=70)
        # Indicar que está en uso luego de crearse
        self.__class__.en_uso=True


    def seleccionar_usuario(self):
        usuario_seleccionado=self.lista_usuarios.get()
        f=open("usuario_actual.txt","w",encoding="utf8")
        f.write(usuario_seleccionado)

        f.close()

        self.callback(self.lista_usuarios.get())


     
    def destroy(self):
        self.__class__.en_uso=False
        return super().destroy()

#########################################################################################

class CrearUsuario(tk.Toplevel):
    en_uso=False

    def __init__(self,*args,callback=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=280,height=100)

        self.callback=callback

        self.title("Crear usuario")

        self.boton_cerrar=ttk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )


        self.etiqueta_nuevo_usuario=ttk.Label(
            self,
            text="Nuevo usuario"
        )
        self.etiqueta_nuevo_usuario.place(x=10,y=10)

        self.caja_nuevo_usuario=ttk.Entry(self)
        self.caja_nuevo_usuario.place(x=120,y=10,width=150,height=25)


        self.boton_agregar_usuario=ttk.Button(
            self,
            text="Agregar usuario",
            command=self.crear_base_datos
        )
        self.boton_agregar_usuario.place(x=10,y=70)

        self.boton_cerrar.place(x=190,y=70)

        # Indicar que está en uso luego de crearse
        self.__class__.en_uso=True


    def crear_base_datos(self):
        usuario=self.caja_nuevo_usuario.get()
        if usuario.strip()=="":
            messagebox.showwarning(
                title="Advertencia",
                message="Por favor agregue un nombre de usuario válido."
            )

        else:
            f=open("usuario_actual.txt","w",encoding="utf8")
            f.write(usuario)
            f.close()

            f=open("usuarios.txt","a",encoding="utf8")
            f.write(f'{usuario}\n')
            f.close()
       
            conn=sqlite3.connect(f'{usuario}.db')
            cursor=conn.cursor()
            
            self.callback(self.caja_nuevo_usuario.get())


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
        self.__class__.en_uso=False
        return super().destroy()

#########################################################################################

class NuevoAhorro(tk.Toplevel):
    en_uso=False

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=300,height=300)
        self.title("Ahorros")

        ######Llama al usuario
        f=open("usuario_actual.txt","r",encoding="utf8")
        self.usuario_actual=str(f.read())
        f.close()

        ######TIPO
        self.etiqueta_tipo_movimiento=ttk.Label(
            self,
            text="Tipo:"    
        )
        self.etiqueta_tipo_movimiento.place(x=10,y=10)
        self.lista_tipo_movimiento=ttk.Combobox(
            self,
            state="readonly",
            values=["Acción","Bono", "Cedear", "Dolar", "Oro"]
        )
        self.lista_tipo_movimiento.place(x=150,y=10)

        ######ESPECIE
        self.etiqueta_especie=ttk.Label(
            self,
            text="Especie:"
        )
        self.etiqueta_especie.place(x=10,y=40)
        self.caja_especie=ttk.Entry(
            self
            )
        self.caja_especie.place(x=150,y=40)

        ######CANTIDAD
        self.etiqueta_cantidad=ttk.Label(
            self,
            text="Cantidad:"
        )
        self.etiqueta_cantidad.place(x=10,y=70)
        self.caja_cantidad=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validar_entrda_numeros), "%S")
            )
        self.caja_cantidad.place(x=150,y=70,width=142 ,height=20)        

        ######FECHA
        self.etiqueta_fecha_gasto=ttk.Label(
            self,
            text="Fecha (aaaa-mm-dd):"
        )
        self.etiqueta_fecha_gasto.place(x=10,y=190)
        self.caja_fecha_gasto=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validar_fecha), "%P")
        )
        self.caja_fecha_gasto.place(x=150,y=190,width=142,height=20)

        self.boton_agregar=ttk.Button(
            self,
            text="Agregar",
            command=self.agregar_nuevo_ahorro
        )
        self.boton_agregar.place(x=10,y=270)
        self.boton_cerrar=tk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )
        self.boton_cerrar.place(x=210,y=270)
        self.__class__.en_uso=True


    def agregar_nuevo_ahorro(self):
        
        tipo=self.lista_tipo_movimiento.get()
        especie=self.verificar_vacio(self.caja_especie.get())
        cantidad=self.verificar_vacio(self.caja_cantidad.get())
        # importe=self.verificar_vacio(self.caja_nuevo_gasto.get())
        # forma_pago=self.lista_forma_pago.get()
        # cuotas=self.lista_cantidad_cuotas.get()
        fecha_ahorro=self.caja_fecha_gasto.get()

        self.caja_especie.delete(0,tk.END)
        self.caja_cantidad.delete(0,tk.END)
        # self.lista_tipo_gasto.delete(0,tk.END) ESTO NO FUNCIONA BUSCAR SOLUCIÓN
        self.caja_fecha_gasto.delete(0,tk.END)
        if especie==False or cantidad==False or fecha_ahorro==None:
            pass

        else:
            conn=sqlite3.connect(f'{self.usuario_actual}.db')
            cursor=conn.cursor()
            cursor.execute("INSERT INTO ahorros VALUES (?, ?, ?, ?)", (tipo, especie, cantidad,fecha_ahorro))
            conn.commit()
            conn.close()

    def validar_entrda_numeros(self,texto):
        return texto.isdecimal()

    def validar_fecha(self,fecha):
        if len(fecha)>10:
            return False
        chequeo=[]
        for i, letra in enumerate(fecha):
            if i in (4,7):
                chequeo.append(letra=="-")
            else:
                chequeo.append(letra.isdecimal())
        return all(chequeo)

    def verificar_vacio(self,dato):
        dato_verificar=dato
        if dato_verificar=="":
            messagebox.showwarning(
                title="Advertencia",
                message="Por favor ingrese un monto en pesos."
            )
            return False
        else:
            return dato_verificar

    def destroy(self):
        self.__class__.en_uso=False
        return super().destroy()

#########################################################################################

class GastosMensuales(tk.Toplevel):
    en_uso=False
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=800,height=800)
        self.title("Gastos Mensuales")
        
        self.tabla_gasto=ttk.Treeview(self,
            columns=("descripcion","importe", "fp","cuota", "cuotas","fecha"),
            show="headings"
        )
        self.tabla_gasto.heading("descripcion", text="Descripción")
        self.tabla_gasto.heading("importe",text="importe")
        self.tabla_gasto.heading("fp", text="Forma de pago")
        self.tabla_gasto.heading("cuota",text="Cuota")
        self.tabla_gasto.heading("cuotas",text="Cuotas")
        self.tabla_gasto.heading("fecha",text="Fecha")

        self.tabla_gasto.column("descripcion",width=50)
        self.tabla_gasto.column("importe",width=50)
        self.tabla_gasto.column("fp",width=70)
        self.tabla_gasto.column("cuota",width=25)
        self.tabla_gasto.column("cuotas",width=25)
        self.tabla_gasto.column("fecha",width=50)

        self.tabla_gasto.place(x=10,y=45,width=750,height=550)


        self.etiqueta_año=ttk.Label(
            self,
            text="Año:"
        )
        self.etiqueta_año.place(x=10,y=10)
        self.caja_año=ttk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validar_entrada_año), "%P")
        )
        self.caja_año.place(x=50,y=10)

        self.etiqueta_mes=ttk.Label(
            self,
            text="Mes:"
        )
        self.etiqueta_mes.place(x=200,y=10)
        self.lista_meses=ttk.Combobox(
            self,
            state="readonline",
            values=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio" ,"Agosto" ,"Septiembre" ,"Octubre" ,"Noviembre" ,"Diciembre"]
        )
        self.lista_meses.place(x=240,y=10)

        self.boton_mostrar_mes=ttk.Button(
            self,
            text="Mostrar",
            command=self.mostrar_gastos_mes
        )
        self.boton_mostrar_mes.place(x=400,y=8)

        self.boton_cerrar=ttk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )
        self.boton_cerrar.place(x=500,y=770)
        self.__class__.en_uso=True


    def mostrar_gastos_mes(self):
        mes=self.lista_meses.get()
        meses={"Enero":"01","Febrero":"02","Marzo":"03","Abril":"04","Mayo":"05","Junio":"06","Julio":"07" ,"Agosto":"08" ,"Septiembre":"09" ,"Octubre":"10" ,"Noviembre":"11" ,"Diciembre":"12"}
        mes_mostrar=meses[mes]

        f=open("usuario_actual.txt","r",encoding="utf8")
        usuario_actual=str(f.read())
        f.close()
        
        conn=sqlite3.connect(f'{usuario_actual}.db')
        
        cursor=conn.cursor()
        cursor.execute(f"SELECT descripcion, importe, formadepago, cuota, cantidadCuotas, fecha FROM gastos WHERE tipo='Gasto' AND strftime('%m', fecha)='{mes_mostrar}' ORDER BY fecha")
        gastos_mensuales=cursor.fetchall()
        self.tabla_gasto.delete(*self.tabla_gasto.get_children())
        for gasto in gastos_mensuales:
            
            descripcion=gasto[0]
            importe=f'$ {gasto[1]}'
            formadepago=gasto[2]
            cuota=gasto[3]
            cuotas=gasto[4]
            fecha=gasto[5]
            self.tabla_gasto.insert("",tk.END,values=(descripcion, importe, formadepago, cuota, cuotas, fecha))

    def validar_entrada_año(self,texto):
        if len(texto)>4:
            return False
        return texto.isdecimal()

    def destroy(self):
        self.__class__.en_uso=False
        return super().destroy()

#########################################################################################

class VentanaPrincipal(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=800,height=300)
        self.title("Gestor de gastos")
        icono_chico=tk.PhotoImage(data=b64decode(icono_chico_datos))
        icono_grande=tk.PhotoImage(data=b64decode(icono_grande_datos))
        self.iconphoto(True,icono_grande,icono_chico)

        self.boton_crear_usuario=ttk.Button(
            self,
            text="Crear usuario",
            command=self.abrir_crear_usuario
            )
        self.boton_crear_usuario.place(x=270,y=10,width=110, height=25)

        self.boton_usuario_exitente=ttk.Button(
            self,
            text="Usuario existente",
            command=self.abrir_usuario_existente
            )
        self.boton_usuario_exitente.place(x=390,y=10,width=110, height=25)

        self.boton_nuevo_gasto=ttk.Button(
            self,
            text="Nuevo Registro",
            command=self.abrir_nuevo_gasto
            )
        self.boton_nuevo_gasto.place(x=390,y=45,width=110, height=25)

        self.boton_consumo=ttk.Button(
            self,
            text="Gastos mensuales",
            command=self.abrir_gastos_mensuales
            )
        self.boton_consumo.place(x=270,y=45,width=110, height=25)

        self.boton_ahorros=ttk.Button(
            self,
            text="Ahorros",
            command=self.abrir_ahorros
        )
        self.boton_ahorros.place(x=270,y=80,width=110, height=25)

        self.boton_nuevo_ahorro=ttk.Button(
            self,
            text="Nuevo Ahorro",
            command=self.abrir_nuevo_ahorro
        )
        self.boton_nuevo_ahorro.place(x=390,y=80,width=110, height=25)

        ###################VERIFICA SI EXISTE UN USUARIO###########
        
        if os.path.isfile("usuario_actual.txt")==True:

            f=open("usuario_actual.txt","r",encoding="utf8")

            usuario_actual=str(f.read())
                
            f.close()

        else:
            usuario_actual="No existe ningún usuario."
                
        self.etiqueta_usuario_actual=ttk.Label(
            self,
            text=f'El usuario actual es: {usuario_actual}'
        )
        self.etiqueta_usuario_actual.place(x=10,y=10)

        ##########################################################   

    def abrir_crear_usuario(self):
        if not CrearUsuario.en_uso:
            self.crear_usuario=CrearUsuario(
                callback=self.usuario_actual
            )
    
    def abrir_usuario_existente(self):
        if not UsuarioExistente.en_uso:
            self.usuario_existente=UsuarioExistente(
                callback=self.usuario_actual
            )

    def abrir_nuevo_gasto(self):
        if not NuevoGasto.en_uso:
            self.nuevo_gasto=NuevoGasto()
    
    def abrir_nuevo_ahorro(self):
        if not NuevoAhorro.en_uso:
            self.nuevo_gasto=NuevoAhorro()

    def abrir_gastos_mensuales(self):
        if not GastosMensuales.en_uso:
            self.gastos_mensuales=GastosMensuales()

    def usuario_actual(self, usuario):
            self.etiqueta_usuario_actual.config(
                text=f'El usuario actual es: {usuario}'
            )
    
    def abrir_ahorros(self):
        if not VentanaAhorros.en_uso:
            self.ahorros=VentanaAhorros()

ventana_principal=VentanaPrincipal()
ventana_principal.mainloop()