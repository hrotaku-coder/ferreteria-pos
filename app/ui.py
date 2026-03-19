import tkinter as tk

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Ferretería POS")     # Título
ventana.geometry("1080x800")        # Tamaño
ventana.configure(bg="#D1D3D5")     #Color ventana

# 🔲 Frame superior
frame_top = tk.Frame(
    ventana, 
    bg="#bfcad3", 
    height=80,
    bd=2,           #Grosor borde
    relief="groove" #Borde Ranura
)
frame_top.pack(fill="x")

btn_nueva_venta = tk.Button(
    frame_top,
    text="Nueva Venta F1",
    bg="#bfcad3",
    fg="black",
    font=("Arial", 12, "bold"),
    bd=2,
    relief="raised",
    cursor="hand2"
)

btn_nueva_venta.pack(side="left", padx=10, pady=20)

btn_cliente_nuevo = tk.Button(
    frame_top,
    text="Cliente Nuevo F2",
    bg="#bfcad3",
    fg="black",
    font=("Arial", 12, "bold"),
    bd=2,
    relief="raised",
    cursor="hand2"    
)

btn_cliente_nuevo.pack(side="left", padx=10, pady=20)

btn_eliminar_producto = tk.Button(
    frame_top,
    text="Elimimar Producto Del.",
    bg="#bfcad3",
    fg="black",
    font=("Arial", 12, "bold"),
    bd=2,
    relief="raised",
    cursor="hand2"    
)

btn_eliminar_producto.pack(side="left", padx=10, pady=20)


# Ejecutar aplicación
ventana.mainloop()