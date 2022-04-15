#include <stdio.h>

#define DEPTH 7
#define MID
#ifdef MID
  #define UPPERBOUND
#endif
#define U (1<<DEPTH)
#define W (U*6)
#define H (U*4)
#define max(a,b) ((a)>(b)?(a):(b))
#define min(a,b) ((a)<(b)?(a):(b))
#define abs(a) ((a)>=0?(a):-(a))

char grid[W][H];

int mx[3][3]={1,2,3,6,7,8,2,9,5};
#ifdef MID
int maximals[4][4+4*7]={{
0,-4,  4,7
,0,9,1,15,4,12,0
,12,15,12,5,9,4,9
,4,13,13,15,13,13,1
,0,6,14,15,13,3,0
},
{
-4,-4,  7,4
,0,8,9,0
,12,11,15,3
,13,11,9,2
,15,15,10,15
,11,11,3,8
,6,11,8,9
,0,2,3,0
},
{
-3,0,  7,4
,0,12,8,0
,6,2,14,9
,2,12,14,14
,15,10,15,15
,8,6,14,7
,12,15,14,3
,0,6,2,0
},
{
-4,-3,  4,7
,0,12,7,15,11,9,0
,4,7,7,15,7,7,1
,6,1,6,5,3,15,3
,0,3,1,15,4,6,0
}};
#else
int maximals[4][4+4*7]={{0,-4,  4,7
,12,15,9,15,12,15,9
,14,15,15,5,15,15,11
,6,15,15,15,15,15,3
,0,6,15,15,15,3,0},
{-4,-4,  7,4
,0,12,13,9
,12,15,15,15
,15,15,15,3
,15,15,10,15
,15,15,15,9
,6,15,15,15
,0,6,7,3},
{-3,0,  7,4
,12,13,9,0
,15,15,15,9
,6,15,15,15
,15,10,15,15
,12,15,15,15
,15,15,15,3
,6,7,3,0},
{-4,-3,  4,7
,0,12,15,15,15,9,0
,12,15,15,15,15,15,9
,14,15,15,5,15,15,11
,6,15,3,15,6,15,3}};
#endif

void drawTreeB(int x, int y, int dx, int dy);

void drawTreeA(int x, int y, int dx, int dy){
  //printf("dtA\n");
  
  int e = abs(dx+dy);
  #ifdef UPPERBOUND
  if(e==1){
    int a = dy*3+dx+3 >> 1;
    //printf("(%d,%d)%d",dx,dy,a);
    int* k = (&(maximals[0][0])) + a*32;
    //printf("%d: (%d,%d) %d %d\n",i,k[0],k[1],k[2],k[3],k[4]);
    //printf("(%d,%d)\n",x,y);
    x+=k[0];
    y+=k[1];
    for(int i=0; i<k[2]; i++)
      for(int j=0; j<k[3]; j++){
        //printf("(%d,%d),%d\n",x+i,y+j, 4 + i*k[3] + j);
        //printf("%d, %d  -- %d\n", a, k[4 + i*k[3] + j], maximals[a][4 + i*k[3] + j]);
        grid[x+i][y+j] |= k[4 + i*k[3] + j];
        //printf("pt\n");
    }
    return;
  }
  #endif
  int mnx = x+min(0,dx-dy);
  int mny = y+min(0,dy+dx);
  for (int i=mnx;i<mnx+e;i++) for (int j=mny;j<mny+e;j++){
    grid[i][j]=15;
  }
  if(e>1){
    drawTreeB(x-dy, y+dx, (dx-dy)>>1, (dy+dx)>>1);
    drawTreeB(x - dy + (dx-dy>>1), y+dx + (dx+dy>>1), (dx+dy)>>1, (dy-dx)>>1);
  }
}
void drawTreeB(int x, int y, int dx, int dy){
  //printf("dtb\n");
  int mx = x+(dx-dy>>1);
  int my = y+(dy+dx>>1);
  int sz=abs(dx);
  for(int i=0;i<sz;i++){
    grid[mx-sz+i][my-1-i] |= 0b1100;
    for(int j=my-i;j<my+i;j++){
      grid[mx-sz+i][j] = 0b1111;
    }
    grid[mx-sz+i][my+i] |= 0b1001;
    
    grid[mx+i][my-sz+i] |= 0b0110;
    for(int j=my-sz+i+1; j<my+sz-1-i; j++){
      grid[mx+i][j] = 0b1111;
    }
    grid[mx+i][my+sz-1-i] |=0b0011;
  }
  
  drawTreeA(x-dy, y+dx, (dx-dy)>>1, (dy+dx)>>1);
  drawTreeA(x - dy + (dx-dy>>1), y+dx + (dx+dy>>1), (dx+dy)>>1, (dy-dx)>>1);
}

//char** ss[16] = {" ","▲","▶","◣","▼","⧗","◤","ᕒ","◀","◢","⧓","M","◥","Σ","W","█"};
//char** ss2[16] = {" ","░","░","▒","░","▒","▒","▓","░","▒","▒","▓","▒","▓","▓","█"};

int popcount[16] = {0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4};

int main (int argc, char** argv){
  printf("%s\n",argv[argc-1]);
  drawTreeA((U*5)>>1,0,U,0);
  long long tot=0;
  for(int x=0;x<W;x++) for(int y=0;y<H;y++){
    //printf("%d\n",grid[x][y]);
    tot += popcount[grid[x][y]];
  }
  /*
  for(int y=H-1;y>=0;y--){
    for(int x=0;x<W;x++){
      //printf("%d ",grid[x][y]);
      printf("%s",ss[grid[x][y]] ); //" abcdefghijklmn#qqqqqqqq"[grid[x][y]]);
    }
    printf("\n");
  }*/
  printf("%lld\n",tot);
  printf("%.18f\n",((float)tot)/(4*U*U));
  
}
