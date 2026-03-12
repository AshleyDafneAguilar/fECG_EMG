import pandas as pd
import numpy as np

"""
Calcula la correlación de Pearson entre todos los canales de vientre y todos los de tórax.
Retorna la mejor pareja encontrada basada en la correlación absoluta.
"""
def encontrar_mejor_pareja(df_vientre, df_torax):
    resultados = []
    
    for c_vientre in df_vientre.columns:
        for c_torax in df_torax.columns:
            # Calculamos la correlación de Pearson (r)
            r = np.corrcoef(df_vientre[c_vientre], df_torax[c_torax])[0, 1]
            resultados.append({
                'Vientre': c_vientre,
                'Torax': c_torax,
                'Correlacion': abs(r) # Usamos valor absoluto
            })
    
    df_corr = pd.DataFrame(resultados)
    
    # Ordenar por la correlación más alta
    df_corr = df_corr.sort_values(by='Correlacion', ascending=False)
    
    return df_corr