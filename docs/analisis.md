# 🧠 Análisis de Base de Datos – Ferretería

## 🎯 Objetivo del sistema

El sistema debe permitir:

* Controlar el inventario
* Registrar ventas
* Manejar entradas y salidas de productos
* Gestionar clientes y proveedores
* Generar reportes confiables

---

## 🧩 1. Entidades principales

El sistema se compone de las siguientes entidades:

* **Productos** → Elemento central del sistema
* **Clientes** → Personas o empresas que compran
* **Proveedores** → Suministran productos
* **Ventas** → Registro de transacciones
* **Compras** → Entrada de productos
* **Movimientos de inventario** → Control del stock
* **Categorías** → Clasificación de productos

---

## 🔑 2. Identificadores únicos

Cada entidad debe tener un identificador único para evitar duplicados:

* Producto → referencia única o código
* Cliente → cédula o NIT (único)
* Proveedor → NIT (único)

⚠️ Nota:

* El nombre puede repetirse
* La cédula/NIT NO puede repetirse

---

## 🔗 3. Relaciones del sistema

* Un cliente puede tener muchas ventas
* Una venta contiene varios productos
* Un producto puede estar en muchas ventas
* Un proveedor puede estar en muchas compras
* Un producto puede tener múltiples movimientos

---

## 🔄 4. Flujo del negocio

### 🟢 Venta

* Se registra la venta
* Se agregan productos vendidos
* Se descuenta el stock
* Se registra un movimiento de salida

### 🔵 Compra

* Se registra la compra
* Se agregan productos comprados
* Se aumenta el stock
* Se registra un movimiento de entrada

### 🟡 Ajustes

* Productos dañados
* Pérdidas
* Correcciones

---

## 📦 5. Control de inventario

### ✔️ Enfoque básico

Guardar stock directamente en el producto

### ✔️ Enfoque recomendado

Calcular stock con movimientos:

stock = entradas - salidas

Ventajas:

* Mayor control
* Historial completo
* Menos errores

---

## 📊 6. Reportes necesarios

* Ventas por día/mes
* Productos más vendidos
* Stock bajo
* Historial de movimientos
* Compras por proveedor

---

## ⚠️ 7. Problemas a evitar

* Productos duplicados
* Clientes repetidos
* Stock incorrecto
* Ventas sin detalle
* Falta de historial

---

## 🧠 8. Buenas prácticas

* Usar identificadores únicos
* Separar ventas y detalle de ventas
* Registrar todos los movimientos
* Evitar duplicidad de datos
* Diseñar pensando en crecimiento

---

## 🎯 Conclusión

El sistema debe garantizar:

* Control preciso del inventario
* Registro detallado de ventas y compras
* Integridad de los datos
* Capacidad de generar reportes

Una buena estructura de base de datos permite construir un sistema POS sólido, escalable y confiable.