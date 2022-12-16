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


def srtrmdups(ts):
    """Sort and remove dupliactes"""
    l = sorted(ts)
    ps = tuple([a for a,b in zip(l,l[1:]+[None]) if a!=b])
    return ps
from drawSystems import drawTri
print("\n".join(drawTri([(5,0,0)],"u",5,(lambda ys,b:srtrmdups([x for a in ys for x in edges[a][b]])),lambda l:" " if len(l)==0 else"#")))


import fractalCalc
sMap = fractalCalc.studyFractal(edges,list(map(tuple,compositions.values())), "Chaos Game")
mx = max(sMap.values())

print("\n".join(" "*(32-p)+r for p,r in enumerate(
    drawTri(compositions[1],"u",5,(lambda ys,b:srtrmdups([x for a in ys for x in edges[a][b]])),
                        lambda l:" ,./+x=&#"[int((sMap[l]if l in sMap else 0 if l==() else 0)*8/mx)]))))
