# LESGO GPU Porting Guide

This documentation is an engineering handoff for the GPU-ported LESGO branch in this repository. It is written for developers who already understand the original CPU LESGO code and need to understand what changed, where the GPU paths live, how MPI/GPU ownership works, and how to modify the code without breaking validated behavior.

The official target is FP64. The production path assumes CUDA Fortran with NVHPC, CUDA-aware MPI, and the current z-slab MPI decomposition. Most GPU paths are enabled by default after validation. Remaining environment switches are limited to core fallbacks, timing checkpoints, and validation aids.

## What This Guide Covers

| Topic | Where To Read |
|---|---|
| Main timestep ownership and timings | [Main Timestep Flow](main-flow.md) |
| GPU memory, synchronization, and MPI rules | [GPU Architecture](architecture.md) |
| Derecho build and runtime controls | [Build And Runtime](build-runtime.md) |
| Correctness checks and performance baselines | [Validation And Performance](validation-performance.md) |
| Detailed module porting notes | [Module Notes](modules/core-solver.md) |
| Generated 69-file audit matrix | [File Audit](file-audit.md) |

## Current Default Philosophy

The GPU branch is no longer a collection of independent experiments. The validated GPU implementation is the default execution path. Fallback switches are kept only where they are useful for isolating numerical or MPI/GPU issues.

The remaining GPU checkpoint count is intentionally small: 17 LESGO-owned GPU environment switches, excluding CPU reference timing and system probes such as `CUDA_VISIBLE_DEVICES` and `MPICH_GPU_SUPPORT_ENABLED`.

## How To Regenerate The File Audit

The file audit is generated directly from the repository sources:

```bash
cd /glade/u/home/wchen/lesgo-gpu-test
python3 tools/generate_gpu_file_audit.py
```

This refreshes `docs/gpu/file-audit.md` with the current file list, procedure inventory, GPU markers, retained switches, and developer notes.

## Scope Boundaries

The documentation separates three categories of code:

| Category | Policy |
|---|---|
| Runtime timestep kernels | GPU-enabled or explicitly documented |
| MPI exchange and transpose paths | GPU-aware, contiguous-buffer based where validated |
| I/O, parsing, and one-time initialization | May remain CPU if they do not affect timestep performance |

If future work changes any production GPU path, update the relevant module page and rerun the file audit generator.
