import time
from os.path import exists
import numpy as np
import os
import ast
from itertools import permutations, product, combinations
from numpy import matrix, copy, zeros
from io import StringIO
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
path='ISO_Files/'
########################
### 2022/8/7
### Every non-directed colored graph (multi-graph) represented by a matrix
### for example:
### [3,1,4]
### [1,2,0]
### [4,0,0]
### We will save the matrix column-by-column as list
### [3,1,2,4,0,0]
########################

### recolor the graph by new color
def RecolorV(M,color_lis):
    A=copy(M)
    for i in range(len(color_lis)):
        A[i,i]=color_lis[i]
    return A.astype(int)

### just input the color graph

### return the information for the color for all vertex
def VColor(M):
    return np.array([M[i,i] for i in range(np.shape(M)[0])]).astype(int)

### find the edge-color set for the graph
def EColor(M):
    n=np.shape(M)[0]
    A=RecolorV(M,n*[-1])
    color=[A[i,j] for i in range(n) for j in range(n)]
    color=list(set(color))
    color.sort()
    color.remove(-1)
    return np.array(color).astype(int)


### input is list

def RecolorE(M,origin_color,new_color):
    A=copy(M)
    for i in range(np.shape(A)[0]):
        for j in range(np.shape(A)[1]):
            if A[i,j] not in origin_color:
                continue
            indij = origin_color.index(A[i,j])
            A[i,j] = new_color[indij]
    return A.astype(int)

### characteristic matrix of M of edges that is value-color
def CharacterMatrix(M,value):
    n=np.shape(M)[0]
    A=RecolorV(M,n*[-1])
    return matrix([[1 if A[i,j]==value else 0 for j in range(n)] for i in range(n)]).astype(int)

### turn mat into a list
def mat2lis(M,digraph=False):
    if digraph==False:
        return np.array([M[j,i] for i in range(np.shape(M)[1]) for j in range(i+1)]).astype(int)
    else:
        n=np.shape(M)[1]
        L=[]
        for i in range(n):
            L+=[M[p,i] for p in range(i+1) ]+[ M[i,i-p-1] for p in range(i)]
        return np.array(L).astype(int)


### turn list into matrix form (strictly upper triangular part)
def lis2mat(v,n):
    M=zeros((n,n))
    if len(v)==n**2:
        ind = 0;
        for i in range(n):
            for p in range(i+1):
                M[p,i]=v[ind]
                ind+=1
            for p in range(i):
                M[i,i-p-1]=v[ind]
                ind+=1
        return M.astype(int)

    elif len(v)==(n+1)*n/2:
        k=0
        for j in range(n):
            for i in range(j+1):
                M[i,j]=v[k]
                if i!=j:
                    M[j,i]=v[k]
                k+=1
        return M.astype(int)
    
    # May still want to check if the length of input list is expected.
    else:
        ValueError("input format error")

### upper triangle to strictly upper triangle
def u2su(lis,n):
    L=[]
    for i in range(n):
        L.extend(lis[int((i)*(i+1)/2): int(((i)*(i+1)/2)+(i))])
    return np.array(L)


### strictly upper triangle to upper triangle
def su2u(lis,n):
    L=[0]
    for i in range(n-1):
        L.extend(lis[int((i)*(i+1)/2): int(((i)*(i+1)/2)+ (i+1))])
        L.extend([0])
    outcome = np.array(L)
    return outcome.astype(int)


### turn list [1,2,3,4,5,6] into [0,1,0,2,3,4,0,5,6]
### [ ,1,3]  [0,1,3]
### [2, ,4]->[2,0,4]
### [6,5, ]  [6,5,0]
def nd2d(v,n):
    L=[0]
    for i in range(1,n):
        K= (i-1)*i
        L = np.append(L,  np.append (np.append(v[K: K+i], [0]) , v[K+i: K+2*i]))
    return np.array(L).astype(int)

#######################################################################
#every permutation save as a list for example (0,1,4)(2,3)=[1,4,3,2,0]#
#######################################################################

########################
### Part Backtracking ver:
########################

