import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

class VistaReporteCliente:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#D1D3D5")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- TÍTULO ---
        lbl_titulo = tk.Label(self.frame, text="Reporte de Ventas por Cliente", font=("Arial", 16, "bold"), bg="#D1D3D5")
        lbl_titulo.pack(pady=(0, 15))

        # --- BARRA DE FILTROS ---
        self.frame_filtros = tk.Frame(self.frame, bg="#D1D3D5")
        self.frame_filtros.pack(fill="x", pady=(0, 15))

        # 1. Filtro Cliente
        tk.Label(self.frame_filtros, text="Cliente (Nombre/Doc):", font=("Arial", 11, "bold"), bg="#D1D3D5").pack(side="left", padx=(0, 5))
        self.entry_cliente = ttk.Entry(self.frame_filtros, font="sans 11", width=20)
        self.entry_cliente.pack(side="left", padx=(0, 15))

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

        # --- TABLA DE VENTAS POR CLIENTE ---
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.configure("Treeview", font=("Arial", 11), rowheight=25)

        self.tabla = ttk.Treeview(self.frame, columns=("comprobante", "fecha", "documento", "cliente", "total"), show="headings", height=15)
        
        self.tabla.heading("comprobante", text="No. Comprobante")
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("documento", text="Documento")
        self.tabla.heading("cliente", text="Nombre Cliente")
        self.tabla.heading("total", text="Total Venta")

        self.tabla.column("comprobante", width=150, anchor="center")
        self.tabla.column("fecha", width=120, anchor="center")
        self.tabla.column("documento", width=120, anchor="center")
        self.tabla.column("cliente", width=250, anchor="w")
        self.tabla.column("total", width=150, anchor="e")

        self.tabla.pack(fill="both", expand=True)

        # Cargar datos al inicio
        self.cargar_datos()

    def aplicar_filtro(self):
        cliente_texto = self.entry_cliente.get().strip()
        fecha_desde = self.entry_desde.get()
        fecha_hasta = self.entry_hasta.get()

        if not fecha_desde or not fecha_hasta:
            messagebox.showwarning("Fechas incompletas", "Por favor ingresa un rango de fechas válido.")
            return

        # Llamamos a cargar datos enviando los 3 filtros
        self.cargar_datos(cliente_texto, fecha_desde, fecha_hasta)

    def ver_todo(self):
        self.entry_cliente.delete(0, tk.END)
        self.entry_desde.set_date("2024-06-01")
        self.entry_hasta.set_date(datetime.now())
        self.cargar_datos()

    def cargar_datos(self, fecha_inicio=None, fecha_fin=None):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        filtro = self.entry_cliente.get()

        from db import conectar
        conn = conectar()
        cursor = conn.cursor()

        # Consulta SQL correcta
        query = """
            SELECT v.numero_factura, v.fecha, c.documento, c.nombre, v.total 
            FROM ventas v
            JOIN clientes c ON v.cliente_id = c.id
            WHERE 1=1
        """
        params = []

        # Filtro de Nombre o Documento
        if filtro:
            query += " AND (c.nombre LIKE ? OR c.documento LIKE ?)"
            params.extend([f"%{filtro}%", f"%{filtro}%"])
        
        # Filtro de Fechas
        if fecha_inicio and fecha_fin:
            query += " AND v.fecha BETWEEN ? AND ?"
            params.extend([f"{fecha_inicio} 00:00:00", f"{fecha_fin} 23:59:59"])

        try:
            cursor.execute(query, params)
            ventas_reales = cursor.fetchall()

            for v in ventas_reales:
                factura, fecha, doc, nombre, total = v
                total_formateado = f"$ {total:,.0f}"
                self.tabla.insert("", "end", values=(factura, fecha, doc, nombre, total_formateado))
                
        except Exception as e:
            print(f"Error Reporte Cliente: {e}")
            
        finally:
            conn.close()