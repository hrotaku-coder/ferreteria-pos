import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

class VistaReporteProducto:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#D1D3D5")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- TÍTULO ---
        lbl_titulo = tk.Label(self.frame, text="Reporte de Ventas por Producto", font=("Arial", 16, "bold"), bg="#D1D3D5")
        lbl_titulo.pack(pady=(0, 15))

        # --- BARRA DE FILTROS ---
        self.frame_filtros = tk.Frame(self.frame, bg="#D1D3D5")
        self.frame_filtros.pack(fill="x", pady=(0, 15))

        # 1. Filtro Producto
        tk.Label(self.frame_filtros, text="Producto (Ref/Nombre):", font=("Arial", 11, "bold"), bg="#D1D3D5").pack(side="left", padx=(0, 5))
        self.entry_producto = ttk.Entry(self.frame_filtros, font="sans 11", width=25)
        self.entry_producto.pack(side="left", padx=(0, 15))

        # 2. Filtro Desde
        tk.Label(self.frame_filtros, text="Desde:", font=("Arial", 11, "bold"), bg="#D1D3D5").pack(side="left", padx=(0, 5))
        self.entry_desde = DateEntry(
            self.frame_filtros, width=12, background='#2C3E50', foreground='white', 
            borderwidth=2, font="sans 11", date_pattern='y-mm-dd'
        )
        self.entry_desde.pack(side="left", padx=(0, 15))
        self.entry_desde.set_date("2024-06-01")

        # 3. Filtro Hasta
        tk.Label(self.frame_filtros, text="Hasta:", font=("Arial", 11, "bold"), bg="#D1D3D5").pack(side="left", padx=(0, 5))
        self.entry_hasta = DateEntry(
            self.frame_filtros, width=12, background='#2C3E50', foreground='white', 
            borderwidth=2, font="sans 11", date_pattern='y-mm-dd'
        )
        self.entry_hasta.pack(side="left", padx=(0, 15))

        # 4. Botones
        self.btn_filtrar = tk.Button(
            self.frame_filtros, text="Buscar", font=("Arial", 10, "bold"), 
            bg="#2C3E50", fg="white", command=self.aplicar_filtro
        )
        self.btn_filtrar.pack(side="left", padx=(10, 0))

        self.btn_limpiar = tk.Button(
            self.frame_filtros, text="Ver Todo", font=("Arial", 10), 
            bg="#7F8C8D", fg="white", command=self.ver_todo
        )
        self.btn_limpiar.pack(side="left", padx=(5, 0))

        # --- TABLA DE VENTAS POR PRODUCTO ---
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.configure("Treeview", font=("Arial", 11), rowheight=25)

        self.tabla = ttk.Treeview(self.frame, columns=("referencia", "nombre", "cantidad", "total"), show="headings", height=15)
        
        self.tabla.heading("referencia", text="Referencia")
        self.tabla.heading("nombre", text="Nombre Producto")
        self.tabla.heading("cantidad", text="Cantidad Vendida")
        self.tabla.heading("total", text="Total Venta")

        self.tabla.column("referencia", width=150, anchor="center")
        self.tabla.column("nombre", width=350, anchor="w")
        self.tabla.column("cantidad", width=150, anchor="center")
        self.tabla.column("total", width=150, anchor="e")

        self.tabla.pack(fill="both", expand=True)

        # Cargar datos al inicio
        self.cargar_datos()

    def aplicar_filtro(self):
        producto_texto = self.entry_producto.get().strip()
        fecha_desde = self.entry_desde.get()
        fecha_hasta = self.entry_hasta.get()

        if not fecha_desde or not fecha_hasta:
            messagebox.showwarning("Fechas incompletas", "Por favor ingresa un rango de fechas válido.")
            return

        self.cargar_datos(producto_texto, fecha_desde, fecha_hasta)

    def ver_todo(self):
        self.entry_producto.delete(0, tk.END)
        self.entry_desde.set_date("2024-06-01")
        self.entry_hasta.set_date(datetime.now())
        self.cargar_datos()

    def cargar_datos(self, producto_filtro="", fecha_inicio=None, fecha_fin=None):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # DATOS DE PRUEBA: (Fecha, Referencia, Nombre, Cantidad, Subtotal)
        # Observa que el cemento y la pintura se venden en varios días distintos
        datos_brutos = [
            ("2024-06-01", "REF-001", "Cemento Argos 50kg", 10, 350000),
            ("2024-06-02", "REF-002", "Pintura Blanca 1 Galón", 2, 90000),
            ("2024-06-03", "REF-001", "Cemento Argos 50kg", 5, 175000), # Otra venta de cemento
            ("2024-08-15", "REF-003", "Martillo con mango madera", 1, 25000),
            ("2024-08-16", "REF-002", "Pintura Blanca 1 Galón", 1, 45000), # Otra venta de pintura
        ]

        # Diccionario para agrupar las cantidades y sumar el dinero
        productos_agrupados = {}

        for v in datos_brutos:
            fecha, referencia, nombre, cantidad, total = v 
            
            # 1. Validar Rango de Fechas
            if fecha_inicio and fecha_fin:
                if not (fecha_inicio <= fecha <= fecha_fin):
                    continue
            
            # 2. Validar Filtro de Producto
            if producto_filtro:
                filtro_min = producto_filtro.lower()
                if filtro_min not in nombre.lower() and filtro_min not in referencia.lower():
                    continue

            # 3. Lógica de Agrupación (Acumular cantidades y totales)
            if referencia in productos_agrupados:
                productos_agrupados[referencia]["cantidad"] += cantidad
                productos_agrupados[referencia]["total"] += total
            else:
                productos_agrupados[referencia] = {
                    "nombre": nombre,
                    "cantidad": cantidad,
                    "total": total
                }

        # Dibujar en la tabla los productos ya sumados
        for ref, datos in productos_agrupados.items():
            total_formateado = f"$ {int(datos['total']):,}" # Le ponemos formato de dinero
            self.tabla.insert("", "end", values=(ref, datos["nombre"], datos["cantidad"], total_formateado))