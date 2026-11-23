# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 16:04:45 2025

@author: sanch
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt 


archivoEW=open(r"C:\Users\sanch\Documents\SARA\geofisica\P4\tenerife3.EW.dat", "r")
archivoNS=open(r"C:\Users\sanch\Documents\SARA\geofisica\P4\tenerife3.NS.dat", "r")

ajusteNS=open(r"C:\Users\sanch\Documents\SARA\geofisica\P4\ajusteNS.dat", "w+")
ajusteEW=open(r"C:\Users\sanch\Documents\SARA\geofisica\P4\ajusteEW.dat", "w+")
#%%Cálculos de EW
# Latitud=phi. Archivo tiene en orden: longitud, latitdu, profundidad del fondo marino, gravedad

dataEW = np.loadtxt(archivoEW)
dataNS = np.loadtxt(archivoNS)

geq=9.780327	
beta1=5302.4E-6
beta2=-5.8E-6

gnEW=np.zeros(len(dataEW))
correcionalEW=np.zeros(len(dataEW))
bougerEW=np.zeros(len(dataEW))
gteoricaEW=np.zeros(len(dataEW))
gobservadaEW=np.zeros(len(dataEW))
anomaliabougerEW=np.zeros(len(dataEW))

for i in range(len(dataEW)):
    gnEW[i]=geq*(1+beta1*np.sin(np.radians(dataEW[i][1]))*np.sin(np.radians(dataEW[i][1]))+beta2*np.sin(2*np.radians(dataEW[i][1]))*np.sin(2*np.radians(dataEW[i][1])))
    if dataEW[i][2]<0: correcionalEW[i]=0 
    else: correcionalEW[i]= -3.086E-6*dataEW[i][2]
    if dataEW[i][2]>0: 
        bougerEW[i]=2*np.pi*(6.67e-11)*(2.67)*1000*dataEW[i][2]
    else: bougerEW[i]=2*np.pi*(6.67e-11)*(2.67-1.02)*1000*dataEW[i][2]
    gteoricaEW[i]=gnEW[i]+correcionalEW[i]+bougerEW[i]
    gobservadaEW[i]=dataEW[i][3]*0.01/1000
    anomaliabougerEW[i]=+gobservadaEW[i]-gteoricaEW[i]
    
    
    
    ajusteEW.write(str(dataEW[i][0])  + "  "  + str(anomaliabougerEW[i]) + "\n" )
    
    
#%% Cálculos de NS 1gal=0.01 m/s^2 
#1mgal 0.01/1000

gnNS=np.zeros(len(dataNS))
correcionalNS=np.zeros(len(dataNS))
bougerNS=np.zeros(len(dataNS))
gteoricaNS=np.zeros(len(dataNS))
gobservadaNS=np.zeros(len(dataNS))
anomaliabougerNS=np.zeros(len(dataNS))

for i in range(len(dataNS)):
    gnNS[i]=geq*(1+beta1*np.sin(np.radians(dataNS[i][1]))*np.sin(np.radians(dataNS[i][1]))+beta2*np.sin(2*np.radians(dataNS[i][1]))*np.sin(2*np.radians(dataNS[i][1])))
    if dataNS[i][2]<0: correcionalNS[i]=0 
    else: correcionalNS[i]= -3.086E-6*dataNS[i][2]
    if dataNS[i][2]>0: 
        bougerNS[i]=2*np.pi*(6.67e-11)*(2.67)*1000*dataNS[i][2]
    else: bougerNS[i]=(-1)*-2*np.pi*(6.67e-11)*(2.67-1.02)*1000*dataNS[i][2]
    gteoricaNS[i]=gnNS[i]+correcionalNS[i]+bougerNS[i]
    gobservadaNS[i]=dataNS[i][3]*0.01/1000
    anomaliabougerNS[i]=gobservadaNS[i]-gteoricaNS[i]
    
 #%% Plotear TODO   
  
    
plt.figure()
plt.plot(dataEW[:,0], gobservadaEW, 'o')   # 'o' para puntos, quítalo si quieres línea
plt.xlabel("Longitud (º)")
plt.ylabel("Gravedad observada $g_o \ [ms^{-2}]$")
plt.grid(True) 
plt.tight_layout()
plt.savefig("EW_gobservadavslongitud.png", dpi=300) 
plt.show()    

