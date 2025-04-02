
## Calculating the area of the Pythagoras tree
#from heapq import merge
import operator as op
import itertools
from collections import defaultdict
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

syms = {FULL:FULL, EMPTY:EMPTY}
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

DRAWTRI=False
#draw the squares of area 1/2
if DRAWTRI:
    addEdge(10,0,FULL)
    addEdge(10,1,cors[0])
    addEdge(10,2,cors[3])
    addEdge(10,3,FULL)
    addEdge(9,3,cors[2])
    addEdge(9,2,FULL)
    addEdge(11,0,cors[1])
    addEdge(11,1,FULL)
else:
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
        if ID not in [FULL,EMPTY] :
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

def merge2(*args):
    l = []
    for a in args:
        a=iter(a)
        nw = [-2,-2]
        i=0
        try:
            na = next(a)
            while i<len(l):
                if l[i]==na:
                    if nw[-2]!=na:
                        nw.append(na)
                    if nw[-2]!=na:
                        nw.append(na)
                    i+=1
                    na=next(a)
                elif l[i]<na:
                    if nw[-2]!=l[i]: nw.append(l[i])
                    i+=1
                else:
                    if nw[-2]!=na: nw.append(na)
                    na=next(a)
        except StopIteration as e:
            while i<len(l):
                if nw[-2]!=l[i]: nw.append(l[i])
                i+=1
            l=nw[2:]
            continue
        if nw[-2]!=na: nw.append(na)
        for na in a:
            if nw[-2]!=na: nw.append(na)
        l=nw[2:]
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

def reflect(ID):
    """reflect across a vertical axis"""
    special = {EMPTY:EMPTY, cors[0]:cors[3],cors[3]:cors[0],cors[1]:cors[2],cors[2]:cors[1]}
    if ID in special: return special[ID]
    (q,r) = divmod(ID,(4*7))
    y,x = divmod(r,7)
    return rotate(7*y+(6-x) ,-q)
def canonical(IDs):
    if area(list(IDs))==(4,4):
        return (FULL,)
    rots = [sorted(rotate(ID,n) for ID in ids) for n in range(4) for ids in [IDs,list(map(reflect,IDs))]]
    #for x in rots: print(x)
    return tuple(min(rots))
def canonN(n,sym=True):
    def canonical2(IDs):
        """for calculating the area covered exactly once"""
        nFull = IDs.count(FULL)
        if nFull>=n:
            return (FULL,)*n
        elif nFull==n-1:
            IDs = tuple(set(IDs)) + (FULL,)*(nFull-1)
        else:
            counts=defaultdict(int)
            for k in IDs:
                counts[k]+=1
            IDs=[]
            for k in counts:
                for i in range(min(counts[k],n-nFull)):
                    IDs.append(k)
            if n-nFull<nFull:
                for i in range(n-nFull,nFull):
                    IDs.append(FULL)
        if sym:
            rots = [sorted(rotate(ID,th) for ID in ids) for th in range(4) for ids in [IDs,list(map(reflect,IDs))]]
            return tuple(min(rots))
        else:
            return IDs
    return canonical2

def hedges(IDs):
    return tuple(canonical(merge(*(edges[ID][i] for ID in IDs))) for i in range(4))

seen = set()
l=[canonical([c]) for r in grids[0] for c in r if c!=-1]
startingPts = tuple(l)
import fractalCalc
eMap = fractalCalc.from_nondet(edges,set(l),canonical)
"""
eMap={}
for IDs in l:
    if IDs not in eMap:
        eMap[IDs] = hedges(IDs)
        for nxt in eMap[IDs]:
            if nxt not in seen:
                seen.add(nxt)
                l.append(nxt)
print(len(seen),len(l),len(eMap))
"""
import sympy
from time import perf_counter
class Perf():
    def __init__(self,name):
        self.name=name
        self.start = perf_counter()
    def __enter__(self):
        print(self.name)
        self.start = perf_counter()
    def __exit__(self,*args):
        delta = perf_counter() - self.start
        print(self.name,"complete. Time:",delta)
        return delta
        
#def var(tup):
#    return sympy.var("x_"+"_".join(map(str,tup)))
var = fractalCalc.var
with Perf("constructing a system of linear equations"):
    eqns = [
        var(can)*4 - sum(var(x) for x in eMap[can] if len(x))
        for can in eMap
        ]+[var((FULL,))-1]
from sympy.solvers.solveset import linsolve
IDs = list(eMap)
rIDs = {t:ix for ix,t in enumerate(IDs)}
with Perf("solving system of linear equations"):
    res = linsolve(eqns,list(map(var,IDs)))
print("number of solutions: ",len(res))
res=list(res)[0]
print("The exact answer (a ratio):", sol:=sum(res[rIDs[canonical([c])]] for r in grids[0] for c in r if c!=-1))
#Should print: 12823413011547414368862997525616691741041579688920794331363953564934456759066858494476606822552437442098640979/877512406035620068631903180662851572553488753575243048137500508983979170248733422547196905684808937723408093
print("Aproximate value as a decimal:",float(sol))
#Should print: 14.613369478706703

