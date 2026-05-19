# Validation And Performance

<span class="lesgo-status">updated benchmark policy</span>

This page separates **correctness validation** from **performance benchmarking**. The numbers currently shown are smoke-validation values from the cleanup run; they prove that the GPU code still produces the expected diagnostics, but they should not be used as final CPU/GPU speedup claims until the grid, CPU core count, CMake options, `lesgo.conf`, and I/O policy are all locked.

<div class="lesgo-image-frame">
  <img src="../../assets/validation-benchmark-pipeline.svg" alt="Validation and benchmark workflow diagram">
</div>

<div class="lesgo-callout">
<strong>Current status:</strong> correctness checks are valid; final performance comparison is pending. The final benchmark must compare CPU and GPU using the same grid and active modules.
</div>

## Correctness Release Gates

| Area | Required Checks |
|---|---|
| Flow field | Divergence, kinetic energy, bottom wall stress |
| Pressure | Divergence, pressure timing, pressure checksum or norm when touching solver internals |
| SGS | Divergence, KE, wall stress, tau halo consistency |
| ATM forcing | Global force sums, turbine thrust, torque, power, sampled velocity checksum |
| MPI paths | Same diagnostics for 1 MPI / 1 GPU and multi-MPI / multi-GPU |

## Latest Smoke Validation

These values are from a short post-cleanup run. They are useful for regression detection, not for final benchmark reporting.

| Case | Divergence | KE | Bot Wall Stress | Step Time | Interpretation |
|---|---:|---:|---:|---:|---|
| 1 MPI / 1 GPU | `0.2681679E-03` | `0.4998491E+00` | `0.8686115E-05` | `0.1051949 s` | Correctness smoke test |
| 2 MPI / 2 GPU | `0.2681714E-03` | `0.4998491E+00` | `0.8686115E-05` | `0.0634820 s` | Correctness smoke test |

## Why The Old Table Was Misleading

The previous version showed module timings without a corresponding CPU table and without a frozen benchmark grid. That made the data look like a final speedup comparison. It was not. For a meaningful CPU/GPU comparison, all of the following must be identical or explicitly documented:

| Requirement | Required State Before Reporting Speedup |
|---|---|
| Grid | Fixed, for example `Nx x Ny x Nz` documented in the table caption |
| Active modules | Same CMake options and same runtime flags |
| Input file | Same `lesgo.conf`, same turbine/ATM inputs |
| I/O | Either disabled or measured separately |
| CPU baseline | Sweep core counts and report the fastest valid CPU run |
| GPU baseline | Report 1 GPU, same-node multi-GPU, and multi-node if relevant |
| Numerical checks | Divergence, KE, wall stress, and ATM force quantities match |

## Final Benchmark Table Template

Fill this table only after the case is locked.

| Module | Best CPU Time | CPU MPI Ranks | 1 GPU Time | 2 GPU Time | Speedup vs Best CPU | Notes |
|---|---:|---:|---:|---:|---:|---|
| Forcing | pending | pending | pending | pending | pending | Include ATM settings |
| Derivatives | pending | pending | pending | pending | pending | Same grid required |
| SGS & Stresses | pending | pending | pending | pending | pending | Same SGS model required |
| Convection | pending | pending | pending | pending | pending | No-I/O timing preferred |
| Pressure Solver | pending | pending | pending | pending | pending | Include transpose/RHS halo mode |
| Projection | pending | pending | pending | pending | pending | Usually small but still tracked |
| Other | pending | pending | pending | pending | pending | Explain what is included |
| Total step | pending | pending | pending | pending | pending | Primary headline value |

## CPU Baseline Protocol

The CPU comparison should be a core-count sweep, not a single arbitrary CPU run. Recommended minimum:

| Run | Purpose |
|---|---|
| CPU 1 node, low rank count | Establish scaling start point |
| CPU 1 node, medium rank count | Detect best on-node balance |
| CPU 1 node, high rank count | Detect saturation or MPI overhead |
| CPU fastest valid setting | Use this as the official CPU baseline |
| GPU 1 MPI / 1 GPU | Single-GPU baseline |
| GPU 2 MPI / 2 GPU same node | Multi-GPU communication baseline |
| GPU multi-node, if needed | Scaling and network sensitivity |

## Timing Rules

Diagnostic timers can change performance by adding synchronization. Use production timings with diagnostic switches off for headline results. Use detailed timers only to attribute bottlenecks.

| Timing Mode | Use Case |
|---|---|
| Clean production timing | Performance reporting |
| Stage timing | Coarse module regression checks |
| GPU event timing | Kernel attribution without overcharging sync debt |
| Strict sync timing | Debug only; not representative of production |

## Reporting Standard

A final performance figure should include this caption information:

```text
Grid: <Nx x Ny x Nz>
Case: <test-case path or name>
CMake options: <active options>
CPU baseline: <rank count, node type, compiler, average step time>
GPU baseline: <GPU model, MPI ranks, average step time>
I/O policy: <included or excluded>
Validation: <divergence, KE, wall stress, force checks>
```
