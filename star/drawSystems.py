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
