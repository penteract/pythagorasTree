#include<stdio.h>
#include<mpfr.h>
#include<mpfi.h>
#include<mpfi_io.h>
#include<stdbool.h>
// precision:
#ifndef P
#define P 1000
#endif

//
#ifndef MAX_VARS
#define MAX_VARS 10000
#endif

int N;
mpfr_t vars[MAX_VARS];
mpfi_t ovars[MAX_VARS];
int refs[MAX_VARS][4];

// ln(2)
mpfi_t l2;

mpfi_t dim;

// Apply a single step of iteration
// vs is the current map, ovs is the output map, d2 is 2^-dim
// returns 1 if all members of vs grow, -1 if all shrink, 0 otherwise
int step(mpfr_t vs[], mpfi_t ovs[], mpfr_t d2){
  bool all_smaller = true;
  bool all_bigger = true;
  for(int i=0;i<N;i++){
    mpfi_set_fr(ovs[i],vs[refs[i][0]]);
    mpfi_add_fr(ovs[i],ovs[i],vs[refs[i][1]]);
    mpfi_add_fr(ovs[i],ovs[i],vs[refs[i][2]]);
    mpfi_add_fr(ovs[i],ovs[i],vs[refs[i][3]]);
    mpfi_mul_fr(ovs[i],ovs[i],d2);
    int n = mpfi_cmp_fr(ovs[i],vs[i]);
    if(n>=0) all_smaller=false;
    if(n<=0) all_bigger=false;
  }
  for(int i=0;i<N;i++){
    mpfi_get_fr(vs[i],ovs[i]);
  }
  if(all_bigger) return 1;
  if(all_smaller) return -1;
  return 0;
}

// returns -n if d2 is less than the correct value of 2^-dim,
//         n if it is greater
//         0 if the result is unknown given num_iters and the initial state of vars
//     (where n is the number of iterations needed to compute the result)
int iterate(mpfr_t d2, int num_iters){
  for(int i=0;i<num_iters;i++){
    int res = step(vars,ovars,d2);
    if (res!=0) return res*(i+1);
  }
  return 0;
}

// iteratively improve 'bounds' as a value for 2^-dim
void bsearch(mpfi_t bounds, int num_iters){
    mpfr_t mid;
    mpfr_init(mid);
    
    // used as a temporary. Using mpfi_bisect cleverly could avoid the need for this
    // but I'm not sure that wouldn't need a mpfi_t as a temporary
    //   and "the two halves [] may overlap" is a little concerning
    mpfr_t bound; 
    mpfr_init(bound);

    mpfi_t dm;
    mpfi_init(dm);
    int total_iters=0;
    while(true){
      mpfi_out_str(stdout,10,0,bounds);printf("\ndim:");
      mpfi_get_fr(mid,bounds);
      mpfi_log(dm,bounds);
      mpfi_div(dm,dm,l2);
      mpfi_out_str(stdout,10,0,dm);printf("\n");
      int r = iterate(mid,num_iters);
      printf("needed_iters %d\n\n",r);
      if(r==0) {
        printf("total iters: %d\n",total_iters+num_iters);
        return;
      }
      else if(r>0){
        mpfi_get_left(bound,bounds);
        total_iters+=r;
      }
      else if(r<0){
        mpfi_get_right(bound,bounds);
        total_iters-=r;
      }
      mpfi_interv_fr(bounds,mid,bound);
    }
}

int main(int argc, char** argv){
  mpfr_set_default_prec(P);
  mpfi_init(l2);
  mpfi_const_log2(l2); // set up log2 constant

  // Read system of equations:
  scanf("%d",&N);
  if(N>=MAX_VARS){
    printf("Too many numbers, recompile with larger MAX_VARS");
  }
  for(int i=0;i<N;i++){
    double f;
    scanf("%d %d %d %d %lf",&refs[i][0],&refs[i][1],&refs[i][2],&refs[i][3],&f);
    mpfr_init(vars[i]);
    mpfi_init(ovars[i]);
    mpfr_set_d(vars[i],f,MPFR_RNDN);
  }
  mpfr_init(vars[N]);
  mpfr_set_si(vars[N],0,MPFR_RNDN);

  // Initialize bounds
  mpfi_init(dim);
  //mpfi_interv_d(dim, -1.9340071829882908,-1.9340071829882910);
  mpfi_interv_d(dim, -1.0,-2.0);
  mpfi_mul(dim,l2,dim);
  mpfi_exp(dim,dim);

  
  //mpfr_out_str(stdout,10,0,dim,MPFR_RNDN); printf("\n");
  // Binary search for the right answer
  bsearch(dim,100);
  //printf("%d\n",iterate(dim,20));
}
