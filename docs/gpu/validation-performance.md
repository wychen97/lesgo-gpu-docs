# 480x240x240 Validation And Benchmark

This page reports a short no-I/O comparison for the actuator turbine model workload at `480 x 240 x 240`. The goal is to provide a compact CPU/GPU efficiency check, not a full production benchmark campaign.

## Test Case

| Item | Setting |
|---|---|
| Case | `test-cases/actuator_turbine_model` |
| Grid | `Nx=480`, `Ny=240`, `Nz=240` |
| Active module | `USE_ATM=ON` |
| Output policy | Domain/plane output disabled for timing |
| CPU executable | `lesgo-mpi-ATM-cpu` |
| GPU executable | `lesgo-mpi-ATM` |
| CPU sweep | 24, 40, 60, 80, 120 MPI ranks; 3 steps |
| GPU runs | 1 MPI / 1 GPU and 2 MPI / 2 GPU; 10 steps |

## Main Result

| Run | Time Used For Comparison | Speedup vs Best CPU | Notes |
|---|---:|---:|---|
| Best CPU | `0.634 s/step` | `1.0x` | 120 MPI ranks, step 3 |
| 1 GPU / 1 MPI | `0.103 s/step` | `6.1x` | average of steps 2-10 |
| 2 GPU / 2 MPI | `0.061 s/step` | `10.4x` | average of steps 2-10 |

<div class="lesgo-image-frame">
  <img src="../../assets/benchmark-480-step-times.svg" alt="480x240x240 step time over iterations">
</div>

## CPU Sweep

The CPU baseline uses the fastest short CPU run observed in the sweep.

<div class="lesgo-image-frame">
  <img src="../../assets/benchmark-480-cpu-sweep.svg" alt="CPU core-count sweep for the 480 workload">
</div>

## Module Breakdown

The module comparison uses the best CPU run and GPU averages from steps 2-10.

<div class="lesgo-image-frame">
  <img src="../../assets/benchmark-480-module-breakdown.svg" alt="CPU and GPU module timing breakdown for the 480 workload">
</div>

## Correctness Check

| Run | Divergence | KE | Bot Wall Stress |
|---|---:|---:|---:|
| CPU 120 MPI | `0.8952595E-04` | `0.4999226E+00` | `0.8685739E-05` |
| 1 GPU / 1 MPI | `0.2681679E-03` | `0.4998491E+00` | `0.8686115E-05` |
| 2 GPU / 2 MPI | `0.2681714E-03` | `0.4998491E+00` | `0.8686115E-05` |

The CPU sweep ran only 3 steps while the GPU runs ran 10 steps, so the final-step flow fields are not at the same physical time. These values are included as a sanity check for the short comparison, not as a final physics-validation table.

## Reproducing The Short Runs

The comparison scripts already configure the grid and disable heavy output:

```bash
cd /glade/u/home/wchen/lesgo-gpu-test/test-cases/actuator_turbine_model
qsub job_compare_cpu120.pbs
qsub job_compare_gpu1_noio.pbs
qsub job_compare_gpu2_noio.pbs
```

For a publication-quality benchmark, rerun CPU and GPU for the same number of steps, discard warmup steps consistently, and report the average over a longer steady timing window.
