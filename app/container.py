import tkinter as tk
from tkinter import ttk

from reporte_general import VistaReporteGeneral
from reporte_cliente import VistaReporteCliente
from reporte_producto import VistaReporteProducto

class VentanaReportes:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Reportes")
        self.ventana.configure(bg="#D1D3D5")
        
        # Centrar ventana
        ancho_ventana = 1100
        alto_ventana = 750
        x = int((self.ventana.winfo_screenwidth() / 2) - (ancho_ventana / 2))
        y = int((self.ventana.winfo_screenheight() / 2) - (alto_ventana / 2))
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # 1. BARRA LATERAL DE NAVEGACIÓN
        self.sidebar = tk.LabelFrame(self.ventana, text="  Reportes", font="Arial 14 bold", fg="white", bg="#2C3E50", relief="solid", bd=0)
        self.sidebar.pack(side="top", fill="x")


        # Botones de navegación
        self.btn_general = tk.Button(self.sidebar, text="Ventas Generales", font="Arial 11", bg="#2C3E50", fg="white", 
                                     relief="flat", overrelief="raised", command=self.mostrar_general)
        self.btn_general.pack(side="left", padx=(0, 0), pady=(10, 0))

        self.btn_clientes = tk.Button(self.sidebar, text="Ventas por Cliente", font="Arial 11", bg="#2C3E50", fg="white", 
                                      relief="flat", overrelief="raised", command=self.mostrar_por_cliente)
        self.btn_clientes.pack(side="left", padx=(0, 0), pady=(10, 0))

        self.btn_productos = tk.Button(self.sidebar, text="Ventas por Producto", font="Arial 11", bg="#2C3E50", fg="white", 
                                       relief="flat", overrelief="raised", command=self.mostrar_por_producto)
        self.btn_productos.pack(side="left", padx=(0, 0), pady=(10, 0))

        # 2. CONTENEDOR PRINCIPAL (Donde se cargarán las vistas)
        self.area_trabajo = tk.Frame(self.ventana, bg="#D1D3D5")
        self.area_trabajo.pack(side="right", fill="both", expand=True)
        
        self.mostrar_general()


    def limpiar_area_trabajo(self):
        """Elimina todo lo que haya dentro del contenedor antes de cargar algo nuevo"""
        for widget in self.area_trabajo.winfo_children():
            widget.destroy()
            
    def resaltar_boton_activo(self, boton_seleccionado):
        # 1. Definimos los colores
        bg_inactivo = "#2C3E50"  # Azul oscuro original
        fg_inactivo = "white"    # Texto blanco
        
        bg_activo = "#D1D3D5"    # Mismo color gris del fondo del área de trabajo
        fg_activo = "black"      # Texto negro y en negrita para resaltar

        # 2. Reseteamos TODOS los botones al estado inactivo
        self.btn_general.config(bg=bg_inactivo, fg=fg_inactivo, font=("Arial", 11))
        self.btn_clientes.config(bg=bg_inactivo, fg=fg_inactivo, font=("Arial", 11))
        self.btn_productos.config(bg=bg_inactivo, fg=fg_inactivo, font=("Arial", 11))

        # 3. Aplicamos el color activo SOLO al botón que recibimos por parámetro
        if boton_seleccionado:
            boton_seleccionado.config(bg=bg_activo, fg=fg_activo, font=("Arial", 11, "bold"))


    def mostrar_general(self):
        self.limpiar_area_trabajo()
        # Llamamos a la función y le pasamos cuál es el botón activo
        self.resaltar_boton_activo(self.btn_general)
        
        # Aquí cargas tu vista (Asegúrate de tener importado VistaReporteGeneral)
        VistaReporteGeneral(self.area_trabajo)

    def mostrar_por_cliente(self):
        self.limpiar_area_trabajo()
        self.resaltar_boton_activo(self.btn_clientes)
        
        # Cargamos la nueva vista de clientes
        VistaReporteCliente(self.area_trabajo)

    def mostrar_por_producto(self):
        self.limpiar_area_trabajo()
        self.resaltar_boton_activo(self.btn_productos)
        
        # Cargamos la vista de productos
        VistaReporteProducto(self.area_trabajo)