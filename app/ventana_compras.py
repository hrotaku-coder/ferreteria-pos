import tkinter as tk
from tkinter import ttk, messagebox
import proveedores
import productos
import compras


class VentanaCompras:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Ingresar factura de compra")
        self.ventana.config(bg="#D1D3D5")
        
        ancho_ventana = 1080
        alto_ventana = 800
        
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        y = int((alto_pantalla / 2) - (alto_ventana / 2))
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        

        self.carrito_compras = []
        self.total_compra = 0.0

        self.crear_widgets()

    def crear_widgets(self):
        
        frame_proveedor = tk.LabelFrame(self.ventana, text="Datos del Proveedor", bg="#D1D3D5", font="Arial 10 bold")
        frame_proveedor.pack(fill="x", padx=10, pady=10)

        
        tk.Label(frame_proveedor, text="Proveedor:", bg="#D1D3D5").grid(row=0, column=0, padx=5, pady=5)
        self.combo_proveedor = ttk.Combobox(frame_proveedor, width=40)
        self.combo_proveedor.grid(row=0, column=1, padx=5, pady=5)
        
        self.bt_crear_proveedor = tk.Button(frame_proveedor, text="Nuevo Proveedor", bg="#17a2b8", fg="white", font="Arial 9 bold", command=self.abrir_crear_proveedor)
        self.bt_crear_proveedor.grid(row=0, column=2, padx=20, pady=5)

        tk.Label(frame_proveedor, text="N° Factura Proveedor:", bg="#D1D3D5").grid(row=0, column=3, padx=20, pady=5)
        self.entry_factura = tk.Entry(frame_proveedor, width=20)
        self.entry_factura.grid(row=0, column=4, padx=5, pady=5)

        self.cargar_proveedores()
        
        # --- 2. MARCO CENTRAL: BUSCAR Y AGREGAR PRODUCTOS ---
        frame_producto = tk.LabelFrame(self.ventana, text="Agregar Artículo al Inventario", bg="#D1D3D5", font="Arial 10 bold")
        frame_producto.pack(fill="x", padx=10, pady=5)

        # Buscar Producto
        tk.Label(frame_producto, text="Producto:", bg="#D1D3D5").grid(row=0, column=0, padx=5, pady=5)
        self.combo_producto = ttk.Combobox(frame_producto, width=35)
        self.combo_producto.grid(row=0, column=1, padx=5, pady=5)

        # --- ¡EL NUEVO BOTÓN PARA PRODUCTOS! --- (Columna 2)
        self.btn_nuevo_prod = tk.Button(frame_producto, text="➕ Nuevo", bg="#28a745", fg="white", font="Arial 9 bold", command=self.abrir_crear_producto)
        self.btn_nuevo_prod.grid(row=0, column=2, padx=5, pady=5)

        # Cantidad que llega (Movemos a Columna 3 y 4)
        tk.Label(frame_producto, text="Cant:", bg="#D1D3D5").grid(row=0, column=3, padx=5, pady=5)
        self.entry_cant = tk.Entry(frame_producto, width=8)
        self.entry_cant.grid(row=0, column=4, padx=5, pady=5)

        # Precio de Costo (Movemos a Columna 5 y 6)
        tk.Label(frame_producto, text="Costo Und ($):", bg="#D1D3D5").grid(row=0, column=5, padx=5, pady=5)
        self.entry_costo = tk.Entry(frame_producto, width=12)
        self.entry_costo.grid(row=0, column=6, padx=5, pady=5)

        # Botón para agregar a la lista (Movemos a Columna 7)
        self.btn_agregar = tk.Button(frame_producto, text="Agregar a Lista", bg="#28a745", fg="white", font="Arial 9 bold", command=self.agregar_a_tabla)
        self.btn_agregar.grid(row=0, column=7, padx=10, pady=5)

        # --- 3. MARCO INFERIOR: TABLA DE LA COMPRA ---
        frame_tabla = tk.Frame(self.ventana, bg="#D1D3D5")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        # Definimos las columnas de la tabla
        columnas = ("Referencia", "Descripción", "Cantidad", "Costo Und", "Subtotal")
        self.tabla_compra = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

        # Le ponemos título y tamaño a cada columna
        for col in columnas:
            self.tabla_compra.heading(col, text=col)
            if col == "Descripción":
                self.tabla_compra.column(col, width=300) # Más espacio para el nombre
            else:
                self.tabla_compra.column(col, width=100, anchor="center")

        self.tabla_compra.pack(fill="both", expand=True)

        # Cargamos los productos en el combobox al iniciar
        self.cargar_productos()
        
        # --- 4. MARCO INFERIOR: TOTAL Y GUARDAR ---
        frame_total = tk.Frame(self.ventana, bg="#D1D3D5")
        frame_total.pack(fill="x", padx=10, pady=10)

        # Etiqueta para mostrar la suma de dinero
        self.lbl_total = tk.Label(frame_total, text="Total: $0", font="Arial 14 bold", bg="#D1D3D5", fg="#b30000")
        self.lbl_total.pack(side="left", padx=20)

        # El botón maestro
        self.btn_guardar = tk.Button(frame_total, text="💾 GUARDAR COMPRA", bg="#007bff", fg="white", font="Arial 12 bold", height=2, command=self.guardar_compra)
        self.btn_guardar.pack(side="right", padx=20)

    def cargar_proveedores(self):
      
        lista = proveedores.obtener_proveedores() 
        
        self.combo_proveedor["values"] = [f"{p[2]} - {p[1]}" for p in lista]
        
    def cargar_productos(self):
        # Llamamos a tu archivo de productos para traer el inventario
        lista = productos.listar_productos()
        
        # Guardamos la lista completa en la memoria de la ventana para usarla luego
        self.lista_productos_bd = lista 
        
        # Formateamos el combobox: "Referencia - Nombre"
        self.combo_producto["values"] = [f"{p[2]} - {p[1]}" for p in lista]

    def agregar_a_tabla(self):
        # 1. Obtener los textos de las cajas
        producto_seleccionado = self.combo_producto.get()
        cant_str = self.entry_cant.get()
        costo_str = self.entry_costo.get()

        # 2. VALIDACIÓN 1: Que no dejen cajas en blanco
        if not producto_seleccionado or not cant_str or not costo_str:
            messagebox.showwarning("Advertencia", "Por favor llena todos los campos del producto.")
            return # El return detiene la función aquí mismo para que no dé error

        # 3. VALIDACIÓN 2: Que escriban números y no letras en cantidad y costo
        try:
            cantidad = int(cant_str)
            costo_und = float(costo_str)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero y el costo un número.")
            return

        # 4. Extraer la referencia
        # Recuerda que el combobox dice "REF01 - Tubo PVC". 
        # Usamos split() para partir el texto por el guion y quedarnos con la Parte 0 (REF01) y la Parte 1 (Tubo PVC)
        partes = producto_seleccionado.split(" - ")
        referencia = partes[0]
        nombre = partes[1]

        # 5. La Matemática
        subtotal = cantidad * costo_und

        # 6. Guardar los datos puros en la memoria del programa (para la base de datos)
        # OJO: Guardamos exactamente el orden que espera compras.py: [referencia, cantidad, costo, subtotal]
        self.carrito_compras.append([referencia, cantidad, costo_und, subtotal])

        # 7. Mostrar en la tabla visual (para el cajero)
        self.tabla_compra.insert("", "end", values=(
            referencia, 
            nombre, 
            cantidad, 
            f"${costo_und:,.0f}", 
            f"${subtotal:,.0f}"
        ))

        # 8. Limpiar las cajas para el siguiente producto
        self.combo_producto.set('')
        self.entry_cant.delete(0, tk.END)
        self.entry_costo.delete(0, tk.END)
        
        # Actualizar el total visualmente
        self.total_compra += subtotal
        self.lbl_total.config(text=f"Total: ${self.total_compra:,.0f}")
        
    def guardar_compra(self):
        # 1. VALIDACIONES DE SEGURIDAD
        if len(self.carrito_compras) == 0:
            messagebox.showwarning("Atención", "No hay productos en la lista para guardar.")
            return

        prov_texto = self.combo_proveedor.get()
        factura_prov = self.entry_factura.get()

        if not prov_texto or not factura_prov:
            messagebox.showwarning("Atención", "Debes seleccionar un proveedor y digitar el N° de factura.")
            return

        # 2. EXTRAER EL ID DEL PROVEEDOR
        # En el combobox tenemos "NIT - Empresa". Partimos el texto y sacamos el NIT (posición 0)
        nit_proveedor = prov_texto.split(" - ")[0]
        
        # Buscamos en la BD usando la función que creaste en proveedores.py
        datos_proveedor = proveedores.buscar_proveedor_por_nit(nit_proveedor)
        
        if datos_proveedor is None:
            messagebox.showerror("Error", "No se encontró el proveedor en la base de datos.")
            return
            
        # En la tabla proveedores, el ID está en la posición 0
        id_proveedor = datos_proveedor[0]

        # 3. ¡ENVIAR A LA BASE DE DATOS! (Llamamos a tu archivo compras.py)
        exito = compras.registrar_compra(id_proveedor, factura_prov, self.total_compra, self.carrito_compras)

        # 4. QUÉ HACER DESPUÉS DE GUARDAR
        if exito:
            messagebox.showinfo("Éxito", "¡Compra guardada! El stock de los productos ha sumado correctamente.")
            
            # Limpiar todo para dejar la caja lista para otra compra
            self.carrito_compras.clear()
            self.tabla_compra.delete(*self.tabla_compra.get_children()) # Borra las filas visuales
            self.total_compra = 0.0
            self.lbl_total.config(text="Total: $0")
            self.entry_factura.delete(0, tk.END)
            self.combo_proveedor.set('')
        else:
            messagebox.showerror("Error", "Hubo un error crítico al guardar en la base de datos.")
            
    def abrir_crear_proveedor(self):
        # 1. Crear la ventana modal (hija de compras)
        ventana_prov = tk.Toplevel(self.ventana)
        ventana_prov.title("Nuevo Proveedor")
        ventana_prov.configure(bg="#D1D3D5")

        # Centrar la ventanita
        ancho_ventana = 350
        alto_ventana = 350
        ancho_pantalla = ventana_prov.winfo_screenwidth()
        alto_pantalla = ventana_prov.winfo_screenheight()
        x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        y = int((alto_pantalla / 2) - (alto_ventana / 2))
        ventana_prov.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Bloquear la ventana de atrás
        ventana_prov.transient(self.ventana)
        ventana_prov.grab_set()
        ventana_prov.focus_set()

        # 2. Dibujar el formulario
        tk.Label(ventana_prov, text="Nombre de la Empresa:", bg="#D1D3D5", font="Arial 10 bold").pack(pady=(15, 5))
        entry_empresa = tk.Entry(ventana_prov, width=35)
        entry_empresa.pack()

        tk.Label(ventana_prov, text="NIT:", bg="#D1D3D5", font="Arial 10 bold").pack(pady=(10, 5))
        entry_nit = tk.Entry(ventana_prov, width=35)
        entry_nit.pack()

        tk.Label(ventana_prov, text="Teléfono:", bg="#D1D3D5", font="Arial 10 bold").pack(pady=(10, 5))
        entry_telefono = tk.Entry(ventana_prov, width=35)
        entry_telefono.pack()

        tk.Label(ventana_prov, text="Nombre del Vendedor:", bg="#D1D3D5", font="Arial 10 bold").pack(pady=(10, 5))
        entry_vendedor = tk.Entry(ventana_prov, width=35)
        entry_vendedor.pack()

        # 3. La función interna que guarda los datos
        def guardar_proveedor_nuevo():
            empresa = entry_empresa.get()
            nit = entry_nit.get()
            telefono = entry_telefono.get()
            vendedor = entry_vendedor.get()

            # Validar que no falten los datos clave
            if not empresa or not nit:
                messagebox.showwarning("Atención", "El nombre de la empresa y el NIT son obligatorios.", parent=ventana_prov)
                return

            # Enviar a la base de datos (usando el archivo proveedores.py)
            exito = proveedores.agregar_proveedor(empresa, nit, telefono, vendedor)

            if exito:
                messagebox.showinfo("Éxito", "Proveedor guardado correctamente.", parent=ventana_prov)
                
                # TRUCO DE ORO: Recargar la lista y seleccionarlo automáticamente
                self.cargar_proveedores()
                self.combo_proveedor.set(f"{nit} - {empresa}")
                
                # Cerrar la ventana modal
                ventana_prov.destroy()
            else:
                messagebox.showerror("Error", "Ya existe un proveedor registrado con ese NIT.", parent=ventana_prov)

        # 4. El botón guardar de la ventanita
        btn_guardar_prov = tk.Button(ventana_prov, text="💾 Guardar Proveedor", bg="#007bff", fg="white", font="Arial 10 bold", command=guardar_proveedor_nuevo)
        btn_guardar_prov.pack(pady=20)
        
    def abrir_crear_producto(self):
        # 1. Crear la ventana modal
        ventana_prod = tk.Toplevel(self.ventana)
        ventana_prod.title("Crear Nuevo Producto")
        ventana_prod.configure(bg="#D1D3D5")

        # Centrar
        ancho_ventana = 350
        alto_ventana = 350
        ancho_pantalla = ventana_prod.winfo_screenwidth()
        alto_pantalla = ventana_prod.winfo_screenheight()
        x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        y = int((alto_pantalla / 2) - (alto_ventana / 2))
        ventana_prod.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Bloquear la ventana de atrás
        ventana_prod.transient(self.ventana)
        ventana_prod.grab_set()
        ventana_prod.focus_set()

        # 2. Dibujar el formulario
        tk.Label(ventana_prod, text="Referencia (Código):", bg="#D1D3D5", font="Arial 10 bold").pack(pady=(15, 5))
        entry_ref = tk.Entry(ventana_prod, width=35)
        entry_ref.pack()

        tk.Label(ventana_prod, text="Nombre / Descripción:", bg="#D1D3D5", font="Arial 10 bold").pack(pady=(10, 5))
        entry_nombre = tk.Entry(ventana_prod, width=35)
        entry_nombre.pack()

        tk.Label(ventana_prod, text="Precio de Venta al Público ($):", bg="#D1D3D5", font="Arial 10 bold").pack(pady=(10, 5))
        entry_precio = tk.Entry(ventana_prod, width=35)
        entry_precio.pack()

        # 3. La lógica de guardado
        def guardar_producto_nuevo():
            ref = entry_ref.get().upper() # Convertimos a mayúscula para evitar errores
            nombre = entry_nombre.get()
            precio_str = entry_precio.get()

            # Validar campos vacíos
            if not ref or not nombre or not precio_str:
                messagebox.showwarning("Atención", "Todos los campos son obligatorios.", parent=ventana_prod)
                return

            # Validar que el precio sea un número
            try:
                precio_venta = float(precio_str)
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número válido.", parent=ventana_prod)
                return

            # Usamos tu función buscar_producto para saber si la referencia ya existe
            if productos.buscar_producto(ref) is not None:
                messagebox.showerror("Error", "Ya existe un producto con esa referencia.", parent=ventana_prod)
                return

            # --- EL TRUCO DEL CERO ---
            # OJO: Le mandamos '0' como stock. 
            # ¿Por qué? Porque apenas estamos creando la "ficha" del producto. 
            # El stock real se sumará cuando terminemos de hacer esta compra. 
            # Si le ponemos stock aquí, ¡se sumaría doble cuando guardemos la factura!
            productos.agregar_producto(nombre, ref, precio_venta, 0)

            messagebox.showinfo("Éxito", "Producto creado. Ahora ingresa la cantidad que llegó y su costo.", parent=ventana_prod)
            
            # Recargar la lista y seleccionarlo automáticamente
            self.cargar_productos()
            self.combo_producto.set(f"{ref} - {nombre}")
            
            # Cerrar la ventanita
            ventana_prod.destroy()

        # 4. Botón de guardar
        btn_guardar = tk.Button(ventana_prod, text="💾 Crear Producto", bg="#007bff", fg="white", font="Arial 10 bold", command=guardar_producto_nuevo)
        btn_guardar.pack(pady=20)