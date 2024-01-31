#include <stdio.h>
#include <immintrin.h>

float calculateForce(float x0, float *positions, float rm, size_t N, float eps) {
    float force = 0.0f;
        __m256 xmm_x0 = _mm256_set1_ps(x0);
    for (size_t i = 0; i < N; i += 8) {
        __m256 xmm_positions = _mm256_loadu_ps(positions + i);
        __m256 xmm_diff = _mm256_sub_ps(xmm_x0, xmm_positions);
        __m256 xmm_r2 = _mm256_mul_ps(xmm_diff, xmm_diff);
        __m256 xmm_s2 = _mm256_div_ps(_mm256_set1_ps(rm * rm), xmm_r2);
        __m256 xmm_s6 = _mm256_mul_ps(_mm256_mul_ps(xmm_s2, xmm_s2), xmm_s2);
        __m256 xmm_force = _mm256_mul_ps(_mm256_set1_ps(12.0f * eps), _mm256_sub_ps(_mm256_mul_ps(_mm256_mul_ps(xmm_s6, xmm_s6), xmm_s6), xmm_s6));
        float force_arr[8];
        _mm256_storeu_ps(force_arr, xmm_force);
        for (size_t j = 0; j < 8; j++) {
            force += force_arr[j];
        }
    }
    
    return force;
}

int main() {
    float x0 = 1.0f;
    size_t N = 100;
    float rm = 2.0f;
    float eps = 0.1f;
    float positions[100];
    

    float result = calculateForce(x0, positions, rm, N, eps);
    printf("Force: %f", result);
    
    return 0;
}
/* 
#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>

double get_wtime(void) {
  struct timeval t;
  gettimeofday(&t, NULL);
  return (double)t.tv_sec + (double)t.tv_usec*1.0e-6;
}

/// parameters
const size_t N  = 1<<16; // system size
const float eps = 5.0;    // Lenard-Jones, eps
const float rm  = 0.1;   // Lenard-Jones, r_m


/// compute the Lennard-Jones force particle at position x0
float compute_force(float *positions, float x0)
{
	float rm2 = rm * rm;
	float force = 0.;
	for (size_t i=0; i<N; ++i) {
		float r = x0 - positions[i];
		float r2 = r * r; // r^2
		float s2 = rm2 / r2; // (rm/r)^2
		float s6 = s2*s2*s2; // (rm/r)^6
		force += 12 * eps * (s6*s6 - s6) / r;
	}
	return force;
}

int main(int argc, const char** argv)
{
    /// init random number generator
		srand48(1);

    float *positions;
		positions = malloc(N*sizeof(float));

		for (size_t i=0; i<N; i++)
			positions[i] = drand48()+0.1;

    /// timings
		double start, end;

    float x0[] = { 0., -0.1, -0.2 };
    float f0[] = { 0, 0, 0 };

    const size_t repetitions = 1000;
    start = get_wtime();
    for (size_t i = 0; i < repetitions; ++i )
    {
        for( size_t j = 0; j < 3; ++j )
            f0[j] += compute_force(positions, x0[j]);
    }
    end = get_wtime();

    for(size_t j = 0; j < 3; ++j )
        printf("Force acting at x_0=%lf : %lf\n", x0[j], f0[j]/repetitions);

    printf("elapsed time: %lf mus\n", 1e6*(end-start));
		return 0;
}

*/