plt.figure()
plt.plot(dataEW[:,0], gnEW, 'o')   # 'o' para puntos, quítalo si quieres línea
plt.xlabel("Longitud (º)")
plt.ylabel("Gravedad normal $g_n \ [ms^{-2}]$")
plt.grid(True) 
plt.tight_layout()
plt.savefig("EW_gnvslongitud.png", dpi=300) 
plt.show()

plt.figure()
plt.plot(dataEW[:,0], correcionalEW, 'o', label='$C_{AL}$')   # 'o' para puntos, quítalo si quieres línea
plt.plot(dataEW[:,0], bougerEW, 'o',  label='$C_B$') 
plt.legend()
plt.xlabel("Longitud (º)")
plt.ylabel("Correciones $[ms^{-2}]$")
plt.grid(True) 
plt.tight_layout()
plt.savefig("EW_correcioneslvslongitud.png", dpi=300) 
plt.show()


plt.figure()
plt.plot(dataEW[:,0], gteoricaEW, 'o')   # 'o' para puntos, quítalo si quieres línea
plt.xlabel("Longitud (º)")
plt.ylabel("Gravedad teórica $g_t\ [ms^{-2}]$")
plt.grid(True) 
plt.tight_layout()
plt.savefig("EW_gteoricavslongitud.png", dpi=300) 
plt.show()




plt.figure()
plt.plot(dataEW[:,0], anomaliabougerEW, 'o')   # 'o' para puntos, quítalo si quieres línea
plt.xlabel("Longitud (º)")
plt.ylabel("Anomalía de Bouger $\Delta g \ [ms^{-2}]$")
plt.grid(True) 
plt.tight_layout()
plt.savefig("EW_anomaliavslongitud.png", dpi=300) 
plt.show()


plt.figure()
plt.plot(dataNS[:,1], gobservadaNS, 'o')   # 'o' para puntos, quítalo si quieres línea
plt.xlabel("Latitud (º)")
plt.ylabel("Gravedad observada $g_o \ [ms^{-2}]$")
plt.grid(True) 
plt.tight_layout()
plt.savefig("NS_gobservadavslongitud.png", dpi=300) 
plt.show()    
    
plt.figure()
plt.plot(dataNS[:,1], gnNS, 'o')   # 'o' para puntos, quítalo si quieres línea
plt.xlabel("Latitud (º)")
plt.ylabel("Gravedad normal $g_n \ [ms^{-2}]$")
plt.grid(True) 
plt.tight_layout()
plt.savefig("NS_gnvslatitud.png", dpi=300) 
plt.show()


plt.figure()
plt.plot(dataNS[:,1], correcionalNS, 'o', label='$C_{AL}$')   # 'o' para puntos, quítalo si quieres línea
plt.plot(dataNS[:,1], bougerNS, 'o', label='$C_B$') 
plt.xlabel("Latitud(º)")
plt.ylabel("Correciones $[ms^{-2}]$")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("NS_correcionesvslatitud.png", dpi=300) 
plt.show()
        
plt.figure()
plt.plot(dataNS[:,1], gteoricaNS, 'o')   # 'o' para puntos, quítalo si quieres línea
plt.xlabel("Latitud(º)")
plt.ylabel("Gravedad teórica $g_t \ [ms^{-2}]$")
plt.grid(True)
plt.tight_layout()
plt.savefig("NS_gteoricavslatitud.png", dpi=300) 
plt.show()
        


plt.figure()
plt.plot(dataNS[:,1], anomaliabougerNS, 'o')   # 'o' para puntos, quítalo si quieres línea
plt.xlabel("Latitud(º)")
plt.ylabel("Anomalía de Bouger $\Delta g  \ [ms^{-2}]$")
plt.grid(True)
plt.tight_layout()
plt.savefig("NS_anomaliavslatitud.png", dpi=300)
plt.show()


#%% Parte 2 

datosajusteEW=np.zeros((len(dataEW),2))
datosajusteNS=np.zeros((len(dataNS),2))

