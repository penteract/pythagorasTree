"""
This library provides functions for working with fractals which can be broken into a set of pieces,
each of which are composed of 4 other pieces in the set, scaled linearly by a factor of 2.
(e.g. a picture in a square is composed of it's 4 corners)
"""

"""
import sympy
def var(tup):
    #print(repr("x_"+"_".join(map(lambda t:f"{t[0]}{t[1]}{t[2]}" ,tup))))
    return sympy.var("x_"+"_".join(map(lambda t:f"{t[0]}{t[1]}{t[2]}" ,tup)))
print("constructing a system of linear equations")
eqns = [
    var(can)*4 - sum(var(x) for x in eMap[can] if len(x))
    for can in eMap
    ]
print(eqns[0])
from sympy.solvers.solveset import linsolve
IDs = list(eMap)
rIDs = {t:ix for ix,t in enumerate(IDs)}
print("solving system of linear equations")
res = linsolve(eqns,list(map(var,IDs)))
print("number of solutions: ",len(res))
res=list(res)[0]"""

#TODO: rotations+reflections (cannonicalization) and known full nodes

def from_nondet(system,starting,cannonical=None):
    """ system[Key] = {0:[Key],1:[Key],2:[Key],3:[Key]}
       starting = [Key] | [tuple[Key]]
       cannonical(tuple[Key]) = tuple[Key]
       cannoncical(cannonical(x))==cannonical(x)
       Given a system where a piece may be described in terms of overlapping pieces,
       return one where a piece is described in terms of non overlapping pieces.
       The returned system is limited to those nodes which can be reached from `starting`.
       This is equivalent to a transformation from a non-deterministic automaton to a deterministic automaton
       result[tuple[Key]] = (tuple[Key],tuple[Key],tuple[Key],tuple[Key]) """
    if cannonical==None:
        cannonical = lambda x:x
    l = list(starting)
    if l[0] in system:
        # the starting pieces are single tiles, not lists of overlapping ones
        l = [cannonical((x,)) for x in l]
    seen = set(l)
    eMap={}
    for ps in l:
        if ps not in eMap:
            eMap[ps]= tuple([cannonical(tuple(sorted(set(p2 for p in ps for p2 in system[p][lab])))) for lab in range(4)])
            for ks in eMap[ps]:
                if ks not in seen:
                    l.append(ks)
                    seen.add(ks)
    return eMap

def getArea(eMap):
    #todo: consider full nodes
    import sympy
    def var(tup):
        s = str(tup)
        for c in "() ,-+":
            s=s.replace(c,"_")
        return sympy.var("x_"+s)
    print("constructing a system of linear equations")
    eqns = [
        var(can)*4 - sum(var(x) for x in eMap[can] if len(x))
        for can in eMap
        ]
    #print(eqns[0])
    from sympy.solvers.solveset import linsolve
    IDs = list(eMap)
    rIDs = {t:ix for ix,t in enumerate(IDs)}
    print("solving system of linear equations")
    sols = linsolve(eqns,list(map(var,IDs)))
    if len(sols)==0:
        print("No solutions found (unexpected)")
        return None
    sol = list(sols)[0]
    #if len(sols)==1:
    aMap = {c: sol[rIDs[c]] for c in rIDs}
    return aMap

def uget(a,ufds):
    while a!=(a:=ufds[a]):
        pass
    return a

def findCCs(g):
    components = []
    bestNodes = [None]
    seen = set()
    ufds = {}
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
            target = uget(nxt,ufds) # target is the earliest on the path that we know is in the SCC
            if target in pathSet:
                i = len(path)-1
                while uget(path[i][0],ufds) != target:
                    ufds[path[i][0]]=target
                    i-=1
            elif nxt in seen:
                continue
            else:
                seen.add(nxt)
                pathSet.add(nxt)
                path.append((nxt,list(g[nxt])))
    return components,ufds

def iterate(eMap, mp, d = 2, N = 1000):
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

def bsearch(eMap,mp,bot=1.0,top=2.0):
    steps=0
    while (mid:=(top+bot)/2) not in [top,bot]:
        hi,mp,n = iterate(eMap,mp,mid)
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

def findDim(eMap):
    comps,ufds = findCCs(eMap)
    dd = {c:[x for x in ufds if uget(x,ufds)==c] for c in comps}
    mp = {k:1 for k in dd[list(dd)[-1]]}
    result = bsearch(eMap,mp)
    lb,ub,steps,mp = result
    return result

