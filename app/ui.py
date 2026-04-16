import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
from factura_pdf import generar_pdf
from ticket import imprimir_ticket, generar_texto_ticket

from db import obtener_siguiente_factura
from db import ver_siguiente_factura
import productos
import ventas
import clientes

class VentanaVenta:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Ferretería POS")
        self.ventana.configure(bg="#D1D3D5")
        
        # --- CENTRAR VENTANA DE VENTAS ---
        ancho_ventana = 1080
        alto_ventana = 800
        
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        
        x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        y = int((alto_pantalla / 2) - (alto_ventana / 2))
        
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        
        
        
        # CONTENEDOR PARA BOTONES NUEVA VENTA, CREAR CLIENTE Y ELIMINAR PRODUCTO
        self.frame_top = tk.Frame(self.ventana, bg="#D1D3D5", bd=3, relief="groove",)
        self.frame_top.pack(fill="x", padx=10, pady=5)
        
        # BOTONES
        self.btn_nueva = tk.Button(
            self.frame_top,
            text="Nueva Venta F1",
            font=("Arial", 11),
            bd=2,
            relief="raised",
            command=self.nueva_venta
        )

        self.btn_nueva.pack(side="left", padx=10, pady=10)
        
        self.btn_crearcliente = tk.Button(
            self.frame_top,
            text="Crear cliente F2",
            font=("Arial", 11),
            bd=2,
            relief="raised",
            command=self.abrir_ventana_cliente
        )

        self.btn_crearcliente.pack(side="left", padx=10, pady=10)
        
        self.btn_eliminarproducto = tk.Button(
            self.frame_top,
            text="Eliminar producto Del.",
            font=("Arial", 11),
            bd=2,
            relief="raised",
            command=self.eliminar_producto
        )

        self.btn_eliminarproducto.pack(side="left", padx=10, pady=10)
    
        # CONTENEDOR DATOS CLIENTE
        self.frame_datoscliente = tk.LabelFrame(self.ventana, text="Datos Cliente", font="Arial 12 bold", bg="#D1D3D5",)
        self.frame_datoscliente.place(x=15, y=70, width=520, height=100)
        
        self.lbl_nit = tk.Label(self.frame_datoscliente, text="NIT/CC:", font="Arial 12", bg="#D1D3D5")
        self.lbl_nit.grid(row=0, column=0, padx=5, pady=5)
        self.combo_nit = ttk.Combobox(self.frame_datoscliente, font="sans 12", state="normal")
        self.combo_nit.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.combo_nit.bind("<<ComboboxSelected>>", self.seleccionar_y_continuar_nit)
        self.combo_nit.bind("<KeyRelease>", self.filtrar_clientes_nit)
        
        self.combo_nit.bind("<Return>", self.ir_a_producto)
        
        self.combo_nit.bind("<Down>", lambda e: self.combo_nit.event_generate("<Button-1>"))
        
        self.lbl_cliente = tk.Label(self.frame_datoscliente, text="Cliente:", font="Arial 12", bg="#D1D3D5")
        self.lbl_cliente.grid(row=1, column=0, padx=5, pady=5)
        self.combo_cliente = ttk.Combobox(self.frame_datoscliente, font="sans 12", width=40, state="normal")
        self.combo_cliente.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        self.combo_cliente.bind("<<ComboboxSelected>>", self.seleccionar_y_continuar_cliente)
        self.combo_cliente.bind("<KeyRelease>", self.filtrar_clientes_nombre)
        
        self.combo_cliente.bind("<Return>", self.ir_a_producto)
        
        self.combo_cliente.bind("<Down>", lambda e: self.combo_cliente.event_generate("<Button-1>"))
        
        self.cargar_clientes()
        
        # CONTENEDOR INFORMACION FACTURA
        self.frame_informacionfactura = tk.LabelFrame(self.ventana, text="Informacion De Factura", font="Arial 12 bold", bg="#D1D3D5",)
        self.frame_informacionfactura.place(x=545, y=70, width=520, height=100)
        
        self.lbl_factura = tk.Label(self.frame_informacionfactura, text="No Factura:", font="Arial 12", bg="#D1D3D5")
        self.lbl_factura.grid(row=0, column=0, padx=5, pady=5)
        
        self.entry_factura = ttk.Entry(
            self.frame_informacionfactura,
            font="sans 12",
            width=10,
            state="readonly"
        )        
        self.entry_factura.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.entry_factura.config(state="normal")
        self.entry_factura.insert(0, "PENDIENTE")
        self.entry_factura.config(state="readonly")
        
        self.lbl_fecha = tk.Label(self.frame_informacionfactura, text="Fecha:", font="Arial 12", bg="#D1D3D5")
        self.lbl_fecha.grid(row=1, column=0, padx=5, pady=5)
        self.entry_fecha = ttk.Entry(self.frame_informacionfactura, font="sans 12", width=15)
        self.entry_fecha.grid(row=1, column=1, padx=5, pady=5, sticky="w")
      
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        self.entry_fecha.insert(0, fecha_actual)
        
        # CONTENEDOR BUSQUEDA DE PRODUCTO
        self.frame_busqueda = tk.LabelFrame(self.ventana, text="Busqueda de producto", font="Arial 12 bold", bg="#D1D3D5",)
        self.frame_busqueda.place(x=10, y=180, width=1060, height=70)
        
        self.lbl_producto = tk.Label(self.frame_busqueda, text="Buscar producto:", font="Arial 12", bg="#D1D3D5")
        self.lbl_producto.grid(row=0, column=0, padx=5, pady=5)
        self.combo_producto = ttk.Combobox(self.frame_busqueda, font="sans 12", width=40, state="normal")
        self.combo_producto.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.combo_producto.bind("<<ComboboxSelected>>", self.seleccionar_y_continuar_producto)
        self.combo_producto.bind("<KeyRelease>", self.filtrar_productos)
        
        self.combo_producto.bind("<Return>", self.ir_a_cantidad)

        self.combo_producto.bind("<Down>", lambda e: self.combo_producto.event_generate("<Button-1>"))
        
        self.cargar_productos()
        
        self.lbl_cantidad = tk.Label(self.frame_busqueda, text="Cantidad", font="Arial 12", bg="#D1D3D5")
        self.lbl_cantidad.grid(row=0,column=2, padx=5, pady=5)
        self.entry_cantidad = ttk.Entry(self.frame_busqueda, font="sans 12", width=6)
        self.entry_cantidad.grid(row=0, column=3,padx=5, pady=5, sticky="w")
        
        self.entry_cantidad.insert(0, "1")
        
        self.entry_cantidad.bind("<Return>", self.agregar_producto_evento)
        self.entry_cantidad.bind("<FocusIn>", lambda e: self.entry_cantidad.select_range(0, tk.END))
        
        self.lbl_stock = tk.Label(self.frame_busqueda, text="Stock", font="Arial 12", bg="#D1D3D5")
        self.lbl_stock.grid(row=0,column=4, padx=5, pady=5)
        self.entry_stock = ttk.Entry(self.frame_busqueda, font="sans 12", width=6)
        self.entry_stock.grid(row=0, column=5,padx=5, pady=5, sticky="w")
        
        # 🔥 TIPO DE PRECIO
        self.tipo_precio = tk.StringVar(value="precio1")

        self.combo_tipo_precio = ttk.Combobox(
            self.frame_busqueda,
            textvariable=self.tipo_precio,
            values=["precio1", "precio2", "manual"],
            width=10,
            state="readonly"
        )
        
        self.combo_tipo_precio.bind("<<ComboboxSelected>>", self.cambiar_tipo_precio)
        
        self.combo_tipo_precio.grid(row=0, column=6, padx=5, pady=5)

        # 🔥 PRECIO MANUAL
        self.entry_precio_manual = ttk.Entry(self.frame_busqueda, width=10, state="disabled")
        self.entry_precio_manual.grid(row=0, column=7, padx=5, pady=5)
        
        self.btn_agregar = tk.Button(
            self.frame_busqueda,
            text="Agregar",
            font=("Arial", 11),
            bd=2,
            relief="raised",
            command=self.agregar_y_reset
        )

        self.btn_agregar.grid(row=0, column=8, padx=5, pady=5)
        
        self.btn_agregar.bind("<Return>", lambda e: self.agregar_y_reset())
        
        #TABLA DE DETALLE FACTURA
        self.frame_tabla = tk.LabelFrame(
            self.ventana,
            text="Detalle de Venta",
            font=("Arial", 12, "bold"),
            bg="#D1D3D5"
        )
        self.frame_tabla.place(x=10, y=260, width=1060, height=400)
        
        # ESTILO DE LA TABLA
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        
        self.tabla = ttk.Treeview(self.frame_tabla)

        self.tabla["columns"] = ("referencia", "producto", "cantidad", "valor", "tipo", "total")

        self.tabla.column("#0", width=0, stretch=tk.NO)

        self.tabla.column("referencia", anchor="w", width=100)
        self.tabla.column("producto", anchor="w", width=400)
        self.tabla.column("cantidad", anchor="center", width=80)
        self.tabla.column("valor", anchor="e", width=80)
        self.tabla.column("tipo", anchor="center", width=100)
        self.tabla.column("total", anchor="e", width=80)

        self.tabla.heading("#0", text="")
        self.tabla.heading("referencia", text="Referencia")
        self.tabla.heading("producto", text="Producto")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.heading("valor", text="Valor")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.heading("total", text="Total")

        self.tabla.pack(fill="both", expand=True)
        
        # CONTENEDOR DE COBRO
        self.frame_cobro = tk.LabelFrame(
            self.ventana,
            text="Cobro",
            font=("Arial", 12, "bold"),
            bg="#D1D3D5"
        )
        self.frame_cobro.place(x=10, y=670, width=1060, height=100)
        
        self.lbl_total_valor = tk.Label(
            self.frame_cobro,
            text="$ 0",
            font=("Arial", 16, "bold"),
            fg="green",
            bg="#D1D3D5"
        )
        self.lbl_total_valor.pack(side="right", padx=5, pady=5)
        
        self.lbl_total = tk.Label(
            self.frame_cobro,
            text="TOTAL:",
            font=("Arial", 14, "bold"),
            bg="#D1D3D5"
        )
        self.lbl_total.pack(side="right", padx=5, pady=5)
        
        self.btn_cobrar = tk.Button(
            self.frame_cobro,
            text="COBRAR F3",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            width=15,
            height=2,
            command=self.cobrar
        )

        self.btn_cobrar.pack(side="top", pady=5)
        
        self.ventana.bind("<F1>", self.nueva_venta_evento)
        self.ventana.bind("<F2>", self.atajo_crear_cliente)
        self.ventana.bind("<Delete>", self.eliminar_producto_evento)
        self.ventana.bind("<F3>", self.cobrar_evento)
        
        self.ventana.after(100, lambda: self.combo_nit.focus())
        
    def cargar_productos(self):
        lista_productos = productos.listar_productos()

        self.lista_productos = []
        self.productos_dict = {}

        for p in lista_productos:
            id_, nombre, referencia, precio1, precio2, stock = p

            self.lista_productos.append(nombre)

            # guardamos todo para usar después
            self.productos_dict[nombre] = {
                "referencia": referencia,
                "precio1": precio1,
                "precio2": precio2,
                "stock": stock
            }

        self.combo_producto["values"] = self.lista_productos
        
    def seleccionar_producto(self, event):
        nombre = self.combo_producto.get()

        if nombre in self.productos_dict:
            datos = self.productos_dict[nombre]

            stock = datos["stock"]
            precio1 = datos["precio1"]
            precio2 = datos["precio2"]

            # STOCK
            self.entry_stock.delete(0, tk.END)
            self.entry_stock.insert(0, stock)

            
    def seleccionar_y_continuar_producto(self, event):
        self.seleccionar_producto(event)
        self.ir_a_cantidad(event)
            
    def seleccionar_cliente_nit(self, event):
        documento = self.combo_nit.get()

        if documento in self.clientes_dict:
            nombre = self.clientes_dict[documento]["nombre"]
            self.combo_cliente.set(nombre)
            
    def seleccionar_y_continuar_nit(self, event):
        self.seleccionar_cliente_nit(event)
        self.ir_a_producto(event)

            
    def seleccionar_cliente_nombre(self, event):
        nombre = self.combo_cliente.get()

        for doc, datos in self.clientes_dict.items():
            if isinstance(datos, dict) and datos.get("nombre") == nombre:
                self.combo_nit.set(doc)
                break
            
    def seleccionar_y_continuar_cliente(self, event):
        self.seleccionar_cliente_nombre(event)
        self.ir_a_producto(event)
            
    def agregar_producto(self):
        nombre = self.combo_producto.get()
        cantidad = self.entry_cantidad.get()

        # Validación básica
        if not nombre or not cantidad:
            messagebox.showwarning("Campos incompletos", "Debes seleccionar un producto y cantidad")
            return

        try:
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            self.entry_cantidad.focus()
            return

        # ✅ VALIDAR QUE SEA MAYOR A 0
        if cantidad <= 0:
            messagebox.showwarning("Cantidad inválida", "La cantidad debe ser mayor a 0")
            self.entry_cantidad.focus()
            return
        
        # ✅ VALIDAR QUE EL PRODUCTO EXISTA
        if nombre not in self.productos_dict:
            messagebox.showerror("Error", "Producto no válido")
            return

        datos = self.productos_dict[nombre]

        referencia = datos["referencia"]
        
        precio1 = datos["precio1"]
        precio2 = datos["precio2"]

        tipo = self.tipo_precio.get()

        if tipo == "precio1":
            precio = precio1
        elif tipo == "precio2":
            precio = precio2
        else:
            precio_texto = self.entry_precio_manual.get()

            # ❌ vacío
            if not precio_texto:
                messagebox.showerror("Error", "Debes ingresar un precio manual")
                self.entry_precio_manual.focus()
                return

            # ❌ no numérico
            try:
                precio = float(precio_texto)
            except ValueError:
                messagebox.showerror("Error", "Precio manual inválido")
                self.entry_precio_manual.focus()
                return

            # ❌ menor o igual a 0
            if precio <= 0:
                messagebox.showerror("Error", "El precio debe ser mayor a 0")
                self.entry_precio_manual.focus()
                return
        
        stock = datos["stock"]

        # 🔥 BUSCAR SI YA EXISTE EN LA TABLA
        for item in self.tabla.get_children():
            valores = self.tabla.item(item, "values")

            ref_tabla = valores[0]
            tipo_tabla = valores[4]  # 🔥 nuevo
            cantidad_tabla = int(valores[2])

            # 🔥 ahora compara referencia + tipo de precio
            precio_tabla = float(valores[3])

            if ref_tabla == referencia and tipo_tabla == tipo and precio_tabla == precio:
                nueva_cantidad = cantidad_tabla + cantidad

                # ❌ VALIDAR STOCK
                if nueva_cantidad > stock:
                    messagebox.showerror("Stock insuficiente", f"Disponible: {stock}")
                    return

                nuevo_total = nueva_cantidad * precio

                self.tabla.item(item, values=(
                    referencia,
                    nombre,
                    nueva_cantidad,
                    precio,
                    tipo,
                    nuevo_total
                ))

                self.calcular_total()
                return

        # 👉 SI NO EXISTE → VALIDAR STOCK
        if cantidad > stock:
            messagebox.showerror("Stock insuficiente", f"Disponible: {stock}")
            return

        total = cantidad * precio

        tipo = self.tipo_precio.get()

        self.tabla.insert("", "end", values=(
            referencia,
            nombre,
            cantidad,
            precio,
            tipo,
            total
        ))

        self.calcular_total()
        
    def agregar_y_reset(self):
        self.agregar_producto()

        # reset cantidad
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, "1")
        self.entry_precio_manual.delete(0, tk.END)

        # limpiar producto
        self.combo_producto.set("")

        # limpiar stock
        self.entry_stock.delete(0, tk.END)
        
        # RESET TIPO DE PRECIO
        self.tipo_precio.set("precio1")

        # volver al buscador
        self.combo_producto.focus()
                
    def calcular_total(self):
        total = 0

        for item in self.tabla.get_children():
            valores = self.tabla.item(item, "values")

            subtotal = float(valores[5])  # ✅ ahora sí
            total += subtotal

        self.lbl_total_valor.config(text=f"$ {int(total)}")

    def cobrar(self):
        documento = self.combo_nit.get()
        nombre_cliente = self.combo_cliente.get() # Tomamos el nombre del cliente

        if not documento:
            messagebox.showwarning("Cliente requerido", "Debes seleccionar un cliente")
            return

        productos_bd = []
        productos_pdf = []
        total_venta = 0

        for item in self.tabla.get_children():
            valores = self.tabla.item(item, "values")

            # Obtenemos todos los datos de la fila
            referencia = valores[0]
            nombre = valores[1]
            cantidad = int(valores[2])
            precio = float(valores[3])
            tipo = valores[4]
            subtotal = float(valores[5])


            productos_bd.append((referencia, cantidad, precio, tipo))
            
            # Lista completa para que el PDF se vea bien
            productos_pdf.append((referencia, nombre, cantidad, precio, subtotal))
            total_venta += subtotal

        if not productos_bd:
            messagebox.showwarning("Sin productos", "No hay productos en la venta")
            return

        numero_factura = obtener_siguiente_factura()
        
        # 🔥 GUARDAR EN BD
        resultado = ventas.crear_venta(numero_factura, documento, productos_bd)

        if resultado:
            self.cargar_productos()
            
            self.entry_factura.config(state="normal")
            self.entry_factura.delete(0, tk.END)
            self.entry_factura.insert(0, numero_factura)
            self.entry_factura.config(state="readonly")
            # 🔥 GENERAR EL PDF
            try:
                ruta_pdf = generar_pdf(resultado, documento, nombre_cliente, productos_pdf, total_venta)
                
            except Exception as e:
                messagebox.showerror("Error PDF", f"Venta guardada, pero falló el PDF: {e}")

            self.limpiar_venta()

        else:
            messagebox.showerror("Error", "No se pudo guardar la venta")
            
        # 🔥 PREGUNTAR SI DESEA IMPRIMIR
        imprimir = messagebox.askyesno("Imprimir", "¿Desea imprimir ticket?")

        if imprimir:
            texto = generar_texto_ticket(
                numero_factura,
                nombre_cliente,
                productos_pdf,
                total_venta
            )

            imprimir_ticket(texto)

            self.ventana.after(1500, lambda: self.preguntar_copia(
                numero_factura,
                nombre_cliente,
                productos_pdf,
                total_venta
            ))

        else:
            # 🔥 SOLO SI NO IMPRIME
            self.mostrar_mensaje_temporal("✅ Venta registrada")

            # 🔥 PREGUNTAR COPIA SOLO SI IMPRIME
            self.ventana.after(1500, lambda: self.preguntar_copia(
                numero_factura,
                nombre_cliente,
                productos_pdf,
                total_venta
            ))
            
            
    def preguntar_copia(self, numero_factura, nombre_cliente, productos, total):
        respuesta = messagebox.askyesno("Copia", "¿Desea imprimir copia del ticket?")

        if respuesta:
            texto_copia = generar_texto_ticket(
                numero_factura,
                nombre_cliente,
                productos,
                total,
                copia=True
            )
            imprimir_ticket(texto_copia)        
    
    def cobrar_evento(self, event):
        self.cobrar()

    def mostrar_mensaje_temporal(self, mensaje, duracion=1500):
        ventana_msg = tk.Toplevel(self.ventana)
        ventana_msg.title("Información")
        ventana_msg.geometry("300x100")
        ventana_msg.resizable(False, False)

        # Centrar ventana
        ancho = 300
        alto = 100
        x = (ventana_msg.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana_msg.winfo_screenheight() // 2) - (alto // 2)
        ventana_msg.geometry(f"{ancho}x{alto}+{x}+{y}")

        label = tk.Label(
            ventana_msg,
            text=mensaje,
            font=("Arial", 12, "bold"),
            fg="green"
        )
        label.pack(expand=True)

        # Siempre al frente
        ventana_msg.lift()
        ventana_msg.attributes('-topmost', True)

        # Cerrar automáticamente
        ventana_msg.after(duracion, ventana_msg.destroy)
                
            
    def limpiar_venta(self):
        # limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, "1")

        # limpiar campos
        self.combo_producto.set("")
        self.combo_nit.set("")
        self.combo_cliente.set("")
        self.entry_stock.delete(0, tk.END)

        # reset total
        self.lbl_total_valor.config(text="$ 0")
        
        # aumentar número de factura
        self.entry_factura.config(state="normal")
        self.entry_factura.delete(0, tk.END)
        self.entry_factura.insert(0, "PENDIENTE")
        self.entry_factura.config(state="readonly")
                
        self.ventana.after(100, lambda: self.combo_nit.focus())
        
    def nueva_venta(self):
        respuesta = messagebox.askyesno("Confirmar", "¿Deseas iniciar una nueva venta?")

        if respuesta:
            self.limpiar_venta()
 
    def cargar_clientes(self):
        lista = clientes.listar_clientes()

        self.clientes_dict = {}

        self.lista_docs = []
        self.lista_nombres = []

        for c in lista:
            id_, nombre, documento, telefono = c

            self.lista_docs.append(documento)
            self.lista_nombres.append(nombre)

            self.clientes_dict[documento] = {
                "id": id_,
                "nombre": nombre
            }

            self.clientes_dict[nombre] = {
                "id": id_,
                "documento": documento
            }

        self.combo_nit["values"] = self.lista_docs
        self.combo_cliente["values"] = self.lista_nombres
        
    def abrir_ventana_cliente(self):
        self.ventana_cliente = tk.Toplevel(self.ventana)
        self.ventana_cliente.title("Nuevo Cliente")
        
        # --- 2. CENTRAR LA VENTANA EN LA PANTALLA ---
        # (Ajusta el 400 y 500 al tamaño que tenga tu formulario de clientes)
        ancho_ventana = 400 
        alto_ventana = 250
        
        ancho_pantalla = self.ventana_cliente.winfo_screenwidth()
        alto_pantalla = self.ventana_cliente.winfo_screenheight()
        
        x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        y = int((alto_pantalla / 2) - (alto_ventana / 2))
        
        self.ventana_cliente.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        
        # --- 3. CONVERTIRLA EN VENTANA MODAL (BLOQUEAR LA DE ATRÁS) ---
        
        # Evita que se minimice de forma independiente y la mantiene al frente
        self.ventana_cliente.transient(self.ventana) 
        
        # Atrapa todos los eventos (clics y teclado), bloqueando la VentanaVenta
        self.ventana_cliente.grab_set() 
        
        # Pone el cursor/foco automáticamente en esta nueva ventana
        self.ventana_cliente.focus_set()

        # Documento
        tk.Label(self.ventana_cliente, text="Documento").pack(pady=5)
        self.entry_doc_cliente = tk.Entry(self.ventana_cliente)
        self.entry_doc_cliente.pack(pady=5)
        
        # Nombre
        tk.Label(self.ventana_cliente, text="Nombre").pack(pady=5)
        self.entry_nombre_cliente = tk.Entry(self.ventana_cliente)
        self.entry_nombre_cliente.pack(pady=5)

        # Teléfono
        tk.Label(self.ventana_cliente, text="Teléfono").pack(pady=5)
        self.entry_tel_cliente = tk.Entry(self.ventana_cliente)
        self.entry_tel_cliente.pack(pady=5)

        # Botón guardar
        tk.Button(
            self.ventana_cliente,
            text="Guardar",
            command=self.guardar_cliente
        ).pack(pady=10)
        
    def guardar_cliente(self):
        nombre = self.entry_nombre_cliente.get()
        documento = self.entry_doc_cliente.get()
        telefono = self.entry_tel_cliente.get()

        if not nombre or not documento:
            print("⚠️ Datos incompletos")
            return

        clientes.agregar_cliente(nombre, documento, telefono)

        print("✅ Cliente guardado")

        # 🔥 Cerrar ventana
        self.ventana_cliente.destroy()

        # 🔥 Recargar clientes
        self.cargar_clientes()

        # 🔥 SELECCIONAR AUTOMÁTICAMENTE EL NUEVO CLIENTE
        self.combo_nit.set(documento)
        self.combo_cliente.set(nombre)

        # 🔥 Mover foco a producto (flujo rápido)
        self.combo_producto.focus()
        
    def atajo_crear_cliente(self, event):
        self.abrir_ventana_cliente()
        
    def filtrar_productos(self, event):
        texto = self.combo_producto.get().lower()

        filtrados = [p for p in self.lista_productos if texto in p.lower()]

        self.combo_producto["values"] = filtrados
        
    def filtrar_clientes_nombre(self, event):
        texto = self.combo_cliente.get().lower()

        filtrados = [n for n in self.lista_nombres if texto in n.lower()]

        self.combo_cliente["values"] = filtrados
        
    def filtrar_clientes_nit(self, event):
        texto = self.combo_nit.get().lower()

        filtrados = [d for d in self.lista_docs if texto in d.lower()]

        self.combo_nit["values"] = filtrados
        
    def eliminar_producto(self):
        seleccion = self.tabla.focus()

        if not seleccion:
            print("⚠️ Selecciona un producto para eliminar")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Eliminar producto?")

        if respuesta:
            self.tabla.delete(seleccion)
            self.calcular_total()
        
    def eliminar_producto_evento(self, event):
        self.eliminar_producto()
        
        
    def ir_a_producto(self, event):
        self.combo_producto.focus()
        
    def ir_a_cantidad(self, event):
        self.entry_cantidad.focus()
        
    def agregar_producto_evento(self, event):
        self.agregar_y_reset()
        
    def nueva_venta_evento(self, event):
        self.nueva_venta()

    def cambiar_tipo_precio(self, event):
        tipo = self.tipo_precio.get()

        if tipo == "manual":
            self.entry_precio_manual.config(state="normal")
            self.entry_precio_manual.focus()
        else:
            self.entry_precio_manual.delete(0, tk.END)
            self.entry_precio_manual.config(state="disabled")
        
# Ventana principal
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = VentanaVenta(root)
#     root.mainloop()