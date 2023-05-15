import random
import numpy as np
def verification(tournee,i,j,n):
    v=False
    i1=tournee.index(i)
    if(tournee[i1+1]==j):
            v=True
    return v
def verification_proba(tournee,i,j,n):
    v=False
    i1=tournee.index(i)
    for i2 in range(i1+1,n):
        if(tournee[i2]==j):
            v=True
    return v
def inverse(n,c):
    nij=[[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            if(i!=j):
                if(c[i][j]!=0):
                    nij[i][j]=1/c[i][j]
    return nij
def Longueur(n,c,sol):
    s=0
    for i in range(n):
            s=s+c[sol[i]][sol[i+1]]
    return s
def deltatk(n,solutions,c,Q):
    toijk=[[0 for i in range(n)] for j in range(n)]
    for i in range(len(solutions)):
        L=Longueur(n,c,solutions[i])
        #print("L = ", L)
        for j in range(n):
            for k in range(n):
                if(j!=k):
                    if(verification(solutions[i],j,k,n)==True):
                        toijk[j][k]=(Q/L)+toijk[j][k]
        #print("toijk = ",np.array(toijk))
    return toijk
def deltatk2(n,solutions,c,Q):
    toijk=[[0 for i in range(n)] for j in range(n)]
    Longueurs=[]
    for i in range(len(solutions)):
        Longueurs.append(Longueur(n,c,solutions[i]))
    Solution=solutions[Longueurs.index(min(Longueurs))]
    L=Longueur(n,c,Solution)
    #print("L = ", L)
    for j in range(n):
        for k in range(n):
            if(j!=k):
                if(verification(Solution,j,k,n)==True):
                    toijk[j][k]=Q/L
    #print("toijk = ",np.array(toijk))
    return toijk
def tours(n,k):
    solutions=[]
    for i in range(k):
        sol = [i for i in range(1,n)]
        random.shuffle(sol)
        solutions.append(sol)
    tournees=[solutions[i] for i in range(k)]
    for i in range(k):
        tournees[i].append(0)
        tournees[i].insert(0,0)
    return tournees
def transtoij(toij,p,n):
    for i in range(n):
        for j in range(n):
            toij[i][j]=(1-p)*toij[i][j]
    return toij
def probability(toij,nij,alpha,beta,tournee,n):
    pijk=[[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            if(verification_proba(tournee,i,j)==True):
                pijk[i][j]=(toij[i][j]**(alpha))*(nij[i][j]**(beta))
    return pijk
def probtrans(n,toij,nij,alpha,beta,sommet):
    pijk=[0 for i in range(n)]
    s=0
    for l in range(n):
        s=s+((toij[sommet][l]**alpha)*(nij[sommet][l]**beta))
    for j in range(n):
        pijk[j]=((toij[sommet][j]**alpha)*(nij[sommet][j]**beta))/s
    return pijk
def ACS(n,toij,nij,beta,sommet):
    ai=[0 for i in range(n)]
    for l in range(n):
        ai[l]=((toij[sommet][l])*(nij[sommet][l]**beta))
    return ai
def Longueur_partielle(C,solution):
    s=0
    for i in range(len(solution)-1):
        s=s+C[solution[i]][solution[i+1]]
    return s
def construction(n,toij,nij,alpha,beta,c,k,q0):
    solutions=[]
    for i1 in range(k):
        ai=ACS(n,toij,nij,beta,i1)
        pi=probtrans(n,toij,nij,alpha,beta,i1)
        d=[]
        for i in range(n):
                d.append(c[i])
        d=np.array(d)
        v=[i for i in range(n)]
        chemin=[i1]
        j=i1
        n1=n
        toij1=toij
        nij1=nij
        while(n1!=1):
            q=random.random()
            if(q<=q0):
                i=ai.index(max(ai))
                #print("pi = ",pi)
                #print("v = ",vi)
                #print("Le prochain sommet est: ",v[i])
                chemin.append(v[i])
                a=v[i]
                toij1=np.delete(toij1,j,0)
                toij1=np.delete(toij1,j,1)
                nij1=np.delete(nij1,j,0)
                nij1=np.delete(nij1,j,1)
                v.remove(v[j])
                n1=n1-1
                pi=probtrans(n1,toij1,nij1,alpha,beta,v.index(a))
                ai=ACS(n1,toij1,nij1,beta,v.index(a))
                j = v.index(a)
               

            else:
                i=pi.index(max(pi))
                #print("pi = ",pi)
                #print("v = ",vi)
                #print("Le prochain sommet est: ",v[i])
                chemin.append(v[i])
                a=v[i]
                toij1=np.delete(toij1,j,0)
                toij1=np.delete(toij1,j,1)
                nij1=np.delete(nij1,j,0)
                nij1=np.delete(nij1,j,1)
                v.remove(v[j])
                n1=n1-1
                pi=probtrans(n1,toij1,nij1,alpha,beta,v.index(a))
                ai=ACS(n1,toij1,nij1,beta,v.index(a))
                j = v.index(a)
                

                    
        chemin.append(i1)
        #print("Tournée : ",chemin)
        #print("Distance: ", Longueur(n,c,chemin))
        solutions.append(chemin)
    return solutions
def somme(n,E):
    s=0
    for i in range(n):
        for j in range(n):
            s=s+E[i][j]
    return s
def NN(n,E):
    E1=E
    E = np.array(E)
    t2=[i for i in range(n)]
    i=0
    t = [i]

    while(somme(n,E)!=0):
        c = E[i][E[i] > 0].min() #calculer le minimum dans la ligne i
        for j in range(n):
                if E[i][j]==c: #chercher l'indice
                    t.append(t2[j])
                    for ind in range(n):
                        E[i][ind]=0
                    for ind in range(n):
                        E[ind][i]=0
                    i=j
                    break
    t.append(0)
    L=Longueur(n,E1,t)
    return L
def colonie_de_fourmis(n,toij,nij,alpha,beta,c,k,q0,N,Q,p):
    Solutions=construction(n,toij,nij,alpha,beta,c,k,q0)
    Longueurs=[]
    for i in range(len(Solutions)):
        Longueurs.append(Longueur(n,c,Solutions[i]))
    #print("La meilleure solution: ",Solutions[Longueurs.index(min(Longueurs))])
    #print("Distance: ",min(Longueurs))
    Nit=0
    while(Nit<N):
        deltatoij=deltatk2(n,Solutions,c,Q)
        for i in range(n):
            for j in range(n):
                toij[i][j]=(toij[i][j]*(1-p))+deltatoij[i][j]*p
        #print("MAJ toij = ",toij)
        toij1=toij
        Solutions=construction(n,toij1,nij,alpha,beta,c,k,q0)
        Longueurs=[]
        for i in range(len(Solutions)):
            Longueurs.append(Longueur(n,c,Solutions[i]))
        Nit=Nit+1
    return Solutions[Longueurs.index(min(Longueurs))]