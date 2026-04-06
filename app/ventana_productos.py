import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from openpyxl import load_workbook
from tkinter import messagebox
import csv

import productos

class VentanaProductos:
    
    def __init__ (self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestion de Productos")
        self.ventana.configure(bg="#D1D3D5")
        
        # --- CENTRAR VENTANA DE PRODUCTOS ---
        ancho_ventana = 1080
        alto_ventana = 800
        
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        
        x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        y = int((alto_pantalla / 2) - (alto_ventana / 2))
        
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        self.frame_operaciones = tk.LabelFrame(self.ventana, text="Gestion de Productos", font="Arial 12 bold", bg="#D1D3D5")
        self.frame_operaciones.pack(fill="x", padx=10, pady=10,)
        
        self.lbl_buscarproducto = tk.Label(self.frame_operaciones, text="Buscar Producto:", font="Arial 12", bg="#D1D3D5")
        self.lbl_buscarproducto.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.combo_buscarproducto = ttk.Combobox(self.frame_operaciones, font="sans 12", width=40)
        self.combo_buscarproducto.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")

        self.combo_buscarproducto.bind("<KeyRelease>", self.filtrar_productos)
        
        
        self.btn_crearproducto = tk.Button(
            self.frame_operaciones,
            text="Crear Nuevo Producto",
            font=("Arial", 11),
            bg="#D1D3D5",
            width=20,
            command=self.abrir_formulario_producto
            
        )

        self.btn_crearproducto.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        
        self.btn_editarproducto = tk.Button(
            self.frame_operaciones,
            text="Editar Producto",
            font=("Arial", 11),
            bg="#D1D3D5",
            width=20,
            command=self.editar_producto
            
        )

        self.btn_editarproducto.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        ruta_impot = "iconos/import.png"
        
        img = Image.open(ruta_impot)
        img = img.resize((40, 24))
        self.icono_import = ImageTk.PhotoImage(img)
        
        
        self.btn_importarproducto = tk.Button(
            self.frame_operaciones,
            text="  Importar Productos",
            image=self.icono_import,
            compound="left",
            font=("Arial", 11),
            bg="#D1D3D5",
            width=180,
            command=self.importar_productos
            
        )

        self.btn_importarproducto.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        
        self.btn_importarproducto.image = self.icono_import
        
        self.btn_eliminarproducto = tk.Button(
            self.frame_operaciones,
            text="Eliminar Producto",
            font=("Arial", 11),
            bg="#D1D3D5",
            width=20,
            command=self.eliminar_producto
            
        )
        
        self.btn_eliminarproducto.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        
        
        self.frame_tabla = tk.LabelFrame(
            self.ventana,
            text="Lista de Productos",
            font="Arial 12 bold",
            bg="#D1D3D5"
        )

        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tabla = ttk.Treeview(self.frame_tabla)

        self.tabla["columns"] = ("referencia", "nombre", "precio", "stock")

        self.tabla.column("#0", width=0, stretch=tk.NO)

        self.tabla.column("referencia", anchor="w", width=150)
        self.tabla.column("nombre", anchor="w", width=300)
        self.tabla.column("precio", anchor="e", width=100)
        self.tabla.column("stock", anchor="center", width=100)

        self.tabla.heading("#0", text="")
        self.tabla.heading("referencia", text="Referencia")
        self.tabla.heading("nombre", text="Nombre del Producto")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("stock", text="Stock")

        self.tabla.pack(fill="both", expand=True)
        
        self.cargar_productos()
        
    def abrir_formulario_producto(self):
        self.ventana_form = tk.Toplevel(self.ventana)
        self.ventana_form.title("Nuevo Producto")
        self.ventana_form.configure(bg="#D1D3D5")
        
        ancho_ventana = 600
        alto_ventana = 250
        
        ancho_pantalla = self.ventana_form.winfo_screenwidth() # --- Obtener ancho de pantalla
        alto_pantalla = self.ventana_form.winfo_screenheight() # --- Obtener alto de pantalla
        
        x = int((ancho_pantalla / 2) - (ancho_ventana / 2)) # --- Calcular coordenada x
        y = int((alto_pantalla / 2) - (alto_ventana / 2)) # --- Calcular coordenada y
        
        self.ventana_form.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}") # --- Aplicar tamaño y posición
        
        # convertir la ventana en modal
        self.ventana_form.transient(self.ventana) # --- Hacer que la ventana hija dependa de la ventana principal
        self.ventana_form.grab_set() # --- Capturar todos los eventos en la ventana hija
        self.ventana.focus_set() # --- Establecer el foco en la ventana principal
        
        
        tk.Label(self.ventana_form, text="Refernecia", font="Arial 12", bg="#D1D3D5").place(x=15, y=20)
        self.entry_referen = tk.Entry(self.ventana_form, font="sans 12", width=40)
        self.entry_referen.place(x=15, y=40)
        
        tk.Label(self.ventana_form, text="Nombre del Producto", font="Arial 12", bg="#D1D3D5").place(x=15, y=70)
        self.entry_producto = tk.Entry(self.ventana_form, font="sans 12", width=40)
        self.entry_producto.place(x=15, y=90)
        
        tk.Label(self.ventana_form, text="Precio", font="Arial 12", bg="#D1D3D5").place(x=15, y=120)
        self.entry_precio = tk.Entry(self.ventana_form, font="sans 12", width=40)
        self.entry_precio.place(x=15, y=140)
        
        tk.Label(self.ventana_form, text="Stock", font="Arial 12", bg="#D1D3D5").place(x=15, y=170)
        self.entry_stock = tk.Entry(self.ventana_form, font="sans 12", width=40)
        self.entry_stock.place(x=15, y=190)
        
        self.btn_guardar = tk.Button(
            self.ventana_form,
            text="GUARDAR",
            font="Arial 12 bold",
            bg="#D1D3D5",
            width=10,
            command=self.guardar_producto
        )
        
        self.btn_guardar.place(x=450,y=125)
        
    def guardar_producto(self):
        referencia = self.entry_referen.get()
        nombre = self.entry_producto.get()
        precio = self.entry_precio.get()
        stock = self.entry_stock.get()
        
        if not referencia or not nombre or not precio or not stock:
            print("⚠️ Todos los campos son obligatorios")
            return
    
        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            print("⚠️ Precio o stock inválidos")
            return
        
        if hasattr(self, "modo_edicion") and self.modo_edicion:
            productos.actualizar_producto(self.referencia_original, nombre, referencia, precio, stock)
            print("✏️ Producto actualizado")
            self.modo_edicion = False
        else:
            productos.agregar_producto(nombre, referencia, precio, stock)
            print("✅ Producto guardado correctamente")
        
        self.cargar_productos()
        self.ventana_form.destroy()
        
    def cargar_productos(self):

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        lista = productos.listar_productos()

        for p in lista:
            id_, nombre, referencia, precio, stock = p

            self.tabla.insert("", "end", values=(
                referencia,
                nombre,
                precio,
                stock
            ))

    def obtener_producto_seleccionado(self):
        seleccion = self.tabla.focus()

        if not seleccion:
            print("⚠️ Selecciona un producto")
            return None

        datos = self.tabla.item(seleccion, "values")
        return datos
    
    def editar_producto(self):
        datos = self.obtener_producto_seleccionado()

        if not datos:
            return

        referencia, nombre, precio, stock = datos

        self.abrir_formulario_producto()

        self.entry_referen.insert(0, referencia)
        self.entry_producto.insert(0, nombre)
        self.entry_precio.insert(0, precio)
        self.entry_stock.insert(0, stock)

        self.modo_edicion = True
        self.referencia_original = referencia


    def importar_productos(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=(
                ("Archivos Excel", "*.xlsx"),
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            )
        )

        if not ruta:
            return

        print("Archivo seleccionado:", ruta)

        if ruta.endswith(".xlsx"):
            self.importar_excel(ruta)
        elif ruta.endswith(".csv"):
            self.importar_csv(ruta)

        self.cargar_productos()
        print("✅ Importación completada")

    def importar_excel(self, ruta):
        libro = load_workbook(ruta)
        hoja = libro.active

        for fila in hoja.iter_rows(min_row=2, values_only=True):
            try:
                nombre = fila[0]
                referencia = fila[1]
                precio = float(fila[2])
                stock = int(fila[3])

                productos.agregar_producto(nombre, referencia, precio, stock)

            except Exception as e:
                print("Error en fila:", fila, e)

        self.cargar_productos()
        print("✅ Importación desde Excel completada")

    def filtrar_productos(self, event):
        texto = self.combo_buscarproducto.get().lower()

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        lista = productos.listar_productos()

        for p in lista:
            id_, nombre, referencia, precio, stock = p

            if texto in nombre.lower() or texto in referencia.lower():
                self.tabla.insert("", "end", values=(
                    referencia,
                    nombre,
                    precio,
                    stock
                ))
                
    def importar_csv(self, ruta):
        with open(ruta, newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)

            for fila in lector:
                try:
                    nombre = fila[0]
                    referencia = fila[1]
                    precio = float(fila[2])
                    stock = int(fila[3])

                    productos.agregar_producto(nombre, referencia, precio, stock)

                except Exception as e:
                    print("Error en fila:", fila, e)
                    
    def eliminar_producto(self):
        datos = self.obtener_producto_seleccionado()

        if not datos:
            return

        referencia = datos[0]

        respuesta = tk.messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar producto {referencia}?"
        )

        if respuesta:
            conn = productos.conectar()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM productos WHERE referencia = ?", (referencia,))
            conn.commit()
            conn.close()

            print("🗑 Producto eliminado")

            self.cargar_productos()


            
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaProductos(root)
    root.mainloop()