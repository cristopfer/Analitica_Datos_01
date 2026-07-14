"""
=============================================================================
SISTEMA DE GENERACIÓN DE DATOS SINTÉTICOS - ANDINARETAIL S.A.C.
=============================================================================
Proyecto: Analítica de Datos - Datos Sintéticos para Machine Learning
Autor: Ingeniero de Datos Senior
Versión: 1.1 (Corregida)
Python: 3.11
Descripción: Script completo para la generación reproducible de datos
             sintéticos para una empresa de retail peruana.
             
CORRECCIONES APLICADAS:
- Ajuste de ventas para obtener ~250,000 registros (factor 0.90)
- Aumento de datos faltantes a 1.5-3.5%
- Control de outliers de edad (máximo ~95 años)
=============================================================================
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from pathlib import Path
from datetime import datetime, timedelta
import warnings

# Suprimir advertencias para una salida más limpia
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURACIÓN DE SEMILLAS PARA REPRODUCIBILIDAD
# =============================================================================
np.random.seed(2026)
random.seed(2026)
Faker.seed(2026)

# Inicializar Faker con manejo de errores para diferentes versiones
try:
    fake = Faker('es_PE')
except AttributeError:
    try:
        fake = Faker('es_MX')
        print("⚠️  Usando locale es_MX como alternativa")
    except AttributeError:
        fake = Faker('es')
        print("⚠️  Usando locale español genérico")

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================
DIRECTORIO_SALIDA = Path('./')

FECHA_INICIO = pd.Timestamp('2023-01-01')
FECHA_FIN = pd.Timestamp('2025-12-31')

DIAS_INACTIVIDAD_CHURN = 90

PCT_FALTANTES_MIN = 0.015  # 1.5% (CORREGIDO)
PCT_FALTANTES_MAX = 0.035  # 3.5% (CORREGIDO)

NUM_TIENDAS = 12
CIUDADES = ['Lima', 'Arequipa', 'Trujillo', 'Cusco', 'Piura']
TIPOS_TIENDA = ['Supermercado', 'Hipermercado', 'Express', 'Virtual']

NUM_PRODUCTOS = 800
CATEGORIAS_PRODUCTOS = {
    'Abarrotes': {'precio_min': 2, 'precio_max': 50},
    'Bebidas': {'precio_min': 3, 'precio_max': 80},
    'Limpieza': {'precio_min': 5, 'precio_max': 100},
    'Cuidado Personal': {'precio_min': 8, 'precio_max': 150},
    'Electrohogar': {'precio_min': 300, 'precio_max': 5000},
    'Hogar': {'precio_min': 20, 'precio_max': 500}
}

NUM_CLIENTES = 15000
EDAD_MEDIA = 38
EDAD_DESVIACION = 12
EDAD_MIN = 18
EDAD_MAX = 80

NUM_VENTAS_OBJETIVO = 250000
CANALES = ['Tienda Física', 'Web', 'App']
METODOS_PAGO = ['Efectivo', 'Tarjeta', 'Yape', 'Plin', 'Transferencia']
SEGMENTOS = ['Premium', 'Regular', 'Ocasional', 'Nuevo']

# =============================================================================
# FUNCIONES UTILITARIAS
# =============================================================================

def crear_directorio():
    """
    Verifica que el directorio de salida exista.
    No intenta borrar si es la carpeta actual.
    """
    # Si es la carpeta actual, solo verificar que existe
    if DIRECTORIO_SALIDA == Path('.'):
        print(f"✓ Usando directorio actual: {DIRECTORIO_SALIDA.absolute()}")
        return
    
    # Si es una subcarpeta, intentar limpiar
    if DIRECTORIO_SALIDA.exists():
        import shutil
        try:
            shutil.rmtree(DIRECTORIO_SALIDA)
        except PermissionError:
            print(f"⚠️  No se pudo limpiar '{DIRECTORIO_SALIDA}'. Continuando...")
    
    DIRECTORIO_SALIDA.mkdir(parents=True, exist_ok=True)
    print(f"✓ Directorio '{DIRECTORIO_SALIDA}' listo.")


def guardar_csv(dataframe, nombre_archivo):
    """Guarda un DataFrame como archivo CSV en el directorio de salida."""
    ruta = DIRECTORIO_SALIDA / nombre_archivo
    dataframe.to_csv(ruta, index=False, encoding='utf-8')
    print(f"✓ Archivo '{nombre_archivo}' guardado ({len(dataframe)} registros)")


def calcular_estacionalidad(fecha):
    """Calcula el factor de estacionalidad para una fecha dada."""
    mes = fecha.month
    
    if mes == 7:  # Julio - Fiestas Patrias
        return np.random.uniform(1.4, 1.6)
    elif mes == 12:  # Diciembre - Navidad
        return np.random.uniform(1.6, 2.0)
    else:
        return 1.0


def insertar_faltantes(dataframe, columnas_excluir=None):
    """
    Inserta valores nulos (NaN) de manera controlada en el DataFrame.
    CORREGIDO: Asegura 1.5% - 3.5% de datos faltantes.
    """
    if columnas_excluir is None:
        columnas_excluir = []
    
    columnas_candidatas = [col for col in dataframe.columns 
                          if col not in columnas_excluir 
                          and col not in ['id_tienda', 'id_producto', 'id_cliente', 'id_venta']]
    
    if not columnas_candidatas:
        return dataframe
    
    # CORREGIDO: Porcentaje ajustado para 1.5% - 3.5%
    pct_faltantes = np.random.uniform(0.015, 0.035)
    
    for columna in columnas_candidatas:
        mascara = np.random.random(len(dataframe)) < (pct_faltantes / len(columnas_candidatas))
        dataframe.loc[mascara, columna] = np.nan
    
    return dataframe


def insertar_outliers(dataframe, columna, factor_min=3, factor_max=10, pct_outliers=0.005):
    """Inserta outliers controlados multiplicando valores existentes."""
    if columna not in dataframe.columns or not pd.api.types.is_numeric_dtype(dataframe[columna]):
        return dataframe
    
    mascara = np.random.random(len(dataframe)) < pct_outliers
    num_outliers = mascara.sum()
    
    if num_outliers > 0:
        factores = np.random.uniform(factor_min, factor_max, num_outliers)
        dataframe.loc[mascara, columna] *= factores
    
    return dataframe


# =============================================================================
# GENERACIÓN DE DIMENSIONES
# =============================================================================

def generar_tiendas():
    """Genera la tabla de tiendas con 12 registros."""
    print("\n>>> Generando tiendas...")
    
    tiendas = []
    
    distribucion_ciudades = {
        'Lima': 4,
        'Arequipa': 2,
        'Trujillo': 2,
        'Cusco': 2,
        'Piura': 2
    }
    
    id_tienda = 1
    for ciudad, num_tiendas in distribucion_ciudades.items():
        for i in range(num_tiendas):
            if id_tienda == NUM_TIENDAS:
                tipo = 'Virtual'
                area = np.random.uniform(0, 50)
            elif ciudad == 'Lima' and i < 2:
                tipo = 'Hipermercado'
                area = np.random.uniform(5000, 10000)
            elif ciudad in ['Arequipa', 'Trujillo'] and i == 0:
                tipo = 'Hipermercado'
                area = np.random.uniform(3000, 7000)
            else:
                tipo = np.random.choice(['Supermercado', 'Express'], p=[0.7, 0.3])
                if tipo == 'Express':
                    area = np.random.uniform(200, 500)
                else:
                    area = np.random.uniform(1000, 3000)
            
            dias_aleatorios = np.random.randint(0, 2922)
            fecha_apertura = pd.Timestamp('2015-01-01') + pd.Timedelta(days=int(dias_aleatorios))
            
            nombre = f"AndinaRetail {ciudad} {tipo} {i+1}" if tipo != 'Virtual' else "AndinaRetail Online"
            
            tienda = {
                'id_tienda': id_tienda,
                'nombre': nombre,
                'ciudad': ciudad,
                'region': ciudad,
                'tipo': tipo,
                'area_m2': round(area, 2),
                'fecha_apertura': fecha_apertura.strftime('%Y-%m-%d')
            }
            
            tiendas.append(tienda)
            id_tienda += 1
    
    df_tiendas = pd.DataFrame(tiendas)
    print(f"  - Generadas {len(df_tiendas)} tiendas")
    return df_tiendas


def generar_productos():
    """Genera la tabla de productos con 800 registros."""
    print("\n>>> Generando productos...")
    
    productos = []
    
    subcategorias = {
        'Abarrotes': ['Arroz', 'Azúcar', 'Aceite', 'Menestras', 'Conservas', 'Pastas', 'Salsas'],
        'Bebidas': ['Gaseosas', 'Jugos', 'Aguas', 'Cervezas', 'Vinos', 'Licores', 'Energizantes'],
        'Limpieza': ['Detergentes', 'Desinfectantes', 'Limpiadores', 'Escobas', 'Trapeadores', 'Ambientadores'],
        'Cuidado Personal': ['Shampoo', 'Jabón', 'Crema Dental', 'Desodorante', 'Cuidado Facial', 'Protección Solar'],
        'Electrohogar': ['Televisores', 'Refrigeradoras', 'Lavadoras', 'Microondas', 'Licuadoras', 'Planchas'],
        'Hogar': ['Menaje', 'Decoración', 'Muebles Pequeños', 'Textil Hogar', 'Iluminación', 'Organización']
    }
    
    marcas_por_categoria = {
        'Abarrotes': ['Costeño', 'Nicolini', 'Primor', 'Valle', 'Doña Clara', 'Tondero'],
        'Bebidas': ['Coca-Cola', 'Inca Kola', 'San Mateo', 'Cusqueña', 'Pilsen', 'Red Bull'],
        'Limpieza': ['Sapolio', 'Ariel', 'Ace', 'Magia', 'Poett', 'Glade'],
        'Cuidado Personal': ['Pantene', 'Protex', 'Colgate', 'Rexona', 'Nivea', 'Esika'],
        'Electrohogar': ['Samsung', 'LG', 'Sony', 'Bosh', 'Oster', 'Philips'],
        'Hogar': ['Fantasía', 'Basement', 'Ilko', 'Ripley Home', 'Uno', 'Orange']
    }
    
    for id_producto in range(1, NUM_PRODUCTOS + 1):
        categoria = np.random.choice(
            list(CATEGORIAS_PRODUCTOS.keys()),
            p=[0.25, 0.20, 0.15, 0.15, 0.10, 0.15]
        )
        
        rango = CATEGORIAS_PRODUCTOS[categoria]
        precio_medio = (rango['precio_min'] + rango['precio_max']) / 2
        precio_lista = np.random.lognormal(
            mean=np.log(precio_medio) - 0.5,
            sigma=0.3
        )
        precio_lista = np.clip(precio_lista, rango['precio_min'], rango['precio_max'])
        precio_lista = round(precio_lista, 2)
        
        porcentaje_costo = np.random.uniform(0.60, 0.80)
        costo_unitario = round(precio_lista * porcentaje_costo, 2)
        
        subcategoria = np.random.choice(subcategorias[categoria])
        marca = np.random.choice(marcas_por_categoria[categoria])
        nombre = f"{marca} {subcategoria} {fake.word().capitalize()}"
        
        dias_aleatorios = np.random.randint(0, 1096)
        fecha_alta = pd.Timestamp('2020-01-01') + pd.Timedelta(days=int(dias_aleatorios))
        
        producto = {
            'id_producto': id_producto,
            'nombre': nombre,
            'categoria': categoria,
            'subcategoria': subcategoria,
            'marca': marca,
            'precio_lista': precio_lista,
            'costo_unitario': costo_unitario,
            'fecha_alta': fecha_alta.strftime('%Y-%m-%d')
        }
        
        productos.append(producto)
    
    df_productos = pd.DataFrame(productos)
    print(f"  - Generados {len(df_productos)} productos")
    return df_productos


def generar_clientes():
    """Genera la tabla de clientes con 15000 registros."""
    print("\n>>> Generando clientes...")
    
    edades = np.random.normal(EDAD_MEDIA, EDAD_DESVIACION, NUM_CLIENTES)
    edades = np.clip(edades, EDAD_MIN, EDAD_MAX).astype(int)
    
    generos = np.random.choice(['M', 'F'], NUM_CLIENTES, p=[0.48, 0.52])
    
    ciudades_cliente = np.random.choice(
        CIUDADES, 
        NUM_CLIENTES, 
        p=[0.45, 0.20, 0.15, 0.10, 0.10]
    )
    
    distritos_por_ciudad = {
        'Lima': ['Miraflores', 'San Isidro', 'Surco', 'La Molina', 'San Miguel', 'Lince', 
                 'Jesus María', 'Pueblo Libre', 'Magdalena', 'Barranco'],
        'Arequipa': ['Cercado', 'Cayma', 'Yanahuara', 'Paucarpata', 'Cerro Colorado'],
        'Trujillo': ['Centro', 'Vista Alegre', 'La Merced', 'El Recreo', 'Mansiche'],
        'Cusco': ['Cercado', 'San Sebastián', 'Wanchaq', 'Santiago', 'San Jerónimo'],
        'Piura': ['Centro', 'Castilla', 'Veintiséis de Octubre', 'Miraflores', 'Sullana']
    }
    
    distritos = []
    for ciudad in ciudades_cliente:
        distrito = np.random.choice(distritos_por_ciudad[ciudad])
        distritos.append(distrito)
    
    segmentos = np.random.choice(
        SEGMENTOS, 
        NUM_CLIENTES, 
        p=[0.15, 0.35, 0.30, 0.20]
    )
    
    canales_preferidos = np.random.choice(
        ['Tienda Física', 'Web', 'App'],
        NUM_CLIENTES,
        p=[0.50, 0.30, 0.20]
    )
    
    nombres = []
    for genero in generos:
        if genero == 'M':
            nombres.append(fake.name_male())
        else:
            nombres.append(fake.name_female())
    
    fechas_registro = []
    for _ in range(NUM_CLIENTES):
        dias_aleatorios = np.random.randint(0, 1096)
        fecha = pd.Timestamp('2020-01-01') + pd.Timedelta(days=int(dias_aleatorios))
        fechas_registro.append(fecha.strftime('%Y-%m-%d'))
    
    clientes = []
    for i in range(NUM_CLIENTES):
        cliente = {
            'id_cliente': i + 1,
            'nombre': nombres[i],
            'edad': edades[i],
            'genero': generos[i],
            'ciudad': ciudades_cliente[i],
            'distrito': distritos[i],
            'fecha_registro': fechas_registro[i],
            'canal_preferido': canales_preferidos[i],
            'segmento': segmentos[i]
        }
        clientes.append(cliente)
    
    df_clientes = pd.DataFrame(clientes)
    
    # CORREGIDO: Outliers de edad más controlados (máximo ~95 años)
    df_clientes = insertar_outliers(df_clientes, 'edad', factor_min=1.1, factor_max=1.3, pct_outliers=0.002)
    
    # Insertar valores faltantes
    df_clientes = insertar_faltantes(df_clientes, columnas_excluir=['id_cliente', 'nombre'])
    
    print(f"  - Generados {len(df_clientes)} clientes")
    return df_clientes


# =============================================================================
# GENERACIÓN DE HECHOS (VENTAS)
# =============================================================================

def generar_ventas(df_tiendas, df_productos, df_clientes):
    """Genera la tabla de ventas con aproximadamente 250,000 registros."""
    print("\n>>> Generando ventas (esto puede tomar unos segundos)...")
    
    dias_totales = (FECHA_FIN - FECHA_INICIO).days + 1
    # CORREGIDO: Factor 0.90 para ajustar a ~250,000 ventas
    ventas_por_dia_base = (NUM_VENTAS_OBJETIVO / dias_totales) * 0.90
    
    ventas = []
    id_venta = 1
    
    ids_tiendas = df_tiendas['id_tienda'].values
    ids_productos = df_productos['id_producto'].values
    ids_clientes = df_clientes['id_cliente'].values
    
    precios_productos = df_productos.set_index('id_producto')['precio_lista'].to_dict()
    categorias_productos = df_productos.set_index('id_producto')['categoria'].to_dict()
    
    tiendas_trujillo = df_tiendas[df_tiendas['ciudad'] == 'Trujillo']['id_tienda'].values
    tienda_virtual = df_tiendas[df_tiendas['tipo'] == 'Virtual']['id_tienda'].values[0]
    
    frecuencia_cliente = {id_cliente: 0 for id_cliente in ids_clientes}
    ultima_compra_cliente = {}
    
    fecha_actual = FECHA_INICIO
    
    while fecha_actual <= FECHA_FIN:
        factor_estacionalidad = calcular_estacionalidad(fecha_actual)
        
        ventas_dia = int(np.random.poisson(ventas_por_dia_base * factor_estacionalidad))
        ventas_dia = max(ventas_dia, 1)
        
        progreso_digital = (fecha_actual - FECHA_INICIO).days / dias_totales
        prob_canal_digital = 0.15 + (progreso_digital * 0.30)
        
        for _ in range(ventas_dia):
            id_cliente = np.random.choice(ids_clientes)
            
            if np.random.random() < prob_canal_digital:
                canal = np.random.choice(['Web', 'App'], p=[0.6, 0.4])
                if np.random.random() < 0.7:
                    id_tienda = tienda_virtual
                else:
                    id_tienda = np.random.choice(ids_tiendas[ids_tiendas != tienda_virtual])
            else:
                canal = 'Tienda Física'
                id_tienda = np.random.choice(ids_tiendas[ids_tiendas != tienda_virtual])
            
            id_producto = np.random.choice(ids_productos)
            precio_lista = precios_productos[id_producto]
            categoria = categorias_productos[id_producto]
            
            if categoria == 'Abarrotes':
                cantidad_base = np.random.poisson(3)
            elif categoria == 'Bebidas':
                cantidad_base = np.random.poisson(2)
            elif categoria == 'Electrohogar':
                cantidad_base = np.random.poisson(1)
            else:
                cantidad_base = np.random.poisson(2)
            
            cantidad = max(cantidad_base, 1)
            
            descuento_pct = np.random.triangular(0, 5, 30) / 100
            
            if (fecha_actual >= pd.Timestamp('2025-04-01') and 
                id_tienda in tiendas_trujillo):
                descuento_pct = np.random.triangular(10, 20, 40) / 100
            
            if factor_estacionalidad > 1.5:
                descuento_pct *= 1.2
            
            descuento_pct = min(descuento_pct, 0.5)
            
            precio_unitario = precio_lista * (1 + np.random.uniform(-0.05, 0.05))
            monto_total = cantidad * precio_unitario * (1 - descuento_pct)
            monto_total = round(monto_total, 2)
            precio_unitario = round(precio_unitario, 2)
            
            metodo_pago = np.random.choice(
                METODOS_PAGO,
                p=[0.30, 0.25, 0.20, 0.15, 0.10]
            )
            
            frecuencia_cliente[id_cliente] += 1
            ultima_compra_cliente[id_cliente] = fecha_actual
            
            venta = {
                'id_venta': id_venta,
                'fecha': fecha_actual.strftime('%Y-%m-%d'),
                'id_cliente': id_cliente,
                'id_tienda': id_tienda,
                'id_producto': id_producto,
                'cantidad': cantidad,
                'precio_unitario': precio_unitario,
                'descuento_pct': round(descuento_pct * 100, 2),
                'monto_total': monto_total,
                'canal': canal,
                'metodo_pago': metodo_pago
            }
            
            ventas.append(venta)
            id_venta += 1
        
        fecha_actual += timedelta(days=1)
    
    df_ventas = pd.DataFrame(ventas)
    
    df_ventas = insertar_outliers(df_ventas, 'cantidad', factor_min=5, factor_max=20, pct_outliers=0.001)
    df_ventas = insertar_outliers(df_ventas, 'monto_total', factor_min=3, factor_max=10, pct_outliers=0.002)
    
    df_ventas = insertar_faltantes(
        df_ventas, 
        columnas_excluir=['id_venta', 'fecha', 'id_cliente', 'id_tienda', 'id_producto']
    )
    
    print(f"  - Generadas {len(df_ventas)} ventas")
    return df_ventas


def generar_inventario(df_productos, df_tiendas):
    """Genera la tabla de inventario."""
    print("\n>>> Generando inventario...")
    
    inventario = []
    
    tiendas_trujillo = df_tiendas[df_tiendas['ciudad'] == 'Trujillo']['id_tienda'].values
    tienda_virtual = df_tiendas[df_tiendas['tipo'] == 'Virtual']['id_tienda'].values[0]
    
    for _, producto in df_productos.iterrows():
        id_producto = producto['id_producto']
        costo_unitario = producto['costo_unitario']
        categoria = producto['categoria']
        
        for _, tienda in df_tiendas.iterrows():
            id_tienda = tienda['id_tienda']
            
            if id_tienda == tienda_virtual:
                stock = np.random.randint(0, 10)
                stock_minimo = 0
                stock_maximo = 10
                costo_almacenamiento = 0.0
            else:
                if categoria == 'Electrohogar':
                    stock_base = np.random.poisson(5)
                elif categoria in ['Abarrotes', 'Bebidas']:
                    stock_base = np.random.poisson(50)
                else:
                    stock_base = np.random.poisson(20)
                
                stock = max(stock_base, 0)
                stock_minimo = int(stock * 0.2)
                stock_maximo = int(stock * 1.5)
                
                costo_almacenamiento = costo_unitario * np.random.uniform(0.05, 0.15)
                
                if id_tienda in tiendas_trujillo:
                    costo_almacenamiento *= 1.3
            
            dias_aleatorios = np.random.randint(0, 30)
            fecha_actualizacion = pd.Timestamp('2025-12-31') - pd.Timedelta(days=int(dias_aleatorios))
            
            registro = {
                'id_producto': id_producto,
                'id_tienda': id_tienda,
                'stock': stock,
                'stock_minimo': stock_minimo,
                'stock_maximo': stock_maximo,
                'costo_almacenamiento': round(costo_almacenamiento, 2),
                'ultima_actualizacion': fecha_actualizacion.strftime('%Y-%m-%d')
            }
            
            inventario.append(registro)
    
    df_inventario = pd.DataFrame(inventario)
    
    df_inventario = insertar_outliers(df_inventario, 'costo_almacenamiento', 
                                      factor_min=2, factor_max=5, pct_outliers=0.003)
    
    df_inventario = insertar_faltantes(df_inventario, 
                                       columnas_excluir=['id_producto', 'id_tienda'])
    
    print(f"  - Generados {len(df_inventario)} registros de inventario")
    return df_inventario


# =============================================================================
# GENERACIÓN DEL DICCIONARIO DE DATOS
# =============================================================================

def generar_diccionario():
    """Genera un archivo Markdown con la documentación del diccionario de datos."""
    print("\n>>> Generando diccionario de datos...")
    
    contenido = """# Diccionario de Datos - AndinaRetail S.A.C.

