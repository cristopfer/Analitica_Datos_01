# Diccionario de Datos - AndinaRetail S.A.C.

## Descripción General
Este documento describe la estructura, campos y restricciones de todas las tablas 
del sistema de datos sintéticos de AndinaRetail S.A.C., una empresa de retail peruana.

---
## Tabla: tiendas

**Descripción:** Información de las tiendas físicas y virtuales de AndinaRetail.

| Campo | Tipo de Dato | Descripción | Dominio | Valores Permitidos |
|-------|--------------|-------------|---------|--------------------|
| id_tienda | INT | Identificador único de la tienda | 1 - 12 | Valores enteros consecutivos |
| nombre | VARCHAR(100) | Nombre comercial de la tienda | AndinaRetail [Ciudad] [Tipo] [N] | Formato estandarizado |
| ciudad | VARCHAR(50) | Ciudad donde se ubica la tienda | Lima, Arequipa, Trujillo, Cusco, Piura | Una de las 5 ciudades principales |
| region | VARCHAR(50) | Región geográfica | Igual que ciudad | Mismo valor que ciudad |
| tipo | VARCHAR(20) | Tipo de establecimiento | Supermercado, Hipermercado, Express, Virtual | Al menos una tienda virtual |
| area_m2 | FLOAT | Área total en metros cuadrados | 0 - 10000 | Virtual: área mínima; Hipermercado: 3000-10000 |
| fecha_apertura | DATE | Fecha de inicio de operaciones | 2015-01-01 a 2022-12-31 | Formato YYYY-MM-DD |

---

## Tabla: productos

**Descripción:** Catálogo de productos disponibles para la venta.

| Campo | Tipo de Dato | Descripción | Dominio | Valores Permitidos |
|-------|--------------|-------------|---------|--------------------|
| id_producto | INT | Identificador único del producto | 1 - 800 | Valores enteros consecutivos |
| nombre | VARCHAR(200) | Nombre descriptivo del producto | Marca + Subcategoría + Palabra | Nombre compuesto descriptivo |
| categoria | VARCHAR(50) | Categoría principal del producto | Abarrotes, Bebidas, Limpieza, Cuidado Personal, Electrohogar, Hogar | Una de las 6 categorías definidas |
| subcategoria | VARCHAR(100) | Subcategoría específica | Ver categorías | Pertenece a la categoría principal |
| marca | VARCHAR(50) | Marca del producto | Marcas peruanas e internacionales | Marca reconocida en el mercado |
| precio_lista | FLOAT | Precio de venta sugerido en soles | 2 - 5000 | Acotado por categoría |
| costo_unitario | FLOAT | Costo de adquisición del producto | 60%-80% del precio_lista | Siempre menor al precio de lista |
| fecha_alta | DATE | Fecha de incorporación al catálogo | 2020-01-01 a 2022-12-31 | Formato YYYY-MM-DD |

---

## Tabla: clientes

**Descripción:** Información de clientes registrados con comportamiento de compra.

| Campo | Tipo de Dato | Descripción | Dominio | Valores Permitidos |
|-------|--------------|-------------|---------|--------------------|
| id_cliente | INT | Identificador único del cliente | 1 - 15000 | Valores enteros consecutivos |
| nombre | VARCHAR(200) | Nombre completo del cliente | Nombres peruanos | Generados con Faker |
| edad | INT | Edad del cliente en años | 18 - 95 (con outliers controlados) | Distribución normal truncada μ=38 σ=12 |
| genero | CHAR(1) | Género del cliente | M, F | M: Masculino, F: Femenino |
| ciudad | VARCHAR(50) | Ciudad de residencia | Lima, Arequipa, Trujillo, Cusco, Piura | Una de las 5 ciudades |
| distrito | VARCHAR(100) | Distrito de residencia | Distritos válidos por ciudad | Corresponde a la ciudad |
| fecha_registro | DATE | Fecha de registro del cliente | 2020-01-01 a 2023-12-31 | Formato YYYY-MM-DD |
| canal_preferido | VARCHAR(20) | Canal de compra preferido | Tienda Física, Web, App | Canal principal de compra |
| segmento | VARCHAR(20) | Segmento de valor del cliente | Premium, Regular, Ocasional, Nuevo | Premium: 15%, Regular: 35%, Ocasional: 30%, Nuevo: 20% |

