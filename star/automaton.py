from pprint import pp
"""
Pieces are identified by being one of 6 triangles in a hexagon, and the 2 most recent point selections that lead to that

These shapes have the form (t,recent,prev) where the shape is the empty set if t not in {recent,(recent-1)%6} and
((t+i)%6, (recent+i)%6,  (prev+i)%6) is a rotation of (t,recent,prev) by (i*pi)/3 radians.
recent != (prev+1)%6 may also be assumed

Subtriangles of a triangle are identified as follows (these correspond to labels of the automaton):
        /\
       /  \
      / 0  \
     /------\
    / \  3 / \
   / 2 \  / 1 \
  /-----\/-----\


\-----/\-----/
 \ 0 /  \ 1 /
  \ / 3  \ /
   \------/
    \  2 /
     \  /
      \/
"""

# positions of centers of subtriangles relative to the center of the triangle (center of (sub)triangle meaning center of axis aligned rectangle containing triangle)
tup = {
    0: (0,1),
    2: (-1,-1),
    3: (0,-1),
    1: (1,-1),
    }

tdown = {
    0: (-1,1),
    3: (0,1),
    1: (1,1),
    2: (0,-1)
    }

"""
corners of the hexagon (recent,prev) and pieces (t) are identifed as follows:

 0       1 
   /-----\
  / \ 0 / \
 / 5 \ / 1 \
5----------- 2
 \ 4 / \ 2 /
  \ / 3 \ /
   \-----/ 3
   4
"""


# positions of corners of a stretched hexagon
corners = [(-2,4),(2,4),(4,0),(2,-4),(-2,-4),(-4,0)]


# positions of the center of the axis aligned square containing each triangular piece
pieces = {}
for i,p in enumerate([5,0,1]):
    pieces[p] = (2*i-2,2)

for i,p in enumerate([4,3,2]):
    pieces[p] = (2*i-2,-2)

subPieceAt = {}
for p in pieces:
    x,y = pieces[p]
    tri = [tdown,tup][p%2]
    for sub in tri:
        dx,dy = tri[sub]
        subPieceAt[(x+dx,y+dy)] = (p,sub)


def getEdges(t, recent, prev):
    """lists subtriangles with edges from the given triangle
    (i.e. which subtriangles include shrunk copies of (t,recent,prev))"""
    #print(t,recent,prev)
    for c in range(6):
        if c not in [(recent+1)%6, (prev-1)%6]:
            x,y = pieces[t]
            cx,cy = corners[c]
            newt,subt = subPieceAt[(x+cx)/2,(y+cy)/2]            
            yield ((newt,c,recent), subt)
compositions = {k:[] for k in range(6)}
edges = {}

def drawTri(t, orientation, depth, subfn, drawfn):
    if depth == 0:
        yield drawfn(t)
    elif orientation=="u":
        for k in drawTri(subfn(t,0),"u",depth-1,subfn,drawfn):
            yield k
        for k in hconcat(drawTri(subfn(t,2),"u",depth-1,subfn,drawfn),
                         drawTri(subfn(t,3),"d",depth-1,subfn,drawfn),
                         drawTri(subfn(t,1),"u",depth-1,subfn,drawfn) ):
            yield k
    elif orientation=="d":
        for k in hconcat(drawTri(subfn(t,0),"d",depth-1,subfn,drawfn),
                         drawTri(subfn(t,3),"u",depth-1,subfn,drawfn),
                         drawTri(subfn(t,1),"d",depth-1,subfn,drawfn)):
            yield k
        for k in drawTri(subfn(t,2),"d",depth-1,subfn,drawfn):
            yield k
    else:
        raise Exception("unknown orientation")

def hconcat(*args):
    for x in zip(*args):
        yield "".join(x)

for recent in range(6):
    for prev in range(6):
        for t in range(6):
            edges[t,recent,prev] = {k:[] for k in range(4)}
for recent in range(6):
    for prev in range(6):
        if prev!=(recent-1)%6:
            for t in range(6):#[(recent-1)%6, recent]:
                piece = (t,recent,prev)
                compositions[t].append(piece)
                for (src,lab) in getEdges(*piece):
                    edges[src][lab].append(piece)

def countTri(t, orientation, depth, subfn, drawfn):
    tot=0
    if depth == 0:
        return drawfn(t)
    elif orientation=="u":
        tot+=countTri(subfn(t,0),"u",depth-1,subfn,drawfn)
        tot+=sum([countTri(subfn(t,2),"u",depth-1,subfn,drawfn),
                         countTri(subfn(t,3),"d",depth-1,subfn,drawfn),
                         countTri(subfn(t,1),"u",depth-1,subfn,drawfn) ])
    elif orientation=="d":
        tot+=sum([countTri(subfn(t,0),"d",depth-1,subfn,drawfn),
                         countTri(subfn(t,3),"u",depth-1,subfn,drawfn),
                         countTri(subfn(t,1),"d",depth-1,subfn,drawfn)])
        tot+=countTri(subfn(t,2),"d",depth-1,subfn,drawfn)
    else:
        raise Exception("unknown orientation")
    return tot
id=lambda x:x

def srtrmdups(ts):
    l = sorted(ts)
    ps = [a for a,b in zip(l,l[1:]+[None]) if a!=b]
    return ps
print("\n".join(drawTri([(5,0,0)],"u",5,(lambda ys,b:srtrmdups([x for a in ys for x in edges[a][b]])),lambda l:" " if len(l)==0 else"#")))

for i in range(8):
    print(countTri([(5,0,4)],"u",i,(lambda ys,b:sorted(set([x for a in ys for x in edges[a][b]]))),lambda l:len(l)>0 ))

l = list(map(tuple,compositions.values()))
seen = set(l)
eMap = {}
for ps in l:
    if ps not in eMap:
        eMap[ps]= [tuple(sorted(set(p2 for p in ps for p2 in edges[p][lab]))) for lab in range(4)]
        for ks in eMap[ps]:
            if ks not in seen:
                l.append(ks)
                seen.add(ks)
                
print(len(l))
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

def bsearch(mp,bot=1.5,top=2.0):
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
comps,ufds = findCCs(eMap)
dd = {c:[x for x in ufds if uget(x,ufds)==c] for c in comps}
#lb,ub,steps,mp = bsearch(mp)
#print(f"The dimension of Levy dragon is between {lb} and {ub} (with caveats about floating point precision)")
#print(f"  calculated in a total of {steps} steps")

mp = {k:1 for k in dd[list(dd)[-1]]}
lb,ub,steps,mp = bsearch(mp)
print(f"The dimension of This fractal is between {lb} and {ub} (with caveats about floating point precision)")
print(f"  calculated in a total of {steps} steps")
