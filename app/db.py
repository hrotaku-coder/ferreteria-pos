import sqlite3

def conectar():
    return sqlite3.connect("database/data.db")


def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    # TABLA CONFIGURACION
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

    conn.commit()
    conn.close()