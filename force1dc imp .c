#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
#include <xmmintrin.h>
#include <malloc.h>

// Define the missing variables
#define N 1000
#define rm 0.1

double get_wtime(void) {
  struct timeval t;
  gettimeofday(&t, NULL);
  return (double)t.tv_sec + (double)t.tv_usec * 1.0e-6;
}

__m128 compute_force_sse(float *positions, __m128 x0)
{
  __m128 rm2 = _mm_set1_ps(rm * rm);
  __m128 force = _mm_setzero_ps();
  
  for (size_t i = 0; i < N; i += 4) {
    __m128 pos = _mm_loadu_ps(positions + i);
    __m128 r = _mm_sub_ps(x0, pos);
    __m128 r2 = _mm_mul_ps(r, r); // r^2
    __m128 s2 = _mm_div_ps(rm2, r2); // (rm/r)^2
    __m128 s6 = _mm_mul_ps(_mm_mul_ps(s2, s2), s2); // (rm/r)^6
    __m128 term = _mm_sub_ps(s6, s2); // (rm/r)^6 - (rm/r)^2
    force = _mm_add_ps(force, _mm_div_ps(_mm_mul_ps(_mm_set1_ps(12.0 * 1.0), term), r));
  }
  
  return force;
}

int main(int argc, const char **argv)
{
  srand48(1);

  float *positions;
  positions = (float *)malloc(N * sizeof(float));

  for (size_t i = 0; i < N; i++)
    positions[i] = drand48() + 0.1;

  double start, end;

  float x0[] = {0., -0.1, -0.2};
  float f0[] = {0, 0, 0};

  const size_t repetitions = 1000;
  start = get_wtime();

  __m128 x0_sse = _mm_set_ps(x0[2], x0[2], x0[1], x0[0]);
  __m128 f0_sse = _mm_setzero_ps();

  for (size_t i = 0; i < repetitions; i++) {
    f0_sse = _mm_add_ps(f0_sse, compute_force_sse(positions, x0_sse));
  }

  _mm_storeu_ps(f0, f0_sse);

  end = get_wtime();

  for (size_t j = 0; j < 3; ++j)
    printf("Force acting at x_0=%lf : %lf\\n", x0[j], f0[j] / repetitions);

  printf("elapsed time: %lf mus\\n", 1e6 * (end - start));
  return 0;
}
 /* Force acting at x_0=0.000000 : 879.933716\nForce acting at x_0=-0.100000 : 396.914124\nForce acting at x_0=-0.200000 : 170.291214\nelapsed time: 518.083572 mus
 */
