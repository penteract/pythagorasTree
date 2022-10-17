import random
from math import pi,sin,cos
p = (0,0)

STAR = 6 # len(choices)
choices = [(sin(2*pi*c / STAR)*2,2*cos(2*pi*c / STAR) ) for c in range(STAR)]
N = 600000
pts=[]
choice = 0
prevChoice = 0
for i in range(N):
    opts = [x for x in range(STAR) if x not in [(choice+1)%STAR, (prevChoice-1)%STAR ] ]
    prevChoice = choice
    choice = random.choice(opts)
    p = tuple((p[i]+choices[choice][i])/2 for i in range(2))
    #print(choice, opts,"{:.2f} {:.2f}".format(p[0],p[1]))
    pts.append(p)



import matplotlib.pyplot as plt
plt.scatter([p[0] for p in pts],[p[1] for p in pts], s=0.1)
plt.show()
