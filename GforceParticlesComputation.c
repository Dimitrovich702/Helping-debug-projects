#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
#include <omp.h>

#define GRAV_CONST 6.67408e-11

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
    //openmp parallelize the computation
    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        double x_i = particles[i].x;
        double y_i = particles[i].y;
        double z_i = particles[i].z;
        double m_i = particles[i].m;

        double fx_i = 0.0, fy_i = 0.0, fz_i = 0.0;

        // g force particles
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

                // app s f 2 par
                particles[j].fx -= dx * magnitude;
                particles[j].fy -= dy * magnitude;
                particles[j].fz -= dz * magnitude;
            }
        }

        //  kompt gravitational f 2 particle
        particles[i].fx += fx_i;
        particles[i].fy += fy_i;
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

    for (int i = 0; i < n; i++) {
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

    printf("%d particles: sfx=%e sfy=%e sfz=%e", n, sfx, sfy, sfz);
    printf("%d particles: minfx=%f maxfx=%f", n, minfx, maxfx);
    printf("%d particles: minfy=%f maxfy=%f", n, minfy, maxfy);
    printf("%d particles: minfz=%f maxfz=%f", n, minfz, maxfz);
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
// nano komputp.c
// gcc -o komputp komputp.c -g -O3 -Wall -fopenmp -lm 
// ./komputp
// 16384 particles: sfx=5.302674e-03 sfy=5.004778e-02 sfz=-3.048625e-0416384 particles: minfx=678.017889 maxfx=-695.39115916384 particles: minfy=818.966179 maxfy=-826.03497816384 particles: minfz=865.729531 maxfz=-796.521716Elapsed time=6.730759 seconds
