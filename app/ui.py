from tkinter import *
import tkinter as tk
from tkinter import ttk

import productos

class VentanaVenta:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Ferretería POS")
        self.ventana.geometry("1080x800")
        self.ventana.configure(bg="#D1D3D5")
        
        # CONTENEDOR PARA BOTONES NUEVA VENTA, CREAR CLIENTE Y ELIMINAR PRODUCTO
        self.frame_top = tk.Frame(self.ventana, bg="#D1D3D5", bd=3, relief="groove",)
        self.frame_top.pack(fill="x", padx=10, pady=5)
        
        # BOTONES
        self.btn_nueva = tk.Button(
            self.frame_top,
            text="Nueva Venta F1",
            font=("Arial", 11),
            bd=2,
            relief="raised"
        )

        self.btn_nueva.pack(side="left", padx=10, pady=10)
        
        self.btn_crearcliente = tk.Button(
            self.frame_top,
            text="Crear cliente F2",
            font=("Arial", 11),
            bd=2,
            relief="raised"
        )

        self.btn_crearcliente.pack(side="left", padx=10, pady=10)
        
        self.btn_eliminarproducto = tk.Button(
            self.frame_top,
            text="Eliminar producto Del.",
            font=("Arial", 11),
            bd=2,
            relief="raised"
        )

        self.btn_eliminarproducto.pack(side="left", padx=10, pady=10)
    
        # CONTENEDOR DATOS CLIENTE
        self.frame_datoscliente = tk.LabelFrame(self.ventana, text="Datos Cliente", font="Arial 12 bold", bg="#D1D3D5",)
        self.frame_datoscliente.place(x=15, y=70, width=520, height=100)
        
        self.lbl_nit = tk.Label(self.frame_datoscliente, text="NIT/CC:", font="Arial 12", bg="#D1D3D5")
        self.lbl_nit.grid(row=0, column=0, padx=5, pady=5)
        self.combo_nit = ttk.Combobox(self.frame_datoscliente, font="sans 12")
        self.combo_nit.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.lbl_cliente = tk.Label(self.frame_datoscliente, text="Cliente:", font="Arial 12", bg="#D1D3D5")
        self.lbl_cliente.grid(row=1, column=0, padx=5, pady=5)
        self.combo_cliente = ttk.Combobox(self.frame_datoscliente, font="sans 12", width=40)
        self.combo_cliente.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # CONTENEDOR INFORMACION FACTURA
        self.frame_informacionfactura = tk.LabelFrame(self.ventana, text="Informacion De Factura", font="Arial 12 bold", bg="#D1D3D5",)
        self.frame_informacionfactura.place(x=545, y=70, width=520, height=100)
        
        self.lbl_factura = tk.Label(self.frame_informacionfactura, text="No Factura:", font="Arial 12", bg="#D1D3D5")
        self.lbl_factura.grid(row=0, column=0, padx=5, pady=5)
        self.entry_factura = ttk.Entry(self.frame_informacionfactura, font="sans 12", width=10)
        self.entry_factura.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.lbl_fecha = tk.Label(self.frame_informacionfactura, text="Fecha:", font="Arial 12", bg="#D1D3D5")
        self.lbl_fecha.grid(row=1, column=0, padx=5, pady=5)
        self.entry_fecha = ttk.Entry(self.frame_informacionfactura, font="sans 12", width=15)
        self.entry_fecha.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # CONTENEDOR BUSQUEDA DE PRODUCTO
        self.frame_busqueda = tk.LabelFrame(self.ventana, text="Busqueda de producto", font="Arial 12 bold", bg="#D1D3D5",)
        self.frame_busqueda.place(x=10, y=180, width=1060, height=70)
        
        self.lbl_producto = tk.Label(self.frame_busqueda, text="Buscar producto:", font="Arial 12", bg="#D1D3D5")
        self.lbl_producto.grid(row=0, column=0, padx=5, pady=5)
        self.combo_producto = ttk.Combobox(self.frame_busqueda, font="sans 12", width=40)
        self.combo_producto.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.combo_producto.bind("<<ComboboxSelected>>", self.seleccionar_producto)
        
        self.cargar_productos()
        
        self.lbl_cantidad = tk.Label(self.frame_busqueda, text="Cantidad", font="Arial 12", bg="#D1D3D5")
        self.lbl_cantidad.grid(row=0,column=2, padx=5, pady=5)
        self.entry_cantidad = ttk.Entry(self.frame_busqueda, font="sans 12", width=6)
        self.entry_cantidad.grid(row=0, column=3,padx=5, pady=5, sticky="w")
        
        self.lbl_stock = tk.Label(self.frame_busqueda, text="Stock", font="Arial 12", bg="#D1D3D5")
        self.lbl_stock.grid(row=0,column=4, padx=5, pady=5)
        self.entry_stock = ttk.Entry(self.frame_busqueda, font="sans 12", width=6)
        self.entry_stock.grid(row=0, column=5,padx=5, pady=5, sticky="w")
        
        self.btn_agregar = tk.Button(
            self.frame_busqueda,
            text="Agregar",
            font=("Arial", 11),
            bd=2,
            relief="raised",
            command=self.agregar_producto
        )

        self.btn_agregar.grid(row=0, column=6, padx=5, pady=5)
        
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

        self.tabla["columns"] = ("referencia", "producto", "cantidad", "valor", "total")

        self.tabla.column("#0", width=0, stretch=NO)

        self.tabla.column("referencia", anchor="w", width=100)
        self.tabla.column("producto", anchor="w", width=400)
        self.tabla.column("cantidad", anchor="center", width=80)
        self.tabla.column("valor", anchor="e", width=80)
        self.tabla.column("total", anchor="e", width=80)

        self.tabla.heading("#0", text="")
        self.tabla.heading("referencia", text="Referencia")
        self.tabla.heading("producto", text="Producto")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.heading("valor", text="Valor")
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
            height=2
        )

        self.btn_cobrar.pack(side="top", pady=5)
        
    def cargar_productos(self):
        lista_productos = productos.listar_productos()

        nombres = []
        self.productos_dict = {}

        for p in lista_productos:
            id_, nombre, referencia, precio, stock = p

            nombres.append(nombre)

            # guardamos todo para usar después
            self.productos_dict[nombre] = {
                "referencia": referencia,
                "precio": precio,
                "stock": stock
            }

        self.combo_producto["values"] = nombres
        
    def seleccionar_producto(self, event):
        nombre = self.combo_producto.get()

        if nombre in self.productos_dict:
            datos = self.productos_dict[nombre]

            stock = datos["stock"]
            precio = datos["precio"]

            # STOCK
            self.entry_stock.delete(0, tk.END)
            self.entry_stock.insert(0, stock)

            # 👉 NUEVO: guardar precio en memoria
            self.precio_actual = precio
            
    def agregar_producto(self):
        nombre = self.combo_producto.get()
        cantidad = self.entry_cantidad.get()

        # Validación básica
        if not nombre or not cantidad:
            print("⚠️ Falta producto o cantidad")
            return

        cantidad = int(cantidad)

        datos = self.productos_dict[nombre]

        referencia = datos["referencia"]
        precio = datos["precio"]

        total = cantidad * precio

        # Insertar en tabla
        self.tabla.insert("", "end", values=(
            referencia,
            nombre,
            cantidad,
            precio,
            total
        ))

        print("✅ Producto agregado")
        
        
        
# Ventana principal
root = tk.Tk()
app = VentanaVenta(root)

root.mainloop()