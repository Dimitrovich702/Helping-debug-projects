#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
#include <omp.h>

//#define GRAV_CONST 6.67408e-11

typedef struct Particle_s
{
  double x, y, z, m;
  double fx, fy, fz;
} Particle_t;

void initParticles(Particle_t *particles, int n)
{
    srand48(10);
    for (int i = 0; i < n; i++) {
        particles[i].x = 10 * drand48();
        particles[i].y = 10 * drand48();
        particles[i].z = 10 * drand48();
        particles[i].m = 1e7 / sqrt((double)n) * drand48();
    }
}

void computeGravitationalForces(Particle_t *particles, int n)
{
    const double GRAV_CONST = 6.67408e-11;
    
    // OpenMP parallelize the computation
    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        double x_i = particles[i].x;
        double y_i = particles[i].y;
        double z_i = particles[i].z;
        double m_i = particles[i].m;

        double fx_i = 0.0, fy_i = 0.0, fz_i = 0.0;
        
        // Compute gravitational forces between particles
        #pragma omp simd reduction(+: fx_i, fy_i, fz_i)
        for (int j = 0; j < n; j++) {
            if (i != j) {
                double x_j = particles[j].x;
                double y_j = particles[j].y;
                double z_j = particles[j].z;
                double m_j = particles[j].m;

                double dx = x_i - x_j;
                double dy = y_i - y_j;
                double dz = z_i - z_j;
                double tmp = pow(dx, 2.0) + pow(dy, 2.0) + pow(dz, 2.0);
                double magnitude = GRAV_CONST * m_i * m_j / pow(tmp, 1.5);

                fx_i += dx * magnitude;
                fy_i += dy * magnitude;
                fz_i += dz * magnitude;
            }
        }

        // Update the forces of particle i
        #pragma omp atomic
        particles[i].fx += fx_i;
        #pragma omp atomic
        particles[i].fy += fy_i;
        #pragma omp atomic
        particles[i].fz += fz_i;
    }
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

    Particle_t *particles = (Particle_t *)malloc(n * sizeof(Particle_t));

    initParticles(particles, n);

    double t0 = omp_get_wtime();
    computeGravitationalForces(particles, n);
    double t1 = omp_get_wtime();

    printStatistics(particles, n);

    printf("Elapsed time=%lf seconds", t1 - t0);

    free(particles);

    return 0;
}

// nano potx.c
// gcc -o potx potx.c -g -O3 -Wall -fopenmp -lm 
// ./potx
// 16384 particles: sfx=2.201972e-11 sfy=2.870770e-11 sfz=5.353940e-12
// 16384 particles: minfx=339.008944 maxfx=-347.695580
// 16384 particles: minfy=409.483089 maxfy=-413.017489
// 16384 particles: minfz=432.864766 maxfz=-398.260858
// Elapsed time=6.518719

// very important to have proper results in any code 


