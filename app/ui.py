import tkinter as tk

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Ferretería POS")     # Título
ventana.geometry("1080x800")        # Tamaño
ventana.configure(bg="#D1D3D5")     #Color ventana

# 🔲 Frame superior
frame_top = tk.Frame(
    ventana, 
    bg="#D1D3D5",
    bd=3,           #Grosor borde
    relief="groove" #Borde Ranura
)
frame_top.pack(fill="x", padx=10, pady=5)

frame_contenedor = tk.Frame(ventana, bg="#D1D3D5")
frame_contenedor.pack(fill="x", padx=10, pady=5)

frame_datos = tk.LabelFrame(
    ventana,
    text="Datos Cliente",
    bg="#D1D3D5",
    font=("Arial", 12, "bold"),
    bd=3,
    relief="groove"
)

frame_datos.pack(anchor="w", padx=10, pady=5)

tk.Label(frame_datos, bg="#D1D3D5", text="NIT/CC:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entry_documento = tk.Entry(frame_datos, width=25)
entry_documento.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_datos, bg="#D1D3D5", text="Cliente:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
entry_cliente = tk.Entry(frame_datos, width=50)
entry_cliente.grid(row=1, column=1, padx=5, pady=5, sticky="w")

btn_nueva_venta = tk.Button(
    frame_top,
    text="Nueva Venta F1",
    bg="#D1D3D5",
    fg="black",
    font=("Arial", 11),
    bd=2,
    relief="raised",
    cursor="hand2"
)

btn_nueva_venta.pack(side="left", padx=10, pady=20)

btn_cliente_nuevo = tk.Button(
    frame_top,
    text="Cliente Nuevo F2",
    bg="#D1D3D5",
    fg="black",
    font=("Arial", 11),
    bd=2,
    relief="raised",
    cursor="hand2"    
)

btn_cliente_nuevo.pack(side="left", padx=10, pady=20)

btn_eliminar_producto = tk.Button(
    frame_top,
    text="Elimimar Producto Del.",
    bg="#D1D3D5",
    fg="black",
    font=("Arial", 11),
    bd=2,
    relief="raised",
    cursor="hand2"    
)

btn_eliminar_producto.pack(side="left", padx=10, pady=20)


# Ejecutar aplicación
ventana.mainloop()