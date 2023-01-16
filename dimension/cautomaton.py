#from heapq import merge
import operator as op
import itertools
#(bottom left is (0,0))
grid = [[y*7+x for y in range(4)] for x in range(7)]

#EMPTY=-1
#grid[0][3] = EMPTY
#grid[6][3] = EMPTY
#grid[3][0] = EMPTY

#[[0, 7, 14, 21],
# [1, 8, 15, 22],
# [2, 9, 16, 23],
# [3, 10, 17, 24],
# [4, 11, 18, 25],
# [5, 12, 19, 26],
# [6, 13, 20, 27]]
#FULL = grid[3][0]

#syms = {EMPTY:EMPTY}
syms={}
grids = [grid]
for i in range(3):
    g=grids[-1]
    ng = list(zip(*reversed(g)))
    grids.append ([[ syms[x] if x in syms else x+(4*7) for x in r] for r in ng])

edges = {}
for rot in grids:
    for col in rot:
        for ID in col:
            edges[ID] = ([],[],[],[])

def addEdge(frm,cor,to):
    #print(frm,cor,to)
    if to not in edges[frm][cor]:
        edges[frm][cor].append(to)

def rotate(ID,n):
    n=n%4
    if n==0:
        return ID
    else:
        return rotate(syms[ID] if ID in syms else (ID+(4*7))%(4*4*7),n-1)


