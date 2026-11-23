# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 16:33:29 2025

@author: sanch
"""

import numpy as np
import matplotlib.pyplot as plt

# Parámetros
R = 6371                  
sigma=0.25 
vp1=9
vp=np.array((9.0,12.0))
factorsigma=np.sqrt((1-2*sigma)/(2*(1-sigma)))
vs=vp*factorsigma
a=0.55

deltamax=2*np.arccos(a)*180/np.pi

     # puedes cambiarlo

velocidades = [vp[0],vp[1] ,vs[0], vs[1]]      # tus 4 valores de v

# Rango de delta en grados
delta_deg = np.linspace(0, deltamax, 500)
delta_rad = np.radians(delta_deg)

# Crear la gráfica
plt.figure(figsize=(8,5))

for i in range(len(velocidades)):
    v = velocidades[i]
    y = 2*R/v * np.sin(delta_rad/2)

    if i == 0 or  i ==1:
        label = f"$v_m$={round(v, 2)}, onda P"
    else:
        label = f"$v_m$={round(v, 2)}, onda S"

    plt.plot(delta_deg, y, label=label)


plt.title("Tiempo de llegada de telesismos para diferentes velocidades")
plt.xlabel(r'$\Delta$ (grados)')
plt.ylabel(r'$t(s)$')
plt.legend()

plt.xlim(0, deltamax)   # <-- AQUÍ marcas el límite del eje X

plt.grid(True)
plt.show()
