## Prompt para generación de datos sintéticos
Actúa como un Ingeniero de Datos Senior, Científico de Datos y Desarrollador Python con experiencia en generación de datos sintéticos para proyectos de analítica de datos y machine learning.

Tu objetivo es generar un único script compatible con Python 3.11 que produzca un conjunto completo de datos sintéticos para una empresa ficticia llamada "AndinaRetail S.A.C.", siguiendo estrictamente los requisitos descritos.

===========================
OBJETIVO
===========================

Generar un sistema completamente reproducible que cree automáticamente los archivos CSV necesarios para un proyecto universitario de Analítica de Datos.

El código debe ser limpio, modular, comentado y seguir buenas prácticas de programación.
No debes generar los CSV manualmente.
Debes generar un único archivo llamado:
generar_datos.py
que al ejecutarse cree automáticamente todos los archivos.

===========================
LIBRERÍAS
===========================

Utiliza únicamente:

- pandas
- numpy
- Faker (locale='es_PE')
- random
- pathlib
- datetime

No utilizar bases de datos.

===========================
REPRODUCIBILIDAD
===========================

Fijar obligatoriamente las semillas:

numpy.random.seed(2026)
random.seed(2026)
Faker.seed(2026)

El script debe generar exactamente los mismos datos cada vez que sea ejecutado.

===========================
ESTRUCTURA DEL CÓDIGO
===========================

Organiza el código utilizando funciones independientes.

Como mínimo:

crear_directorio()
generar_tiendas()
generar_productos()
generar_clientes()
generar_ventas()
generar_inventario()
insertar_faltantes()
insertar_outliers()
guardar_csv()
generar_diccionario()
main()

Todo el código debe estar ampliamente comentado.

===========================
SALIDA
===========================

Crear automáticamente una carpeta llamada

datos/
Dentro de ella guardar:

tiendas.csv
productos.csv
clientes.csv
ventas.csv
inventario.csv
data_dictionary.md

===========================
TABLAS
===========================

1. tiendas.csv

12 tiendas

Campos:

id_tienda
nombre
ciudad
region
tipo
area_m2
fecha_apertura
Ciudades:

Lima
Arequipa
Trujillo
Cusco
Piura

Debe existir al menos una tienda virtual.

===========================

2. productos.csv

800 productos

Campos

id_producto
nombre
categoria
subcategoria
marca
precio_lista
costo_unitario
fecha_alta

Categorías:

Abarrotes
Bebidas
Limpieza
Cuidado Personal
Electrohogar
Hogar

El costo_unitario debe representar entre el 60% y 80% del precio_lista.
Los precios deben ser coherentes según la categoría.

Ejemplo:

Electrohogar:
S/300 - S/5000

Abarrotes:
S/2 - S/50

===========================

3. clientes.csv

15000 clientes

Campos:

id_cliente
nombre
edad
genero
ciudad
distrito
fecha_registro
canal_preferido
segmento

Edad: Distribución normal

Media = 38
Desviación = 12
Truncada entre 18 y 80 años.

Los nombres deben ser completamente ficticios utilizando Faker.

===========================

4. ventas.csv

Aproximadamente 250000 registros

Periodo: 2023-01-01 hasta 2025-12-31

Campos

id_venta
fecha
id_cliente
id_tienda
id_producto
cantidad

precio_unitario
descuento_pct
monto_total
canal
metodo_pago

Métodos de pago:

Efectivo
Tarjeta
Yape
Plin
Transferencia

===========================
RELACIONES
===========================

Todas las claves foráneas deben ser válidas.
Todo id_cliente debe existir.
Todo id_producto debe existir.
Todo id_tienda debe existir.
No debe existir ninguna referencia inválida.

===========================
PATRONES OBLIGATORIOS
===========================

Implementar obligatoriamente los siguientes patrones.

1. Estacionalidad. Julio y diciembre deben tener incrementos importantes de ventas.

2. Canal digital. El porcentaje de ventas Web y App debe aumentar progresivamente desde 2023 hasta 2025.

3. Caída del margen. Desde el segundo trimestre de 2025:

Las tiendas de Trujillo deben presentar:

mayor descuento
mayor costo de almacenamiento
menor margen.

4. Churn.

Un cliente será considerado inactivo cuando no compre durante los últimos 90 días del periodo.
La probabilidad de abandono debe aumentar cuando:

su frecuencia histórica sea baja
su última compra sea antigua.
Este patrón debe ser suficientemente fuerte para que posteriormente un modelo Random Forest o Gradient Boosting pueda aprenderlo.

