# LESGO GPU Porting Guide

This site documents the public LESGO GPU implementation: its build options,
runtime model, validation cases, and the source boundaries that matter when the
solver is changed.

The maintained source is
[`wychen97/lesgo-gpu-porting`](https://github.com/wychen97/lesgo-gpu-porting).
The current `main` branch uses NVHPC, explicit device residency, CUDA-aware MPI
where available, and the original LESGO z-slab decomposition.

## Current release

| Item | Status |
| --- | --- |
| Source branch | `main` |
| Documentation checkpoint | `f46eca2fbaad00793da140ce77de4830b3098026` |
| Arithmetic | FP64 |
| GPU memory model | Separate host/device memory with persistent device data |
| Validated systems | Derecho A100 and Delta A100 RH96 |
| Public examples | Eight cases under `test-cases/` |

## Documentation

| Topic | Page |
| --- | --- |
| Release scope and limitations | [Current Release](gpu/explicit-residency.md) |
| Runnable examples | [Public Test Cases](gpu/test-cases.md) |
| Compilation and submission | [Build and Runtime](gpu/build-runtime.md) |
| CMake options and cluster environments | [CMake and Environment](gpu/cmake-environment.md) |
| GPU ownership and MPI rules | [GPU Architecture](gpu/architecture.md) |
| Validation evidence and historical benchmarks | [Validation and Performance](gpu/validation-performance.md) |
| Source audit references | [Source Inventory](gpu/file-audit.md) |

The compact validation cases establish build, execution, restart, and
CPU/GPU numerical parity. They are not substitutes for statistically converged
turbulence or production-scale performance studies.

<div class="lesgo-affiliation-logo">
  <img src="assets/rosei-logo-footer.png" alt="Johns Hopkins Ralph O'Connor Sustainable Energy Institute" width="220">
</div>
