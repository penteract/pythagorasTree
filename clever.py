
IDN = 0
IDdict={}
class Box():
    def __init__(self):
        global IDN,IDdict
        IDdict[IDN] = self
        self.id=IDN
        IDN+=1
        self.cannon=self
        
    def area(self,depth):
        """return the area of the box, to max resolution depth"""
        abstract
    def part(self,x,y):
        """return a corner of the box (x and y should be 0 or 1; 0,0 being lower left)"""
        abstract
    def add(self,other,depth):
        """Return a box containing the union of the pixels in each box, limited to depth"""
        abstract
    def rotate(self,n):
        """Return a box rotated n*90 degrees clockwise"""
        abstract
    def getCannon(self):
        """return a """
        if self.cannon.cannon is not self.cannon:
            self.cannon=self.cannon.getCannon()
        return self.cannon
        

class Full(Box):
    def area(self,*args):
        return 1
    def part(self,*args):
        return self
    def add(self,other,depth):
        return self
    def rotate(self,*args):
        return self
FULL=Full()
class Empty(Box):
    def area(self,*args):
        return 0
    def part(self,*args):
        return self
    def add(self,other,depth):
        return other
    def rotate(self,*args):
        return self
EMPTY = Empty()
DiagDict = {}
class Diag(Box):
    def __init__(self,x,y):
        """x and y are each 0 or 1, indicating the corner which is full"""
        super().__init__()
        self.x=x
        self.y=y
    def part(self,x,y):
        return [EMPTY,self,FULL][(x==self.x)+(y==self.y)]
    def add(self,other,depth):
        if other is FULL or other is EMPTY:
            return other.add(self)
        elif other is self.rotate(2):
            return FULL
        elif other is self:
            return self
        return addByParts(other,self,depth)
    def rotate(self,n):
        x,y=self.x,self.y
        return `DiagDict[[(x,y),(y,1-x),(1-x,1-y),(1-y,x)][n%4]]
    def area(self,*args):
        return (1/2)
    
CORNERS = [(x,y) for x in range(2) for y in range(2)]
for t in CORNERS:
    DiagDict[t] = Diag(*t)
class Ref(Box):
    """An incomplete box that can be referred to before it's filled in"""
    def __init__(self):
        super().__init__()
        self.parts={t:[] for t in CORNERS}
    def __done__(self):
        self.cannon = byParts({k:sm(self.parts(v)) for ]
    def insert(self,x,y,box):
        self.parts[(x,y)].append(box)
    def part(self,*args):
        return self.getCannon().part(*args)
    def area(self,*args):
        return self.getCannon().area(*args)
    def rotate(self,*args):
        return self.getCannon().rotate(*args)
    def add(self,*args):
        return self.getCannon().add(*args)

BPD = {}
def byParts(dct):
    IDtup = tuple(dct[t].getCannon().id for t in CORNERS)
    if IDtup in BPD:
        return BPD[IDtup]
    else:
        BPD[IDtup] = Quad(dct)
    return BPD[IDtup]
def Quad(Box):
    def __init__(self):
        super().__init__()
        self.dct = dct
    def part(self,x,y):
        return self.dct[x,y]
