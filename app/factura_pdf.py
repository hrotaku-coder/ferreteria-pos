import os
from datetime import datetime
from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter #---esto es pra definir el tamaño del papel, en este caso carta (8.5 x 11 pulgadas)

def generar_pdf(numero_factura, nit_cliente, nombre_cliente, productos, total_venta):
    # 1. Crear una carpeta para guardar las facturas si no existe
    if not os.path.exists("facturas_pdf"):
        os.makedirs("facturas_pdf")
        
    nombre_archivo = f"facturas_pdf/Factura_{numero_factura}.pdf"
    
    # 2. Calcular alto dinámico
    margen_superior_inferior = 150 # Espacio para encabezado y firma
    espacio_por_producto = 25      # Espacio aproximado por cada fila de producto
    
    # Calculamos el alto: (cantidad de productos * espacio) + márgenes
    alto_dinamico = margen_superior_inferior + (len(productos) * espacio_por_producto)
    
    # Establecemos un alto mínimo (por si solo hay 1 producto)
    if alto_dinamico < 400:
        alto_dinamico = 400

    ancho_ticket = 227 
    c = canvas.Canvas(nombre_archivo, pagesize=(ancho_ticket, alto_dinamico))
    
    # --- ENCABEZADO ---
    centro = 113
    y = alto_dinamico - 20 # Empezamos a escribir desde un poco abajo del borde superior
    
    c.setFont("Helvetica-Bold", 12) #---establece la fuente y el tamaño para el encabezado
    c.drawCentredString(centro, y, "GRAN COMERCIO") #---drawCentredString centra el texto en la posición horizontal dada por 'centro'  
   
    y -= 20 # Bajamos para la siguiente línea
    c.setFont("Helvetica", 9) #---cambia la fuente para el resto del texto
    c.drawString(10, y, f"Factura No: {numero_factura}")#---drawString coloca el texto en la posición (x, y) especificada, en este caso cerca del borde izquierdo y un poco más abajo del encabezado
    
    y -= 15
    c.drawString(10, y, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")#---Aquí se muestra la fecha y hora actual formateada como 'YYYY-MM-DD HH:MM:SS'
    
    y -= 25
    c.drawString(10, y, f"Cliente: {nombre_cliente}") # ---drawString coloca el nombre del cliente cerca del borde izquierdo y un poco más abajo de los datos de la factura
    
    y -= 15
    c.drawString(10, y, f"NIT/CC: {nit_cliente}") # ---drawString coloca el NIT o CC del cliente cerca del borde izquierdo y un poco más abajo del nombre del cliente``
    
    y -= 30 # Bajamos un poco más para dejar espacio antes de la tabla de productos
    
    # --- ENCABEZADO DE LA TABLA ---
    
    y = alto_dinamico - 120 # Posición inicial para la tabla (ajustable según el diseño)
    
    # Definimos columnas fijas dentro de los 227 puntos disponibles:
    col_ref = 10     # Casi al borde izquierdo
    col_desc = 60    # Un poco más a la derecha
    col_cant = 160   # Cerca del final
    col_total = 215  # Alineado a la derecha (usaremos drawRightString para este)
    
    # Ejemplo de encabezado de tabla:
    c.setFont("Helvetica-Bold", 8)
    c.drawString(col_ref, y, "REF")
    c.drawString(col_desc, y, "DESCRIPCIÓN")
    c.drawString(col_cant, y, "CANT") # <--- Agrega esta línea
    c.drawRightString(col_total, y, "TOTAL") # <--- Alinea "TOTAL" a la derecha
    

    
    c.setFont("Helvetica", 9)
    y -= 15 
    
    for p in productos:
        ref, nombre, cant, precio, subtotal = p 
        
        # 1. Escribimos los datos que NO cambian (Ref, Cant y Total)
        c.drawString(col_ref, y, str(ref))
        c.drawString(col_cant, y, str(cant))
        c.drawRightString(col_total, y, f"${subtotal:,.0f}")

        # 2. Lógica para el NOMBRE (Salto de línea)
        if len(nombre) > 18:
            primera_parte = nombre[:18]
            segunda_parte = nombre[18:36] # Toma los siguientes caracteres
            
            c.drawString(col_desc, y, primera_parte) # Escribe la primera línea
            y -= 10                                  # Baja un poco (salto interno)
            c.drawString(col_desc, y, segunda_parte) # Escribe lo que sobró
        else:
            c.drawString(col_desc, y, nombre) # Si es corto, se escribe normal
            
        y -= 15 # Espacio para separar del SIGUIENTE producto

    # --- TOTAL ---
    c.setFont("Helvetica-Bold", 10)
    # Ponemos la palabra "TOTAL:" cerca del margen derecho
    c.drawString(130, y - 15, "TOTAL:")
    
    # Alineamos el valor a la derecha igual que los subtotales
    c.drawRightString(col_total, y - 15, f"${total_venta:,.0f}")
    
    # 3. Guardar el archivo
    c.save()
    return nombre_archivo