### construct the matrix of permutation (i,j)
def Permutateij(n,i,j):
    p=np.identity(n)
    if i==j:
        return p
    p[i,j]=1
    p[j,i]=1
    p[i,i]=0
    p[j,j]=0
    p = p.astype(int)
    return p

def deg_T(A, T, v):
    deg = 0
    for t in T:
        deg += A[t, v]
    return deg

def refine(n, A, B):

    S = B.copy()
    while len(S) > 0:
        
        T = S[-1]
        S = S[:-1]
        
        ### Bnew is used to record the update B
        Bnew = []
        
        for block in B:
            
            bl = len(block)
            degset = []
            Deg = []
            
            for b in block:
                t = deg_T(A,block, b)
                Deg.append([b,t])
                if t not in degset:
                    degset.append(t)         
            if len(degset) == 1:
                Bnew.append(block)
                continue
            
            degset.sort()
            for m in degset:

                KK = [ Deg[i][0] for i in range(bl) if Deg[i][1] == m]
                S.append(KK)
                Bnew.append(KK)
                
                
        B=Bnew
        
    return B

def compare(G,pi,mu,l):
    for j in range(l):
        for i in range(j+1):
            x=G[mu[i],mu[j]]
            y=G[pi[i],pi[j]]
            if x<y:
                return 'Worse'
            elif x>y:
                return 'Better'
    return 'Equal'

def Canonical(GG,ref=-1):
    
    def BackTrackSearch(n,G,P):
        nonlocal BestExists 
        nonlocal mu
        nonlocal Res
        
        Q = refine(n,G,P)
        l = n

        for i in range(len(Q)):
            if len(Q[i]) > 1:
                l = i
                break
                              
        if BestExists == True:
            Res = compare(G,[Q[i][0] for i in range(l)], mu, l)
      
        if len(Q) == n:

            if BestExists == False:
                mu = [Q[i][0] for i in range(n)]
                BestExists = True

            else:  
                if Res == 'Better':
                    mu = [Q[i][0] for i in range(n)]
                    
        else:
            if Res != 'Worse':
                
                Choose = copy(Q[l])
                
                R = [Q[j] for j in range(l)]+[[],[]]+[Q[j] for j in range(l+1,len(Q))]

                while len(Choose) > 0:

                    u = Choose[0]

                    R[l] = [u]
                    D=copy(Q[l])
                    D = D[D!=u]
                    R[l+1]=D

                    BackTrackSearch(n,G,R)
                    Choose = Choose[Choose != u]
                    
    n = np.shape(GG)[1]
    if ref >= 1:
        p = Permutateij(n,ref,0)
        G = np.dot(np.dot(p,GG),p)  
    else:
        G = GG    

    BestExists = False
    Res = 'Better'
    if ref == -1:
        P = [list(range(n))]
    else:
        P = [[0],list(range(1,n))]
    mu = []
    
    BackTrackSearch(n,G,P)

    L = []
    for j in range(n):
        L += [G[mu[i],mu[j]] for i in range(j+1) ]
    
    return np.array(L,dtype='int')



### write the output as a npy file
def write_file(lis, filename):
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(filename+'.npy','wb') as f:
        np.save(f, lis)

def load_file( filename,n):
    with open(filename+'.npy', 'rb') as f:
        new_dict = np.load(f)
        
    return np.array(new_dict).astype(int)

### -1: A>B
###  0: A=B
###  1: A<B
# Perhaps check if they have the same length. Maybe rename it to LexicographicallyCompare

########################
### Part Opt: This part related to functions that display the graph
########################

### check the connectivity
def IsConnect(M):
    if (M==M.transpose()).all():
        if connected_components(M)[0]==1:
            return True
        else:
            return False
        #return Graph(M).is_connected()
    else:
        if connected_components(M, directed=True)[0]==1:
            return True
        else:
            return False


def LexicographicallyCompare(A,B):
    for i in range(len(A)):
        if A[i]<B[i]:
            return 1
        if A[i]>B[i]:
            return -1
    return 0

########################
def LexicographicallyCompareV2(A,B):
    return -int(LexicographicallyCompare(A, B))

