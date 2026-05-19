# Pressure Solver

The pressure solver is the most communication-sensitive part of the multi-GPU branch. The current implementation keeps the pressure equation and zero-mode handling intact while moving the dominant work to GPU kernels, cuFFT, and a pressure-specific transpose-Thomas path.

## Primary Files

| File | Role |
|---|---|
| `press_stag_array.f90` | Pressure RHS, pressure halos, cuFFT orchestration |
| `tridag_array.f90` | Tridiagonal solve and pressure transpose-Thomas helper |
| `mpi_transpose_mod.f90` | MPI transpose support |

## Implemented GPU Changes

| Area | Change |
|---|---|
| Forward/inverse FFT | cuFFT batched plans |
| RHS assembly | GPU kernels with combined RHS halo path |
| Tridiagonal solve | GPU Thomas path with cached coefficients |
| Multi-GPU pressure | nproc==2 specialized pressure transpose-Thomas helper |
| Output path | Direct Thomas output avoids a separate pack-out stage where possible |
| Timing | Clean production timing separated from detailed diagnostic timing |

## Retained Controls

| Switch | Purpose |
|---|---|
| `LESGO_PRESS_RHS_HALO_COMBINED` | Fallback-safe control for combined RHS halo |
| `LESGO_PRESS_TRANSPOSE_GENERIC` | Force old generic transpose helper |
| `LESGO_PRESS_DIRECT_THOMAS_OUT` | Control direct Thomas output path |
| `LESGO_PRESS_STAGE_TIMING` | Enable pressure stage timing |
| `LESGO_PRESS_TRANSPOSE_TIMING` | Enable transpose helper timing |

Do not replace Thomas with PCR, CR, or SPIKE-style solvers unless that is a deliberate new algorithmic project. The current production goal is to preserve the original Thomas solve and optimize ownership/layout around it.
