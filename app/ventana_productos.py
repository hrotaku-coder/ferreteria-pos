import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import productos

class VentanaProductos:
    
    def __init__ (self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestion de Productos")
        self.ventana.geometry("1080x800")
        self.ventana.configure(bg="#D1D3D5")

        self.frame_operaciones = tk.LabelFrame(self.ventana, text="Gestion de Productos", font="Arial 12 bold", bg="#D1D3D5")
        self.frame_operaciones.pack(fill="x", padx=10, pady=10,)
        
        self.lbl_buscarproducto = tk.Label(self.frame_operaciones, text="Buscar Producto:", font="Arial 12", bg="#D1D3D5")
        self.lbl_buscarproducto.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.combo_buscarproducto = ttk.Combobox(self.frame_operaciones, font="sans 12", width=40)
        self.combo_buscarproducto.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        
        
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
            width=20
            
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
            width=180
            
        )

        self.btn_importarproducto.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        
        self.btn_importarproducto.image = self.icono_import
        
    def abrir_formulario_producto(self):
        self.ventana_form = tk.Toplevel(self.ventana)
        self.ventana_form.title("Nuevo Producto")
        self.ventana_form.geometry("600x250")
        self.ventana_form.configure(bg="#D1D3D5")
        
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
        
        productos.agregar_producto(nombre, referencia, precio, stock)

        print("✅ Producto guardado correctamente")
        
        self.ventana_form.destroy()
            
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaProductos(root)
    root.mainloop()