def BinarySearch(arr,itm):
    def inside(arr,itm,low,high):
        if low > high:
            return -1
        else:
            mid = int((low + high) / 2)
            out = LexicographicallyCompare(itm, arr[mid])
            if out == 0:
                return mid
            elif out == 1:
                return inside(arr,itm,low, mid - 1)
            else:
                return inside(arr,itm,mid+1,high)
    return inside(arr,itm,0,len(arr)-1)
    
### construct the matrix of permutation (i,j)

def mergeSort(array):
    if len(array) > 1:

        #  r is the point where the array is divided into two subarrays
        r = len(array)//2
        L = array[:r].copy()
        M = array[r:].copy()

        # Sort the two halves
        mergeSort(L)
        mergeSort(M)

        i = j = k = 0

        # Until we reach either end of either L or M, pick larger among
        # elements L and M and place them in the correct position at A[p..r]
        new_arr = []
        while i < len(L) and j < len(M):
            if LexicographicallyCompare(L[i], M[j]) == 1:
                array[k] = L[i]
                i += 1
            else:
                array[k] = M[j]
                j += 1
            k += 1

        # When we run out of elements in either L or M,
        # pick up the remaining elements and put in A[p..r]
        while i < len(L):
            array[k] = L[i]
            i += 1
            k += 1

        while j < len(M):
            array[k] = M[j]
            j += 1
            k += 1
            
def AddEdge(G,connect=False):
    n=np.shape(G)[1]
    # You can make IsoFree a set rather than a list: IsoFree = set(), this way
    # checking for existance of a given element should be much faster.
    IsoFree=set()
    GG=RecolorV(copy(G), n*[0])
    cg=mat2lis( GG)
    
    ### we consider all possible way that we can add at most one edge between every pairs ij, i!=j in [0..n-1]
    inn = int(n*(n-1)/2)
    tup = list(product([1,0], repeat=inn) )
    for ss in tup:
        s=su2u(ss,n)
        T=[cg[i]+s[i] for i in range(len(cg))]
        M=lis2mat(T,n)
        lab=Canonical(M)
        lab_str = tuple(lab)
        if lab_str not in IsoFree:            
            if connect==True:
                if IsConnect(M)==False:
                    continue
            IsoFree.add(lab_str)
    outcome = [np.array(s).astype(int) for s in IsoFree]
    mergeSort(outcome)
    return np.array(outcome).astype(int)            

def AddVertex(G,sizee, connect=False):
    n=np.shape(G)[1]
    IsoFree=set()
    cg=mat2lis(G)
    
    ### consider all possible way that we can add one vertex
    tup = list(product([ i for i in  range(sizee)], repeat = n))
    for s in tup:
        
        T= np.append(cg, np.append(np.array(list(s)), np.array([0]) ) )
        M=lis2mat(T,n+1)
        lab=Canonical(M)
        lab_str = tuple(lab)
        if lab_str not in IsoFree:
            if connect==True:
                if IsConnect(M)==False:
                    continue
            IsoFree.add(lab_str)
    outcome = [np.array(s).astype(int) for s in IsoFree]
    mergeSort(outcome)
    return np.array(outcome).astype(int)

