import sqlite3

def conectar():
    return sqlite3.connect("database/data.db")


def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    # TABLA secuencia para facturas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracion (
        clave TEXT PRIMARY KEY,
        valor TEXT
    )
    """)
    
    cursor.execute("""
    INSERT OR IGNORE INTO configuracion (clave, valor)
    VALUES ('consecutivo_factura', '1')
    """)
    
    # TABLA PROVEEDORES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_empresa TEXT NOT NULL,
            nit TEXT UNIQUE NOT NULL,
            telefono TEXT,
            nombre_vendedor TEXT
        )
    """)
    
    # TABLA COMPRAS (El encabezado de la factura)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            total REAL,
            proveedor_id INTEGER,
            numero_factura_proveedor TEXT
        )
    """)

    # TABLA DETALLE COMPRA (Los productos dentro de la factura)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_compra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_compra INTEGER,
            referencia TEXT,
            cantidad INTEGER,
            precio_costo REAL,
            subtotal REAL,
            FOREIGN KEY (id_compra) REFERENCES compras(id)
        )
    """)

    conn.commit()
    conn.close()
    
def obtener_siguiente_factura():
    conn = conectar()
    cursor = conn.cursor()

    # Obtener valor actual
    cursor.execute("""
    SELECT valor FROM configuracion
    WHERE clave = 'consecutivo_factura'
    """)
    
    resultado = cursor.fetchone()
    numero = int(resultado[0])

    # Formatear factura
    factura = f"FAC-{numero:04d}"

    # Actualizar siguiente número
    cursor.execute("""
    UPDATE configuracion
    SET valor = ?
    WHERE clave = 'consecutivo_factura'
    """, (str(numero + 1),))

    conn.commit()
    conn.close()

    return factura

def ver_siguiente_factura():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT valor FROM configuracion
    WHERE clave = 'consecutivo_factura'
    """)

    resultado = cursor.fetchone()
    numero = int(resultado[0])

    conn.close()

    return f"FAC-{numero:04d}"