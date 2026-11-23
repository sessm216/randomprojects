# -*- coding: utf-8 -*-
"""
Created on Sun May 18 19:52:11 2025

@author: sanch
"""

#Import de paquetes necesarios 
import numpy as np
from scipy import constants as con
from scipy.integrate import quad
import math
import matplotlib.pyplot as plt


#Definición de funciones iniciales 

def f(E,mu):  #Función de Fermi 
    A=100
    if E > mu +A*K*T: #Control de la f para que no explote: exp->inf 
        return 0.0
    elif E < mu -A*K*T: #control: exp->0
        return 1.0
    else:
        return 1/(1+np.exp((E-mu)/(K*T)))


def inten(E,mu,omega): #función a integrar
    return math.sqrt(E-omega)*f(E,mu)

#Parámetros, constantes iniciales

q=con.elementary_charge
K=con.Boltzmann/q 
hbar=con.hbar/q 
h=con.h/q 
me=con.electron_mass #kg

E_f=-5 #Nivel de fermi que coincide con el nivel químico de la fuente
Ec_i=-4.7
T=1
L=4e-8
W=3*L
Ar=L*W
gamma=0.1
mef=0.5*me
tau=con.hbar/q/0.1

Cg=0.1*1e-15
Cd=0
Cs=0
Ces=Cg+Cd+Cs
Cq=q*mef*W*L/(2*con.pi*hbar**2)

eta0=Cg/(Cs+Cd+Cg)
eta=Cg/(Cs+Cd+Cg+Cq)
Vt=(Ec_i-E_f)/(eta0)


Vds_i=0 #Voltaje inicial drain-source
Vds_f=0.5 #Voltajel final
paso_ds=0.01

#Voltaje gate-source 
Vgs_i=0.3
Vgs_f=0.5
paso_g=0.05

#Vectores
Vds=Vds_i
Vg=Vgs_i


#Valor inicial de N0
Ec1=Ec_i
N_0,_=quad(lambda E: f(E,E_f),Ec1,np.inf) #integro
N_0=(L*W*mef/(q*con.pi*hbar**2))*N_0 #constantes

#Bucle en g 
while Vg<Vgs_f:
    i=0
    Vds=Vds_i
    V=np.zeros(int(((np.abs(Vds_i)+np.abs(Vds_f))/paso_ds)))
    It=np.zeros(int(((np.abs(Vds_i)+np.abs(Vds_f))/paso_ds))) #Inicialización de las matrices
    I_0=0
    V_0=0
    #Bucle en Vds para 1 valor de Vgs 
    while Vds<Vds_f:
        
        #Calculo los niveles de la fuente y el drenador para el potencial dado
        mu_s=E_f
        mu_d=E_f-Vds
        error=1
        alfa=0.01
        U=-Vg*(Cg/Ces)
        iter=0
        while error>0.0001 and iter<10000:
            #Numero de electrones N 
            Ns1,_=quad(lambda E: f(E,mu_s),U+Ec1-Vg,np.inf)
            Nd1,_=quad(lambda E: f(E,mu_d),U+Ec1-Vg,np.inf)
            N=(Ns1+Nd1)*(L*W*mef/(q*con.pi*hbar**2))/2
            #Antes de calcular el nuevo U, lo guardo
            Uold=U
            #calculo el nuevo U  
            U=(q/Ces)*(N-N_0)
            #calculo el error
            error=np.abs(U-Uold)
            #para que U converja
            U=Uold+alfa*(U-Uold)
            iter=iter+1
        U=U-Vg
        Is,_=quad(lambda E: inten(E,mu_s,Ec1+U),Ec1+U,np.inf)
        Id,_=quad(lambda E: inten(E,mu_d,Ec1+U),Ec1+U,np.inf)
        I=(Is-Id)*(W*math.sqrt(2*mef*q))/((np.pi*hbar)**2)
        #Ahora lo guardo en un vector para representarlo luego
        V[i]=Vds
        It[i]=I*1e6#multiplico por 1e9 para conseguir nanoamperios
        I_0=I
        V_0=Vds
        #Aumento contadores
        i=i+1
        Vds=Vds+paso_ds
    
    #Graficación
    plt.plot(V, It,label='Vg='+str(round(Vg,2)))
    plt.legend(loc='lower right')
    plt.title('Características I-V a T=1K')
    plt.xlabel('Voltaje (V)')
    plt.ylabel(r'Intensidad ($\mu A$)')
    Vg=Vg+paso_g
    
    
plt.grid(True)
plt.legend(fontsize=9)
plt.show()