# Pressure Solver

The pressure path retains LESGO's pressure equation and tridiagonal method. Its
GPU implementation combines cuFFT, device kernels, packed communication, and a
GPU/MPI tridiagonal pipeline while preserving the outer z-slab decomposition.

## Main source files

| File | Role |
| --- | --- |
| `press_stag_array.f90` | pressure RHS, FFT orchestration, pressure gradients |
| `tridag_gpu.f90` | GPU/MPI tridiagonal pipeline |
| `tridag_array.f90` | shared/reference tridiagonal support |
| `mpi_transpose_mod.f90` | transpose communication support |

`LESGO_TRIDAG_GPU_MPI` can disable the GPU/MPI tridiagonal pipeline for a
controlled comparison. `LESGO_TRIDAG_NCHUNK` changes its chunk count. These are
the maintained pressure-path controls; older collections of per-kernel pressure
switches are not part of the current source.

Pressure changes require multi-rank validation. At minimum, compare divergence,
kinetic energy, pressure-gradient fields, and CPU/GPU continuation behavior.
Timing must distinguish regular steps from steps that perform scheduled output
or additional statistics.
