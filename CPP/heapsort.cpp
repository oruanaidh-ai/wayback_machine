

#include <iostream>
#include <cstdlib>

using std::cout;
using std::endl;

void swap(int &a, int &b)
{
  int tmp = a;
  a = b;
  b = tmp;
}

/// make a max-heap
void heapify(int * const a, int len)
{
  int * p = a-1;

  for (int i=len; i >= 2; --i)
    {
      if (p[i] > p[i>>1])
	{
	  swap(p[i], p[i>>1]);
	}
    }
}


/// put an element on the max heap. It bubbles down until it finds the right level.
void push_down(int * const aa, int len)
{
  for (int l = 2; l < len; l <<= 1)
    {
      if (l+1 < len && aa[l+1]>aa[l]) ++l;
      
      if (aa[l] > aa[l>>1])
	{
	  swap(aa[l], aa[l>>1]);
	}
    }
}


int main(int argc, char ** argv)
{
  const int N = 700000;
  int * a = new int[N];

  srand(time(NULL));

  for (int i=0; i < N; ++i) a[i] = rand(); 

// uncomment for nasty slow bubble sort
  //#define BUBBLE
#ifdef BUBBLE

  for (int i=N-1; i > 0; i--)
    {
      int max = a[0];
      int indx = 0;
      for (int j=1; j <= i; ++j)
	{
	  if (a[j] > max)
	    {
	      max = a[j];
	      indx = j;
	    }
	}
      swap(a[i], a[indx]);
    }

#else // heap sort
  heapify(a, N);
  
  int * aa = a-1;

  for (int i=N; i > 1; i--)
    {
      swap(aa[1], aa[i]);
      push_down(aa, i);
    }

#endif
  
  for (int i=0; i < 10; ++i)
    {
      cout << a[i] << endl;
    }

  delete [] a;

  return 0;
}