def Generator(n,sizev, sizee, orbg=False ,connect=False,Time=True):
    start=time.time()
    ### deal with graphs
    if orbg==False:
        
        ### path to save results later

        finpath=path+'n{}V{}E{}Graph'.format(n,sizev,sizee)
        if connect==True:
            finpath+='_connect'
            
        ### if the we already compute before, just read the result
        if  exists(finpath+'.npy')==True:
            lis=load_file(finpath,n) 
            return lis
        ### our strategy is 
        ### sizee  |__s5_|_s4_|_s3_|__s2__|_s1_|
        ### sizee-1|__s6_|____|____|______|____|
        ### ...    |__s7_|____|____|______|____|
        ### 2      |__s8_|____|____|______|____|
        ###           3    4    5    ...    n
        ### we will do the step: s1,...,s8 in order
        if sizev==1:

            if n==3:
                
                ### base case
                if sizee==2:
                    ppath=path+'n{}V1E{}Graph'.format(n,2)
                    if connect==True:
                        ppath+='_connect'
                    if connect==True:
                        lis=[[0, 0, 0, 1, 1, 0], [0, 1, 0, 1, 1, 0]]
                    else:
                        lis=[[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 1, 0, 1, 1, 0]]
                        
                    lis = np.array(lis).astype(int)
                    write_file(lis,ppath)
                    return lis

                ### else case
                ppath=path+'n{}V1E{}Graph'.format(n,sizee-1)
                if connect==True:
                    ppath+='_connect'
                if  exists(ppath+'.npy')==False:
                    lis=Generator(n,1,sizee-1,False,connect,False)
                    write_file(lis,ppath)
                else:
                    lis=load_file(ppath,n) 
                
                ### do the operation: add edge
                which_one ='adde'

            if n>3:
                ppath=path+'n{}V1E{}Graph'.format(n-1,sizee)
                if connect==True:
                    ppath+='_connect'
                if  exists(ppath+'.npy')==False:
                    lis=Generator(n-1,1,sizee,False,connect,False)
                    write_file(lis,ppath)
                else:
                    lis=load_file(ppath,n) 
                
                ### do the operation: add point
                which_one='addp'

        else:
            #sizev > 1
            VL=list(range(sizev))

            ppath=path+'n{}V1E{}Graph'.format(n,sizee)
            if connect==True:
                ppath+='_connect'
            
            if  exists(ppath+'.npy')==False:
                lis=Generator(n,1,sizee,False,connect,False)
                write_file(lis,ppath)
            else:
                lis=load_file(ppath,n) 
            
            ### do the operation: add color to vertex
            which_one='addc'
            
        ### do the operation we determine before
        IsoFree=set()
        if which_one=='adde':
            for g in lis:
                for t in AddEdge(lis2mat(g,n), connect):
                    t_str = tuple(t)
                    
                    if t_str not in IsoFree:
                        IsoFree.add(t_str)
        elif which_one=='addp':
            for g in lis:
                for t in AddVertex(lis2mat(g,n-1),sizee, connect):
                    t_str = tuple(t)
                    if t_str not in IsoFree:
                        IsoFree.add(t_str)
        elif which_one=='addc':
            #print(len(lis)) 
            #num = 0
            for l in lis:
                #print(num + 1)
                #num += 1
                
                ll=lis2mat(l,n)
                tup = list(product([ i for i in  range(sizev)], repeat = n))
                for s in tup:
                    t=Canonical((RecolorV(ll,s)))
                    t_str = tuple(t)
                    if t_str not in IsoFree:
                        IsoFree.add(t_str) 
        IsoFree=[np.array(s).astype(int) for s in IsoFree]
        mergeSort(IsoFree)
        #if sizev==1:
        #    IsoFree.sort()
        #write_file(IsoFree,finpath)
        if Time==True:
            end=time.time()
            print('it cost {} hour'.format((end-start)/3600))
            
        return np.array(IsoFree).astype(int)
    
    # caring about orbit
    else:
        
        ### if the we already compute before, just read the result
        finpath=path+'n{}V{}E{}Orbit'.format(n,sizev,sizee)
        if connect==True:
            finpath+='_connect'

        if  exists(finpath+'.npy')==True:
            lis=load_file(finpath,n) 
            return np.array(lis).astype(int)

        ### otherwise, we generate the graph and count the orbits
        ppath=path+'n{}V{}E{}Graph'.format(n,sizev,sizee)
        if connect==True:
            ppath+='_connect'
        if  exists(ppath+'.npy')==False:
            lis=Generator(n,sizev,sizee,False,connect,False)
            write_file(lis,ppath)
        else:
            lis=load_file(ppath,n) 

        IsoFree=set()
        for l in lis:
            cg=lis2mat(l,n)

            for ref in range(n):
                K=Canonical(cg,ref)
                K_str = tuple(K)
                if K_str not in IsoFree:
                    IsoFree.add(K_str)
        
        IsoFree=[np.array(s).astype(int) for s in IsoFree]
        mergeSort(IsoFree)
        write_file(IsoFree,finpath)
        if Time==True:
            end=time.time()
            print('it cost {} hour'.format((end-start)/3600))
        return np.array(IsoFree).astype(int)

