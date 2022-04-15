DEPTH = 4

U = 2**DEPTH
W = U*6
H = U*4

grid = [[0]*H for  i in range(W)]
#number 0b0000 through 0b1111 indicates which corners are included
#\ 2 /
# \ /
#1 X 3
# / \
#/ 0 \

#(bottom left is (0,0))


# Represent subtrees by root position and base vector
base = ((U*5//2,0), (U,0))

popcount =[0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4]
# vector given as 

def myrange(n):
    if n > 0:
        return range(n)
    if n < 0:
        return range(-1, n-1, -1)
    if n ==0:
        raise Exception("invalid input")

nxt=[base]
for i in range(DEPTH*2+1):
    this=nxt
    nxt=[]
    #print(this)
    for (pt,e1) in this:
        (dx,dy) = e1
        (x,y)=pt
        #draw box
        e2 = (-dy,dx)
        if dx*dy==0:#axis aligned
            try:
                for xx in myrange(e1[0]+e2[0]):
                    for yy in myrange(e1[1]+e2[1]):
                        grid[x+xx][y+yy]=15
            except Exception as e:
                print(pt,e1,e2,this[:10])
                raise e
        else:#diagonal
            mx,my = (x+(e1[0]+e2[0])//2, y+(e1[1]+e2[1])//2)
            sz = abs(dx)
            for i in range(sz):
                grid[mx-sz+i][my-1-i] |= 0b1100
                for j in range(my-i,my+i):
                    grid[mx-sz+i][j] = 0b1111
                grid[mx-sz+i][my+i] |= 0b1001
            for i in range(sz):
                grid[mx+i][my-sz+i] |= 0b0110
                for j in range(my-sz+i+1,my+sz-1-i):
                    grid[mx+i][j] = 0b1111
                grid[mx+i][my+sz-1-i] |=0b0011
        #add children
        nxt.append(((x-dy,y+dx), ((dx-dy)//2,(dy+dx)//2)))
        nxt.append(((x - dy + (dx-dy)//2, y+dx + (dx+dy)//2 ), ((dx+dy)//2, (dy-dx)//2)))

grmin=list(map(list,grid))
print("lower bound: ", sum(popcount[x] for r in grid for x in r)/(U*U)/4)
s=" ▲▶◣▼⧗◤ᕒ◀◢⧓M◥ΣW■"
s=" ??+??+??+??+??#"
for y in range(H-1,-1,-1):
    print("".join(s[grid[x][y]] for x in range(W)))
maximalv = [
    [ 0, 9,15,15,15, 3, 0],
    [ 9,15,15,15,15,15, 3],
    [13,15,15,10,15,15, 7],
    [12,15, 6,15,12,15, 6]
    ]
middlev = [
    [ 0, 9,14,15,7, 3, 0],
    [ 8,14,14,15,14,14, 2],
    [12,2,12,10,6,15, 6],
    [0,6, 2,15,8,12, 0]
    ]
#maximalv=middlev
print(sum(popcount[x] for r in middlev for x in r)/4)
maximalh = list(zip(*reversed(maximalv)))
maximals={(1,0):maximalh,
          (-1,0):[[((x>>2)|(x<<2))&15 for x in reversed(r)] for r in reversed(maximalh)],
          (0,1): [[((x>>1)|(x<<3))&15  for x in r] for r in maximalv],
          (0,-1): [[((x>>3)|(x<<1))&15  for x in reversed(r)] for r in reversed(maximalv)]
          }
toBotLeft={
    (1,0) : (-3, 0),
    (-1,0): (-4,-4),
    (0,1) : (-4,-3),
    (0,-1): (0,-4)
    }
def printCArray():
    """Turn the maximals array into something that can be used as a constant in C programs"""
    for k in [(0,-1),(-1,0),(1,0),(0,1)]:
        print("{")
        g = maximals[k]
        print(",".join(map(str,toBotLeft[k]))+",  "+str(len(g))+","+str(len(g[0])))
        for r in g:
            print(","+",".join(map(str,r)))
        print("},")

for pt,e1 in this:
    x,y = pt
    dx,dy = toBotLeft[e1]
    x+=dx
    y+=dy
    for i,r in enumerate(maximals[e1]):
        for j,k in enumerate(r):
            grid[x+i][y+j] |=k

print("upper bound: ", sum(popcount[x] for r in grid for x in r)/(U*U)/4)

    
"""
s=" ▲▶◣▼⧗◤ᕒ◀◢⧓M◥ΣW■"
#print(sum(popcount[x] for r in grid for x in r)/(U*U)/4)
for y in range(H-1,-1,-1):
    print("".join(s[grid[x][y]] for x in range(W)))
"""