5. Demanda.

La cantidad vendida debe depender de:

categoría
mes
canal
descuento
agregando únicamente ruido aleatorio moderado.

===========================
DATOS SUCIOS
===========================

Agregar entre 1% y 3% de valores faltantes en diferentes columnas. Agregar outliers controlados.

Ejemplos:

cantidades extremadamente altas
precios muy elevados
edades anómalas únicamente cuando tenga sentido.

===========================
REALISMO
===========================

Los datos deben parecer reales. No utilizar distribuciones completamente uniformes.

Preferir:

Normal
Poisson
Lognormal
Triangular

cuando corresponda.

===========================
RENDIMIENTO
===========================

Optimizar el código para generar aproximadamente 250000 registros rápidamente.
Preferir operaciones vectorizadas de NumPy y pandas.
Evitar bucles innecesarios.

===========================
DICCIONARIO DE DATOS
===========================

Generar automáticamente un archivo

data_dictionary.md

que describa para cada tabla:

nombre
campo
tipo de dato
descripción
dominio
valor permitido

===========================
CALIDAD DEL CÓDIGO
===========================

Aplicar buenas prácticas.
PEP8.
Variables descriptivas.
Funciones pequeñas.
Código reutilizable.
Comentarios explicativos.
No generar código redundante.

===========================
SALIDA ESPERADA
===========================

La respuesta debe contener únicamente el código completo del archivo generar_datos.py.
No omitir ninguna función.
No dejar código incompleto.
No utilizar pseudocódigo.
Todo debe ser completamente funcional y ejecutable en Python 3.11.

## PROMPT PARA NOTEBOOK ESTADÍSTICO

Actúa como un Científico de Datos Senior y Analista Estadístico experto en Python para analítica de negocios.

Tu tarea es generar un notebook completo en Python (formato Jupyter Notebook .ipynb) para la empresa ficticia "AndinaRetail S.A.C.", utilizando el dataset sintético previamente generado.

===========================
OBJETIVO DEL NOTEBOOK
===========================

Realizar un análisis estadístico completo del negocio utilizando técnicas de estadística descriptiva e inferencial, con enfoque en toma de decisiones empresariales.

El notebook debe ser profesional, estructurado, con markdown explicativo y código optimizado.

===========================
DATASET DE ENTRADA
===========================

El notebook debe asumir la existencia de los siguientes archivos en la carpeta /datos:

- ventas.csv
- clientes.csv
- productos.csv
- tiendas.csv
- inventario.csv

Debe realizar joins cuando sea necesario.

===========================
LIBRERÍAS OBLIGATORIAS
===========================

- pandas
- numpy
- scipy.stats
- matplotlib.pyplot
- seaborn
- statsmodels.api

Opcional:
- warnings (para limpiar outputs)

===========================
ESTRUCTURA DEL NOTEBOOK
===========================

El notebook debe estar dividido en secciones claras con Markdown:

# 1. Carga de datos
- Importación de librerías
- Lectura de CSV
- Merge de tablas si es necesario
- Revisión de estructura (shape, info, head)

# 2. Exploración inicial de datos
- Tipos de datos
- Valores nulos
- Duplicados
- Outliers preliminares (boxplot)

# 3. Estadística descriptiva
Calcular para variables clave:

- monto_total
- cantidad
- precio_unitario
- edad (clientes)
- ticket promedio por cliente

Incluir:

- media
- mediana
- moda
- desviación estándar
- varianza
- rango
- IQR
- asimetría (skewness)
- curtosis

Interpretar brevemente cada resultado en lenguaje de negocio.

# 4. Visualización de datos

Generar y explicar:

- histogramas (distribución de ventas, ticket)
- boxplots (outliers en ventas y precios)
- scatter plot (descuento vs cantidad)
- heatmap de correlación
- violin plots si es necesario

Cada gráfico debe tener interpretación.

# 5. Análisis de correlación

Calcular:

- correlación de Pearson
- correlación de Spearman

Entre:

- descuento vs cantidad
- precio_unitario vs cantidad
- monto_total vs descuento

Interpretar fuerza de relación usando escala:

0.00–0.19 muy débil
0.20–0.39 débil
0.40–0.59 moderada
0.60–0.79 fuerte
0.80–1.00 muy fuerte

# 6. Estadística inferencial (OBLIGATORIO)

Realizar al menos 3 pruebas:

## 6.1 t-test
Comparar ticket promedio entre:

