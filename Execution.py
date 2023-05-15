from kmeans import*
from ACO1 import*
n=25
xy=[[random.randint(0,5) for i in range(2)] for j in range(n)]
r=[0]
for i in range(1,n):
    r.append(random.randint(1,5))
r1 =[]
for i in range(n):
    r1.append(r[i])
Qj= 15
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
################################Clusters######################################################
k1=n
Q=1
p=0.1
N=25
q0=0.9
alpha=0.1
beta=2
c=[[0 for i in range(n)] for j in range(n)]
for i in range(n):
    for j in range(n):
        if(i!=j):
            c[i][j]=dist_euc(xy,i,j)
for i in range(n):
    for j in range(n):
        if(i!=j):
            if(c[i][j]==0):
                c[i][j]=2
print(np.array(c))

c1=c

solutions=[]

##########################ACO###################################
clusters=clustering(n,k,Qj,D,R,r,xy)
clusters=convergence(n,k,Qj,D,R,r,xy,clusters)
print("cluster final ",clusters)
for i in clusters:
    if 0 not in i:
        i.append(0)
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
for i in range(len(Tournees)):
    print("La tournée: ",T[i])
    print("Distance de la tournée: ",Distances[i])
    print("____________________________________")




