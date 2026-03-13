import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pywt
from preprocesamiento_emg import crear_dataset_3d, aplicar_filtro_emg
from caracteristicas import extraer_tiempo, extraer_frecuencia, extraer_dwt, extraer_cwt

def main(ruta):
    # 1. Crear dataset y filtrar
    X, Y = crear_dataset_3d(ruta)
    X_limpio = aplicar_filtro_emg(X)

    data_tiempo, data_frec, data_tf = [], [], []
    
    # Inicializar contadores para graficar solo 2 instancias por clase
    contadores = {clase: 0 for clase in np.unique(Y)}

    for i in range(len(X_limpio)):
        instancia = X_limpio[i]
        clase = Y[i]
        
        # 2. Extracción de características
        tiempo = extraer_tiempo(instancia)
        frec = extraer_frecuencia(instancia)
        
        # Combinamos DWT y CWT para el dominio Tiempo-Frecuencia
        tf = np.concatenate([extraer_dwt(instancia), extraer_cwt(instancia)])
        
        # 3. Guardado en memoria
        data_tiempo.append({'Instancia': i, 'Clase': clase, **{f't{j}': v for j,v in enumerate(tiempo)}})
        data_frec.append({'Instancia': i, 'Clase': clase, **{f'f{j}': v for j,v in enumerate(frec)}})
        data_tf.append({'Instancia': i, 'Clase': clase, **{f'tf{j}': v for j,v in enumerate(tf)}})

        # 4. Graficación (Punto 2: 2 instancias por clase)
        if contadores[clase] < 2:
            idx_paciente = contadores[clase]
            contadores[clase] += 1
            
            # Gráfica Tiempo
            plt.figure(figsize=(6, 2))
            plt.plot(instancia[:, 0])
            plt.title(f'Tiempo - Clase {clase} (Instancia {idx_paciente})')
            plt.savefig(f'tiempo_c{clase}_i{idx_paciente}.png')
            plt.close()
            
            # Gráfica Frecuencia
            plt.figure(figsize=(6, 2))
            plt.magnitude_spectrum(instancia[:, 0], Fs=200)
            plt.title(f'Frecuencia - Clase {clase} (Instancia {idx_paciente})')
            plt.savefig(f'frecuencia_c{clase}_i{idx_paciente}.png')
            plt.close()

            # Gráfica Tiempo-Frecuencia (CWT)
            plt.figure(figsize=(6, 2))
            # Usamos la lógica de la transformada continua directamente para la imagen
            coeffs, _ = pywt.cwt(instancia[:, 0], np.arange(1, 65), 'cmor')
            plt.imshow(np.abs(coeffs), aspect='auto', cmap='jet')
            plt.title(f'T-F (CWT) - Clase {clase} (Instancia {idx_paciente})')
            plt.savefig(f'tf_cwt_c{clase}_i{idx_paciente}.png')
            plt.close()
            
            # Gráfica Tiempo-Frecuencia (DWT - Niveles)
            coeffs_dwt = pywt.wavedec(instancia[:, 0], 'db4', level=4)
            plt.figure(figsize=(6, 4))
            for level, c in enumerate(reversed(coeffs_dwt)):
                plt.subplot(len(coeffs_dwt), 1, level + 1)
                plt.plot(c)
                plt.title(f'DWT Nivel {len(coeffs_dwt)-level}')
            plt.tight_layout()
            plt.savefig(f'tf_dwt_c{clase}_i{idx_paciente}.png')
            plt.close()

    # 5. Generación de los 3 CSV requeridos
    pd.DataFrame(data_tiempo).to_csv('caracteristicas_tiempo.csv', index=False)
    pd.DataFrame(data_frec).to_csv('caracteristicas_frecuencia.csv', index=False)
    pd.DataFrame(data_tf).to_csv('caracteristicas_tiempo_frecuencia.csv', index=False)
    print("CSV y gráficas generados exitosamente.")
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python main_2.py <ruta_de_la_carpeta>")
        sys.exit(1)
        
    ruta = sys.argv[1]
    main(ruta)