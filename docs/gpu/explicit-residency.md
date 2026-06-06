# Explicit Residency WIP Branch

The current explicit-residency work is available in the LESGO source repository as:

```text
gpu-explicit-residency-wip
```

Source branch:

[wychen97/lesgo/tree/gpu-explicit-residency-wip](https://github.com/wychen97/lesgo/tree/gpu-explicit-residency-wip)

This branch is intended for collaborator testing and code review. It is **not** a final production release.

## What This Branch Is Testing

The purpose is to move active timestep data away from implicit CUDA managed-memory migration and toward explicit device residency:

| Area | Current explicit-residency work |
|---|---|
| Build route | Adds `USE_LES_GPU=ON` and `PPLES_GPU` compile-time path |
| Core GPU modules | Adds helper modules for FFT, tridiagonal solve, convection, derivatives, pressure, Lagrangian SGS, and SGS kernels |
| ATM force metadata | Adds persistent GPU force-field shadow arrays |
| ATM blade data | Adds explicit device mirrors for blade points and blade forces |
| ATM gather path | Packs/unpacks blade forces through device mirrors in the normal slim GPU gather path |
| Nacelle scratch | Converts the small nacelle scratch buffer to explicit device storage in the `PPLES_GPU` path |

The design goal is direct: keep hot timestep arrays resident on the GPU, use explicit copies only at known boundaries, and avoid hidden managed-memory migrations caused by host touches.

## What Is Still Not Complete

Managed memory has **not** been fully removed.

The branch still compiles with:

```text
-gpu=mem:managed
```

This remains necessary because fallback paths and some non-refactored modules still depend on managed-memory semantics. Do not remove this flag until each remaining managed-memory island has an explicit device-resident replacement and has passed validation.

## Current Validation Level

The latest strict checks on Derecho were short ATM validation runs:

| Check | Result |
|---|---|
| Experimental build | `build_acc_residency` passed |
| Default build | `build_codex_default` passed |
| 1 GPU ATM short validation | Passed |
| 2 GPU ATM short validation | Passed |
| Divergence | `0.1466988E-03` |
| Kinetic energy | `0.4999399E+00` |
| Bottom wall stress | `0.2316200E-05` |

The point-owner ATM load-balancing path remains experimental. It has run as a smoke test, but it should not be treated as production-validated until strict same-step force, thrust, torque, power, and flow-field comparisons are completed.

## Recommended Collaborator Workflow

1. Build the default executable and the explicit-residency executable from a clean checkout.
2. Run the existing short ATM validation on 1 GPU and 2 GPUs.
3. Confirm divergence, kinetic energy, and bottom wall stress match the recorded values above.
4. Audit remaining `managed` declarations before removing `-gpu=mem:managed`.
5. Convert one module at a time to explicit device residency.
6. After each conversion, rerun both build targets and the short validation.

## Branch Policy

Use this branch as a WIP integration point. Do not present it as fully managed-free or fully optimized. The correct claim is:

> The branch introduces an explicit-residency route and validates selected active ATM paths, while preserving managed-memory compatibility for fallback and incomplete modules.
