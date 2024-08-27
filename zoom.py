# Copyright 2024 David Chew

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# https://github.com/dcc5480

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty
#from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from PIL import Image
from random import randint
#import time
#import math
from os import environ, getenv, mkdir, system, pathsep
from os.path import exists
from numpy import zeros, ones, ravel, concatenate
#from subprocess import run
for i in ["/usr/local/bin/","/opt/homebrew/bin"]:
  if i not in environ["PATH"]:environ["PATH"]+=pathsep+i

Builder.load_string("""<CustomWidget>:
    imagev:imageview
    Label:
        text: "Click to zoom into a quadrant"
        pos: 150,20
        size: 100, 30
        font_size: 25
        opacity: root.opacity1
    Label:
        text: "'ffmpeg' is needed to create video, but is not installed. Would you like\\nto auto-install 'ffmpeg' and its dependencies (using 'homebrew')?\\nOtherwise, exit."
        pos: 525,600
        size: 500, 90
        font_size: 40
        opacity: root.opacity3
    Button:
        text: "Exit"
        pos: 750,20
        size: 100, 30
        on_release: app.stop()
        font_size: 25
    Button:
        text: "Exit and Save Video"
        pos: 900,20
        size: 300, 30
        on_release: root.saveVideo();app.stop()
        font_size: 25
        opacity: root.opacity4
        disabled: root.disabled4
    Button:
        text: "Exit and Save Video"
        pos: 900,root.x5
        size: 300, 30
        on_release: root.ffmpegPrompt()
        font_size: 25
        opacity: root.opacity5
        disabled: root.disabled5
    Button:
        text: "Yes"
        pos: 525,root.x3
        size: 500, 90
        on_release: root.ffmpegInstall();root.saveVideo();app.stop()
        font_size: 50
        opacity: root.opacity3
        disabled: root.disabled3
    Image:
        id: imageview
        pos: 20,65
        size: root.imagesize
        source: root.imagepath
        allow_stretch: True


""")

#https://stackoverflow.com/questions/46045092/save-text-input-to-a-variable-in-a-kivy-app