dxdyToCor = {(0,0):0,(0,1):1,(1,1):2,(1,0):3}
# Add the 4 subtrees 1/4 of the area
def insertCorner(x,y,ID):
    addEdge(grids[0][x//2][y//2],dxdyToCor[x%2,y%2],ID)

def addCopy(gr,sx,sy):
    """Add a copy of the grid with lower left at position (sx/2,sy/2)"""
    for x,r in enumerate(gr,sx):
        for y,c in enumerate(r,sy):
            insertCorner(x,y,c)
addCopy(grids[0],2,4)
addCopy(grids[0],5,4)
addCopy(grids[1],9,0)
addCopy(grids[3],1,0)

for i in range(3):
    for ID in sum(grids[i],[]):
        for cr,l in enumerate(edges[ID]):
            rot = rotate(ID,1)
            if edges[rot][(cr+1)%4]:
                print(ID,rot,cr,edges[rot][(cr+1)%4])
            assert not edges[rot][(cr+1)%4]
            for t in l:
                addEdge(rot,(cr+1)%4,rotate(t,1))

for quad in edges:
    for es in edges[quad]:
        es.sort()

def merge(*args):
    l = []
    for a in args:
        a=iter(a)
        nw = []
        i=0
        try:
            na = next(a)
            while i<len(l):
                if l[i]==na:
                    nw.append(na)
                    i+=1
                    na=next(a)
                elif l[i]<na:
                    nw.append(l[i])
                    i+=1
                else:
                    nw.append(na)
                    na=next(a)
        except StopIteration as e:
            while i<len(l):
                nw.append(l[i])
                i+=1
            l=nw
            continue
        nw.append(na)
        nw.extend(a)
        l=nw
    if any(map(op.eq,l,l[1:])):
        print(args,l)
    return l
    
Zs=0
def area(IDs):
    """Given a list of IDs, return a lower bound and upper bound for the area of the region times 4"""
    if len(IDs)==0:
        return (4,4)
    else:
        return (0,4)

cache = {}
def cash(f):
    def g(IDs,depth):
        t=tuple(IDs)
        """if t in cache:
            print(cache[t])"""
        if t not in cache or cache[t][0]<depth:
            """if t in cache:
                c=cache[t]
                a=max(a,c[1][0])
                b=min(b,c[1][1])"""
            cache[t] = (depth, f(IDs,depth))
        c=cache[t]
        return tuple( x / (4**(c[0]-depth)) for x in c[1])
    return g

@cash
def sqArea(IDs,depth):
    a,b = area(list(IDs) if depth>0 else IDs)
    if depth==0 or a==b:
        return (a<<2*depth,b<<2*depth)
    sa,sb = 0,0
    for i in range(4):
        da,db = sqArea(list(merge(*(edges[ID][i] for ID in IDs))),depth-1)
        sa+=da
        sb+=db
    return (sa,sb)
def draw(IDs,depth):
    if depth==0:
        (a,b)=area(list(IDs))
        if a==3:
            print(IDs)
        return [" ?+&#"[a]]
        if a==4:
            return ["#"]
        if a==0:
            return [" "]
        else:
            return ["+"]
    else:
        return (
            list(map(op.add, draw(list(merge(*(edges[ID][1] for ID in IDs))),depth-1),
                        draw(list(merge(*(edges[ID][2] for ID in IDs))),depth-1)))
            +list(map(op.add, draw(list(merge(*(edges[ID][0] for ID in IDs))),depth-1),
                        draw(list(merge(*(edges[ID][3] for ID in IDs))),depth-1)))
            )

def drawAll(depth):
    res=[]
    print("\n".join(itertools.chain(*(map((lambda *args:"".join(args)), *(draw([grids[0][x][y]],depth) for x in range(7))) for y in range(3,-1,-1) )) ))
if __name__=="__main__":
    import sys
    if len(sys.argv)==2: drawAll(int(sys.argv[1]))

def reflect(ID):
    """reflect across a vertical axis"""
    (q,r) = divmod(ID,(4*7))
    y,x = divmod(r,7)
    return rotate(7*y+(6-x) ,-q)

empties = [rotate(grids[0][x][y],i) for i in range(4) for x,y in [(0,3),(6,3),(3,0),(3,1)]]

def canonical(IDs):
    #return tuple(IDs)
    IDs = list(ID for ID in IDs if ID not in empties)
    if area(list(IDs))==(4,4):
        return tuple()
    rots = [sorted(rotate(ID,n) for ID in ids if ID not in empties) for n in range(4) for ids in [IDs,list(map(reflect,IDs))]]
    #for x in rots: print(x)
    return tuple(min(rots))

def hedges(IDs):
    return tuple(canonical(merge(*(edges[ID][i] for ID in IDs))) for i in range(4))

seen = set()
l=list(set(canonical([c]) for r in grids[0] for c in r))
eMap={}
for IDs in l:
    if IDs not in eMap:
        eMap[IDs] = hedges(IDs)
        for nxt in eMap[IDs]:
            if nxt not in seen:
                seen.add(nxt)
                l.append(nxt)
print(len(seen),len(l),len(eMap))
import fractalCalc

eMap2 = fractalCalc.from_nondet(edges,[c for r in grids[0] for c in r],canonical)

print(len(eMap),len(eMap2))

#eMap=eMap2    
def uget(a,ufds):
    while a!=(a:=ufds[a]):
        pass
    return a

def findCCs(g):
    components = []
    bestNodes = [None]
    seen = set()
    ufds = {}
    def uget(a):
        while a!=(a:=ufds[a]):
            pass
        return a
    #def union(a,b):
    #    a=uget(a)
    #    while b!=ufds[b]:
    #        b,ufds[b] = ufds[b],a
    #    ufds[b] = a
    for node in g:
        ufds[node]=node
    for node in g:
        if node in seen:
            continue
        edgs = list(g[node])
        path = [(node,edgs)] #path to current node
        pathSet = {node}
        seen.add(node)
        
        while path:
            n,es = path[-1]
            if not es:
                if ufds[n]==n:
                    components.append(n)
                path.pop()
                pathSet.remove(n)
                continue
            nxt = es.pop()
            target = uget(nxt) # target is the earliest on the path that we know is in the SCC
            if target in pathSet:
                i = len(path)-1
                while uget(path[i][0]) != target:
                    ufds[path[i][0]]=target
                    i-=1
            elif nxt in seen:
                continue
            else:
                seen.add(nxt)
                pathSet.add(nxt)
                path.append((nxt,list(g[nxt])))
    return components,ufds





import sympy
def var(tup):
    return sympy.var("x_"+"_".join(map(str,tup)))
print("constructing a system of linear equations")
eqns = [
    var(can)*4 - sum(var(x) for x in eMap[can])
    for can in eMap
    ]+[var(())-1]
from sympy.solvers.solveset import linsolve
IDs = list(eMap)
rIDs = {t:ix for ix,t in enumerate(IDs)}


print("solving system of linear equations")
varList = list(map(var,IDs))
ress1 = linsolve(eqns,varList)
#print("number of solutions: ",len(res))
res=list(ress1)[0]
#print("The exact answer (with a free variable):", sol:=28-sum(res[rIDs[canonical([c])]] for r in grids[0] for c in r))

rgs = [(i,res[i].args) for i,x in enumerate(IDs) if len(res[i].args)==2]
minv,mini = min((args[0],i) for i,args in rgs)
#print(res[mini])
eqns.append(res[mini])
ress2 = linsolve(eqns,varList)
print("solving another linear equations")#this could be avoided since we've already done the work
#print("number of solutions: ",len(res))
res=list(ress2)[0]
print("The exact area of the Levy dragon:", sol:=28-sum(res[rIDs[canonical([c])]] for r in grids[0] for c in r))
#print("The exact answer as a decimal",float(sol))
#print(minv,mini)

# Work out dimension
comps,ufds = findCCs(eMap)
dd = {c:[x for x in ufds if uget(x,ufds)==c] for c in comps}

def iterate(mp, d = 2, N = 1000):
    omp = mp
    tst = next(iter(mp))
    for i in range(N):
        mp = { k : sum(mp[ch] for ch in eMap[k] if ch in mp)/(2**d) for k in mp}
        sgn = mp[tst]>=omp[tst]
        for k in mp:
            if (mp[k]>=omp[k])!=sgn:
                break
        else:
            return sgn,mp,i
    return (None,mp,N)

mp = {k:1 for k in dd[7,]} # using the area (1-res[rIDs[k]]) is not a better starting point  (338 steps vs 119)

def bsearch(mp):
    bot = 1.9
    top = 2.0
    steps=0
    while (mid:=(top+bot)/2) not in [top,bot]:
        hi,mp,n = iterate(mp,mid)
        steps += n+1
        if hi is None:
            return (bot,top,steps)
        if hi:
            bot = mid
        else:
            top = mid
    return (bot,top,steps,mp)


def syms(mp,delta=0.0001):
    res={}
    for k in mp:
        for j in res:
            if abs(mp[k]-mp[j])<delta:
                res[j].append(k)
                break
        else:
            res[k] = [k]
    return res

lb,ub,steps,mp = bsearch(mp)
print(f"The dimension of the boundary of the Levy dragon is between {lb} and {ub} (with caveats about floating point precision)")
print(f"  calculated in a total of {steps} steps")

if True:
    """Print a description of the system for a high precision library to give more precise bounds on the dimension"""
    fl = open("vs.txt","w")
    l=list(mp)
    rl = {}
    for i,k in enumerate(l):
        rl[k]=i
    N=len(l)
    print(N,file=fl)
    for k in l:
        print(*[rl[x] if x in rl else N for x in eMap[k]], mp[k] ,file=fl)

"""
try:
    from bigfloat import *
except ModuleNotFoundError as e:
    print("install the bigfloat package to get more precision about the dimension (when I implement that)")
"""

#Should print: 12823413011547414368862997525616691741041579688920794331363953564934456759066858494476606822552437442098640979/877512406035620068631903180662851572553488753575243048137500508983979170248733422547196905684808937723408093
#print("Aproximate value as a decimal:",float(sol))
#Should print: 14.613369478706703

def toBitmap(IDs,depth):
    """return a list of byteStrings that can be made into a bitmap"""
    if depth==0:
        c = res[rIDs[canonical(IDs)]]
        ## Doing this sRGB is technically more correct (I think it's closer to what you
        ## would see with bad eyesight at a distance from a higher resolution monitor showing a more detailed image)
        ## but is less informative because it makes it harder to percive differences in brightness
        ## among pixels with values between 0.5 and 1 (I suspect that most pixels which are neither full nor empty lie in this interval)
        #if c==1:
        #    return [b"\xff"]
        #srgb = 1.055*(c**(1/2.4)) - 0.055 if c>0.0031308 else 12.92*c
        #return [bytes([int(srgb*255)])]
        return [bytes([ int(res[rIDs[canonical(IDs)]]*255) ])]
    else:
        return (
            list(map(op.add, toBitmap(list(merge(*(edges[ID][1] for ID in IDs if ID!=-1))),depth-1),
                        toBitmap(list(merge(*(edges[ID][2] for ID in IDs if ID!=-1))),depth-1)))
            +list(map(op.add, toBitmap(list(merge(*(edges[ID][0] for ID in IDs if ID!=-1))),depth-1),
                        toBitmap(list(merge(*(edges[ID][3] for ID in IDs if ID!=-1))),depth-1)))
            )

def saveBitmap(depth,fileName):
    #res=[]
    from PIL import Image
    img = Image.frombytes("L",(7*2**depth,4*2**depth),
                        b"".join(
                            itertools.chain(*(map((lambda *args:b"".join(args)),
                                                 *(toBitmap([grids[0][x][y]],depth) for x in range(7)))
                                              for y in range(3,-1,-1) )) ))
    img.save(fileName)

"""
for i in [10,13,15,17,19,20]:
    # starting with i=20 is much slower
    print(sum(sqArea([c],i)[0] for r in grids[0] for c in r)/(1<<(2*(i+1))) )
"""
