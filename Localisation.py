from pyroutelib3 import Router
from geopy.geocoders import Nominatim 
from geopy.distance import geodesic
import numpy as np
from ACO1 import*
import random
import math
from kmeans import *
import folium 
from folium import plugins
def distance(arrivee,depart,router):
    depart_node = router.findNode(depart[0],depart[1])
    arrivee_node = router.findNode(arrivee[0],arrivee[1])
    status, route = router.doRoute(depart_node, arrivee_node)
    if status == 'success':
        routeLatLons = list(map(router.nodeLatLon, route))
        L=len(routeLatLons)#taille de la liste = nombre de points
        d=[]#initialisation de la distance : liste vide
        d_cum=[]#initialisation de la distance cumulée: liste vide
        for i in range(1, L):
            d.append(router.distance(routeLatLons[i-1],routeLatLons[i]))#liste des distances entre deux points
            d_cum.append(sum(d))#liste des distances cumulées
        distance=round(d_cum[-1], 2)#écriture arrondie à deux chiffres après la virgule
    else:
        distance=geodesic(depart,arrivee).km
    return distance
router=Router('car')
nom=Nominatim(user_agent="user_agent")

Quartiers = ["Kaidi",
"Cité 618 Logements / حي 618 مسكن",
"Cité Berki Benyoucef",
"Cité des 22 logements",
"Cité Les Rosiers",
"Cité Météo",
"Cité Mohamed Boudiaf",
"Cité Mohamed Mechtaoui (225 lgts)",
"Cité Rabah Yakoub (120 Lgts)",
"Cité Slimane Amirat (632 lgts)",
"Cité Zerhouni Mokhtar (Les Bananiers)",
"Coop. des architectes",
"Lot Baha 3",
"Lot. Baha 1",
"Lot. Baha 2",
"Lotissement les Mandariniers",
"Résidence Le Lido",
"حي 80 مسكن",
"حي العسكري, Mohammadia",
"Cinq Maisons",
"Cité Al Ibtissama",
"Lido",
"Pins Maritimes",
"Tamaris",
"411 LOGEMENTS",
"456 LOGTS",
"480 LOGTS",
"536 LOGTS",
"ali Sadek 1",
"Ali Sadek 2"
]
Quartiers = [x + ", Alger" for x in Quartiers]
#print(Quartiers)
Coordonnees=[]
for x in Quartiers:
    n1=nom.geocode(x)
    print(n1)
    Coordonnees.append([n1.latitude,n1.longitude])
n=len(Quartiers)
print("Le nombre de quartiers: ",n)
D=[[0 for i in range(n)] for j in range(n)]
print("Construction de la matrice des distance: ")
for i in range(n):
    for j in range(n):
        if(i!=j):
            D[i][j]=distance(Coordonnees[i],Coordonnees[j],router)
print("Fin de construction")
xy=Coordonnees
c=D
r=[0]
for i in range(1,n):
    r.append(random.randint(1,5))
r1 =[]
for i in range(n):
    r1.append(r[i])
#print("r = ",r)
Qj= 30
k=int(sum(r)/Qj)+1
print("k = ", k)
ind=[i for i in range(n)]
ind = ordre_decroissant(r1,n,ind)
#print(ind) 
D=[ind[i] for i in range(k)]
#print(D)
X=[[0 for i in range(n)] for j in range(k)]
G=[ind[i] for i in range(k,n)]
R=[ind[i] for i in range(k,n)]
###################Clusters#######################
k1=n
Q=1
p=0.1
N=25
q0=0.9
alpha=0.1
beta=2
for i in range(n):
    for j in range(n):
        if(i!=j):
            if(c[i][j]==0):
                c[i][j]=1
#print(np.array(c))

c1=c
lnn=NN(n,c1)
solutions=[]
##########################ACO###################################
clusters=clustering(n,k,Qj,D,R,r,xy)
clusters=convergence(n,k,Qj,D,R,r,xy,clusters)
def matrice_kmeans(n,c,clusters):
    matrices=[]
    for i in range(len(clusters)):
        c1=[[0 for j in range(len(clusters[i]))] for k in range(len(clusters[i]))]
        for j in range(len(clusters[i])):
            for k in range(len(clusters[i])):
                c1[j][k]=c[clusters[i][j]][clusters[i][k]]
        matrices.append(c1)
    return matrices
for i in clusters:
    if 0 not in i:
        i.append(0)
#print("cluster final ",clusters)
#print("Matricessssss",matrice_kmeans(n,c,clusters))   
Matrices=[]
Tournees=[]
for i in range(len(clusters)):
    d=[[0 for j in range(len(clusters[i]))] for k in range(len(clusters[i]))]
    toij1=[[0 for j in range(len(clusters[i]))] for k in range(len(clusters[i]))]
    for j in range(len(clusters[i])):
        for k in range(len(clusters[i])):
            d[j][k]=c[clusters[i][j]][clusters[i][k]]
    Lnn=NN(len(clusters[i]),d)
    for j in range(len(clusters[i])):
        for k in range(len(clusters[i])):
            toij1[j][k]=1/(n*(Lnn))
    nij1=inverse(len(clusters[i]),d)
    Solutions=colonie_de_fourmis(len(clusters[i]),toij1,nij1,alpha,beta,d,2,q0,N,Q,p)
    Tournee_cluster=[]
    for j in range(len(Solutions)):
        Tournee_cluster.append(clusters[i][Solutions[j]])
    Tournees.append(Tournee_cluster)
T=[]
for i in range(len(Tournees)):
    if(Tournees[i][0]!=0):
        j=Tournees[i].index(0)
        a = Tournees[i][j:len(Tournees[i])] + Tournees[i][1:j] 
        a.append(0)
    T.append(a)
Distances=[]
for i in T:
    s=0
    for j in range(len(i)-1):
        s=s+c[i[j]][i[j+1]]
    Distances.append(s)
#for i in range(len(T)):
    #print("La tournée: ",T[i])
#    print("Distance de la tournée: ",Distances[i])
#    print("____________________________________")
Itineraires=[]
for i in range(len(T)):
    Itineraire=[]
    for j in range(len(T[i])):
        Itineraire.append(Quartiers[T[i][j]])
    Itineraires.append(Itineraire)
for i in range(len(T)):
    print("La tournée: ",Itineraires[i])
    print("Distance de la tournée: ",Distances[i])
    print("____________________________________")
print("Distance totale ",sum(Distances))