D=({():(),(0,):(0,),(72,):(72,),(33,):(0,),(84,):(84,),(16,):(0,),(59,):(72,),(76,):(97,8),(31,):(68,5),(8,):(72,),(81,):(59,23),(5,):(31,),(48,):(49,),(89,):(22,),(21,):(29,89),(92,):(92,),(65,):(55,),(23,):(106,),(71,):(2,),(24,):(85,),(96,):(0,),(18,):(96,20),(67,):(67,),(25,):(54,),(97,):(45,),(107,):(46,103),(63,):(0,),(26,):(0,),(75,):(0,),(22,):(84,),(99,):(72,),(30,):(84,),(36,):(74,9),(108,):(35,58),(45,):(37,60),(106,):(44,39),(69,):(6,27),(3,):(13,64),(87,):(10,),(47,):(48,),(88,):(84,),(17,):(47,),(94,):(0,),(39,):(0,),(91,):(86,87),(52,):(25,94),(51,):(36,4),(15,):(61,91),(62,):(62,),(12,):(32,),(58,):(41,),(20,):(21,),(49,):(17,),(95,):(52,),(60,):(76,),(98,):(104,12),(27,):(53,78),(103,):(107,82),(55,):(56,98),(101,):(66,83),(70,):(15,),(4,):(79,),(73,):(90,),(28,):(24,),(104,):(72,),(37,):(84,),(43,):(73,77),(6,):(0,),(53,):(19,30),(1,):(43,65),(79,):(102,108),(13,):(3,),(74,):(93,),(34,):(11,),(85,):(105,),(29,):(18,),(105,):(28,),(38,):(99,),(44,):(50,81),(7,):(34,88),(54,):(38,95),(2,):(57,71),(80,):(7,70),(14,):(14,),(61,):(80,),(56,):(1,),(19,):(69,),(102,):(51,),(66,):(101,)},{():(),(0,):(0,),(33,):(33,),(84,):(0,),(42,):(42,),(77,):(12,),(8,):(0,),(81,):(74,8),(5,):(5,),(48,):(98,),(89,):(36,),(21,):(44,23),(16,):(0,),(59,):(42,),(76,):(96,89),(31,):(67,92),(96,):(42,),(18,):(46,59),(67,):(31,),(25,):(38,),(97,):(30,),(107,):(97,60),(68,):(68,),(90,):(14,),(46,):(3,),(93,):(64,),(47,):(65,),(88,):(33,),(17,):(42,),(94,):(77,),(39,):(22,70),(91,):(0,),(52,):(24,47),(51,):(106,),(15,):(108,83),(62,):(90,52),(12,):(95,),(58,):(82,),(20,):(71,),(49,):(99,),(95,):(94,),(60,):(81,),(98,):(105,49),(27,):(37,58),(103,):(18,10),(55,):(55,),(101,):(19,27),(64,):(93,41),(40,):(101,),(70,):(69,),(32,):(62,),(4,):(80,),(83,):(13,),(63,):(0,),(26,):(0,),(75,):(0,),(22,):(33,),(99,):(42,),(30,):(33,),(36,):(29,88),(108,):(34,87),(45,):(86,20),(106,):(2,51),(69,):(7,91),(3,):(53,103),(73,):(25,),(35,):(50,),(28,):(0,),(104,):(73,),(37,):(33,),(43,):(28,48),(6,):(35,9),(53,):(0,),(1,):(1,),(79,):(6,40),(13,):(66,45),(74,):(107,),(34,):(57,),(85,):(56,),(29,):(76,),(105,):(43,),(38,):(104,),(44,):(11,21),(7,):(100,39),(54,):(85,17),(80,):(102,4),(14,):(54,32),(19,):(79,),(66,):(15,)},{():(),(0,):(0,),(72,):(72,),(84,):(84,),(42,):(0,),(16,):(0,),(59,):(84,),(76,):(24,48),(31,):(18,21),(96,):(84,),(18,):(0,),(67,):(93,76),(25,):(19,),(97,):(37,),(107,):(25,94),(68,):(107,82),(46,):(13,),(93,):(62,),(77,):(40,),(8,):(9,),(81,):(73,77),(5,):(50,81),(48,):(4,),(89,):(39,),(21,):(43,65),(92,):(57,71),(63,):(0,),(26,):(0,),(75,):(0,),(22,):(72,),(99,):(84,),(30,):(72,),(36,):(28,49),(108,):(105,17),(45,):(85,47),(106,):(1,55),(69,):(80,15),(3,):(54,52),(35,):(74,),(86,):(100,),(28,):(72,),(104,):(0,),(37,):(35,),(43,):(11,22),(6,):(104,12),(53,):(86,87),(1,):(106,),(79,):(79,),(13,):(53,78),(74,):(97,),(34,):(44,),(85,):(102,),(29,):(59,),(105,):(36,),(38,):(6,),(44,):(29,89),(7,):(56,98),(54,):(61,91),(2,):(2,),(14,):(66,83),(50,):(68,),(11,):(31,),(57,):(92,),(9,):(58,),(88,):(0,),(17,):(84,),(94,):(72,),(39,):(34,88),(91,):(99,32),(52,):(0,),(51,):(51,),(15,):(69,),(62,):(45,41),(12,):(27,),(58,):(60,),(20,):(23,),(49,):(108,),(95,):(30,),(60,):(8,),(98,):(7,70),(27,):(38,95),(103,):(96,20),(101,):(101,),(64,):(46,103),(78,):(64,),(32,):(3,),(82,):(5,),(83,):(14,),(41,):(67,)},{():(),(0,):(0,),(72,):(0,),(33,):(33,),(42,):(42,),(16,):(0,),(59,):(33,),(76,):(25,77),(31,):(107,81),(8,):(33,),(81,):(0,),(5,):(76,71),(48,):(70,),(89,):(88,),(21,):(28,48),(92,):(11,21),(23,):(51,),(71,):(1,),(24,):(61,),(96,):(86,),(18,):(24,47),(67,):(18,10),(25,):(66,),(97,):(53,),(107,):(90,52),(68,):(93,41),(63,):(0,),(26,):(0,),(75,):(0,),(22,):(42,),(99,):(33,),(30,):(42,),(36,):(73,12),(108,):(104,95),(45,):(38,94),(106,):(43,98),(69,):(79,101),(3,):(14,62),(9,):(78,),(87,):(20,),(88,):(87,),(17,):(0,),(94,):(42,),(39,):(35,9),(91,):(85,17),(52,):(30,82),(51,):(100,39),(15,):(15,),(62,):(3,),(12,):(83,),(58,):(103,),(20,):(89,),(49,):(91,),(95,):(45,),(60,):(59,),(98,):(6,40),(27,):(54,32),(103,):(97,60),(55,):(102,4),(64,):(64,),(10,):(92,),(82,):(31,),(41,):(68,),(86,):(34,),(28,):(42,),(104,):(33,),(37,):(0,),(43,):(0,),(6,):(56,99),(53,):(37,58),(1,):(57,36),(79,):(69,),(13,):(13,),(74,):(46,),(34,):(29,),(85,):(7,),(29,):(96,),(105,):(22,),(38,):(108,),(44,):(74,8),(7,):(105,49),(54,):(19,27),(2,):(44,23),(80,):(80,),(100,):(2,),(11,):(67,),(56,):(106,),(57,):(5,),(102,):(55,)})

