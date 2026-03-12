# Práctica U1-1. De bioseñales a características

**Materia / Docente:** Dr. Alejandro Antonio Torres García

Este repositorio contiene la implementación de la **Práctica U1-1**, enfocada en el análisis, preprocesamiento y extracción de características de bioseñales desarrollados en Python. Se encuentra dividida en dos objetivos principales: el procesamiento del Electrocardiograma Fetal (fECG) y el procesamiento y extracción sobre señales de Electromiografía (EMG).

## Descripción General del Proyecto

El proyecto se divide metodológicamente en las siguientes dos partes:

1. **Análisis de Electrocardiograma Fetal (fECG)**: 
   A partir de registros de las señales del vientre y tórax materno proveídos en `newDataset.mat`, se identifican los mejores canales y se aplican filtros adaptativos (LMS, NLMS, RLS) para extraer de forma aislada la señal del corazón del feto frente a interferencias anatómicas, analizando las anomalías presentes. Esta lógica es orquestada en `main_1.py` y el módulo de `filtros.py`.

2. **Procesamiento de Electromiografía (EMG)**: 
   Con base en el dataset capturado mediante una banda Myo ("EMG_SUJETO10"), el código agrupa las instancias y distintos canales de movimiento en arreglos `3D` (homogeneizando las muestras por instancia usando la duración del movimiento). Posteriormente, aplica un preprocesamiento lógico, seguido de la estructuración de extracción de características en los dominios de: Tiempo, Frecuencia y Tiempo-Frecuencia mediante los métodos pertinentes. Toda esta lógica está conformada alrededor de `main_2.py` para generar tres archivos `.csv` limpios y gráficos correspondientes.

### Asignaciones Específicas de la Práctica 

![Clases del dataset](clases.png)

De acuerdo con las instrucciones de la práctica y la distribución de subconjuntos de datos, las siguientes métricas delimitan los scripts y actividades implementadas considerando mis asignaciones:

*   **Responsable del Entregable:** Ashley
*   **Carpeta a Analizar (EMG):** Carpeta `Dia1`.
*   **Clases Asignadas a Comparar:** `Clase 2` y `Clase 3`.
*   **Extracción de Características (Dominio Tiempo-Frecuencia):**
    *   **DWT (Transformada Wavelet Discreta):** 
    *   **CWT (Transformada Wavelet Continua):** 

Estas asignaciones se ven claramente reflejadas en las implementaciones construidas en `main_2.py` así como las características extraídas dentro del módulo `caracteristicas.py`.

---

## Modo de Uso (Ejecución de Scripts)

### Requisitos Previos

El proyecto cuenta con manejador de dependencias provisto de `uv` (según su configuración nativa con `pyproject.toml`). Si no posees `uv` podrás ejecutar los scripts de forma habitual con `python`, asumiendo que el entorno posea las dependencias del proyecto (`numpy`, `pandas`, `matplotlib`, `pywt`, etc.).

### 1. Ejecución de la Parte 1 (Análisis fECG)

El script utilizará el archivo `.mat` proporcionado por el profesor como argumento. Éste procesará, visualizará y demostrará gráficamente el aislamiento del fECG.

```bash
uv run main_1.py newDataset.mat
# Alternativa:
# python main_1.py newDataset.mat
```

### 2. Ejecución de la Parte 2 (Extracción de Características EMG)

Para el análisis de la electromiografía (segunda mitad de la práctica), deberás apuntar el script a la carpeta del día asignado (`dataset_dia1`). Se extraerán características en cada dominio por instancia, graficará 2 instancias por clase de forma visual y exportará todo a formato CSV.

```bash
uv run main_2.py dataset_dia1
# Alternativa: 
# python main_2.py dataset_dia1
```

Tras culminar, verificarás que se crearon exitosamente 3 archivos principales:
- `caracteristicas_tiempo.csv`
- `caracteristicas_frecuencia.csv`
- `caracteristicas_tiempo_frecuencia.csv`

### 3. Análisis de Relevancia (Clase 2 vs Clase 3)

Una vez obtenidas las características anteriores, se efectúa un análisis (matemático, estadístico o gráfico) que nos permite determinar en qué características se observan diferencias altamente significativas entre nuestras clases (`2` y `3`). Para verificar el método y la explicación visual seleccionada, ejectuta el de análisis referenciado en el repositorio.

```bash
uv run analisis_diferencias.py
```
