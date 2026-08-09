# Developer Guide

## Before editing

1. Classify the routine as timestep-active, setup-only, diagnostic, or I/O.
2. Check the [Source Inventory](file-audit.md) and the code repository's GPU
   coverage audit.
3. Identify which public case exercises the changed path.
4. Determine whether persistent state or MPI communication requires restart or
   multi-rank validation.

## GPU kernel work

Use CUF/OpenACC loops for regular structured work and explicit CUDA Fortran
kernels when launch geometry, scratch storage, or synchronization requires it.

Avoid these patterns inside regular timesteps:

| Pattern | Risk |
| --- | --- |
| Host reduction or print on a device-owned full field | Unplanned transfer or stale host data |
| Full-field `update self`/`update device` without a named boundary | Bandwidth cost and unclear ownership |
| MPI on noncontiguous Fortran sections | Compiler temporaries and unsafe device-pointer behavior |
| Synchronization after every small kernel | Lost overlap and misleading stage timing |
| Rebuilding invariant coefficients | Repeated launch and memory cost |
| New environment variable for a one-off experiment | Unmaintained public interface |

## MPI exchange pattern

```text
pack into a persistent contiguous buffer
satisfy the device-to-MPI dependency
exchange the device buffer, or the compact host fallback buffer
unpack on the owning device
compare against the matched CPU/reference path
```

`USE_GPU_AWARE_MPI=AUTO` is the normal Cray setting. Any edit to communication
must preserve the `OFF` host-staged fallback unless the supported platform scope
is deliberately changed.

## Restart ownership

State that affects the next timestep belongs in the restart contract. This
includes model histories, held forces, structural state, and geometry/transport
state where applicable. A clean short run is not sufficient evidence for a
restart-sensitive change; compare a continuous run with a split continuation at
the same final step.

## Validation checklist

```text
[ ] CMake rejects invalid option combinations
[ ] CPU and GPU builds succeed in the intended environment
[ ] The smallest relevant public case completes
[ ] CPU/GPU numerical acceptance checks pass
[ ] Relevant MPI-rank counts pass when communication changed
[ ] Continuous and restarted runs agree when state changed
[ ] Regular-step timing has no unexplained regression
[ ] Source inventory, environment controls, and testcase record are current
[ ] Repository readiness checks pass
```