def iterate(L,empty=(),full=[(0,)]):
  L=list(L)
  for i in range(len(L)):
    if type(L[i])==list:
      L[i]=iterate(L[i])
    elif L[i]==empty:
      pass
    elif L[i] in full:
      pass
    else:
      t1=[]
      for j in range(len(D)):
        t1.append(sum(sorted(set(D[j].get((k,),())for k in L[i])),()))
        if any(k[0] in t1[-1]for k in full):
          t1[-1]=full[0]
      L[i]=t1
  return L

def drawSquareFractal(n,D,finals=[1],x=0,main=True):
  #inefficient, can be made faster
  #a general approach to turning automata into images
  #D, x, and finals must use tuples of tiles
  #start=time.time()
  #if math.log(n,2)!=int(math.log(n,2)):print("n must be a power of two!");return
  #if n<=1:print("ONE",n)
  #if len(D)!=4:print("Wrong D Size");return
  #if depth==None:
  depth=len(bin(128))-2
  #def DConvert(D,override=False):
  #  if len(D)==0 or (type(D)==dict and type(list(D)[0])==tuple and not override):return D
  #  if type(D)==tuple and type(D[0])==dict:
  #    return tuple(DConvert(i)for i in D)
  #  return {(i[0],):(i[1],)for i in list(zip(D,D.values()))}
  #D=DConvert(D,override)
  #if type(finals[0])!=tuple or override:finals=[(i,)for i in finals]
  #if type(x)!=tuple or override:x=(x,)
  #t3=D#;L=[(0,)]
  L=zeros((n,n),bool)
  if x in finals:
    L=ones((n,n),bool)
  elif x!=() and depth!=0:
    t1=len(L)//2
    t2=iterate([x])[0]
    #tl,tr,br,bl style
    if t1!=0:
      L[:t1,:t1]=drawSquareFractal(t1,D,finals,t2[0],False)
      L[t1:,:t1]=drawSquareFractal(t1,D,finals,t2[3],False)
      L[t1:,t1:]=drawSquareFractal(t1,D,finals,t2[2],False)
      L[:t1,t1:]=drawSquareFractal(t1,D,finals,t2[1],False)
  #if main:
  #  im=Image.new('1',(n,n))
  #  im.putdata(ravel(L))
  #  im.save(f"/Users/suoenallecsim/Downloads/{random.randint(0,10**12)}.png")
  #  im.close()
    #print(time.time()-start)
    #print(np.sum(L)/(n*n))
  #else:
  return L

