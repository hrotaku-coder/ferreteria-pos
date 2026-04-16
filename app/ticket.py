import win32print
from datetime import datetime

def imprimir_ticket(texto):
    nombre_impresora = win32print.GetDefaultPrinter()

    handle = win32print.OpenPrinter(nombre_impresora)
    
    win32print.StartDocPrinter(handle, 1, ("Ticket", None, "RAW"))
    win32print.StartPagePrinter(handle)

    win32print.WritePrinter(handle, texto.encode("utf-8"))

    win32print.EndPagePrinter(handle)
    win32print.EndDocPrinter(handle)
    win32print.ClosePrinter(handle)
    
def generar_texto_ticket(numero, cliente, productos, total, copia=False):
    ancho = 40
    texto = ""
    
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    def linea():
        return "-" * ancho + "\n"

    def centrar(txt):
        return txt.center(ancho) + "\n"

    def izquierda_derecha(izq, der):
        return f"{izq}{' ' * (ancho - len(izq) - len(der))}{der}\n"
    

    # ENCABEZADO
    texto += centrar("GRAN COMERCIO")
    texto += centrar("NIT: 98385254-2")
    texto += centrar("carrera 11 # 16-07 B/Fatima")
    texto += centrar("Tel: 312 854 7140")
    texto += centrar("grancomercio1607.fc@gmail.com")
    texto += linea()

    texto += izquierda_derecha("Factura:", numero)
    texto += izquierda_derecha("Cliente:", cliente)
    texto += izquierda_derecha("Fecha:", fecha)
    texto += linea()

    # PRODUCTOS
    def dividir_texto(texto, ancho):
        palabras = texto.split()
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            if len(linea_actual) + len(palabra) + 1 <= ancho:
                if linea_actual:
                    linea_actual += " " + palabra
                else:
                    linea_actual = palabra
            else:
                lineas.append(linea_actual)
                linea_actual = palabra

        if linea_actual:
            lineas.append(linea_actual)

        return lineas

    for ref, nombre, cant, precio, subtotal in productos:
        # Mostrar referencia
        texto += f"Ref: {ref}\n"

        # Dividir nombre en varias líneas
        lineas_nombre = dividir_texto(nombre, ancho)

        for linea_nombre in lineas_nombre:
            texto += linea_nombre + "\n"

        precio_txt = f"{precio:,.0f}"
        subtotal_txt = f"{subtotal:,.0f}"

        linea_producto = f"{cant} x {precio_txt}"
        texto += izquierda_derecha(linea_producto, subtotal_txt)

    texto += linea()

    # TOTAL
    total_txt = f"{total:,.0f}"
    texto += izquierda_derecha("TOTAL:", total_txt)
    texto += linea()

    texto += centrar("GRACIAS POR SU COMPRA")
    texto += linea()
    
    if copia:
        texto += centrar("***** COPIA *****")
        
    texto += "\n" * 8

    return texto