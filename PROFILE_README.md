# Wenyuan Chen

## LESGO GPU Migration

I am working on a GPU-enabled version of LESGO, a Fortran + MPI large-eddy simulation solver. The current branch focuses on CUDA Fortran, GPU-aware MPI, and FP64 production performance for actuator-turbine simulations.

### Highlights

- Ported the main LESGO timestep pipeline to GPU execution.
- Preserved the original CPU solver equations and validation workflow.
- Added CUDA Fortran kernels for derivatives, SGS/stress construction, convection, pressure, projection, and ATM forcing.
- Optimized the pressure solver with cuFFT, GPU Thomas solves, cached coefficients, and a pressure-specific transpose path.
- Optimized multi-GPU communication using packed contiguous device buffers for SGS and pressure halos.
- Reduced GPU debug/configuration checkpoints to a small maintainable core set.
- Built a MkDocs Material handoff guide for developers already familiar with the CPU code.

### Documentation

- GPU migration guide: https://wychen97.github.io/lesgo-gpu-docs/
- File-by-file GPU audit: https://wychen97.github.io/lesgo-gpu-docs/gpu/file-audit/
- Build/runtime notes: https://wychen97.github.io/lesgo-gpu-docs/gpu/build-runtime/
- Validation/performance notes: https://wychen97.github.io/lesgo-gpu-docs/gpu/validation-performance/

### Current Validation Snapshot

| Case | Divergence | Kinetic Energy | Bot Wall Stress | Step Time |
|---|---:|---:|---:|---:|
| 1 MPI / 1 GPU | `0.2681679E-03` | `0.4998491E+00` | `0.8686115E-05` | `0.1051949 s` |
| 2 MPI / 2 GPU | `0.2681714E-03` | `0.4998491E+00` | `0.8686115E-05` | `0.0634820 s` |

### Technical Focus

`Fortran` ? `MPI` ? `CUDA Fortran` ? `NVHPC` ? `cuFFT` ? `GPU-aware MPI` ? `Large-Eddy Simulation` ? `Wind Turbine Modeling`
