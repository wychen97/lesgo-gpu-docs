# Validation And Performance

Validation is performed after each meaningful GPU code change. Matching kinetic energy and divergence alone is not sufficient; bottom wall stress and module-specific quantities are also checked.

## Required Correctness Checks

| Area | Required Checks |
|---|---|
| Flow field | Divergence, kinetic energy, bottom wall stress |
| Pressure | Divergence, pressure timing, pressure checksum or norm when touching solver internals |
| SGS | Divergence, KE, wall stress, tau halo consistency |
| ATM forcing | Global force sums, turbine thrust, torque, power, sampled velocity checksum |
| MPI paths | Same diagnostics for 1 MPI / 1 GPU and multi-MPI / multi-GPU |

## Latest Cleanup Validation

| Case | Divergence | KE | Bot Wall Stress | Step Time |
|---|---:|---:|---:|---:|
| 1 MPI / 1 GPU | `0.2681679E-03` | `0.4998491E+00` | `0.8686115E-05` | `0.1051949 s` |
| 2 MPI / 2 GPU | `0.2681714E-03` | `0.4998491E+00` | `0.8686115E-05` | `0.0634820 s` |

## Module Timing Snapshot

| Module | 1 MPI / 1 GPU | 2 MPI / 2 GPU | Notes |
|---|---:|---:|---|
| Forcing | 0.001192 s | 0.001106 s | ATM path is short for the 2-turbine case |
| Derivatives | 0.017776 s | 0.009083 s | Scales well after GPU port |
| SGS & Stresses | 0.022613 s | 0.012779 s | Combined tau halo and explicit calc_Sij are active |
| Convection | 0.039461 s | 0.020110 s | Main remaining single-GPU cost in this case |
| Pressure Solver | 0.010828 s | 0.012686 s | Multi-GPU pressure remains communication-sensitive |
| Projection | 0.001794 s | 0.001102 s | Small but GPU-enabled |
| Other | 0.011531 s | 0.006615 s | Includes bookkeeping and residual sync cost |

Diagnostic timers can change performance by adding synchronization. Use production timings with diagnostic switches off for headline results. Use detailed timers only to attribute bottlenecks.