for i in range(len(dataEW)):
    datosajusteEW[i][0]=dataEW[i][0]
    datosajusteEW[i][1]=anomaliabougerEW[i]
    
    
        
cond = (datosajusteEW[:, 0] < -16.8) | (datosajusteEW[:,0] > -16.4)

nuevoEW = datosajusteEW[cond]
ajusteEW.close()
ajusteNS.close()

x = nuevoEW[:, 0]  # longitudes
y = nuevoEW[:, 1]  # anomalías

# Ajuste lineal: grado 1
(mEW, bEW), cov = np.polyfit(x, y, 1, cov=True)

# Incertidumbres (desviación estándar)
sigma_mEW = np.sqrt(cov[0, 0])
sigma_bEW = np.sqrt(cov[1, 1])

rEW = np.corrcoef(x, y)[0, 1]
print("r de Pearson:", rEW)

print(f"Pendiente mEW       = {mEW:.6f} ± {sigma_mEW:.6f}")
print(f"Intercepto bEW      = {bEW:.6f} ± {sigma_bEW:.6f}")

# Valores ajustados
y_ajustada = mEW * x + bEW

# Graficar
plt.figure(figsize=(8,5))
plt.scatter(x, y, color='blue', label='Datos filtrados')
plt.plot(x, y_ajustada, color='red', label=f"Ajuste lineal: y={mEW:.4f}x + {bEW:.4f}", linewidth=2)
plt.plot(dataEW[:,0], anomaliabougerEW, label = " Anomalía de Bouger ") 
plt.xlabel("Longitud")
plt.ylabel("Anomalía de Bouger $[ms^{-2}]$")
plt.legend()
plt.grid(True) 
plt.tight_layout()
plt.savefig("EW_ajuste.png", dpi=300)
plt.show()


anomalialocalEW=datosajusteEW[:,1]-(mEW*datosajusteEW[:,0]+bEW)
plt.figure(figsize=(8,5))
plt.scatter(datosajusteEW[:,0], anomalialocalEW, color='blue', label='Datos')
plt.xlabel("Longitud")
plt.ylabel("Anomalía de Bouger local  $[ms^{-2}]$")
plt.legend()
plt.grid(True)
plt.tight_layout() 

plt.savefig("EW_local.png", dpi=300)
plt.show()

#%% NS 
    
for i in range(len(dataNS)): 
    datosajusteNS[i][0]=dataNS[i][1]
    datosajusteNS[i][1]=anomaliabougerNS[i]


cond = (datosajusteNS[:, 0] < 27.98) | (datosajusteNS[:, 0] > 28.47)
nuevoNS = datosajusteNS[cond]

# Separar columnas
x = nuevoNS[:, 0]  # longitudes
y = nuevoNS[:, 1]  # anomalías

(m, b), cov = np.polyfit(x, y, 1, cov=True)

# Incertidumbres (desviación estándar)
sigma_m = np.sqrt(cov[0, 0])
sigma_b = np.sqrt(cov[1, 1])

print(f"Pendiente m       = {m:.6f} ± {sigma_m:.6f}")
print(f"Intercepto b      = {b:.6f} ± {sigma_b:.6f}")

rNS = np.corrcoef(x, y)[0, 1]
print("r de Pearson:", rNS)

# Valores ajustados
y_ajustada = m * x + b

plt.figure(figsize=(8,5))
plt.scatter(x, y, color='blue', label='Datos filtrados')
plt.plot(x, y_ajustada, color='red', label=f"Ajuste lineal: y={m:.5f}x + {b:4f}", linewidth=2)
plt.plot(datosajusteNS[:,0], datosajusteNS[:,1], label="Anomalía de Bouger " )
plt.xlabel("Latitud")
plt.ylabel("Anomalía de Bouger $[ms^{-2}]$")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("NS_ajuste.png", dpi=300)
plt.show()

anomalialocalNS=datosajusteNS[:,1]-(m*datosajusteNS[:,0]+b)

plt.figure(figsize=(8,5))
plt.scatter(datosajusteNS[:,0], anomalialocalNS, color='blue', label='Datos')
plt.xlabel("Latitud [°]")
plt.ylabel("Anomalía de Bouger local $[ms^{-2}]$")
plt.legend()
plt.grid(True) 
plt.tight_layout()
# plt.savefig("NS_local.png", dpi=300)
plt.show()