def calcOverlap(i):
    """Calculate the area with i overlapping squares (slow)"""
    can = canonN(i+1)
    print()
    print(f"working out the {i}-times overlapping region")
    eMap2 = fractalCalc.from_nondet(edges,l,can,setify=False)
    with Perf("creating system of linear equations"):
        eqns2 = [
            var(can)*4 - sum(var(x) for x in eMap2[can] if len(x))
            for can in eMap2
            ]+[var((FULL,)*j)-(1 if i==j else 0) for j in range(1,i+2)]
    IDs2 = list(eMap2)
    rIDs2 = {t:ix for ix,t in enumerate(IDs2)}
    with Perf("solving system of linear equations"):
        res2 = linsolve(eqns2,list(map(var,IDs2)))
    assert len(res2)==1
    res2=list(res2)[0]
    print("The exact non-overlapping area (a ratio):", sol2:=sum(res2[rIDs2[can(c)]] for c in startingPts))
    print("Aproximate value as a decimal:",float(sol2))
    return (eMap2,IDs2,rIDs2,res2)
overlap1 = calcOverlap(1)
# Takes a while to run. See below for results
# overlap2 = calcOverlap(2)
# overlap3 = calcOverlap(3) 
# overlap4 = calcOverlap(4)

def toBitmap(IDs,depth):
    """return a list of byteStrings that can be made into a bitmap"""
    if depth==0:
        #c = res[rIDs[canonical(IDs)]]
        ## Doing this sRGB is technically more correct (I think it's closer to what you
        ## would see with bad eyesight at a distance from a higher resolution monitor showing a more detailed image)
        ## but is less informative because it makes it harder to percive differences in brightness
        ## among pixels with values between 0.5 and 1 (I suspect that most pixels which are neither full nor empty lie in this interval)
        #if c==1:
        #    return [b"\xff"]
        #srgb = 1.055*(c**(1/2.4)) - 0.055 if c>0.0031308 else 12.92*c
        #return [bytes([int(srgb*255)])]
        return [bytes([ 255-int(res[rIDs[canonical(IDs)]]*255) ])]
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

"""
working out the 1-times overlapping region
creating system of linear equations
creating system of linear equations complete. Time: 0.8558130919700488
solving system of linear equations
solving system of linear equations complete. Time: 28.942160924023483
The exact non-overlapping area (a ratio): 16962637799360785099027471335419220151511764218476912835942824726973528226350841689327698187203341606819204010765988165824780562038671015007009943382620964995725270275795850044026053398538924844543400027671691522915388233/2513371466244324476993631364662566085189790847064880832066101319767961315877203391672625512986104320108351816994597451986760861569174319816374465722439642071633317540592620398893793384970188525908137504707270522414662336
Aproximate value as a decimal: 6.748957735526329
r42 = calcOverlap(2)

working out the 2-times overlapping region
creating system of linear equations
creating system of linear equations complete. Time: 1.9213243189733475
solving system of linear equations
solving system of linear equations complete. Time: 202.45337123802165
The exact twice-overlapping area (a ratio): 248188519611624634494798691885712426550327439346521643104675906666368587607951343934191652449046490393787214407962965160152841982753402107330473870537275979859401685422933042289106654353974315748918870815482754833363250860544611482992460480489468696187157178362370906927508728689546316608164519676663755042880974854950145918857195087/137119996065977176269530961256058362399838187183681321535977707164934792313492566362031917556921249583929991043635271859038531172299937902252756455754633135342520297579963905781271595866735876793038228012192328012457754482195153911358988778738875771300509483558718724811811878210097845978930479718041923468547326348525536254717132800
Aproximate value as a decimal: 1.8100096757018962

working out the 3-times overlapping region
creating system of linear equations
creating system of linear equations complete. Time: 3.742359835014213
solving system of linear equations
solving system of linear equations complete. Time: 879.6345058099832
The exact thrice-overlapping area (a ratio): 11954988691812348924421578517374791872946991981011682506942915152743147168781977813397820759155941660345551812177208758732839332942336513172063861575683095585110331429871379545171292054776116649782359568056688887054013555723308200137975286863500441587509724360809998320574822235234833721939942257521038092932469850414922042432745919230349860348636797834345463866958406477215878276002617979590403159391512501383219353936828145524356867756034829504161/13855837577977153175488658381635418163917680312798339858009184736660622580935151529828014602093446719459101647270912138422048603781510139084247830706463423980465145198278161209888771447649884529994566511045755591150397962626504145750506336872688394388165887238402570944146814907429650287208371170909317662263920287714830494085023359795625225033738290399304141178599276620181184073340214338695571842298681439370361454159950888650660078924299501568000
Aproximate value as a decimal: 0.8628124156719283
calcOverlap(4)

working out the 4-times overlapping region
creating system of linear equations
creating system of linear equations complete. Time: 6.635372391028795
solving system of linear equations
solving system of linear equations complete. Time: 1466.1643018440227
The exact 4-times overlapping area (a ratio): 6078325839163185667399651222931460155025913457141788697607714073072854118433834776318067744134969788725456409670750962828069346410112217140391981625849892492443897823197635634530409261025863447785752897047534329348988474019039613404684821329566571999262104572097587388016489426704142011813680213399654848072245724690567003993014391404599493326445920871079926374997694849967742652531640784973642202848379272004560222119592939477132067451272604396958949356293232960876448614101002094953618051092176750989214004200905131249198127131547757912111411266740945838098257/11112051111260538866707226258412895794897119036407788281035815037005928038947903149254922923472041011047095805743862097320388584071706114254389983611512240784899576623243963266786812256103544452899539049932891437882885685669563238991598287358989002781725479058695189435874432609169476455927024823069177239685403474491136831779938145373424368554126779726151485309246923561696667534935250788253007698522731921225352114238288179079194232048283488060462718556189011634482425734250736361209676713526556757295062906047579735645185878067982781296639491067361707950080000
Aproximate value as a decimal: 0.5470030490593799
"""
