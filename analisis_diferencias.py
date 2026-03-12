import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import os

def generar_reporte_diferencias(nombre_archivo, nombre_dominio):
    # Cargar el archivo CSV
    df = pd.read_csv(nombre_archivo)
    
    clases = sorted(df['Clase'].unique())
    if len(clases) != 2:
        print(f"Advertencia: Se esperaban 2 clases, pero se encontraron {clases}")
    columnas_feat = [c for c in df.columns if c not in ['Instancia', 'Clase']]
    
    resultados = []
    
    # 1. Análisis estadístico (t-test)
    if len(clases) == 2:
        for feat in columnas_feat:
            grupo_a = df[df['Clase'] == clases[0]][feat]
            grupo_b = df[df['Clase'] == clases[1]][feat]
            
            t_stat, p_val = stats.ttest_ind(grupo_a, grupo_b)
            
            resultados.append({'Feature': feat, 'p_value': p_val})
    else:
        print(f"No se puede realizar t-test con {len(clases)} clase(s).")
        return
    
    df_resultados = pd.DataFrame(resultados)
    
    # 2. Filtrar características relevantes (p < 0.05)
    relevantes = df_resultados[df_resultados['p_value'] < 0.05].sort_values('p_value')
    
    print(f"\n--- Dominio: {nombre_dominio} ---")
    print(f"Características con diferencias significativas: {len(relevantes)}")
    
    # 3. Graficar la mejor característica 
    if not relevantes.empty:
        mejor_feat = relevantes.iloc[0]['Feature']
        plt.figure(figsize=(6, 4))
        sns.boxplot(x='Clase', y=mejor_feat, data=df)
        plt.title(f'Característica más relevante: {mejor_feat}\n({nombre_dominio})')
        plt.savefig(f'boxplot_{nombre_dominio.lower()}.png')
        plt.close()
        print(f"Boxplot de la mejor característica guardado: boxplot_{nombre_dominio.lower()}.png")
    else:
        print(f"No se encontraron diferencias significativas en {nombre_dominio}")

if __name__ == '__main__':
    generar_reporte_diferencias('caracteristicas_tiempo.csv', 'Tiempo')
    generar_reporte_diferencias('caracteristicas_frecuencia.csv', 'Frecuencia')
    generar_reporte_diferencias('caracteristicas_tiempo_frecuencia.csv', 'Tiempo-Frecuencia')