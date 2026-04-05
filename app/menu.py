print("SE ESTA EJECUTANDO MENU.PY")

import tkinter as tk
from PIL import Image, ImageTk

from ui import VentanaVenta
from ventana_productos import VentanaProductos
from db import crear_tablas


crear_tablas()

class VentanaMenu:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Menú Principal")
        self.ventana.geometry("400x600")
        
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
            command=self.abrir_factura
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
        
    def abrir_factura(self):
        nueva = tk.Toplevel(self.ventana)
        VentanaVenta(nueva)
            
    def abrir_productos(self):
        nueva = tk.Toplevel(self.ventana)
        VentanaProductos(nueva)

        


# Ejecutar menú
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaMenu(root)
    root.mainloop()