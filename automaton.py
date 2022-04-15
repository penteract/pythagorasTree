#from heapq import merge
import operator as op
import itertools
#(bottom left is (0,0))
grid = [[y*7+x for y in range(4)] for x in range(7)]

EMPTY=-1
grid[0][3] = EMPTY
grid[6][3] = EMPTY

#[[0, 7, 14, 21],
# [1, 8, 15, 22],
# [2, 9, 16, 23],
# [3, 10, 17, 24],
# [4, 11, 18, 25],
# [5, 12, 19, 26],
# [6, 13, 20, 27]]
FULL = grid[3][0]

syms = {FULL:FULL, EMPTY:EMPTY, 10+(4*7):10}
grids = [grid]
for i in range(3):
    g=grids[-1]
    ng = list(zip(*reversed(g)))
    grids.append ([[ syms[x] if x in syms else x+(4*7) for x in r] for r in ng])

#cors[0] is a triangle covering the lower left half of a square
#21 is used since it's empty
cors =[21,21+7*4,21+7*4*2,21+7*4*3]

edges = {}
for rot in grids:
    for col in rot:
        for ID in col:
            if ID!=EMPTY:
                edges[ID] = ([],[],[],[])
for cor in cors:
    edges[cor]=([],[],[],[])

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

for i in range(4):
    addEdge(FULL,i,FULL)
#describe how triangles work
for i in range(4):
    addEdge(cors[i],i,FULL)
    addEdge(cors[i],(i+1)%4,cors[i])
    addEdge(cors[i],(i+3)%4,cors[i])

#draw the squares of area 1/2
addEdge(10,0,cors[1])
addEdge(10,1,cors[0])
addEdge(10,2,cors[3])
addEdge(10,3,cors[2])
addEdge(9,3,cors[2])
addEdge(9,2,cors[3])
addEdge(11,0,cors[1])
addEdge(11,1,cors[0])


dxdyToCor = {(0,0):0,(0,1):1,(1,1):2,(1,0):3}
# Add the 4 subtrees 1/4 of the area
def insertCorner(x,y,ID):
    if ID != EMPTY:
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
        if ID not in [FULL,EMPTY,38] and (ID,i)!=(10,2) :
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
    if IDs==[-1]:
        return (0,0)
    if FULL in IDs:
        return (4,4)
    cs=[]
    for i in range(len(IDs)-1,-1,-1):
        if IDs[i] in cors:
            cs.append(IDs.pop(i))
    a=0
    if len(cs)>2:
        a=4
    elif len(cs)==1:
        a=2
    elif len(cs)==2:
        if abs(cs[0]-cs[1])==7*4*2:
            a=4
        else:
            a=3
    if len(IDs)==0:
        return (a,a)
    else:
        return (a,4)

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
    if IDs==[-1]:
        return (0,0)
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
            list(map(op.add, draw(list(merge(*(edges[ID][1] for ID in IDs if ID!=-1))),depth-1),
                        draw(list(merge(*(edges[ID][2] for ID in IDs if ID!=-1))),depth-1)))
            +list(map(op.add, draw(list(merge(*(edges[ID][0] for ID in IDs if ID!=-1))),depth-1),
                        draw(list(merge(*(edges[ID][3] for ID in IDs if ID!=-1))),depth-1)))
            )

def drawAll(depth):
    res=[]
    print("\n".join(itertools.chain(*(map((lambda *args:"".join(args)), *(draw([grids[0][x][y]],depth) for x in range(7))) for y in range(3,-1,-1) )) ))
if __name__=="__main__":
    import sys
    if len(sys.argv)==2: drawAll(int(sys.argv[1]))
i=0;print(sum(sqArea([c],i)[0] for r in grids[0] for c in r)/(1<<(2*(i+1))) )
