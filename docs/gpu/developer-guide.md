# Developer Guide

## Before Editing

1. Identify whether the routine is timestep-active, initialization-only, or I/O-only.
2. Check the [File Audit](file-audit.md) for the file's current GPU status and retained switches.
3. Find the immediate validation baseline for the case you are modifying.
4. Decide whether the change needs 1-GPU validation only or both 1-GPU and 2-GPU validation.

## Adding Or Modifying GPU Kernels

Prefer CUF kernel loops for straightforward structured loops. Use explicit CUDA Fortran kernels when CUF creates many tiny launches, poor occupancy, or awkward flattened indexing.

Avoid these patterns inside production timestep code:

| Avoid | Reason |
|---|---|
| Host `maxval`, `sum`, or debug print on large managed arrays | Can trigger hidden migration |
| MPI on non-contiguous array sections | May create compiler temporaries or invalid GPU-aware MPI behavior |
| Per-small-kernel `cudaDeviceSynchronize()` | Charges queued work to the wrong stage and slows production |
| Rebuilding invariant coefficients every step | Wastes GPU time and memory bandwidth |
| Adding a new env switch for every experiment | Makes the code harder to read and maintain |

## MPI Exchange Pattern

```text
pack local data into persistent contiguous device send buffer
synchronize once if MPI will read GPU data
perform device-pointer MPI exchange
unpack received device buffer on GPU
validate diagnostics against old path
```

## Adding A Fallback Switch

Do not add a switch unless it protects a validated numerical fallback, controls a major experimental algorithm, enables concise diagnostic timing, or helps debug MPI/GPU correctness.

## Validation Checklist

```text
[ ] Build succeeds
[ ] 1 MPI / 1 GPU short run succeeds
[ ] 2 MPI / 2 GPU short run succeeds if MPI path changed
[ ] Divergence unchanged
[ ] Kinetic energy unchanged
[ ] Bottom wall stress unchanged
[ ] Module timing not regressed unexpectedly
[ ] New switch documented or removed
[ ] File audit regenerated if source files changed
```
