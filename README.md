# ferreteria-pos
Sistema POS para ferretería con Python y SQLite

# estilo de bordes
"flat"     # sin borde (plano)
"raised"   # elevado (sale hacia afuera)
"sunken"   # hundido (hacia adentro)
"ridge"    # borde doble (efecto marco)
"groove"   # borde tipo ranura
"solid"    # línea simple


🔽 ACTUALIZAR PROYECTO (antes de trabajar)
git pull origin main

🔁 FLUJO COMPLETO (RECOMENDADO)

git pull origin main   # traer cambios
# haces cambios en tu código
git add .
git commit -m ""
git push origin main

🔍 VER ESTADO
git status

📜 VER HISTORIAL
git log

empaquetado
pyinstaller --windowed --onefile --add-data "..\iconos;iconos" menu.py

06_04_2026 v1.0 se modifico los archivos clientes.py, productos.py y ventas.py se limpio codigo quitando pruebas y las tablas ya no las genera aqui
                en el archivo db.py se la modifico para creara las tablas

12_04_2026 V1.1 ✔ Base de datos (SQLite)

                Tablas completas: clientes, productos, ventas, compras
                Relaciones bien definidas (FOREIGN KEY)
                Control de consecutivo de facturas automático
                Validación para evitar datos inválidos

                ✔ Módulo de ventas (ui.py)

                Interfaz completa con Tkinter
                Selección de cliente por nombre o documento
                Búsqueda y filtrado de productos
                Manejo de precios (precio1, precio2, manual)
                Validación de stock en tiempo real
                Tabla dinámica de productos vendidos
                Cálculo automático del total

                ✔ Lógica de ventas (ventas.py)

                Validación de cliente y productos
                Control de stock antes de vender
                Registro de venta y detalle en BD
                Descuento automático de inventario

                ✔ Facturación

                Número de factura automático desde BD
                Corrección de duplicados (UNIQUE)
                Flujo correcto entre UI y base de datos

                ✔ Ticket de impresión

                Diseño optimizado para impresora térmica (TM-U220D)
                Formato alineado tipo tirilla
                Espacio extra para corte manual
                Opción de imprimir copia (con flujo real: imprimir → preguntar → imprimir copia)
                Etiqueta "*** COPIA ***"

                ✔ Mejoras UX

                Atajos de teclado (F1, F2, F3, Delete)
                Reset automático de tipo de precio a precio1
                Flujo rápido tipo sistema real de tienda

13_04_2026 V1.10 se corrigieron errores de empaquetacion