- canal Tienda vs Web/App

## 6.2 ANOVA
Comparar monto_total entre ciudades:

- Lima, Arequipa, Trujillo, Cusco, Piura

## 6.3 Chi-cuadrado
Asociación entre:

- categoria de producto vs metodo_pago

===========================
IMPORTANTE EN PRUEBAS
===========================

Para cada prueba debes:

1. Formular H0 y H1
2. Verificar supuestos (normalidad si aplica)
3. Calcular estadístico y p-value
4. Decidir con α = 0.05
5. Interpretar en contexto de negocio

===========================
7. Intervalos de confianza
===========================

Calcular intervalos de confianza al 95% para:

- ticket promedio
- monto_total promedio

Interpretar qué significa en negocio.

===========================
8. CONCLUSIONES DE NEGOCIO
===========================

El notebook debe terminar con conclusiones claras como:

- comportamiento de clientes
- diferencias entre canales
- impacto del descuento en ventas
- insights accionables para la empresa

NO deben ser conclusiones técnicas solamente, sino decisiones de negocio.

===========================
REGLAS IMPORTANTES
===========================

- No usar datos reales
- No omitir interpretaciones
- No entregar solo código: debe incluir explicación
- Evitar gráficos sin análisis
- Debe ser reproducible
- Debe parecer un informe profesional para una empresa real

===========================
SALIDA ESPERADA
===========================

Devuelve únicamente el contenido completo del notebook en formato JSON de Jupyter (.ipynb), listo para ser ejecutado.

## PROMPT MODELO DESCRIPTIVO Y DIAGNÓSTICO

Actúa como un Científico de Datos Senior, Analista de Negocios y Especialista en Business Intelligence con amplia experiencia en analítica descriptiva, analítica diagnóstica, minería de datos y segmentación de clientes mediante Machine Learning.

Debes desarrollar un notebook profesional llamado:

02_descriptivo_diagnostico.ipynb compatible con Python 3.11 y Jupyter Notebook.

El notebook debe estar completamente documentado mediante celdas Markdown, contener explicaciones de negocio, interpretación de resultados y código limpio siguiendo PEP8. No debes omitir pasos.

=========================================================
OBJETIVO
=========================================================

Realizar un análisis descriptivo y diagnóstico completo de la empresa ficticia "AndinaRetail S.A.C." utilizando los datos sintéticos generados previamente.

El objetivo NO es únicamente generar gráficos.

El objetivo es responder:

• ¿Qué ocurrió?
• ¿Por qué ocurrió?
• ¿Qué segmentos existen?
• ¿Qué productos generan mayor valor?
• ¿Qué clientes generan mayor valor?
• ¿Qué factores explican la caída del margen?
• ¿Qué acciones debería tomar la gerencia?

=========================================================
DATASET
=========================================================

Utilizar los siguientes archivos:

datos/

ventas.csv
clientes.csv
productos.csv
tiendas.csv
inventario.csv
Realizar los joins necesarios para construir un DataFrame analítico.

=========================================================
LIBRERÍAS
=========================================================

Utilizar únicamente:

pandas
numpy
matplotlib
seaborn
scipy
statsmodels
scikit-learn
StandardScaler
KMeans
PCA
silhouette_score
warnings
collections

=========================================================
ESTRUCTURA DEL NOTEBOOK
=========================================================

# 1. Introducción

Explicar brevemente:

• Analítica descriptiva
• Analítica diagnóstica
• Objetivo del notebook

=========================================================

# 2. Carga de datos

Importar librerías
Leer CSV
Verificar tipos
Verificar dimensiones
Merge de tablas
Mostrar primeras filas

=========================================================

# 3. Perfilado rápido

Mostrar:

shape
info()
describe()
nulos
duplicados
tipos
consistencia

=========================================================

# 4. SERIES DE TIEMPO

Construir series temporales mensuales.

Analizar:

Ventas
Margen
Cantidad
Ingresos

Realizar análisis por:

• canal
• ciudad
• categoría

=========================================================

Visualizaciones

Línea mensual
Área
Heatmap mensual
Comparaciones por canal

=========================================================

=========================================================
DESCOMPOSICIÓN DE SERIES
=========================================================

Aplicar

seasonal_decompose()
utilizando periodo=12.

Mostrar:

Serie original
Tendencia
Estacionalidad
Residuo
Interpretar cada componente.
Explicar qué significa para el negocio.

=========================================================

=========================================================
AUTOCORRELACIÓN
=========================================================