#%% Cambiar a metros y sacar radios 

lon0 = -16.585       # referencia
R = 6371000        # metros
phi = np.deg2rad(28.2) 

distEW = (datosajusteEW[:,0] - lon0) * (np.pi/180) * R * np.cos(phi)


plt.figure(figsize=(8,5))
plt.scatter(distEW, anomalialocalEW, color='blue', label='Datos')
plt.xlabel("Posición relativa [m]")
plt.ylabel("Anomalía de Bouger local $[ms^{-2}]$")
plt.legend()
plt.grid(True) 
plt.tight_layout()
plt.savefig("EW_local_posicionrelativa.png", dpi=300)
plt.show()



lat0 = 28.183        # referencia
# Conversión latitud → distancia
distNS= (datosajusteNS[:,0] - lat0) * (np.pi/180) * R
plt.figure(figsize=(8,5))
plt.scatter(distNS, anomalialocalNS, color='blue', label='Datos')
plt.xlabel("Posición relativa [m]")
plt.ylabel("Anomalía de Bouger local $[ms^{-2}]$")
plt.legend()
plt.grid(True) 
plt.tight_layout()
plt.savefig("NS_local_posicionrelativa.png", dpi=300)
plt.show()
#%%Sacar mínimos 

minNS=anomalialocalNS[37]
minEW=anomalialocalEW[25]

minimomedia=(minEW+minNS)/2
errorminimo=1E-9




#%%Radio a media altura: 
# EW: 
wEW=(-16.503+16.696)*np.pi/180*R*np.cos(phi)
error=0.001
errEW=np.pi/180*R*np.cos(phi)*np.sqrt(2*error*error)


wNS=(28.278-28.108)* (np.pi/180) * R 
errNS= (np.pi/180) * R *np.sqrt(2*error*error)

# rNS debería ser 20400 m =20km

wmedio=(wEW+wNS)/2
errmedio=1/2*np.sqrt(errNS*errNS+errEW*errEW)
rmedio=wmedio/2
errmediomedio=1/2*errmedio

H=rmedio/np.sqrt(2**(2/3)-1)
errH=errmediomedio/np.sqrt(2**(2/3)-1)
print(H, errH)

#%% Calcular exceso de masa
G=6.674E-11

masa=H*H/G*minimomedia

errormasa=masa/H*np.sqrt(errH*errH*4+H*H/(minimomedia*minimomedia)*errorminimo*errorminimo)    


# Supongamos que tus datos son:
# x_NS, y_NS = coordenadas y anomalías NS
# x_EW, y_EW = coordenadas y anomalías EW

# Concatenamos los datos
x_data = np.concatenate([distNS,distEW])
y_data = np.concatenate([anomalialocalNS, anomalialocalEW])

# Definimos la función
def modelo(x, a, z):
    return a * z / (x**2 + z**2)**(3/2)

# Ajuste
popt, pcov = curve_fit(modelo, x_data, y_data, p0=[1, 1])  # p0=[a_inicial, z_inicial]

a_opt, z_opt = popt
print("Parámetros óptimos: a =", a_opt, ", z =", z_opt)





# Ejemplo: tus datos
# x_NS, x_EW son las coordenadas
# anomalialocalNS, anomalialocalEW son los valores medidos
x_data = np.concatenate([distNS, distEW])
y_data = np.concatenate([anomalialocalNS, anomalialocalEW])

# Función modelo
def modelo(x, a, z):
    return a * z / (x**2 + z**2)**(3/2)

# Ajuste
popt, pcov = curve_fit(modelo, x_data, y_data, p0=[1, 1])

# Parámetros óptimos
a_opt, z_opt = popt

# Errores (desviación estándar)
errors = np.sqrt(np.diag(pcov))
a_err, z_err = errors

print(f"a = {a_opt:.4f} ± {a_err:.4f}")
print(f"z = {z_opt:.4f} ± {z_err:.4f}")


masamasa=a_opt/G 
print(masamasa)

errormasamasa=a_err/G
print(errormasamasa)


radio=3*masamasa/(4*np.pi*(-0.5*1000))

np.float64(-182125527450.6533)
