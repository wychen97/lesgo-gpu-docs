# Current Release

The maintained release is the `main` branch of
[`wychen97/lesgo-gpu-porting`](https://github.com/wychen97/lesgo-gpu-porting).
This page reflects source checkpoint
`f46eca2fbaad00793da140ce77de4830b3098026`.

## Implementation status

The solver now builds its GPU path with NVHPC separate-memory mode. Core LES
arrays have persistent device storage, and copies are made at defined setup,
restart, output, diagnostic, or compatibility boundaries. Regular timesteps do
not depend on implicit managed-memory migration.

| Component | Release status |
| --- | --- |
| Derivatives, convection, pressure, projection | GPU-enabled |
| SGS/stress models | GPU-enabled for disabled SGS and values `1` through `5` |
| ADM and ATM | GPU-enabled; ATM includes rigid and structural configurations |
| Scalar transport | GPU-enabled when both `USE_SCALARS` and `USE_SCALARS_GPU` are on |
| Concurrent precursor | CPU/GPU compact validation available, including scalar coupling |
| Inflow and forcing | HIT, shifted inflow, Coriolis, and sponge compact checks available |
| Level Set | GPU path and CPU/GPU restart matrix validated on Derecho and Delta |

## Compatibility boundaries

Some work remains intentionally on the host:

- configuration parsing and file I/O;
- one-time geometry and model setup;
- selected diagnostics and validation snapshots;
- documented compatibility paths for model operations that are not regular
  full-field timestep kernels.

These boundaries are not evidence that the solver uses managed memory. The
GPU build uses `-gpu=mem:separate`; host and device ownership must therefore be
explicit.

## Release gates

A change is ready for `main` only after the relevant checks pass:

1. strict CMake configuration and compilation on a supported cluster;
2. the case-specific CPU/GPU numerical comparison;
3. restart continuity when the changed state persists across a checkpoint;
4. MPI-rank coverage appropriate to the changed communication path;
5. repository readiness checks and documentation checks.

The public compact cases are designed for these gates. Production performance
claims require a separate, controlled benchmark with identical physics, grid,
MPI layout, output settings, and averaging rules.
