import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry  # 🔥 Importamos el nuevo calendario

class VistaReporteGeneral:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#D1D3D5")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)


        # --- BARRA DE FILTROS ---
        self.frame_filtros = tk.Frame(self.frame, bg="#D1D3D5")
        self.frame_filtros.pack(fill="x", pady=(0, 15))

        tk.Label(self.frame_filtros, text="Desde:", font=("Arial", 11, "bold"), bg="#D1D3D5").pack(side="left", padx=(0, 5))
        
        # 🔥 CALENDARIO DESDE
        self.entry_desde = DateEntry(
            self.frame_filtros, 
            width=12, 
            background='#2C3E50', 
            foreground='white', 
            borderwidth=2, 
            font="sans 11",
            date_pattern='y-mm-dd' # Formato para la base de datos
        )
        self.entry_desde.pack(side="left", padx=(0, 15))
        self.entry_desde.set_date("2024-06-01") # Fecha inicial de prueba

        tk.Label(self.frame_filtros, text="Hasta:", font=("Arial", 11, "bold"), bg="#D1D3D5").pack(side="left", padx=(0, 5))
        
        # 🔥 CALENDARIO HASTA
        self.entry_hasta = DateEntry(
            self.frame_filtros, 
            width=12, 
            background='#2C3E50', 
            foreground='white', 
            borderwidth=2, 
            font="sans 11",
            date_pattern='y-mm-dd'
        )
        self.entry_hasta.pack(side="left", padx=(0, 15))
        # Por defecto DateEntry ya pone el día de hoy, así que no necesitamos insertarlo manualmente

        self.btn_filtrar = tk.Button(
            self.frame_filtros, 
            text="Buscar Ventas", 
            font=("Arial", 10, "bold"), 
            bg="#2C3E50", 
            fg="white", 
            command=self.aplicar_filtro
        )
        self.btn_filtrar.pack(side="left", padx=(10, 0))

        self.btn_limpiar = tk.Button(
            self.frame_filtros, 
            text="Ver Todo", 
            font=("Arial", 10), 
            bg="#7F8C8D", 
            fg="white", 
            command=self.ver_todo
        )
        self.btn_limpiar.pack(side="left", padx=(5, 0))

        # --- TABLA DE VENTAS ---
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.configure("Treeview", font=("Arial", 11), rowheight=25)

        self.tabla = ttk.Treeview(self.frame, columns=("fecha", "comprobante", "cliente", "documento", "total"), show="headings", height=15)
        
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("comprobante", text="No. Comprobante")
        self.tabla.heading("cliente", text="Nombre Cliente")
        self.tabla.heading("documento", text="Documento Cliente")
        self.tabla.heading("total", text="Total Venta")

        self.tabla.column("fecha", width=120, anchor="center")
        self.tabla.column("comprobante", width=150, anchor="center")
        self.tabla.column("cliente", width=250, anchor="w")
        self.tabla.column("documento", width=150, anchor="center")
        self.tabla.column("total", width=150, anchor="e")

        self.tabla.pack(fill="both", expand=True)

        # Llamamos a la función que llenará la tabla
        self.cargar_datos()

    def aplicar_filtro(self):
        # Con DateEntry, obtener la fecha es igual de fácil
        fecha_desde = self.entry_desde.get()
        fecha_hasta = self.entry_hasta.get()

        if not fecha_desde or not fecha_hasta:
            messagebox.showwarning("Fechas incompletas", "Por favor ingresa ambas fechas para buscar.")
            return

        self.cargar_datos(fecha_desde, fecha_hasta)

    def ver_todo(self):
        # Para ver todo, reseteamos las fechas a unos valores amplios y cargamos
        self.entry_desde.set_date("2024-06-01")
        self.entry_hasta.set_date(datetime.now())
        self.cargar_datos()

    def cargar_datos(self, fecha_inicio=None, fecha_fin=None):
        # 1. Limpiamos la tabla visual
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # 2. Conectamos a la base de datos
        from db import conectar
        conn = conectar()
        cursor = conn.cursor()

        # 3. Consulta SQL con los nombres exactos de tu base de datos
        query = """
            SELECT v.fecha, v.numero_factura, c.nombre, c.documento, v.total 
            FROM ventas v
            JOIN clientes c ON v.cliente_id = c.id
            WHERE 1=1
        """
        parametros = []

        # Filtramos por fechas
        if fecha_inicio and fecha_fin:
            query += " AND v.fecha BETWEEN ? AND ?"
            parametros.extend([f"{fecha_inicio} 00:00:00", f"{fecha_fin} 23:59:59"])

        try:
            cursor.execute(query, parametros)
            ventas_reales = cursor.fetchall()

            # 4. Insertamos los datos en la tabla
            for v in ventas_reales:
                fecha, num_factura, nombre, doc, total = v
                total_formateado = f"$ {total:,.0f}" 
                self.tabla.insert("", "end", values=(fecha, num_factura, nombre, doc, total_formateado))
                
        except Exception as e:
            print(f"Error Reporte General: {e}")
            
        finally:
            conn.close()