### input: colored graph G and reference point ref
### return: the statistics data that ref appear in the orbits
def Count(G,ref,k,sizev, sizee,connect=False):
    n=np.shape(G)[1]
    lis=Generator(k,sizev, sizee, True ,connect,False)
    ### swap ref, 0, so that ref=0
    p=Permutateij(n,ref,0)
    
    M= np.dot(np.dot(p,G),p)
    
    ### run through all possible size k subset that contain 0
    ### compute the canonical form and do the statistic
    C2 = list(combinations(list(range(1,n)),k-1))
    C2 = [list(i) for i in C2]
    statistics=len(lis)*[0]
    statistics = np.array(statistics).astype(int)
    for c in C2:
        cc=[0]+c
        matter = M[np.ix_(cc,cc)]
        ccf = Canonical( matter , 0)
        find_orb = BinarySearch(lis,ccf)
        if find_orb >= 0:
            statistics[find_orb] += 1         
        
#        for i in range(len(lis) ):
#            orb = lis[i]
#            if np.array_equal(ccf,orb):
#                statistics[i]+=1
    return statistics

def dicompare(G,pi,mu,l):
    A=zeros((l,l))
    B=zeros((l,l))
    for j in range(l):
        for i in range(l):
            A[i,j]=G[mu[i],mu[j]]
            B[i,j]=G[pi[i],pi[j]]
            
            
    A=mat2lis(A,True)
    B=mat2lis(B,True)
    t=LexicographicallyCompare(A,B)
    if t==-1:
        return 'Better'
    elif t==1:
        return 'Worse'
    else:
        return 'Equal'

### backtracking ver
def DiCanonical(GG,ref=-1):
    def BackTrackSearch(n,G,A,B):
        nonlocal BestExists 
        nonlocal mu
        nonlocal Res
        
        l=len(A)        
        
        if BestExists==True:
            Res=dicompare(G,A,mu,l)
      
        if l==n:
            if BestExists==False:
                mu=A
                BestExists=True

            else:  
                if Res=='Better':
                    mu=A

        else:
            ### if Res='Worse', we direct prune it
            ### that is, we do nothing
            if Res!='Worse':
                
                ### Choose is used to control the branch of the search tree
                Choose=copy(B)
                
                while len(Choose) > 0:

                    D=copy(B)
                    u=Choose[0]
                    D = D[D!=u]

                    ### construct the subtree
                    BackTrackSearch(n,G,A+[u],D)

                    Choose = Choose[Choose != u]

    n=np.shape(GG)[1]
    if ref>=1:
        p=Permutateij(n,ref,0)
        G = np.dot(np.dot(p,GG),p)
    else:
        G=GG

    
    ### mu is a permutation which record the canonical labeling
    mu=[]

    ### initial the default values
    BestExists=False
    Res='Better'
    
    ### start the bracktrack search    
    if ref==-1:
        BackTrackSearch(n,G,[],list(range(n)))
    else:
        BackTrackSearch(n,G,[0],list(range(1,n)))
    
    ### return the graph in canonical labeling

    A=zeros((n,n))
    for j in range(n):
        for i in range(n):
            A[i,j]=G[mu[i],mu[j]]

    return mat2lis(A,True)

def DiAddEdge(G,connect=False):
    n=np.shape(G)[1]
    IsoFree=set()
    GG=RecolorV(copy(G), n*[0])
    cg=mat2lis( GG,True)
    inn = int(n*(n-1))
    tup = list(product([1,0], repeat=inn) )
    
    for ss in tup:
        s=nd2d(ss,n)
        T=[cg[i]+s[i] for i in range(len(cg))]
        
        A= lis2mat(T,n)
        lab=DiCanonical(A)
        lab_str = tuple(lab)
        if lab_str not in IsoFree:
            
            if connect==True:
                if IsConnect(A)==False:
                    continue
            IsoFree.add(lab_str)
            
    outcome = np.array([np.array(s).astype(int) for s in IsoFree]).astype(int)
    mergeSort(outcome)
        
    return outcome