def pythagoreanTreeDrawSquares(n,zoom,name,num,path=getenv("HOME")+'/'+'Downloads/',tree=[[(),(),(),(68,),(67,),(31,),(68,5),(67,92),(31,),(5,),(92,),(),(),()],[(),(),(93,41),(107,82),(18,10),(93,76),(107,81),(18,21),(76,71),(50,81),(11,21),(57,71),(),()],[(),(64,),(46,103),(97,60),(96,20),(46,59),(97,8),(96,89),(59,23),(74,8),(29,89),(44,23),(2,),()],[(),(62,),(90,52),(25,94),(24,47),(0,),(25,77),(24,48),(0,),(73,77),(28,48),(43,65),(1,),()],[(),(3,),(45,),(30,),(0,),(42,),(72,),(42,),(72,),(0,),(22,),(36,),(106,),()],[(),(13,),(53,),(37,),(86,),(84,),(33,),(84,),(33,),(9,),(88,),(39,),(51,),()],[(),(14,),(54,),(38,),(85,),(),(0,),(0,),(),(12,),(49,),(98,),(55,),()],[(),(),(66,),(19,),(61,),(),(0,),(0,),(),(40,),(70,),(4,),(),()]]):
  #zoom in 0,1,2,3=tl,tr,bl,br form
  #start=time.time()
  path+=name+'/'
  if zoom:
    t1,t2=max(0,min(4,int((1-zoom[1])*8-1))),max(0,min(6,int(zoom[0]*14-3)))
    t1,t2,t3,t4=tree[t1][t2:t2+8],tree[t1+1][t2:t2+8],tree[t1+2][t2:t2+8],tree[t1+3][t2:t2+8]
    t1,t2,t3,t4=iterate(t1),iterate(t2),iterate(t3),iterate(t4)
    tree=[[],[],[],[],[],[],[],[]]
    for i in range(8):
      if t1[i]==():t1[i]=[()]*4
      if t2[i]==():t2[i]=[()]*4
      if t1[i]==(0,):t1[i]=[(0,)]*4
      if t2[i]==(0,):t2[i]=[(0,)]*4
      if t3[i]==():t3[i]=[()]*4
      if t4[i]==():t4[i]=[()]*4
      if t3[i]==(0,):t3[i]=[(0,)]*4
      if t4[i]==(0,):t4[i]=[(0,)]*4
      t1[i][2],t1[i][3],t2[i][2],t2[i][3]=t1[i][3],t1[i][2],t2[i][3],t2[i][2]
      t3[i][2],t3[i][3],t4[i][2],t4[i][3]=t3[i][3],t3[i][2],t4[i][3],t4[i][2]
      tree[0]+=t1[i][:2];tree[1]+=t1[i][2:];tree[2]+=t2[i][:2];tree[3]+=t2[i][2:]
      tree[4]+=t3[i][:2];tree[5]+=t3[i][2:];tree[6]+=t4[i][:2];tree[7]+=t4[i][2:]
    if zoom[0]<0.5:tree[0]=tree[0][:-2];tree[1]=tree[1][:-2];tree[2]=tree[2][:-2];tree[3]=tree[3][:-2];tree[4]=tree[4][:-2];tree[5]=tree[5][:-2];tree[6]=tree[6][:-2];tree[7]=tree[7][:-2]
    else:tree[0]=tree[0][2:];tree[1]=tree[1][2:];tree[2]=tree[2][2:];tree[3]=tree[3][2:];tree[4]=tree[4][2:];tree[5]=tree[5][2:];tree[6]=tree[6][2:];tree[7]=tree[7][2:]
  print()
  print(tree)
  print()
  for i in tree:
    print(len(i))
  L=concatenate(tuple(concatenate(tuple(drawSquareFractal(n,D=D,finals=[(0,)],x=tree[i][j],main=False)for j in range(14)),1)for i in range(8)))
  im=Image.new('1',(14*n,8*n))
  im.putdata(ravel(L))
  im.save(path+name+f"_{num}.png")
  im.close()
  #print(time.time()-start)
  if zoom:return tree

