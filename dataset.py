import scipy.io as sio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def read_dataset(mat_path):
    # Cargar datos
    if not Path(mat_path).exists():
        print(f"Error: El archivo {mat_path} no existe.")
    else:
        mat = sio.loadmat(mat_path)
        signal = mat['newDataset'] 
    
        # Calcular Frecuencia de Muestreo y vector de tiempo
        num_samples = signal.shape[0]
        num_channels = signal.shape[1]
        duration_seg = 8
        fs = num_samples / duration_seg
        time = np.linspace(0, duration_seg, num_samples)
    
        # Convertir a DataFrame
        columns =[f'Canal_{i+1}' for i in range(num_channels)]
        df = pd.DataFrame(signal, columns=columns)

        # Guardar en un archivo csv
        df.to_csv('dataset_original.csv', index=False)
    
    return df, time


def plot_dataset(df, time, name_file, subtitle):
    num_channels = df.shape[1]
    max_y = df.to_numpy().max()
    min_y = df.to_numpy().min()
    
    ncols = 2
    nrows = int(np.ceil(num_channels / ncols))
    
    # Graficar en 'nrows' filas y 2 columnas
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, 2.5 * nrows), sharex=True)
    fig.suptitle(subtitle, fontsize=14)
    axes = np.atleast_1d(axes).flatten()
    
    for i in range(nrows * ncols):
        if i < num_channels:
            col_name = df.columns[i]
            axes[i].plot(time, df[col_name], color='b', linewidth=0.8)
            axes[i].set_ylim(min_y, max_y)
            axes[i].set_ylabel(col_name)
            axes[i].grid(True)
        else:
            axes[i].axis('off')

    if num_channels % 2 != 0:
        axes[num_channels - 2].tick_params(labelbottom=True)
        axes[num_channels - 2].set_xlabel('Tiempo (Segundos)')
        axes[num_channels - 1].set_xlabel('Tiempo (Segundos)')
    else:
        axes[-2].set_xlabel('Tiempo (Segundos)')
        axes[-1].set_xlabel('Tiempo (Segundos)')

    plt.tight_layout()
    plt.savefig(name_file + '.png')
    

