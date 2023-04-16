import os
import os.path
import sqlite3
import tkinter as tk
from tkinter import ttk
from base64 import b64decode
from plugin_user import UserList, NewUser
from plugin_spend import NewSpend, SpendMonthly
from plugin_saving import NewSaving, VindowSaving

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.config(width=800,height=300)
        self.title("Gestor de gastos")

        ico_small_data="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwABGUAAARlAAYDjddQAAAJJSURBVDhPY8AH5vip8349W+D770KGGFQIAzBBaazg//9/8X//Mm/6y/RXDyqEARihNBzM8FfX5eNhrFDW43YWVZASl9XXYfj/8/Wlv1+fXP/789UZ7tfn+hnDGP5ClaMaMM9f3YqX/+8eh2BWTm4RKQZWHlkGZm5phv+/PjP8/vwAjL/8ZeCRdL/0FaoF1Qv//v9v0DT6wsnB+Rfk/Me3zrxc8ev7H4Ynt972XDr85uSbF3/fQ5XCAVoYMGrxCkCE/v/5PfP4prvb/v35xyCrJjvbrOSYhWLMVSFk20EAxQDG/wxPv33jgLBZWBPUjMXMMEMJFaAawPSv8fZltj//GZgZGBmZVCz9VXI4eNgY/jF8PfT1qMuST3tUtKBK4QDFgKSNt7e9es5gd/7g/+1fPvz8BRUGOoJRnJmFK5qRkfv0x+0allBhMMDpwPnx8hwK8rKp9rH2k24evf6Kl/etGD//e4Z/f77t5fe44wJVhh6ICJC48OGPBxdfPQZZoWyqGnps05tPjCxcDP8ZmDShSsAAxYC5gar6OwqUz3/eo9f1dKWBK68wJzAVMTAcXnk2XFyek/f/P6Cv/v99BFUOBugJyVda8ecmKy82YAKSZWDhlmFg4ZFh+P3tI8P/748Yfn1++P/vzy9Bgt53N0C1oLrg7z/WUyys7BP+M7Bc/v//LzC5QsxnYWFi+Pfvz31gPIcgawYBnIH4dJMP17O7P2ONfc1mMPz5lcq4nGseY2PjP6g0cWBVmjH//9vVof/uVopDhdAAAwMAm23eqvMMP2oAAAAASUVORK5CYII="
        ico_big_data="iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwABGUAAARlAAYDjddQAAAUvSURBVFhH1ZZdbFRFFMfPzNz96JZtt7Sl0EJpod22yEcfgBJtVfyoBFo+AkRIhD5IfJDoi8bogyEkPDQxiA/6gBAkiJCAEUTRlUpTIQYBpU1MGksVLBSh0O52v9rdu/fOeO7uLF/duyxFY/xlb869c+7MnDnzn3MX/muItONiT5N7wZLXn2opKitwCtXrUWbvPChdGUOlHReckL1CE5upYt8oBJ8rmx+KcQdwaO1aRoiRwUdKYua9P252lxMQ6yihi+0TlDmFJfZJrskuWl3/GDgL80ENXP5JD1/7hqtD1ym1XRyx6V0Fi84FZHdTHhjArjWzJhJVex8Eeal4hoXVLMiCorIcYFmFwKy5QK05QCwTQMTCoKvDwPHSo2hjAZ2rgfPRLL2xsL4nKIcbQ9ot2Nk0q5So+nlGSUvd88AaVligqNQGRLFh6Olix70RnAmuL9LCsSzZmBLTALZsAcqIfginmVH7eAimV0ZQdbr0/nOYBjCts6oJF1mXkxeD8qqwbL0Dqn6gv2coGB2NxZ9vXfVdvXj2r/CVbj+MhrR4WyaYb4GAZsMUlyUHE9JiIri+3SZyp53c9+u58DBmBplYWvSqx9NV2HGo77UvP+z/9tTRcOdAv/BBKO42xXQjdy+vOo3O+vlPqzB9pk+KzQXU4gw4uJJPFv+g7W52e1a+8cwL+aVTQNNizRb3tq9l94wxzQARkB2/oZa4ScaaOPsSQpLOcWMaACb8umFHR+xy7uQWEGfUbt8cvwORVuGZYJ4BKtoMO9AXAWrLN1rwSgTBge1Qf3lx/7SagqlMMZdRJtxJ5318uqQiR7WybrwtaVxvg1yXHzWQi8UHtYAXxSLELIZNFCIeC9/UI0Nd2si1dhTEQUfD91cSI6XHNPwNnt+xjPLVQsDwubYIrnqC9KQGVzKJUNZIFUerrnr/CHoqdvqOzHNJtylp8/fysd6zlNOFw4PQ0XFEw/Mdw03g0psaQhWjTCvElvsKy9bPDn41tUS6UmK6BfezZ0Vlg93BWqrns6Xl8yZPceSl+xb4Qag+0NSQMcEZ54/d9WRr6sgzDuAuyL417rIn11fPGroWfbe2cU4dtTohMHAL9NFbkGX3YZbwfBgBYCCEMNAjg6vylt88Kvvfw3gkLDZ+fvFy2epjxzvb/uxJruHGZe+FLz7o+u3kgQGIhNR4m4Ee9YLiLF8lH8fwSGeIYu/kR7FyQdnnaBbisfVfaA/i1kj9oYoJUaoSD2N5pAASJHeRRzcdM7774kbQGwHCsIBJULimFTNtAHtXVszEer/t5/eq2/wnqpcZi5GuOAlVyQopaOSTFZW1+EpFfrEDhDaSaMceqIiriYexKNKmRNPZ25jiTVYWBsZcz4Xaay/5vxPH+3pJYPCGPea9Hp3LuQCG73ae6N7AOWktnpnN5jY4jX9E8TGMgqWG+k/GH1Jwz4ruZ3dz1S4jgLpng1DqttxbCfHoMWtefAJiyYZIANWPkzISwOMYvH0KBOc3NTFUWbDUm/L/YUYawBTKu7vA45Ug4bNlWcFix4SSu4YkNIbRtJhNbpA+AAIdQoghUPLiFe72fj8IoeMvOig4We5q6vPI1pSkDQBV/Vk4xktG/OFlHBytGMVpjl8dVBhOkqKwoUqFrvq4NrKdU1eNa0l32skN0mogFUJsoZEzZ2Yo9nx3b1fozeonahYbGuDaaDuP+FqZve8UdXui8vV/l/3rZn/Ee94S4tJWwXvf2SGbH4qMRGiGYmMHMOmHsSIc5rq4IJv/TwD8DaeKBW/ao4INAAAAAElFTkSuQmCC"

        ico_small=tk.PhotoImage(data=b64decode(ico_small_data))
        ico_big=tk.PhotoImage(data=b64decode(ico_big_data))
        self.iconphoto(True,ico_big,ico_small)

        self.btn_new_user=ttk.Button(
            self,
            text="Crear usuario",
            command=self.open_new_user
            )
        self.btn_new_user.place(x=270,y=10,width=110, height=25)

        self.btn_user_existing=ttk.Button(
            self,
            text="Usuario existente",
            command=self.open_user_existente
            )
        self.btn_user_existing.place(x=390,y=10,width=110, height=25)

        self.btn_new_spend=ttk.Button(
            self,
            text="Nuevo Gasto",
            command=self.open_new_spend
            )
        self.btn_new_spend.place(x=390,y=45,width=110, height=25)

        self.btn_consumo=ttk.Button(
            self,
            text="Gastos mensuales",
            command=self.open_spend_monthly
            )
        self.btn_consumo.place(x=270,y=45,width=110, height=25)

        self.btn_saving=ttk.Button(
            self,
            text="Ahorros",
            command=self.open_saving
        )
        self.btn_saving.place(x=270,y=80,width=110, height=25)

        self.btn_new_saving=ttk.Button(
            self,
            text="Nuevo Ahorro",
            command=self.open_new_saving
        )
        self.btn_new_saving.place(x=390,y=80,width=110, height=25)

        ###################VERIFICA SI EXISTE UN USUARIO###########
        if os.path.isfile("main.db")==True:
            conn=sqlite3.connect('main.db')
            cursor=conn.cursor()
            cursor.execute(f"SELECT nombre FROM usuarioActual")
            user_current=cursor.fetchone()[0]
        else:
            user_current="No existe ningún usuario."
                
        self.tag_user_current=ttk.Label(
            self,
            text=f'El usuario actual es: {user_current}'
        )
        self.tag_user_current.place(x=10,y=10)

        ##########################################################   

    def open_new_user(self):
        if not NewUser.in_use:
            self.new_user=NewUser(
                callback=self.user_current
            )
    
    def open_user_existente(self):
        if not UserList.in_use:
            self.user_existente=UserList(
                callback=self.user_current
            )

    def open_new_spend(self):
        if not NewSpend.in_use:
            self.new_spend=NewSpend()
    
    def open_new_saving(self):
        if not NewSaving.in_use:
            self.new_spend=NewSaving()

    def open_spend_monthly(self):
        if not SpendMonthly.in_use:
            self.spend_monthly=SpendMonthly()

    def user_current(self, user):
            self.tag_user_current.config(
                text=f'El usuario actual es: {user}'
            )
    
    def open_saving(self):
        if not VindowSaving.in_use:
            self.saving=VindowSaving()

main_window=MainWindow()
main_window.mainloop()