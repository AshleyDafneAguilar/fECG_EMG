import numpy as np
import pandas as pd
from scipy import signal
from pathlib import Path
from scipy.signal import butter, filtfilt

def crear_dataset_3d(ruta_carpeta, N=8192):
    archivos = sorted(list(Path(ruta_carpeta).glob('*.csv')))
    lista_X, lista_Y = [],[]
    
    clases_asignadas =[2, 3] 
    
    for f in archivos:
        df = pd.read_csv(f)
        
        # Extraer canales EMG y etiquetas 
        datos_emg = df.iloc[:, 1:9].values
        etiquetas = df.iloc[:, 9].values 
        
        # Encontrar los puntos exactos donde la etiqueta cambia
        cambios = np.where(np.diff(etiquetas) != 0)[0] + 1
        inicios = np.insert(cambios, 0, 0)
        fines = np.append(cambios, len(etiquetas))
        
        for inicio, fin in zip(inicios, fines):
            clase_actual = etiquetas[inicio]
            
            if clase_actual in clases_asignadas:
                segmento = datos_emg[inicio:fin, :]
                
                # Homogeneizar solo este pedacito con Resampling
                segmento_norm = signal.resample(segmento, N, axis=0)
                
                lista_X.append(segmento_norm)
                lista_Y.append(clase_actual)
                
    return np.array(lista_X), np.array(lista_Y)

def aplicar_filtro_emg(datos, fs=200, low=20, high=90):
    nyq = 0.5 * fs
    b, a = butter(4, [low/nyq, high/nyq], btype='band')
    # Aplicar el filtro a lo largo del eje del tiempo 
    return filtfilt(b, a, datos, axis=1)