Calcular ACF.
Mostrar gráfico.

Interpretar:
si existen patrones repetitivos
si existe estacionalidad
qué lags son importantes

=========================================================

=========================================================
ANÁLISIS DE PARETO
=========================================================

Aplicar regla 80/20 para:

Productos
Clientes
Categorías

Mostrar:

Gráfico Pareto
Curva acumulada
Tabla resumen

Responder:

¿Qué porcentaje de productos genera el 80% de las ventas?
¿Qué porcentaje de clientes genera el 80% de los ingresos?
¿Qué categorías concentran mayor facturación?

=========================================================

=========================================================
ANÁLISIS RFM
=========================================================

Calcular:

Recency
Frequency
Monetary

Usar como fecha de referencia:

31/12/2025
Construir tabla RFM.
Calcular quintiles.

Asignar puntajes:

1-5
Crear código RFM.

Clasificar automáticamente clientes como:

Champions
Leales
Potenciales
Prometedores
En riesgo
Perdidos
Nuevos
Dormidos

Mostrar:

Tabla resumen
Cantidad de clientes
Ingreso por segmento
Ticket promedio
Frecuencia promedio
Interpretar cada segmento.
Proponer acciones comerciales.

=========================================================

=========================================================
CLUSTERING
=========================================================

Aplicar StandardScaler.
Utilizar únicamente variables:
Recency
Frequency
Monetary

=========================================================

Determinar número óptimo de clusters mediante:
Método del Codo
Silhouette Score
Seleccionar automáticamente el mejor K.

=========================================================

Aplicar: KMeans

=========================================================

Mostrar:

Centroides
Cantidad por cluster
Características
Interpretación

=========================================================

=========================================================
PCA
=========================================================

Reducir dimensiones mediante:
PCA (2 componentes)

Mostrar:

Varianza explicada
Scatter Plot
Clusters coloreados
Interpretar la separación entre grupos.

=========================================================

=========================================================
ANÁLISIS DIAGNÓSTICO
=========================================================

Investigar la caída del margen.
Realizar Drill-down por:

Ciudad
Mes
Categoría
Canal

=========================================================

Analizar:

Precio promedio
Descuento promedio
Costo
Margen
Mix de productos

=========================================================

Comparar:
Antes de 2025-Q2
Después de 2025-Q2
Especial atención a: Trujillo

=========================================================

Construir tablas comparativas.
Visualizar diferencias.
Explicar claramente: Qué factor produjo la caída del margen.

=========================================================

=========================================================
COHORTES
=========================================================

Realizar análisis de cohortes.

Agrupar clientes por: Mes de primera compra.
Calcular:

Retención
Ingresos
Frecuencia
Mostrar heatmap.
Interpretar.

=========================================================

=========================================================
KPIs
=========================================================

Calcular como mínimo:
Ventas Totales
Margen Total
Margen %
Ticket Promedio
Ingreso Promedio Cliente
Clientes Activos
Clientes Inactivos
Frecuencia Promedio

=========================================================

=========================================================
INSIGHTS
=========================================================

Cada gráfico debe incluir una interpretación.
Cada análisis debe terminar con:
Insight
Impacto
Acción recomendada

=========================================================

=========================================================
CONCLUSIONES GERENCIALES
=========================================================

Redactar al menos 12 conclusiones.

Deben responder preguntas como:

¿Qué ocurrió?
¿Por qué ocurrió?
¿Qué clientes son estratégicos?
¿Qué clientes deben recuperarse?
¿Qué categorías deben potenciarse?
¿Qué ciudades requieren intervención?
¿Qué productos generan mayor rentabilidad?
¿Qué canal está creciendo?
¿Qué estrategias comerciales se recomiendan?

=========================================================
CALIDAD DEL CÓDIGO
=========================================================

Seguir PEP8.
No repetir código.
Crear funciones reutilizables cuando sea conveniente.
Agregar comentarios.
Separar claramente cada sección.

=========================================================
VISUALIZACIONES
=========================================================

Todas deben tener:

Título
Etiquetas
Leyenda
Tamaño adecuado
Interpretación posterior.

=========================================================
RESULTADO ESPERADO
=========================================================

Generar el notebook completo listo para ejecutar.
No utilizar pseudocódigo.
No dejar secciones incompletas.
No omitir interpretaciones.
No devolver únicamente código.
Cada bloque debe estar acompañado de explicaciones en Markdown.
El notebook debe tener calidad suficiente para ser presentado como informe universitario profesional.