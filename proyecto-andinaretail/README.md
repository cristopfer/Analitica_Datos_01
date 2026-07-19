# Caso Integrador de Analítica de Datos - AndinaRetail S.A.C.

| Rol | Integrante |
|------|----------------|
| Líder de proyecto / Data PM | Guia Muñoz, Wilfredo |
| Ingeniero de datos | Perez Bazan, Eysen Christopher |
| Analista estadístico / descriptivo | Perez Bazan, Eysen Christopher |
| Científico de datos | Guia Muñoz, Wilfredo / Ames Camayo, Daniel |
| Analista de optimización / BI | Huaman Ortiz, Emerson Raul |

## Guía de ejecución

Ejecute los siguientes archivos en el orden indicado, ya que cada etapa utiliza los resultados generados por la anterior.

### 1. `generar_datos.py`
Genera de forma reproducible el conjunto de datos sintéticos del proyecto utilizando una semilla fija. El script crea las tablas requeridas para el análisis y sirve como punto de partida para todas las etapas posteriores.

### 2. `01_estadistica.ipynb`
Realiza la exploración inicial del conjunto de datos, calcula estadísticas descriptivas, analiza correlaciones y valida hipótesis mediante pruebas estadísticas para comprender las características del negocio.

### 3. `02_descriptivo_diagnostico.ipynb`
Analiza el comportamiento histórico de las ventas y clientes mediante series de tiempo, análisis de Pareto, segmentación y diagnóstico de indicadores para identificar patrones y oportunidades de mejora.

### 4. `03_predictivo.ipynb`
Preprocesa los datos, entrena modelos de regresión y clasificación, optimiza hiperparámetros y evalúa el desempeño de los modelos para predecir el comportamiento futuro del negocio.

### 5. `04_prescriptivo.ipynb`
Implementa modelos de optimización y análisis de escenarios para generar recomendaciones que permitan mejorar la toma de decisiones a partir de los resultados predictivos.

### 6. `05_dashboard.pbix`
Integra los resultados obtenidos en las etapas anteriores en un tablero interactivo de Power BI, permitiendo visualizar indicadores clave y facilitar el análisis para la toma de decisiones.
