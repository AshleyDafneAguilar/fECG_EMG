import numpy as np
import matplotlib.pyplot as plt

# Filtro Least Mean Squares (LMS)
def lms_filter(d, x, mu=0.01, order=32):
    n = len(d)
    w = np.zeros(order)
    e = np.zeros(n)
    for i in range(order, n):
        x_buffer = x[i-order:i][::-1]
        y = np.dot(w, x_buffer)
        e[i] = d[i] - y
        w = w + 2 * mu * e[i] * x_buffer
    return e

# Filtro Normalized Least Mean Squares (NLMS)
def nlms_filter(d, x, mu=0.1, eps=0.001, order=32):
    n = len(d)
    w = np.zeros(order)
    e = np.zeros(n)
    for i in range(order, n):
        x_buffer = x[i-order:i][::-1]
        norm = np.dot(x_buffer, x_buffer) + eps
        y = np.dot(w, x_buffer)
        e[i] = d[i] - y
        w = w + (mu / norm) * e[i] * x_buffer
    return e

# Filtro Recursive Least Squares (RLS)
def rls_filter(d, x, lam=0.99, delta=0.1, order=32):
    n = len(d)
    w = np.zeros((order, 1))
    P = np.eye(order) / delta
    e = np.zeros(n)
    for i in range(order, n):
        x_buffer = x[i-order:i][::-1].reshape(-1, 1)
        # Cálculo de ganancia y actualización
        pi = np.dot(P, x_buffer)
        k = pi / (lam + np.dot(x_buffer.T, pi))
        y = np.dot(w.T, x_buffer).item() 
        e[i] = d[i] - y
        w = w + k * e[i]
        P = (P - np.dot(k, np.dot(x_buffer.T, P))) / lam
    return e


def plot_filtros(time, d, lms, nlms, rls):
    plt.figure(figsize=(12, 10))
    
    # Lista de señales para iterar
    senales = [d, lms, nlms, rls]
    titulos = ['Original (Vientre Canal 5)', 'Resultado LMS', 'Resultado NLMS', 'Resultado RLS']
    colores = ['gray', 'blue', 'green', 'red']
    
    # Calcular límites globales del eje Y
    min_y = min(np.min(s) for s in senales)
    max_y = max(np.max(s) for s in senales)

    for i in range(4):
        plt.subplot(4, 1, i+1)
        plt.plot(time, senales[i], color=colores[i], linewidth=0.8)
        plt.ylim(min_y, max_y)
        plt.title(titulos[i])
        plt.grid(True)
        if i == 3:
            plt.xlabel('Tiempo (Segundos)')
            
    plt.tight_layout()
    plt.savefig('comparacion_filtros.png')