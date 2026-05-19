# Main Timestep Flow

The current GPU branch keeps the original LESGO timestep structure. The migration changes where work is executed and how data is exchanged, not the physical model ordering.

## Runtime Sections

The main loop reports the following cumulative module sections. The latest post-cleanup short validation used the actuator turbine model case on Derecho.

| Section | Main Purpose | Primary Files | 1 MPI / 1 GPU Step-10 Time | 2 MPI / 2 GPU Step-10 Time | GPU Migration Status |
|---|---|---|---:|---:|---|
| Forcing | ATM, inflow/fringe, applied forcing | `forcing.f90`, `atm_lesgo_interface.f90`, `actuator_turbine_model.f90` | 0.001192 s | 0.001106 s | GPU-enabled; point-owner LB remains experimental |
| Derivatives | Spatial derivatives, filtering support | `derivatives.f90`, `test_filtermodule.f90` | 0.017776 s | 0.009083 s | GPU-enabled |
| SGS & Stresses | Dynamic SGS, stress tensor, divstress | `sgs_stag_util.f90`, `divstress_uv.f90`, `divstress_w.f90` | 0.022613 s | 0.012779 s | GPU-enabled with optimized 2-rank halo |
| Convection | Nonlinear convective terms | `convec.f90` and reference variants | 0.039461 s | 0.020110 s | GPU-enabled |
| Pressure Solver | RHS, cuFFT, transpose-Thomas, inverse | `press_stag_array.f90`, `tridag_array.f90` | 0.010828 s | 0.012686 s | GPU-enabled; multi-GPU pressure remains communication-sensitive |
| Projection | Velocity projection and pressure gradient correction | `forcing.f90`, pressure/projection helpers | 0.001794 s | 0.001102 s | GPU-enabled |
| Other | Timers, reductions, residual overhead | `main.f90`, diagnostics, MPI bookkeeping | 0.011531 s | 0.006615 s | Mostly CPU bookkeeping plus unavoidable synchronization |

## Timestep Order

```text
initialize state and device mirrors
for each timestep:
  update forcing / ATM state
  compute derivatives
  build SGS model and stresses
  compute convection
  solve pressure Poisson equation
  project velocity field
  update diagnostics and output counters
finalize
```

The GPU migration preserves this ordering. Optimizations focused on reducing data migration, fusing or enlarging underfilled kernels, using CUDA-aware MPI with contiguous buffers, and avoiding unnecessary `cudaDeviceSynchronize()` calls.

## Data Ownership

The main solver still uses the original one-dimensional z-slab decomposition. Each MPI rank owns a slab in `z`, including halo regions required by derivatives, SGS, pressure RHS, and projection. Multi-GPU work maps one local MPI rank to one GPU.

Pressure is the main exception internally: the optimized pressure solver uses a pressure-only transpose-Thomas helper so full vertical lines can be solved efficiently while preserving the outer z-slab decomposition.

## Numerical Release Gates

| Diagnostic | Purpose |
|---|---|
| Velocity divergence metric | Projection/pressure correctness |
| Kinetic energy | Global flow consistency |
| Bottom wall stress | Boundary and SGS/wall model consistency |
| Force sums and turbine quantities | ATM correctness when forcing paths change |
| Module timing | Regression detection |

| Case | Divergence | KE | Bot Wall Stress | Step Time |
|---|---:|---:|---:|---:|
| 1 MPI / 1 GPU | `0.2681679E-03` | `0.4998491E+00` | `0.8686115E-05` | `0.1051949 s` |
| 2 MPI / 2 GPU | `0.2681714E-03` | `0.4998491E+00` | `0.8686115E-05` | `0.0634820 s` |
