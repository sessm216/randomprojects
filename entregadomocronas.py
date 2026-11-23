# -*- coding: utf-8 -*-
"""
Created on Sun Nov 16 18:33:10 2025

@author: sanch
"""

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parámetros del modelo
# -----------------------------
R = 6371.0       # Radio de la superficie [km]
R2 = 6300.0      # Radio de la interfaz entre capas [km]
v1 = 12.0         # Velocidad capa superior [km/s]
v2 = 9.0         # Velocidad capa inferior [km/s]

# -----------------------------
# Funciones analíticas
# -----------------------------
def T_total(p):
    """
    Tiempo total ida y vuelta [s] para un rayo con parámetro de impacto p
    """
    T1 = (np.sqrt(R**2 - (p*v1)**2) - np.sqrt(R2**2 - (p*v1)**2)) / v1
    T2 = np.sqrt(R2**2 - (p*v2)**2) / v2  # capa profunda, r_min = p*v2
    return 2 * (T1 + T2)

def Delta_total(p):
    """
    Distancia epicentral total [rad] para un rayo con parámetro de impacto p
    """
    term1 = np.arccos(p*v1/R) - np.arccos(p*v1/R2)
    term2 = np.arccos(p*v2/R2)  # capa profunda, r_min = p*v2 -> arccos(1)=0
    return 2 * (term1 + term2)

# -----------------------------
# Vector de parámetros de impacto p
# -----------------------------
# p máximo limitado por la capa superficial
p_max = R2 / v2  # Para que el rayo llegue al turning point en la capa profunda
p_values = np.linspace(0, p_max*0.999, 500)  # evitar división por cero

# -----------------------------
# Calcular Delta y T
# -----------------------------
Delta_values = Delta_total(p_values)
T_values = T_total(p_values)

# Convertir Delta a grados
Delta_deg = np.degrees(Delta_values)

# -----------------------------
# Graficar curva dromocrónica
# -----------------------------
plt.figure(figsize=(8,6))
plt.plot(Delta_deg, T_values, 'b', lw=2)
plt.xlabel('Distancia epicentral Δ (°)', fontsize=12)
plt.ylabel('Tiempo total T (min)', fontsize=12)
plt.title('Curva dromocrónica para dos capas homogéneas', fontsize=14)
plt.grid(True)
plt.xlim(0, 180)
plt.show()
