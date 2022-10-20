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

import fractalCalc
fractalCalc.studyFractal(edges,list(map(tuple,compositions.values())), "Chaos Game")
