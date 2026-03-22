import tkinter as tk
from tkinter import ttk

ventana = tk.Tk()
ventana.title("Ferretería POS")
ventana.geometry("1080x800")
ventana.configure(bg="#D1D3D5")

# --- FRAME SUPERIOR (BOTONES) ---
frame_top = tk.Frame(ventana, bg="#D1D3D5", bd=3, relief="groove")
frame_top.pack(fill="x", padx=10, pady=5)

# Botones (usando pack correctamente)
for texto in ["Nueva Venta F1", "Cliente Nuevo F2", "Eliminar Producto Del."]:
    tk.Button(frame_top, text=texto, bg="#D1D3D5", font=("Arial", 11), bd=2, relief="raised").pack(side="left", padx=10, pady=20)

# --- CONTENEDOR PARA LOS LABEL FRAMES (La solución) ---
# Creamos un frame intermedio para que no choque con el pack de arriba
frame_contenedor_medio = tk.Frame(ventana, bg="#D1D3D5")
frame_contenedor_medio.pack(fill="x", padx=10, pady=5)

# --- LABEL FRAME DATOS (Izquierda) ---
frame_datos = tk.LabelFrame(frame_contenedor_medio, text="Datos Cliente", bg="#D1D3D5", font=("Arial", 12, "bold"), bd=3, relief="groove")
frame_datos.pack(side="left", padx=10, fill="both", expand=True)

tk.Label(frame_datos, bg="#D1D3D5", text="NIT/CC:").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(frame_datos, width=25).grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_datos, bg="#D1D3D5", text="Clienete",).grid(row=1, column=0, padx=5, pady=5)
tk.Entry(frame_datos, width=50).grid(row=1, column=1, padx=5, pady=5, sticky="w")

# --- LABEL FRAME FACTURA (Derecha) ---
frame_factura = tk.LabelFrame(frame_contenedor_medio, text="Información De Factura", bg="#D1D3D5", font=("Arial", 12, "bold"), bd=3, relief="groove")
frame_factura.pack(side="left", padx=10, fill="both", expand=True)

tk.Label(frame_factura, bg="#D1D3D5", text="Nro Factura:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
tk.Entry(frame_factura, width=15).grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_factura, bg="#D1D3D5", text="Fecha:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
tk.Entry(frame_factura, width=20).grid(row=1, column=1, padx=5, pady=5, sticky="w")

# --- LABEL FRAME BUSQUEDA DE PRODUCTO ---

frame_busqueda = tk.LabelFrame(ventana, text="Busqueda de producto", bg="#D1D3D5", font=("Arial", 12, "bold"), bd=3, relief="groove")
frame_busqueda.pack(fill="x", padx=10, pady=5)

tk.Label(frame_busqueda, bg="#D1D3D5", text="Buscar producto").grid(row=0, column=0, padx=5, pady=5, sticky="w")
tk.Entry(frame_busqueda, width=40).grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_busqueda, bg="#D1D3D5", text="Cantidad",).grid(row=0, column=2, padx=5, pady=5, sticky="w")
tk.Entry(frame_busqueda, width=10).grid(row=0, column=3, padx=5, pady=5, sticky="w")

for texto in ["Agregar"]:
    tk.Button(frame_busqueda, text=texto, bg="#D1D3D5", font=("Arial", 11), bd=2, relief="raised").grid(row=0, column=4, padx=5, pady=5, sticky="w")
    

tk.Label(frame_busqueda, bg="#D1D3D5", text="Stock",).grid(row=0, column=5, padx=5, pady=5, sticky="w")
tk.Entry(frame_busqueda, width=10).grid(row=0, column=6, padx=5, pady=5, sticky="w")

frame_productos = tk.LabelFrame(ventana, text="Detalle de Venta", bg="#D1D3D5", font=("Arial", 12, "bold"), bd=3, relief="groove", height=400)
frame_productos.pack(fill="x", padx=10, pady=5)
frame_productos.pack_propagate(False)

tabla = ttk.Treeview(frame_productos)
tabla.pack(fill="both", expand=True)

tabla["columns"] = ("ref", "nombre", "cantidad", "precio", "total")
tabla["show"] = "headings"

tabla.heading("ref", text="Referencia")
tabla.heading("nombre", text="Producto")
tabla.heading("cantidad", text="Cantidad")
tabla.heading("precio", text="Valor Unitario")
tabla.heading("total", text="Total")

tabla.column("ref", width=100)
tabla.column("nombre", width=300)
tabla.column("cantidad", width=80)
tabla.column("precio", width=80)
tabla.column("total", width=80)

tabla.column("ref", anchor="center")
tabla.column("cantidad", anchor="center")
tabla.column("precio", anchor="e")
tabla.column("total", anchor="e")

frame_total = tk.Frame(ventana, bg="#D1D3D5")
frame_total.pack(fill="x", padx=10, pady=5)

label_total = tk.Label(frame_total, text="$ 0", font=("Arial", 16, "bold"), fg="green", bg="#D1D3D5")
label_total.pack(side="right", padx=10)

tk.Label(frame_total, text="TOTAL:", font=("Arial", 14, "bold"), bg="#D1D3D5").pack(side="right", padx=5)

for texto in ["Cobrar F3"]:
    tk.Button(frame_total, text=texto, bg="#D1D3D5", font=("Arial", 20, "bold"), fg="red", bd=2, relief="raised").pack(side="left", padx=10, pady=10)

ventana.mainloop()
 