### do the same thing for digraph
def DiAddVertex(G,sizee, connect=False):
    n=np.shape(G)[1]
    IsoFree=set()
    cg=mat2lis(G,True)
    
    tup = list(product([ i for i in  range(sizee)], repeat = n))
    for s1 in tup:
        for s2 in tup:
            T= np.append(np.append(cg,s1),np.append([0],s2))
            M=lis2mat(T,n+1)
            lab=DiCanonical(M)
            lab_str = tuple(lab)
            if lab_str not in IsoFree:

                if connect==True:
                    if IsConnect(M)==False:
                        continue
                IsoFree.add(lab_str)
                
    outcome = np.array([np.array(s).astype(int) for s in IsoFree]).astype(int)
    mergeSort(outcome)
        
    return outcome

def DiGenerator(n,sizev, sizee, orbg=False ,connect=False,Time=True):
    start=time.time()    
    if orbg==False:
        finpath=path+'n{}V{}E{}DiGraph'.format(n,sizev,sizee)
        if connect==True:
            finpath+='_connect'

        if  exists(finpath+'.npy')==True:
            lis=load_file(finpath,n) 
            return lis
        
        if sizev==1:

            if n==3:
                if sizee==2:
                    ppath=path+'n{}V1E{}DiGraph'.format(n,2)
                    if connect==True:
                        ppath+='_connect'
                    if connect==True:
                        lis=[[0, 0, 0, 0, 0, 0, 0, 1, 1],[0, 0, 0, 0, 0, 1, 0, 0, 1],[0, 0, 0, 0, 0, 1, 0, 1, 1],[0, 0, 0, 0, 1, 1, 0, 0, 0],[0, 0, 0, 0, 1, 1, 0, 0, 1],[0, 0, 0, 0, 1, 1, 0, 1, 1],[0, 0, 0, 1, 0, 0, 0, 1, 1],[0, 0, 0, 1, 0, 1, 0, 1, 1],[0, 0, 0, 1, 1, 0, 0, 1, 0],[0, 0, 0, 1, 1, 0, 0, 1, 1],[0, 0, 0, 1, 1, 1, 0, 0, 1],[0, 0, 0, 1, 1, 1, 0, 1, 1],[0, 1, 0, 1, 1, 1, 0, 1, 1]]
                    else:
                        lis=[[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 1],[0, 0, 0, 0, 0, 0, 0, 1, 1],[0, 0, 0, 0, 0, 1, 0, 0, 1],[0, 0, 0, 0, 0, 1, 0, 1, 0],[0, 0, 0, 0, 0, 1, 0, 1, 1],[0, 0, 0, 0, 1, 1, 0, 0, 0],[0, 0, 0, 0, 1, 1, 0, 0, 1],[0, 0, 0, 0, 1, 1, 0, 1, 1],[0, 0, 0, 1, 0, 0, 0, 1, 1],[0, 0, 0, 1, 0, 1, 0, 1, 1],[0, 0, 0, 1, 1, 0, 0, 1, 0],[0, 0, 0, 1, 1, 0, 0, 1, 1],[0, 0, 0, 1, 1, 1, 0, 0, 1],[0, 0, 0, 1, 1, 1, 0, 1, 1],[0, 1, 0, 1, 1, 1, 0, 1, 1]]
                        
                    lis = np.array(lis).astype(int)
                    write_file(lis,ppath)
                    return lis

                #else
                ppath=path+'n{}V1E{}DiGraph'.format(n,sizee-1)
                if connect==True:
                    ppath+='_connect'
                if  exists(ppath+'.npy')==False:
                    lis=DiGenerator(n,1,sizee-1,False,connect,False)
                    write_file(lis,ppath)
                else:
                    lis=load_file(ppath,n) 


                which_one='adde'

            if n>3:
                ppath=path+'n{}V1E{}DiGraph'.format(n-1,sizee)
                if connect==True:
                    ppath+='_connect'
                if  exists(ppath+'.npy')==False:
                    lis=DiGenerator(n-1,1,sizee,False,connect,False)
                    write_file(lis,ppath)
                else:
                    lis=load_file(ppath,n-1) 

                which_one='addp'

        else:
            # sizev > 1
            VL=list(range(sizev))

            ppath=path+'n{}V1E{}DiGraph'.format(n,sizee)
            if connect==True:
                ppath+='_connect'
            
            if  exists(ppath+'.npy')==False:
                lis=DiGenerator(n,1,sizee,False,connect,False)
                write_file(lis,ppath)
            else:
                lis=load_file(ppath,n) 
                
            which_one='addc'
        IsoFree=set()
        if which_one=='adde':
            for g in lis:
                for t in DiAddEdge(lis2mat(g,n), connect):
                    t_str = tuple(t)
                    if t_str not in IsoFree:
                        IsoFree.add(t_str)
        elif which_one=='addp':
            for g in lis:
                for t in DiAddVertex(lis2mat(g,n-1),sizee, connect):
                    t_str = tuple(t)
                    if t_str not in IsoFree:
                        IsoFree.add(t_str)
        elif which_one=='addc':
            for l in lis:

                ll=lis2mat(l,n)
                tup = list(product(VL, repeat = n))
                for s in tup:
                    t=DiCanonical((RecolorV(ll,s)))
                    t_str = tuple(t)
                    if t_str not in IsoFree:
                        IsoFree.add(t_str)
        IsoFree=[np.array(s).astype(int) for s in list(IsoFree)]
        mergeSort(IsoFree)

        tmp = np.array(IsoFree).astype(int)
        write_file(tmp,finpath)
        if Time==True:
            end=time.time()
            print('it cost {} hour'.format((end-start)/3600))
        return tmp
    
    else:
        finpath=path+'n{}V{}E{}DiOrbit'.format(n,sizev,sizee)
        if connect==True:
            finpath+='_connect'

        if  exists(finpath+'.npy')==True:
            lis=load_file(finpath,n)
            return lis
    
        ppath=path+'n{}V{}E{}DiGraph'.format(n,sizev,sizee)
        if connect==True:
            ppath+='_connect'
        if  exists(ppath+'.npy')==False:
            lis=DiGenerator(n,sizev,sizee,False,connect,False)
            write_file(lis,ppath)
        else:
            lis=load_file(ppath,n)

        IsoFree=set()
        for l in lis:

            cg=lis2mat(l,n)
            for ref in range(n):
                K=DiCanonical(cg,ref)
                K_str = tuple(K)
                if K_str not in IsoFree:
                    IsoFree.add(K_str)
                    
        IsoFree=[np.array(s).astype(int) for s in IsoFree]
        
        mergeSort(IsoFree)
        tmp = np.array(IsoFree).astype(int)
        write_file(tmp,finpath)
        if Time==True:
            end=time.time()
            print('it cost {} hour'.format((end-start)/3600))
        
        return tmp

def DiCount(G,ref,k,sizev, sizee,connect=False):
    n=np.shape(G)[1]
    lis=DiGenerator(k,sizev, sizee, True ,connect,False)
    ### swap ref, 0, so that ref=0
    p=Permutateij(n,ref,0)
   
    M= np.dot(np.dot(p,G),p)
   
    ### run through all possible size k subset that contain 0
    ### compute the canonical form and do the statistic
    C2 = list(combinations(list(range(1,n)),k-1))
    C2 = [list(i) for i in C2]
    statistics=len(lis)*[0]
    statistics = np.array(statistics).astype(int)
    
    count = 1
    for c in C2:
        cc=[0]+c
        matter = M[np.ix_(cc,cc)]
        ccf = DiCanonical( matter , 0)
        
        find_orb = BinarySearch(lis,ccf)
        if find_orb >= 0:
            statistics[find_orb] += 1
        
        #for i in range(len(lis)):
        #    orb = lis[i]
        #    if np.array_equal(ccf,orb):
        #        statistics[i]+=1
    return statistics


