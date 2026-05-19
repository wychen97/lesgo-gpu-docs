# Derivatives, Convection, Projection

## Derivatives

Primary files: `derivatives.f90`, `test_filtermodule.f90`, and shared helpers in `functions.f90`.

The derivative work was GPU-enabled by moving loop-heavy x/y/z derivative operations to CUF kernels. The important optimization lesson was to prefer full 3D kernels over many small `do k` launches. Derivative timing now scales well between 1 GPU and 2 GPUs for the validation case.

## Convection

Primary production file: `convec.f90`. Reference variants are retained as `convec-1dfft-cpu.f90`, `convec-1dfft-gpu.f90`, `convec-2dfft-cpu.f90`, and `convec-2dfft-gpu.f90`.

The production convection path is GPU-enabled and uses the validated GPU implementation by default. Convection remains one of the largest single-GPU costs in the current validation case, but it scales reasonably when the slab is split across two GPUs.

## Projection

Projection is GPU-enabled and now a small fraction of the timestep. The retained `LESGO_PROJECT_STAGE_TIMING` switch exists only for detailed timing attribution. The optimized path uses packed/overlapped halo behavior by default rather than a web of small public switches.

## Boundary And Auxiliary Flow Modules

Files such as `wallstress.f90`, `inflow.f90`, `shifted_inflow.f90`, `sponge.f90`, `coriolis.f90`, and `rmsdiv.f90` have GPU coverage for timestep-relevant loops. Initialization, parsing, and output remain CPU-side where they do not affect timestep performance.
