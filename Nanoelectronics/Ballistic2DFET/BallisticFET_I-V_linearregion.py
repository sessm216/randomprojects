# -*- coding: utf-8 -*-
"""
Created on Sun May 18 19:57:21 2025

@author: sanch
"""
from scipy import constants as con
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import math
import plotly.graph_objects as go



q=con.elementary_charge
K=con.Boltzmann/q 
hbar=con.hbar/q 
h=con.h/q 
me=con.electron_mass #Kg

def fermi(E, mu, T):
    A = 100
    if E > mu + A * K * T:
        return 0.0
    elif E < mu - A * K * T:
        return 1.0
    else:
        return 1 / (np.exp((E - mu) / (K * T)) + 1)
    
    
T = 298 #K
E_c = -4.7 #eV
E_f = -5. #eV
m= 0.5*me #Kg
L= 40e-9 #m
W= 3*L #m
Cg = 0.1e-15 #F
Vds=0.5 #V
Vgs_i = 0. #V
Vgs_f = 1. #V
paso_gs = 0.001 #V
Nint = int(abs(Vgs_f-Vgs_i)/paso_gs)



#Variables para el metodo iterativo de Uc
epsilon = 1e-6 #Valor que controlará la convergencia de U en el proceso iterativo.
alfa = 0.1 #valor que nos ayudará a llevar a convergencia U usando la pista 2 aportada por el ejercicio.
Nit_max = 1000 #Número de iteraciones máximas en el calculo iterativo de U.

aux2 = q/Cg #Valor de q^2/C_{ES} en eV
AUX = (W*math.sqrt(2*m*q))/((np.pi*hbar)**2) #Variable que nos ayudará al calculo de la Intensidad, lo sacamos factor común
AUX2 = (L*W*m)/(q*np.pi*hbar**2) #Variable que nos ayudará al cálculo del número de electrones para el proceso iterativo de Uc


#Definimos una función que representará el integrando de la intensidad. Llamaremos alfa al termino E_c+U que se irá actualizando como se sabe por cambiar Uc
def aux (E, mu, omega, T):
    return  math.sqrt(E-omega)*fermi(E,mu, T)


I=np.zeros(Nint+1)
N0aux,_=quad(lambda E: fermi(E, E_f, T), E_c, np.inf)
N0=N0aux*AUX2


salida5=open(r"C:/Users/sanch/Documents/SARA/nano.txt", "a+")
with open("el.txt", "w") as a:
    #Bucle que recorrerá cada valor para Vgs
    for j in range (Nint+1):
        #Valor de Vgs en la iteración
        Vgs=Vgs_i+j*paso_gs 
        #Iniciamos el termino del potencial dará cuenta del charging 
        Uc=[0,2*epsilon] #Vector que recogerá los valores de Uc en el proceso iterativo, su primer elemento recogerá el de la iteración i (en este caso del que partiremos, 0) y
                    #el segundo valor recogerá el de i-1. Inicialmente damos valor 2*epsilon para que entre en el proceso iterativo.
        seguir_ejecutando = True # Variable booleana para controlar el bucle de cálculo de Uc   .
        Nit=0 #Variable que contará el número de iteraciones de cálculo de U por si no convergiese tras un número elevado
        while seguir_ejecutando:
            #Calculamos los electrones aportados por drenador y fuente al hilo.
            Ns,_=quad(lambda E: fermi(E, E_f, T), E_c+Uc[0]-Vgs, np.inf)
            Nd,_=quad(lambda E: fermi(E, E_f-Vds, T), E_c+Uc[0]-Vgs, np.inf)
            N=AUX2*(Ns+Nd)/2
            Uc[1]=Uc[0]        
            Uc[0]=Uc[1]+alfa*(aux2*(N-N0)-Uc[1]) 
            # Verificar las condiciones para continuar el bucle
            condicion_1 = abs(Uc[0] - Uc[1]) < epsilon
            condicion_2 = Nit > Nit_max
            # Si alguna de las condiciones deja de cumplirse, cambiar la variable a False
            if (condicion_1 or condicion_2):
                seguir_ejecutando = False
                Uf=Uc[0]-Vgs#Se le da a U el valor actualizado con esa Uc calculada y sumandole el termino por Vgs
            Nit+=1
        
    
        i1,_=quad(lambda E: aux (E,E_f,E_c+Uf, T), E_c+Uf, np.inf)
        i2,_=quad(lambda E: aux (E, E_f-Vds, E_c+Uf, T), E_c+Uf, np.inf)
        i=i1-i2   
        I[j]=AUX*i
        
        
        salida5.write(str(Vgs)+ "  " + str(I[j]) + "\n ")
        X=math.log10(I[j])
        a.write(f"{Vgs}\t{X}\n")     

    
#Nos interesara además estudiar la pendiente subumbral y comprobar que es 60 mV/década con lo que a partir del
#I[0] representaremos una recta con pendiente 1/0.06 V para comprobar si se obtiene lo mismo
S=np.zeros(int(Nint/3)+1)
with open("Sub.txt", "w") as a:
    for i in range (int(Nint/3)+1):
        Vgs=Vgs_i+i*paso_gs 
        M=math.log10(I[0])
        S[i]=M+Vgs/0.06
        a.write(f"{Vgs}\t{S[i]}\n") 
        
import matplotlib.pyplot as plt

# Carga de los datos
a0 = np.loadtxt('el.txt')
a1 = np.loadtxt('Sub.txt')

# Separa los datos
x0 = a0[:, 0] 
y0 = a0[:, 1]  
x1 = a1[:, 0]
y1 = a1[:, 1]  

# Crear figura
plt.figure(figsize=(10, 6))

# Curva I-V logarítmica
plt.plot(x0, y0, label=r'$V_{DS} = 0.5$ V', color='red')

# Recta con pendiente subumbral ideal
plt.plot(x1, y1, '--', label=r'Recta pendiente $1/0.06$ V', color='blue')

# Línea vertical indicando V_T
plt.axvline(x=0.3, color='yellow', linestyle='--', label=r'$V_T$')

# Etiquetas y título
plt.title(r'$\log_{10}(I_{DS})$ frente a $V_{GS}$. C', fontsize=14)
plt.xlabel(r'$V_{GS}$ (V)', fontsize=12)
plt.ylabel(r'$\log_{10}(I_{DS})$', fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()


salida5.close()

# Mostrar figura
plt.show()
