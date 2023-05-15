from math import*
import random
import numpy as np
def ordre_decroissant(v,n,ind):
    for i in range(n):
        for j in range(i+1,n):
            if(v[j]>v[i]):
                a=v[i]
                v[i]=v[j]
                v[j]=a
                b=ind[i]
                ind[i]=ind[j]
                ind[j]=b
    return ind
def ordre_croissant(v,n):
    ind=[i for i in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            if(v[j]<v[i]):
                a=v[i]
                v[i]=v[j]
                v[j]=a
                b=ind[i]
                ind[i]=ind[j]
                ind[j]=b
    return ind
def dist_euc(x,i,j):
    dist=sqrt((abs((x[i][0]-x[j][0]))*abs((x[i][0]-x[j][0]))))+(abs((x[i][1]-x[j][1]))*abs((x[i][1]-x[j][1])))
    return dist
def centroids(xy,nj,v):
    s1=0
    s2=0
    for i in range(nj):
        s1=s1+xy[v[i]][0]
        s2=s2+xy[v[i]][1]
    xj=s1/nj
    yj=s2/nj
    return xj,yj
def identite(v,v1):
    identique=True
    for x in v: 
        if x not in v1:
            identique=False
    return identique
#print(R)
def capacity(r,k,clusters):
    capacity=[]
    for i in range(k):
        s=0
        for j in range(len(clusters[i])):
            s=s+r[clusters[i][j]]
        capacity.append(s)
    return capacity
def clustering(n,k,Q,D,R,r,xy):
    centres=[]
    for i in range(k):
        centres.append([D[i]])
        #print(centres)
    for i in range(len(R)):
            costij=[0 for j in range(k)]

            for j in range(k):
                costij[j]=dist_euc(xy,D[j],R[i])
                #print("c",D[j],R[i],"=  ",costij[j])
            cost_ordonne=ordre_croissant(costij,k)
            indmin=costij.index(min(costij))
            m=D[indmin]
            
            for j in range(k):
                m1=D[cost_ordonne[j]]
                for i1 in range(len(centres)):
                    if(m1 in centres[i1]):
                        break
                s=0
                for j1 in range(len(centres[i1])):
                    s=s+r[centres[i1][j1]]
                if(s+r[R[i]]<=Q):
                    centres[i1].append(R[i])
                   
                    break
    #print("centres = ",centres)
    return centres
def wcss(clusters,xy):
    Z=0
    for i in clusters:
        z=0
        centr = centroids(xy,len(i),i)
        centre=[centr[0],centr[1]]
        for i1 in range(len(i)):
            z=z+sqrt((abs((xy[i[i1]][0]-centre[0]))*abs((xy[i[i1]][0]-centre[0]))))+(abs((xy[i[i1]][1]-centre[1]))*abs((xy[i[i1]][1]-centre[1])))
        Z=z+Z
    return Z
def iteration(n,k,Q,D,R,r,xy,clusters):
    for c in clusters:
        xy.append([centroids(xy,len(c),c)[0],centroids(xy,len(c),c)[1]])
    n=n+k
    D=[i for i in range(n-k,n)]

    R=[i for i in range(n-k)]

    for i in range(k):
        r.append(0)
    clusters=clustering(n,k,Q,D,R,r,xy)
    #print("Clusters jdid",clusters)
    for c in clusters:
        for i in range(n-k,n):
            if i in c:
                c.remove(i)
    n=n-k
    for i in range(k):
        xy.pop()
        r.pop()
    #print(xy)
    #print("cluster",clusters)
    return clusters
def convergence(n,k,Q,D,R,r,xy,clusters):
    historique=[clusters]
    z=wcss(clusters,xy)
    clusters1=iteration(n,k,Q,D,R,r,xy,clusters)
    z1=wcss(clusters1,xy)
    i=0 
    print("i = ",i)
    historique.append(clusters1)
    clusters1=iteration(n,k,Q,D,R,r,xy,clusters1)
    z1historique=[z1]
    while(clusters1 not in historique):
            print("______________________________________________________")
            historique.append(clusters1)
            z1historique.append(z1)
            clusters1=iteration(n,k,Q,D,R,r,xy,clusters1)
            z1=wcss(clusters1,xy)
            #print("clusters1  = ",clusters1)
            #print("z1 = ",z1)
            #print("capacities: ",capacity(r,k,clusters1))
            i=i+1
    clusters1=historique[z1historique.index(min(z1historique))]
    print(historique)
    return clusters1