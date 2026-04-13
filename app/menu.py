import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from ui import VentanaVenta
from ventana_productos import VentanaProductos
from ventana_compras import VentanaCompras
from db import crear_tablas
import os
import sys

from utils import ruta_recurso

crear_tablas()

class VentanaMenu:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Menú Principal")
        
        # --- CENTRAR VENTANA DEL MENÚ ---
        ancho_ventana = 400
        alto_ventana = 600
        
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        
        # Calcular coordenadas (x, y)
        x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        y = int((alto_pantalla / 2) - (alto_ventana / 2))
        
        # Aplicar tamaño y posición
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        
        self.crear_boton("Crear Factura", "iconos/nuevaventa.png", self.abrir_venta)
        self.crear_boton("Productos", "iconos/producto.png", self.abrir_productos)
        self.crear_boton("Reportes", "iconos/reportes.png", self.abrir_reportes)
        self.crear_boton("Registrar Compra", "iconos/compras.png", self.abrir_compras)
        
    def crear_boton(self, texto, ruta_icono, comando):
        frame = tk.Frame(self.ventana)
        frame.pack(pady=20)

        try:
            ruta = ruta_recurso(ruta_icono)
            img = Image.open(ruta).resize((70, 70))
            icono = ImageTk.PhotoImage(img)
        except:
            icono = None

        label_icono = tk.Label(frame, image=icono)
        label_icono.image = icono  # IMPORTANTE para que no desaparezca
        label_icono.grid(row=0, column=0, padx=10)

        boton = tk.Button(
            frame,
            text=texto,
            font="Arial 10 bold",
            width=20,
            height=2,
            command=comando
        )
        boton.grid(row=0, column=1, padx=10)
        
                
    def abrir_venta(self):
        # 1. Ocultar la ventana del menú principal
        self.ventana.withdraw()
        
        # 2. Crear y abrir la ventana de ventas
        ventana_venta = tk.Toplevel(self.ventana)
        VentanaVenta(ventana_venta)
        
        # 3. Función interna para restaurar el menú al cerrar
        def al_cerrar_venta():
            self.ventana.deiconify() # Vuelve a mostrar el menú
            ventana_venta.destroy()  # Cierra definitivamente la ventana de ventas
            
        # 4. Detectar cuando se presiona la "X" de la ventana de ventas
        ventana_venta.protocol("WM_DELETE_WINDOW", al_cerrar_venta)
            
    def abrir_productos(self):
        # 1. Ocultar la ventana del menú principal
        self.ventana.withdraw()
        
        # 2. Crear y abrir la ventana de productos
        ventana_prod = tk.Toplevel(self.ventana)
        VentanaProductos(ventana_prod)
        
        # 3. Función interna para restaurar el menú al cerrar
        def al_cerrar_productos():
            self.ventana.deiconify() # Vuelve a mostrar el menú
            ventana_prod.destroy()   # Cierra definitivamente la ventana de productos
            
        # 4. Detectar cuando se presiona la "X" de la ventana de productos
        ventana_prod.protocol("WM_DELETE_WINDOW", al_cerrar_productos)

    def abrir_compras(self):
        # 1. Ocultar la ventana del menú principal
        self.ventana.withdraw()
        
        # 2. Crear y abrir la ventana de compras
        ventana_compra = tk.Toplevel(self.ventana)
        VentanaCompras(ventana_compra)
        
        # 3. Función interna para restaurar el menú al cerrar
        def al_cerrar_compras():
            self.ventana.deiconify() # Vuelve a mostrar el menú
            ventana_compra.destroy() # Cierra definitivamente la ventana de compras
            
        # 4. Detectar cuando se presiona la "X" de la ventana
        ventana_compra.protocol("WM_DELETE_WINDOW", al_cerrar_compras)
        
    def abrir_reportes(self):
        messagebox.showinfo("Reportes", "Funcionalidad de reportes en desarrollo.")
        


# Ejecutar menú
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaMenu(root)
    root.mainloop()