def mkFile(eMap, mp, fname):
    """produce a description of the system for accurately computing the dimension
    given eMap[Key]=(Key,Key,Key,Key), mp[Key]=float, fname= string"""
    #reduce the system
    from collections import defaultdict
    classes = defaultdict(list)
    for k,v in mp.items():
        classes[round(v,5)].append(k)
    def reducedSub(k):
        return tuple(sorted(round(mp[x],5) for x in eMap[k] if x in mp))
    newmp = {}
    neweMap = {**eMap}
    reduced=False
    for rv in classes:
        r0 = reducedSub(k0:=classes[rv][0])
        newmp[k0]=mp[k0]
        for k in classes[rv]:
            if (rk := reducedSub(k))!=r0:
                #print("reduction doesn't work, not reducing")
                break
            neweMap[k] = tuple(classes[round(mp[x],5)][0] if x in mp else x for x in eMap[k])
        else:
            continue
        break
    else:
        if len(mp)!=len(newmp):
            reduced=True
        eMap=neweMap
        mp=newmp
    #print the system
    fl = open(fname,"w")
    l=list(mp)
    rl = {}
    for i,k in enumerate(l):
        rl[k]=i
    N=len(l)
    print(f"Saving a {'reduced '*reduced}representation of the system to '{fname}' for computing the fractal dimension with high precision")
    print(N,file=fl)
    for k in l:
        print(*[rl[x] if x in rl else N for x in eMap[k]], mp[k] ,file=fl)

def studyFractal(nondetSystem, starting, name):
    print(f"Properties of {name}:")
    eMap = from_nondet(nondetSystem, starting)
    aMap = getArea(eMap)
    a = sum(aMap[c] for c in starting)
    print(f"Area: {a}")
    lb,ub,steps,mp = findDim(eMap)
    print(f"The dimension of This fractal is between {lb} and {ub} (with caveats about floating point precision)")
    print(f"  calculated in a total of {steps} steps")
    mkFile(eMap,mp,name.replace(" ","_")+"_DimFinder.txt")
    if a>0:
        return aMap
    else:
        return mp
    

    
    

if False:
    rEMap = {}
    for k in eMap:
        for p in eMap[k]:
            if p not in rEMap:
                rEMap[p]=[]
            rEMap[p].append(k)
            
    empty = tuple()
    layer=[empty]
    n=0
    subOne = {empty:0} # dictionary of things with an area known to be less than 1.
    #the largest known hole in a piece p should be of size 0.5**subOne[p]
    while layer: #bfs
        n+=1
        nextLayer = []
        for k in layer:
            for p in rEMap[k]:
                if p not in subOne:
                    subOne[p]=n
                    nextLayer.append(p)
        layer = nextLayer

    empties = [empty]
    se=set(empties)
    for x in empties:
        for k in rEMap[x]:
            if k not in se and all(j in se for j in eMap[k] ):
                empties.append(k)
                se.add(k)
    print(len(empties))
    print("Number of pieces with a hole at a particular depth:")
    print({k:len([x for x in subOne if subOne[x]==k]) for k in subOne.values()})


    #lb,ub,steps,mp = bsearch(mp)
    #print(f"The dimension of Levy dragon is between {lb} and {ub} (with caveats about floating point precision)")
    #print(f"  calculated in a total of {steps} steps")

    print(f"The dimension of This fractal is between {lb} and {ub} (with caveats about floating point precision)")
    print(f"  calculated in a total of {steps} steps")
    import sys
    sys.argv.append("reduce")
    if "reduce" in sys.argv:
        from collections import defaultdict
        classes = defaultdict(list)
        for k,v in mp.items():
            classes[round(v,5)].append(k)
        def reducedSub(k):
            return tuple(round(mp[x],5) for x in eMap[k] if x in mp)
        newmp = {}
        neweMap = {**eMap}
        for rv in classes:
            r0 = reducedSub(k0:=classes[rv][0])
            newmp[k0]=mp[k0]
            for k in classes[rv]:
                if (rk := reducedSub(classes[rv][0]))!=r0:
                    print("bad reduction")
                    break
                neweMap[k] = tuple(classes[round(mp[x],5)][0] if x in mp else x for x in eMap[k])
            else:
                continue
            break
        else:
            eMap=neweMap
            mp=newmp
    if "print_system" in sys.argv:
        fl = open("star_system.txt","w")
        l=list(mp)
        rl = {}
        for i,k in enumerate(l):
            rl[k]=i
        N=len(l)
        print(N,file=fl)
        for k in l:
            print(*[rl[x] if x in rl else N for x in eMap[k]], mp[k] ,file=fl)

