# 480x240x240 Validation And Benchmark

This page is the short no-I/O verification case for the actuator turbine model at `480 x 240 x 240`. The comparison uses the same case setup and reports compute time only.

## Test Setup

| Item | Setting |
|---|---|
| Case | `test-cases/actuator_turbine_model` |
| Grid | `Nx=480`, `Ny=240`, `Nz=240` |
| Active module | `USE_ATM=ON` |
| Output policy | Heavy domain/plane output disabled for timing runs |
| CPU sweep | 24, 40, 60, 80, 120 MPI ranks; 3 steps |
| GPU timing | A100 runs, 10 steps |
| GPU configurations | 1, 2, 3, and 4 same-node A100 GPU runs measured |

## Runtime Summary

| Run | Step Time | Speedup vs Best CPU | Notes |
|---|---:|---:|---|
| Best CPU | `0.634 s/step` | `1.0x` | 120 MPI ranks |
| 1 GPU / 1 MPI | `0.103 s/step` | `6.1x` | A100, optimized default path |
| 2 GPUs / 2 MPI | `0.061 s/step` | `10.4x` | Same-node A100; nproc==2 pressure specialization |
| 3 GPUs / 3 MPI | `0.102 s/step` | `6.2x` | Same-node A100; generic pressure path |
| 4 GPUs / 4 MPI | `0.100 s/step` | `6.4x` | Same-node A100; generic pressure path |

<div class="lesgo-image-frame">
  <img src="../../assets/benchmark-480-step-times.svg" alt="480x240x240 step time over iterations">
</div>

<div class="lesgo-image-frame">
  <img src="../../assets/benchmark-480-gpu-scaling.svg" alt="GPU scaling chart for the 480 workload">
</div>

The 3-GPU and 4-GPU runs are valid same-node A100 measurements, but they do not beat the 2-GPU result because the current pressure solver has a specialized `nproc==2` path. For `nproc=3` and `nproc=4`, pressure falls back to the generic multi-rank path, so pressure dominates the runtime.

## CPU Sweep

The CPU baseline is selected from this short rank sweep.

<div class="lesgo-image-frame">
  <img src="../../assets/benchmark-480-cpu-sweep.svg" alt="CPU line sweep for the 480 workload">
</div>

## Module Breakdown

<div class="lesgo-image-frame">
  <img src="../../assets/benchmark-480-module-breakdown.svg" alt="CPU and GPU module timing breakdown for the 480 workload">
</div>

## Flow-Field Verification

The figure compares the `z=2.5` velocity plane at step 10. The left and center panels show the CPU and GPU `u` field; the right panel shows the absolute difference.

<div class="lesgo-image-frame">
  <img src="../../assets/benchmark-480-flow-compare.svg" alt="CPU and GPU flow-field comparison on the z=2.5 plane">
</div>

| Component | L1 Mean Error | L2 Error | Max Error |
|---|---:|---:|---:|
| `u` | `4.97E-16` | `6.60E-16` | `3.11E-15` |
| `v` | `1.57E-16` | `2.06E-16` | `9.98E-16` |
| `w` | `7.75E-17` | `1.02E-16` | `5.06E-16` |

## Scalar Checks

| Run | Divergence | KE | Bot Wall Stress |
|---|---:|---:|---:|
| CPU, 2 MPI, step 10 | `0.2681714E-03` | `0.4998491E+00` | `0.8686115E-05` |
| 1 GPU / 1 MPI, step 10 | `0.2681679E-03` | `0.4998491E+00` | `0.8686115E-05` |
| 2 GPUs / 2 MPI, step 10 | `0.2681714E-03` | `0.4998491E+00` | `0.8686115E-05` |
| 3 GPUs / 3 MPI, step 10 | `0.2681795E-03` | `0.4998491E+00` | `0.8686115E-05` |
| 4 GPUs / 4 MPI, step 10 | `0.2681829E-03` | `0.4998491E+00` | `0.8686115E-05` |

## Reproduce

```bash
cd /glade/u/home/wchen/lesgo-gpu-test/test-cases/actuator_turbine_model
qsub job_compare_cpu120.pbs
qsub job_compare_gpu1_noio.pbs
qsub job_compare_gpu2_noio.pbs
qsub job_compare_gpu3_noio.pbs
qsub job_compare_gpu4_noio.pbs
```
