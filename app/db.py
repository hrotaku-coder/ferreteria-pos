import sqlite3

def conectar():
    return sqlite3.connect("database/data.db")


def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    # 1. TABLA secuencia para facturas
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

    # 2. TABLAS PADRE (No dependen de nadie)
    
    # Tabla Clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        documento TEXT UNIQUE NOT NULL,
        telefono TEXT
    )
    """)

    # Tabla Productos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        referencia TEXT UNIQUE NOT NULL,
        precio1 REAL NOT NULL,
        precio2 REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """)
    
    # Tabla Proveedores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_empresa TEXT NOT NULL,
            nit TEXT UNIQUE NOT NULL,
            telefono TEXT,
            nombre_vendedor TEXT
        )
    """)

    # 3. TABLAS HIJAS Y NIETAS (Transacciones)

    # Tabla Ventas (Encabezado)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_factura TEXT,
            fecha TEXT,
            total REAL,
            cliente_id INTEGER
        )
    """)

    # Tabla Detalle Venta
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_venta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venta INTEGER,
            referencia TEXT,
            cantidad INTEGER,
            precio_unitario REAL,
            tipo_precio TEXT,
            subtotal REAL
        )
    """)
    
    # Tabla Compras (Encabezado)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            total REAL,
            proveedor_id INTEGER,
            numero_factura_proveedor TEXT
        )
    """)

    # Tabla Detalle Compra
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
    
# --- FUNCIONES DE FACTURACIÓN (Se mantienen igual) ---

def obtener_siguiente_factura():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT valor FROM configuracion
    WHERE clave = 'consecutivo_factura'
    """)
    
    resultado = cursor.fetchone()
    numero = int(resultado[0])

    factura = f"FAC-{numero:04d}"

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