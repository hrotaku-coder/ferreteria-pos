import sqlite3

def conectar():                                 # Función para conectar a la base de datos
    return sqlite3.connect("database/data.db") # Cambia "data.db" por el nombre de tu base de datos

def agregar_proveedor(nombre_empresa, nit, telefono, nombre_vendedor): # Función para agregar un nuevo proveedor a la base de datos
    conn = conectar()                                                  # Conectar a la base de datos
    cursor = conn.cursor()                                             # Crear un cursor para ejecutar comandos SQL    
    
    try:
        cursor.execute("""
            INSERT INTO proveedores (nombre_empresa, nit, telefono, nombre_vendedor)
            VALUES (?, ?, ?, ?)
        """, (nombre_empresa, nit, telefono, nombre_vendedor))
        
        conn.commit()  # Guardar los cambios en la base de datos
        return True     # Retornar True para indicar que el proveedor se agregó correctamente

    except sqlite3.IntegrityError:
        return False    # Retornar False si hubo un error de integridad (por ejemplo, nit duplicado)
    
    finally:
        conn.close()    # Cerrar la conexión a la base de datos
        
def obtener_proveedores(): # Función para obtener la lista de proveedores desde la base de datos
    conn = conectar()   # Conectar a la base de datos
    cursor = conn.cursor() # Crear un cursor para ejecutar comandos SQL
    
    cursor.execute("SELECT * FROM proveedores") # Ejecutar una consulta para obtener todos los proveedores
    proveedores = cursor.fetchall() # Obtener todos los resultados de la consulta
    
    conn.close() # Cerrar la conexión a la base de datos
    return proveedores # Retornar la lista de proveedores obtenida de la base de datos

def buscar_proveedor_por_nit(nit): # Función para buscar un proveedor por su NIT
    conn = conectar()   # Conectar a la base de datos
    cursor = conn.cursor() # Crear un cursor para ejecutar comandos SQL
    
    cursor.execute("SELECT * FROM proveedores WHERE nit = ?", (nit,)) # Ejecutar una consulta para buscar el proveedor por su NIT
    proveedor = cursor.fetchone() # Obtener el primer resultado de la consulta (debería ser único debido a la restricción de NIT)
    
    conn.close() # Cerrar la conexión a la base de datos
    return proveedor # Retornar el proveedor encontrado (o None si no se encontró)