import tkinter as tk
from tkinter import ttk

# Aquí importarás tus futuras vistas cuando las crees
# from vista_reporte_general import VistaReporteGeneral
# from vista_ventas_cliente import VistaVentasCliente

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
        self.sidebar = tk.LabelFrame(self.ventana, text="Reportes", font="Arial 14 bold", fg="white", bg="#2C3E50", relief="solid", bd=0)
        self.sidebar.pack(side="top", fill="x")


        # Botones de navegación
        self.btn_general = tk.Button(self.sidebar, text="Ventas Generales", font="Arial 11", bg="#34495E", fg="white", 
                                     relief="flat", overrelief="raised", command=self.mostrar_general)
        self.btn_general.pack(side="left", padx=10, pady=(10, 0))

        # self.btn_clientes = tk.Button(self.sidebar, text="Ventas por Cliente", font="Arial 11", bg="#34495E", fg="white", 
        #                               relief="flat", overrelief="raised", command=self.mostrar_por_cliente)
        # self.btn_clientes.pack(fill="x", padx=10, pady=5)

        # self.btn_productos = tk.Button(self.sidebar, text="Ventas por Producto", font="Arial 11", bg="#34495E", fg="white", 
        #                                relief="flat", overrelief="raised", command=self.mostrar_por_producto)
        # self.btn_productos.pack(side="left", padx=10, pady=5)

        # 2. CONTENEDOR PRINCIPAL (Donde se cargarán las vistas)
        self.area_trabajo = tk.Frame(self.ventana, bg="#D1D3D5")
        self.area_trabajo.pack(side="right", fill="both", expand=True)

        # Mostrar una pantalla de bienvenida inicial
        self.mostrar_bienvenida()

    def limpiar_area_trabajo(self):
        """Elimina todo lo que haya dentro del contenedor antes de cargar algo nuevo"""
        for widget in self.area_trabajo.winfo_children():
            widget.destroy()

    def mostrar_bienvenida(self):
        self.limpiar_area_trabajo()
        label = tk.Label(self.area_trabajo, text="Seleccione un tipo de reporte en el menú de la izquierda", 
                         font="Arial 14", bg="#D1D3D5", fg="#555")
        label.pack(expand=True)

    def mostrar_general(self):
        self.limpiar_area_trabajo()
        # Aquí llamarás a la clase del reporte general
        tk.Label(self.area_trabajo, text="Cargando Reporte General...", font="Arial 20", bg="#D1D3D5").pack(pady=20)
        # Ejemplo: VistaReporteGeneral(self.area_trabajo)

    def mostrar_por_cliente(self):
        self.limpiar_area_trabajo()
        tk.Label(self.area_trabajo, text="Cargando Ventas por Cliente...", font="Arial 20", bg="#D1D3D5").pack(pady=20)

    def mostrar_por_producto(self):
        self.limpiar_area_trabajo()
        tk.Label(self.area_trabajo, text="Cargando Ventas por Producto...", font="Arial 20", bg="#D1D3D5").pack(pady=20)