---

## Tabla: ventas

**Descripción:** Transacciones de venta realizadas en el período 2023-2025.

| Campo | Tipo de Dato | Descripción | Dominio | Valores Permitidos |
|-------|--------------|-------------|---------|--------------------|
| id_venta | INT | Identificador único de la venta | 1 - ~250000 | Valores enteros consecutivos |
| fecha | DATE | Fecha de la transacción | 2023-01-01 a 2025-12-31 | Formato YYYY-MM-DD |
| id_cliente | INT | FK a clientes.id_cliente | 1 - 15000 | Cliente existente en tabla clientes |
| id_tienda | INT | FK a tiendas.id_tienda | 1 - 12 | Tienda existente en tabla tiendas |
| id_producto | INT | FK a productos.id_producto | 1 - 800 | Producto existente en tabla productos |
| cantidad | INT | Unidades vendidas | 1 - N (con outliers) | Distribución Poisson según categoría |
| precio_unitario | FLOAT | Precio unitario de venta en soles | Variación ±5% del precio_lista | Basado en precio de lista |
| descuento_pct | FLOAT | Porcentaje de descuento aplicado | 0% - 50% | Mayor en Trujillo desde Q2-2025 |
| monto_total | FLOAT | Monto total de la venta en soles | cantidad * precio_unitario * (1 - descuento) | Calculado automáticamente |
| canal | VARCHAR(20) | Canal de venta | Tienda Física, Web, App | Digital creciente 15%→45% en el período |
| metodo_pago | VARCHAR(20) | Método de pago utilizado | Efectivo, Tarjeta, Yape, Plin, Transferencia | Distribución: 30%, 25%, 20%, 15%, 10% |

---

## Tabla: inventario

**Descripción:** Niveles de stock y costos de almacenamiento por producto y tienda.

| Campo | Tipo de Dato | Descripción | Dominio | Valores Permitidos |
|-------|--------------|-------------|---------|--------------------|
| id_producto | INT | FK a productos.id_producto | 1 - 800 | Producto existente |
| id_tienda | INT | FK a tiendas.id_tienda | 1 - 12 | Tienda existente |
| stock | INT | Unidades disponibles | 0 - N | Distribución Poisson según categoría |
| stock_minimo | INT | Punto de reorden | 20% del stock | Umbral mínimo de inventario |
| stock_maximo | INT | Capacidad máxima | 150% del stock | Límite superior de almacenamiento |
| costo_almacenamiento | FLOAT | Costo de almacenar una unidad en soles | 5%-15% del costo_unitario | Mayor en Trujillo (+30%) |
| ultima_actualizacion | DATE | Última fecha de actualización | Últimos 30 días | Formato YYYY-MM-DD |

---

## Notas Importantes

### Patrones Implementados
1. **Estacionalidad:** Julio (Fiestas Patrias) y Diciembre (Navidad) tienen incrementos del 40-100% en ventas.
2. **Crecimiento Digital:** Las ventas por canales Web/App aumentan progresivamente de 15% (2023) a 45% (2025).
3. **Caída de Margen Trujillo:** Desde Q2-2025, tiendas en Trujillo muestran mayores descuentos y costos de almacenamiento.
4. **Churn de Clientes:** Clientes sin compras en últimos 90 días del período son considerados inactivos.

### Calidad de Datos (CORREGIDO)
- **Valores Faltantes:** 1.5-3.5% de datos NaN en columnas no críticas.
- **Outliers Controlados:** Cantidades y montos extremos en ~0.1-0.3% de registros.
- **Edades Anómalas:** Máximo ~95 años por factores multiplicadores controlados.

### Relaciones
- Todas las claves foráneas son válidas y tienen integridad referencial.

### Reproducibilidad
- Semillas fijas: `numpy.random.seed(2026)`, `random.seed(2026)`, `Faker.seed(2026)`
