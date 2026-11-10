# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 15:34:47 2025

@author: sanch
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 13:51:00 2025

@author: sanch
"""


import numpy as np
import random

#%% Parámetros del escenario
# Velocidades de los trenes (km/h)
v = np.array([100, 200])

# Distancias entre estaciones (km)
distancias = np.array([100, 100])  # A–B y B–C

# Tarifas por pasajero de cada tren
x = np.array([5.0, 30.0])

# Límite de pasajeros por tren
nmax = 400

# Tiempo total de operación (min)
horas_operacion = (24 - 6) * 60  # 18 horas

siguienteparada=np.zeros(2,dtype=int)

#%% Inicialización de variables
# Posición de los trenes: 0=A, 1=B, 2=C
posicion = np.zeros(2, dtype=int)

# Dirección: +1 va hacia C, -1 va hacia A
direccion = np.ones(2, dtype=int)

# Tiempos restantes por tren (min)
t= np.array(distancias[0] / v * 60)

# Matriz de pasajeros en cada tren con destino a cada estación
# ntransportados[tren, destino]
ntransportados = np.zeros((2, 3))
for m in range(2):
    for l in range(3):
        if l==0: 
            ntransportados[m,l]=0
        else:ntransportados[m,l]=nmax*0.5
        
genteesperando=np.zeros((2,3))
for m in range(2):
    for l in range(3):
        if l==1: genteesperando[m,l]=190
        else: genteesperando[m,l]=190

# Totales
pasajerostotales= np.zeros(2)
viajes = np.zeros((2, 3))
tiemporestante = np.zeros(2)          # minutos hasta próxima estación
for i in range(2): 
    tiemporestante[i]=(distancias[0]/v[i])*60 #tiempo a la estación B 

ganancia = np.zeros(2)
gentefuera=0

probabilidades=np.array((15.5, 15.0, 15.5))

#%%Simulación de 1 día

for k in range(1081):
  
        for tren in range(2): #en cada minuto revisamos qué le pasa a los 2 trenes
            
            tiemporestante[tren]-=1 #pasa 1 minuto 
            
            if tiemporestante[tren]<=0:
                genteesperando=genteesperando*random.uniform(0.9,1.1)
                posicion[tren]+=direccion[tren] #actualizamos la posición del tren 
                viajes[tren,posicion[tren]]+=1
                pasajerostotales[tren]+=ntransportados[tren,posicion[tren]]
                ntransportados[tren,posicion[tren]]=0 #el tren se vacía, porque nadie quiere ir a B estando en B 
                                    
                otrotren=1-tren 
                otrotiempo=tiemporestante[otrotren]
                if otrotiempo>20: 
                    ahorro=(x[otrotren]-x[tren])/x[otrotren]
                    tiempoviaje=(t[otrotren]-t[tren])/t[otrotren]
                    espera=otrotiempo-20
                    prob=(espera)*probabilidades[0]/100+ahorro*probabilidades[1]/100+tiempoviaje*probabilidades[2]/100
                    prob=max(0,min(prob,1))
                    pasajerosextra=genteesperando[otrotren,posicion[tren]]*prob
                else: pasajerosextra=0
                
                if (posicion[tren]==2) or (posicion[tren]==0):
                    direccion[tren]*=(-1)
                siguienteparada[tren]=posicion[tren]+direccion[tren]
                
                if posicion[tren]==1:
                    ntransportados[tren,siguienteparada[tren]]+=genteesperando[tren,posicion[tren]]
                    if ntransportados[tren,siguienteparada[tren]]>400: 
                        sitioslibres=0
                        ntransportados[tren,siguienteparada[tren]]=400
                        gentefuera+=pasajerosextra
                    else: 
                        sitioslibres=max(0,300-ntransportados[tren,siguienteparada[tren]])
                        gentefuera+=max(0,pasajerosextra-sitioslibres)
                        ntransportados[tren,siguienteparada[tren]]+=sitioslibres
                else: 
                    q=random.uniform(0.3,0.7)
                    genteesperando[tren,posicion[tren]]+=pasajerosextra
                    echamosgente=genteesperando[tren,posicion[tren]]-400
                    if echamosgente>0: 
                        gentefuera+=echamosgente
                        ntransportados[tren,siguienteparada[tren]]+=400*q
                        ntransportados[tren,siguienteparada[tren]+direccion[tren]]+=400*(1-q) 
                    else: 
                        ntransportados[tren,siguienteparada[tren]]+=genteesperando[tren,posicion[tren]]*q
                        ntransportados[tren,siguienteparada[tren]+direccion[tren]]+=genteesperando[tren,posicion[tren]]*(1-q)    


                if 0<=siguienteparada[tren] <=2: 
                    #tiemporestante[tren]=(distancias[(direccion[tren]-1)]/v[tren])*60
                    tiemporestante[tren]=(distancias[0]/v[tren])*60
                else: tiemporestante[tren]=9999
        
        
print(pasajerostotales) 
#%%
pasajerosporviaje=np.zeros(2)
for m in range (2):    
    aux=pasajerostotales[m]
    aux2=sum(viajes[m,:])
    pasajerosporviaje[m]=aux/aux2


f=open(r"C:/Users/sanch/Documents/SARA/vis/tren3dinamico_datos_1530100100"+ str(v[0])+str(v[1])+".txt", "a+")
f.write(str(v[0]) + "  "  + str(v[1]) + "  " +  str(x[0]) + "  " + str (x[1]) + "   "+  str(pasajerosporviaje[0]) + "  "+ str(pasajerosporviaje[1]) + "  " + str(probabilidades[0]) + "  " + str(probabilidades[1])+ "  " + str(probabilidades[2]) + "\n")
f.close()


        