## Descripción General
Este documento describe la estructura, campos y restricciones de todas las tablas 
del sistema de datos sintéticos de AndinaRetail S.A.C., una empresa de retail peruana.

---
"""
    
    tablas = {
        'tiendas': {
            'descripcion': 'Información de las tiendas físicas y virtuales de AndinaRetail.',
            'campos': [
                ('id_tienda', 'INT', 'Identificador único de la tienda', '1 - 12', 'Valores enteros consecutivos'),
                ('nombre', 'VARCHAR(100)', 'Nombre comercial de la tienda', 'AndinaRetail [Ciudad] [Tipo] [N]', 'Formato estandarizado'),
                ('ciudad', 'VARCHAR(50)', 'Ciudad donde se ubica la tienda', 'Lima, Arequipa, Trujillo, Cusco, Piura', 'Una de las 5 ciudades principales'),
                ('region', 'VARCHAR(50)', 'Región geográfica', 'Igual que ciudad', 'Mismo valor que ciudad'),
                ('tipo', 'VARCHAR(20)', 'Tipo de establecimiento', 'Supermercado, Hipermercado, Express, Virtual', 'Al menos una tienda virtual'),
                ('area_m2', 'FLOAT', 'Área total en metros cuadrados', '0 - 10000', 'Virtual: área mínima; Hipermercado: 3000-10000'),
                ('fecha_apertura', 'DATE', 'Fecha de inicio de operaciones', '2015-01-01 a 2022-12-31', 'Formato YYYY-MM-DD')
            ]
        },
        'productos': {
            'descripcion': 'Catálogo de productos disponibles para la venta.',
            'campos': [
                ('id_producto', 'INT', 'Identificador único del producto', '1 - 800', 'Valores enteros consecutivos'),
                ('nombre', 'VARCHAR(200)', 'Nombre descriptivo del producto', 'Marca + Subcategoría + Palabra', 'Nombre compuesto descriptivo'),
                ('categoria', 'VARCHAR(50)', 'Categoría principal del producto', 'Abarrotes, Bebidas, Limpieza, Cuidado Personal, Electrohogar, Hogar', 'Una de las 6 categorías definidas'),
                ('subcategoria', 'VARCHAR(100)', 'Subcategoría específica', 'Ver categorías', 'Pertenece a la categoría principal'),
                ('marca', 'VARCHAR(50)', 'Marca del producto', 'Marcas peruanas e internacionales', 'Marca reconocida en el mercado'),
                ('precio_lista', 'FLOAT', 'Precio de venta sugerido en soles', '2 - 5000', 'Acotado por categoría'),
                ('costo_unitario', 'FLOAT', 'Costo de adquisición del producto', '60%-80% del precio_lista', 'Siempre menor al precio de lista'),
                ('fecha_alta', 'DATE', 'Fecha de incorporación al catálogo', '2020-01-01 a 2022-12-31', 'Formato YYYY-MM-DD')
            ]
        },
        'clientes': {
            'descripcion': 'Información de clientes registrados con comportamiento de compra.',
            'campos': [
                ('id_cliente', 'INT', 'Identificador único del cliente', '1 - 15000', 'Valores enteros consecutivos'),
                ('nombre', 'VARCHAR(200)', 'Nombre completo del cliente', 'Nombres peruanos', 'Generados con Faker'),
                ('edad', 'INT', 'Edad del cliente en años', '18 - 95 (con outliers controlados)', 'Distribución normal truncada μ=38 σ=12'),
                ('genero', 'CHAR(1)', 'Género del cliente', 'M, F', 'M: Masculino, F: Femenino'),
                ('ciudad', 'VARCHAR(50)', 'Ciudad de residencia', 'Lima, Arequipa, Trujillo, Cusco, Piura', 'Una de las 5 ciudades'),
                ('distrito', 'VARCHAR(100)', 'Distrito de residencia', 'Distritos válidos por ciudad', 'Corresponde a la ciudad'),
                ('fecha_registro', 'DATE', 'Fecha de registro del cliente', '2020-01-01 a 2023-12-31', 'Formato YYYY-MM-DD'),
                ('canal_preferido', 'VARCHAR(20)', 'Canal de compra preferido', 'Tienda Física, Web, App', 'Canal principal de compra'),
                ('segmento', 'VARCHAR(20)', 'Segmento de valor del cliente', 'Premium, Regular, Ocasional, Nuevo', 'Premium: 15%, Regular: 35%, Ocasional: 30%, Nuevo: 20%')
            ]
        },
        'ventas': {
            'descripcion': 'Transacciones de venta realizadas en el período 2023-2025.',
            'campos': [
                ('id_venta', 'INT', 'Identificador único de la venta', '1 - ~250000', 'Valores enteros consecutivos'),
                ('fecha', 'DATE', 'Fecha de la transacción', '2023-01-01 a 2025-12-31', 'Formato YYYY-MM-DD'),
                ('id_cliente', 'INT', 'FK a clientes.id_cliente', '1 - 15000', 'Cliente existente en tabla clientes'),
                ('id_tienda', 'INT', 'FK a tiendas.id_tienda', '1 - 12', 'Tienda existente en tabla tiendas'),
                ('id_producto', 'INT', 'FK a productos.id_producto', '1 - 800', 'Producto existente en tabla productos'),
                ('cantidad', 'INT', 'Unidades vendidas', '1 - N (con outliers)', 'Distribución Poisson según categoría'),
                ('precio_unitario', 'FLOAT', 'Precio unitario de venta en soles', 'Variación ±5% del precio_lista', 'Basado en precio de lista'),
                ('descuento_pct', 'FLOAT', 'Porcentaje de descuento aplicado', '0% - 50%', 'Mayor en Trujillo desde Q2-2025'),
                ('monto_total', 'FLOAT', 'Monto total de la venta en soles', 'cantidad * precio_unitario * (1 - descuento)', 'Calculado automáticamente'),
                ('canal', 'VARCHAR(20)', 'Canal de venta', 'Tienda Física, Web, App', 'Digital creciente 15%→45% en el período'),
                ('metodo_pago', 'VARCHAR(20)', 'Método de pago utilizado', 'Efectivo, Tarjeta, Yape, Plin, Transferencia', 'Distribución: 30%, 25%, 20%, 15%, 10%')
            ]
        },
        'inventario': {
            'descripcion': 'Niveles de stock y costos de almacenamiento por producto y tienda.',
            'campos': [
                ('id_producto', 'INT', 'FK a productos.id_producto', '1 - 800', 'Producto existente'),
                ('id_tienda', 'INT', 'FK a tiendas.id_tienda', '1 - 12', 'Tienda existente'),
                ('stock', 'INT', 'Unidades disponibles', '0 - N', 'Distribución Poisson según categoría'),
                ('stock_minimo', 'INT', 'Punto de reorden', '20% del stock', 'Umbral mínimo de inventario'),
                ('stock_maximo', 'INT', 'Capacidad máxima', '150% del stock', 'Límite superior de almacenamiento'),
                ('costo_almacenamiento', 'FLOAT', 'Costo de almacenar una unidad en soles', '5%-15% del costo_unitario', 'Mayor en Trujillo (+30%)'),
                ('ultima_actualizacion', 'DATE', 'Última fecha de actualización', 'Últimos 30 días', 'Formato YYYY-MM-DD')
            ]
        }
    }
    
    for nombre_tabla, info in tablas.items():
        contenido += f"## Tabla: {nombre_tabla}\n\n"
        contenido += f"**Descripción:** {info['descripcion']}\n\n"
        contenido += "| Campo | Tipo de Dato | Descripción | Dominio | Valores Permitidos |\n"
        contenido += "|-------|--------------|-------------|---------|--------------------|\n"
        
        for campo in info['campos']:
            contenido += f"| {campo[0]} | {campo[1]} | {campo[2]} | {campo[3]} | {campo[4]} |\n"
        
        contenido += "\n---\n\n"
    
    contenido += """## Notas Importantes

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
"""
    
    ruta = DIRECTORIO_SALIDA / 'data_dictionary.md'
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"✓ Diccionario de datos guardado en '{ruta}'")


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """Función principal que orquesta la generación de todos los datos."""
    print("=" * 70)
    print("  GENERADOR DE DATOS SINTÉTICOS - ANDINARETAIL S.A.C.")
    print("  VERSIÓN CORREGIDA 1.1")
    print("=" * 70)
    print(f"  Semillas fijadas para reproducibilidad")
    print(f"  Período: {FECHA_INICIO.strftime('%Y-%m-%d')} a {FECHA_FIN.strftime('%Y-%m-%d')}")
    print(f"  Directorio de salida: {DIRECTORIO_SALIDA}")
    print(f"  Ajustes: Ventas ~250K | Faltantes 1.5-3.5% | Edad máx ~95")
    print("=" * 70)
    
    crear_directorio()
    
    df_tiendas = generar_tiendas()
    df_productos = generar_productos()
    df_clientes = generar_clientes()
    
    df_ventas = generar_ventas(df_tiendas, df_productos, df_clientes)
    df_inventario = generar_inventario(df_productos, df_tiendas)
    
    print("\n>>> Guardando archivos CSV...")
    guardar_csv(df_tiendas, 'tiendas.csv')
    guardar_csv(df_productos, 'productos.csv')
    guardar_csv(df_clientes, 'clientes.csv')
    guardar_csv(df_ventas, 'ventas.csv')
    guardar_csv(df_inventario, 'inventario.csv')
    
    generar_diccionario()
    
    print("\n" + "=" * 70)
    print("  GENERACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print(f"  📁 Directorio: {DIRECTORIO_SALIDA.absolute()}")
    print(f"  📊 Archivos generados:")
    print(f"     - tiendas.csv       ({len(df_tiendas)} registros)")
    print(f"     - productos.csv     ({len(df_productos)} registros)")
    print(f"     - clientes.csv      ({len(df_clientes)} registros)")
    print(f"     - ventas.csv        ({len(df_ventas)} registros)")
    print(f"     - inventario.csv    ({len(df_inventario)} registros)")
    print(f"     - data_dictionary.md")
    print("=" * 70)


if __name__ == "__main__":
    import time
    
    tiempo_inicio = time.time()
    main()
    tiempo_total = time.time() - tiempo_inicio
    print(f"\n⏱️  Tiempo total de ejecución: {tiempo_total:.2f} segundos")
    print("✅ Listo para usar en proyecto de Analítica de Datos\n")