class CustomWidget(Widget):
  #imagev=Image()
  opacity1=NumericProperty(100)
  opacity3=NumericProperty(0)
  opacity4=NumericProperty(0)
  opacity5=NumericProperty(0)
  disabled3=BooleanProperty(True)
  disabled4=BooleanProperty(True)
  disabled5=BooleanProperty(True)
  x3=NumericProperty(100000)
  x5=NumericProperty(20)
  imagesize=ObjectProperty((0,0))
  pos=(0,0)
  im=None
  n=128
  imsize=(7*n,4*n)
  name=str(randint(0,10**12))+"_fractal"
  num=1
  mainpath=getenv("HOME")+'/'+'Downloads/'
  filechooser1=ObjectProperty("")
  if not exists(mainpath):mkdir(mainpath)
  mkdir(mainpath+name+'/')
  pythagoreanTreeDrawSquares(n,[],name,0)
  imagepath=StringProperty(mainpath+name+'/'+name+"_0.png")
  tree=ObjectProperty([[(),(),(),(68,),(67,),(31,),(68,5),(67,92),(31,),(5,),(92,),(),(),()],[(),(),(93,41),(107,82),(18,10),(93,76),(107,81),(18,21),(76,71),(50,81),(11,21),(57,71),(),()],[(),(64,),(46,103),(97,60),(96,20),(46,59),(97,8),(96,89),(59,23),(74,8),(29,89),(44,23),(2,),()],[(),(62,),(90,52),(25,94),(24,47),(0,),(25,77),(24,48),(0,),(73,77),(28,48),(43,65),(1,),()],[(),(3,),(45,),(30,),(0,),(42,),(72,),(42,),(72,),(0,),(22,),(36,),(106,),()],[(),(13,),(53,),(37,),(86,),(84,),(33,),(84,),(33,),(9,),(88,),(39,),(51,),()],[(),(14,),(54,),(38,),(85,),(),(0,),(0,),(),(12,),(49,),(98,),(55,),()],[(),(),(66,),(19,),(61,),(),(0,),(0,),(),(40,),(70,),(4,),(),()]])
  if system("which ffmpeg")==0:
    opacity4=100
    opacity5=0
    disabled4=False
    disabled5=True
    x5=100000
  else:
    opacity4=0
    opacity5=100
    disabled4=True
    disabled5=False
  imagesize=ObjectProperty((Window.size[0]-40,Window.size[1]-130))
  #print(self.imagepath)
  def resizeUpdate(self,x,y,z):
    #print(self.size)
    self.imagesize=(Window.size[0]-40,Window.size[1]-130)
    #zoomtext=self.zoom1.text
    #self.zoomtext="nfnnw"+str(self.imagesize)
  def mousePos(self,x,y):
    self.pos=y
  def touchDown(self,x,y):
    #print('hi',self.pos)
    self.opacity1=0
    t1,t2,t3,t4=Window.size[0]-40,Window.size[1]-130,self.imsize[0],self.imsize[1]
    x,y=20,65
    x1,y1=t1,t2
    if t1/t2>t3/t4:s=t2/t4;x+=(t1-s*t3)/2;x1-=(t1-s*t3)
    else:s=t1/t3;y+=(t2-s*t4)/2;y1-=(t2-s*t4)
    x,y=self.pos[0]-x,self.pos[1]-y
    #print(x,y,x1,y1)
    if x>0 and y>0 and x<x1 and y<y1:
      zoom=(x/x1,y/y1)
      #print(zoom)
      print(self.tree)
      self.tree=pythagoreanTreeDrawSquares(self.n,zoom,self.name,self.num,tree=self.tree)
      #time.sleep(5.5)
      self.imagepath=self.mainpath+self.name+'/'+self.name+f"_{self.num}.png"
      self.num+=1
    #print((self.pos[0]-x,self.pos[1]-y))
  def saveVideo(self):
    if self.num!=1:
      #t1=str(len(os.listdir(path))-1)
      #print("hooeoeooe")
      #print(["ffmpeg","-f","image2","-framerate","3","-i",self.mainpath+self.name+'/'+self.name+"%d.png",self.mainpath+self.name+'/'+self.name+".gif"])
      #print(["ffmpeg","-i",self.mainpath+self.name+'/'+self.name+".gif","-pix_fmt","yuv420p",self.mainpath+self.name+'/'+self.name+".mp4"])
      #was subprocess.run:
      system(' '.join(["ffmpeg","-f","image2","-framerate","3","-i",self.mainpath+self.name+'/'+self.name+"_%d.png",self.mainpath+self.name+'/'+self.name+".gif"]))
      system(' '.join(["ffmpeg","-i",self.mainpath+self.name+'/'+self.name+".gif","-pix_fmt","yuv420p",self.mainpath+self.name+'/'+self.name+".mp4"]))
      #print("wwowowoowo")
  def ffmpegPrompt(self):
    self.opacity3=100
    self.x3=375
    self.opacity4=0
    self.opacity5=0
    self.disabled3=False
    self.disabled4=True
    self.disabled5=True
  def ffmpegInstall(self):
    if system("which brew")!=0:
      t1='/bin/bash -c \\"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\\";brew install ffmpeg'
      system(f"""osascript -e 'tell application "Terminal" to do script "{t1}" activate'""")
    else:
      system("brew install ffmpeg")

class CustomWidgetApp(App):
  def build(self):
    wid=CustomWidget()
    Window.bind(on_resize=wid.resizeUpdate,mouse_pos=wid.mousePos,on_touch_down=wid.touchDown)
    return wid

if __name__ == "__main__":
    CustomWidgetApp().run()

