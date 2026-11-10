Code to simulate average occupation rate of two trains covering the same route with different speed and price.

Physical parameters:
v: velocity of train 1 and 2
distancias: distance between station A-B and B-C 
x: price of train tickets 1 and 2
nmax: max number of tickets that can be sold for each train (limit of passengers)
horas_operacion: time interval during which there's train service (in minutes). 
ganancia: how much money is made by selling tickets. It is computed as: pricetrain1*numberofpassengersintrain1+pricetrain2*numberofpassengersintrain2
probabilidades=np.array[savings,timesavings,waitingtime]. This simulates the weight each criterion has on decision-making 

Initial conditions:
Both trains start at station A: posicion=np.zeros
Both trains will start moving in the same direction, towards intermediate station B. 

ntransportados: number of passengers currently in the train traveling. It is a matrix where [train 1 or 2, destination AB or C]
Current version of the code computes ntransportados=nmax*0.5; meaning that when the day starts at 6AM nmax*0.5 passengers are travelling from A to B. 

genteesperando: number of people waiting at station B and C for the trains to arrive. 
Current version of the code assumes that 190 are waiting at both B and C. These numbers can be changed or generates randomly

gentefuera: number of passengers that are left out and cannot access a train because it reached its capacity.
This can happen when a train ticket is very cheap and the passengers prioritize lower prices. It is a measure of efficiency. If gentefuera is too high means that either we are modeling the passengers priorities not so accurately or, in real life, that we need more services.

Interaction between two trains: 
Decision-making process that passengers make when a train arrives at the station. 
Let's say I am waitinf for my train when the other arrives. Will I take this one? Is it worth it to me?
Why is this a neccesary question? The goal is to simulate passengers occupancy rates depending on how important price and speed are to them. 
First criteria: how much time do I have to wait for my original intended train? Current version of the code sets time limit to 20. I will not *consider* changing my train if I'll wait less than 20m for it. 
If I consider changing my choice the probability of changing is computed as follows: 
-ahorro: the relative change in price if I chose the other train.
-tiempodeviaje: relative change in journey length if I chose the other train.
-espera:absolute change in waiting time. 
This decision making process is modelated as a probability function in which each change parameter (ahorro, tiempodeviaje, espera) is weighted by how important they are to passengers (probabilidades array). 
Change probability (prob) is computed. A max function ins used to ensure that it stays withing the (0,1) probability domain. 
pasajerosextra is computed. This is the number of passengers that were waiting for the other train and have decided to jump on the one that just arrived. They will want to board the train just like the ones that were originally waiting for it. 





Algorithm: 
1081 step loop simulatin every minute of service. 
1. In each loop we:
 1.1 Update how much time is left for the trains to arrive at each station. 
1.2 If condition: if the train arrives at the station:
a. We compute how many people there are waiting at the station as a random variable that we overwrite: genteesperando*=random.uniform(0.9,1.1). This way the amount of passengers waiting does have some random element to it, but not fully, as in real life we would expect the authorities to have a forecasted occupancy rate. 
b. We update the position of the train to show that it reached the new station 
c. We update how many journeys the train has done. This way we could compute occupancy/journeys, meaning the average occupancy of the train. 
d. We update how many passengers have succesfully been transported from one station to another. 
e. We update how many passengers are inside the train by updating the matrix ntransportados. Example: if train 1 arrives at B, there will no longer be passengers inside wanting to go to B (they are already there). So the matrix value corresponding to [train1,B] will be 0. 
f. We simulate the decision making process passengers make if the time for the other train to come is t>20
g. We simulate people getting on the train


Simulating people getting on the train. 
1. Passengers originally waiting for the train try to get in. We assume that they had bought their ticket already. 
2. We check whether there are free seats for them. If not If not, they are left out and so will be the ones who changed their mind last minute. gentefuera increases. The train carries full capacity nmax and leaves the station
3. If those waiting fit they get in. We must check whether there are free seats (maybe nmax people fit exactly). We do this with a max function: either 0 free seats or nmax-numberofpassengerscurrentlyatthetrain (a number lower than nmax can be chosen too, if we want to make sure that some last minute passengers get in). 
4. We check whether some of the last minute passengers will be left out. 
5. The train leaves the station




