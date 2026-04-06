print("SE ESTA EJECUTANDO MENU.PY")

import tkinter as tk
from PIL import Image, ImageTk

from ui import VentanaVenta
from ventana_productos import VentanaProductos
from ventana_compras import VentanaCompras
from db import crear_tablas


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
        
        ANCHO_BOTON = 20
        ALTO_BOTON = 2
        
        ruta_icono = "iconos/nuevaventa.png"
        
        img = Image.open(ruta_icono)
        img = img.resize((70, 70))
        self.icono_factura = ImageTk.PhotoImage(img)

        # contenedor
        frame_venta = tk.Frame(self.ventana)
        frame_venta.pack(pady=20)

        # icono
        self.lbl_icono_factura = tk.Label(frame_venta, image=self.icono_factura)
        self.lbl_icono_factura.grid(row=0, column=0, padx=10, pady=15)

        # botón
        self.btn_factura = tk.Button(
            frame_venta,
            text="Crear Factura",
            font="Arial 10 bold",
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            command=self.abrir_venta
        )
        self.btn_factura.grid(row=0, column=1, padx=10)
        
        ruta_icono2 = "iconos/producto.png"
        
        img2 = Image.open(ruta_icono2)
        img2 = img2.resize((70, 70))
        self.icono_producto = ImageTk.PhotoImage(img2)
        
        frame_producto = tk.Frame(self.ventana)
        frame_producto.pack(pady=20)
        
        self.lbl_icono_producto =tk.Label(frame_producto, image=self.icono_producto)
        self.lbl_icono_producto.grid(row=0, column=0, padx=10, pady=15)
        
        self.btn_producto = tk.Button(
            frame_producto,
            text="Productos",
            font="Arial 10 bold",
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            command=self.abrir_productos  
        ) 
        self.btn_producto.grid(row=0, column=1, padx=10)
        
        ruta_icono3 = "iconos/reportes.png"
        
        img3 = Image.open(ruta_icono3)
        img3 = img3.resize((70, 70))
        self.icono_reporte = ImageTk.PhotoImage(img3)
        
        frame_reporte = tk.Frame(self.ventana)
        frame_reporte.pack(pady=20)
        
        self.lbl_icono_reporte =tk.Label(frame_reporte, image=self.icono_reporte)
        self.lbl_icono_reporte.grid(row=0, column=0, padx=10, pady=15)
        
        self.btn_reporte = tk.Button(
            frame_reporte,
            text="Reportes",
            font="Arial 10 bold",
            width=ANCHO_BOTON,
            height=ALTO_BOTON
        ) 
        self.btn_reporte.grid(row=0, column=1, padx=10)
        
        # --- BOTÓN DE COMPRAS ---
        frame_compras = tk.Frame(self.ventana)
        frame_compras.pack(pady=10) # Separa un poco los botones
        
        # (Opcional) Si luego descargas un ícono para compras, lo pones aquí
        ruta_icono_compras = "iconos/compras.png"
        img_compra = Image.open(ruta_icono_compras).resize((70, 70))
        self.icono_compra = ImageTk.PhotoImage(img_compra)
        tk.Label(frame_compras, image=self.icono_compra).grid(row=0, column=0, padx=10)
        
        self.btn_compras = tk.Button(
            frame_compras,
            text="Registrar Compra",
            font="Arial 10 bold",
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            command=self.abrir_compras # Llama a la función que vamos a crear
        ) 
        # Si pusiste ícono, cambia el column a 1. Si no hay ícono, déjalo en 0.
        self.btn_compras.grid(row=0, column=1, padx=10)
        
    def abrir_venta(self):
        # 1. Ocultar la ventana del menú principal
        self.ventana.withdraw()
        
        # 2. Crear y abrir la ventana de ventas
        ventana_venta = tk.Toplevel(self.ventana)
        aplicacion = VentanaVenta(ventana_venta)
        
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
        aplicacion = VentanaProductos(ventana_prod)
        
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
        aplicacion = VentanaCompras(ventana_compra)
        
        # 3. Función interna para restaurar el menú al cerrar
        def al_cerrar_compras():
            self.ventana.deiconify() # Vuelve a mostrar el menú
            ventana_compra.destroy() # Cierra definitivamente la ventana de compras
            
        # 4. Detectar cuando se presiona la "X" de la ventana
        ventana_compra.protocol("WM_DELETE_WINDOW", al_cerrar_compras)
        


# Ejecutar menú
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaMenu(root)
    root.mainloop()