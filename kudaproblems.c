
// some issue compiling this problem i am gonna debug it to help my dear friend
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
#include <cuda.h>

//#define PRINTSTATS

double get_wtime(void) {
  struct timeval t;
  gettimeofday(&t, NULL);
  return (double)t.tv_sec + (double)t.tv_usec*1.0e-6;
}

typedef struct Particle_s
{
  double x, y, z, m;
  double fx, fy, fz;
} Particle_t;

__global__ void computeGravitationalForcesKernel(Particle_t *particles, const double G, int n)
{
	const int idx = threadIdx.x + blockIdx.x * blockDim.x;
	if (idx < n)
	{
		particles[idx].fx = 0;
		particles[idx].fy = 0;
		particles[idx].fz = 0;

		for (int j=0; j<n; j++)
			if (idx!=j)
			{
				double tmp = pow(particles[idx].x-particles[j].x, 2.0) +
							 pow(particles[idx].y-particles[j].y, 2.0) +
							 pow(particles[idx].z-particles[j].z, 2.0);

				double magnitude = G * particles[idx].m * particles[j].m / pow(tmp, 1.5);

				particles[idx].fx += (particles[idx].x-particles[j].x) * magnitude;
				particles[idx].fy += (particles[idx].y-particles[j].y) * magnitude;
				particles[idx].fz += (particles[idx].z-particles[j].z) * magnitude;
			}
	}
}

void computeGravitationalForces(Particle_t *particles, int n)
{
	const double G = 6.67408e-11;

	// Allocate memory on the GPU for the particles array
	Particle_t *d_particles;
	cudaMalloc((void **)&d_particles, n*sizeof(Particle_t));

	// Copy the data from the host particles array to the GPU particles array
	cudaMemcpy(d_particles, particles, n*sizeof(Particle_t), cudaMemcpyHostToDevice);

	// Launch the CUDA kernel
	dim3 threadsPerBlock(256);
	dim3 numBlocks((n + threadsPerBlock.x - 1) / threadsPerBlock.x);
	computeGravitationalForcesKernel<<<numBlocks, threadsPerBlock>>>(d_particles, G, n);

	// Copy the data from the GPU particles array back to the host particles array
	cudaMemcpy(particles, d_particles, n*sizeof(Particle_t), cudaMemcpyDeviceToHost);

	// Free the memory allocated on the GPU
	cudaFree(d_particles);
}

void printStatistics(Particle_t *particles, int n)
{
	double sfx = 0, sfy = 0, sfz = 0;
  double maxfx = particles[0].fx;
  double minfx = particles[0].fx;
  double maxfy = particles[0].fy;
  double minfy = particles[0].fy;
  double maxfz = particles[0].fz;
  double minfz = particles[0].fz;
  for (int i=0; i<n; i++) {
		if (minfx < particles[i].fx) minfx = particles[i].fx;
		if (maxfx > particles[i].fx) maxfx = particles[i].fx;
		if (minfy < particles[i].fy) minfy = particles[i].fy;
		if (maxfy > particles[i].fy) maxfy = particles[i].fy;
		if (minfz < particles[i].fz) minfz = particles[i].fz;
		if (maxfz > particles[i].fz) maxfz = particles[i].fz;
		sfx += particles[i].fx;
		sfy += particles[i].fy;
		sfz += particles[i].fz;
	}

	printf("%d particles: sfx=%e sfy=%e sfz=%e\n", n, sfx, sfy, sfz);
	printf("%d particles: minfx=%f maxfx=%f\n", n, minfx, maxfx);
	printf("%d particles: minfy=%f maxfy=%f\n", n, minfy, maxfy);
	printf("%d particles: minfz=%f maxfz=%f\n", n, minfz, maxfz);
}


int main(int argc, char *argv[])
{
	int n;

	if (argc == 2)
		n = (1 << atoi(argv[1]));
	else
		n = (1 << 14);

	Particle_t *particles = (Particle_t *)malloc(n*sizeof(Particle_t));

	initParticles(particles, n);

	double t0 = get_wtime();
	computeGravitationalForces(particles, n);
	double t1 = get_wtime();

#if defined(PRINTSTATS)
	printStatistics(particles, n);
#endif

	printf("Elapsed time=%lf seconds\n", t1-t0);

	return 0;
}
