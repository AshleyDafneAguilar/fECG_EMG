import sys
import numpy as np
import pandas as pd

from dataset import read_dataset, plot_dataset
from filtros import lms_filter, nlms_filter, rls_filter, plot_filtros
from analisis import encontrar_mejor_pareja


def main(ruta):
    # 1. Lectura y Visualización
    df, time = read_dataset(ruta)
    plot_dataset(df, time, 'señales_original', 'Señales Originales: Tórax materno y Vientre materno')

    # 2. Análisis y División 
    tipo_senal = {'Canal_1': 'vientre', 'Canal_2': 'vientre', 'Canal_3': 'vientre',
                  'Canal_4': 'vientre', 'Canal_5': 'vientre', 'Canal_6': 'torax',
                  'Canal_7': 'torax', 'Canal_8': 'torax'}
    
    cols_vientre = [canal for canal, tipo in tipo_senal.items() if tipo == 'vientre']
    cols_torax = [canal for canal, tipo in tipo_senal.items() if tipo == 'torax']
    
    df_vientre = df[cols_vientre]
    df_torax = df[cols_torax]
    
    df_vientre.to_csv('dataset_vientre.csv', index=False)
    df_torax.to_csv('dataset_torax.csv', index=False)

    plot_dataset(df_vientre, time, 'señales_vientre', 'Señales del Vientre Materno')
    plot_dataset(df_torax, time, 'señales_torax', 'Señales del Tórax Materno')

    # 3. Análisis
    df_corr = encontrar_mejor_pareja(df_vientre, df_torax)
    mejor_pareja = df_corr.iloc[0]
    print(mejor_pareja)
    
    # 4. Filtros
    d = df_vientre[mejor_pareja['Vientre']].values
    x = df_torax[mejor_pareja['Torax']].values
    x = x / np.max(np.abs(x))
    
    fECG_lms  = lms_filter(d, x, mu=0.1, order=56)
    fECG_nlms = nlms_filter(d, x, mu=0.1, order=56)
    fECG_rls  = rls_filter(d, x, lam=0.99, delta=0.1, order=56)


    # 5. Visualización
    plot_filtros(time, d, fECG_lms, fECG_nlms, fECG_rls)
    
    
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: uv run main_1.py <ruta_del_archivo>")
        sys.exit(1)
    
    ruta = sys.argv[1]
    main(ruta)