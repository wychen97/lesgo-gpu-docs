# LESGO GPU Porting Guide

This documentation is an engineering handoff for the GPU-ported LESGO branches. It is written for developers who already understand the original CPU LESGO code and need to understand what changed, where the GPU paths live, how MPI/GPU ownership works, and how to modify the code without breaking validated behavior.

The official target is FP64. The mature GPU path assumes CUDA Fortran with NVHPC, CUDA-aware MPI, and the current z-slab MPI decomposition. A separate work-in-progress branch, `gpu-explicit-residency-wip`, is now available for collaborator testing of the explicit device-residency refactor.

## What This Guide Covers

| Topic | Where To Read |
|---|---|
| Main timestep ownership and timings | [Main Timestep Flow](main-flow.md) |
| Current explicit-residency WIP branch | [Explicit Residency WIP](explicit-residency.md) |
| GPU memory, synchronization, and MPI rules | [GPU Architecture](architecture.md) |
| Derecho build and runtime controls | [Build And Runtime](build-runtime.md) |
| Correctness checks and performance baselines | [Validation And Performance](validation-performance.md) |
| Detailed module porting notes | [Module Notes](modules/core-solver.md) |
| Generated 69-file audit matrix | [File Audit](file-audit.md) |

## Current Branch Status

There are two distinct states to keep separate:

| Branch/status | Meaning |
|---|---|
| Mature optimized GPU path | Validated module-by-module for the documented short benchmarks |
| `gpu-explicit-residency-wip` | WIP refactor toward explicit GPU residency; not fully managed-free and not final production code |

The explicit-residency branch still compiles with `-gpu=mem:managed` because some fallback paths and non-refactored modules still depend on managed-memory semantics. Its purpose is to let collaborators test and continue the residency refactor, not to claim that all managed memory has been removed.

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
