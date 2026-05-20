# Validation And Performance

This page keeps two separate validation records:

- the default `128^3` half-channel physics validation requested for turbulence realism;
- the short `480 x 240 x 240` actuator-turbine benchmark used for CPU/GPU performance comparisons.

## Default Half-Channel Validation

This page records the physics validation requested for the standard LESGO half-channel case: no turbines, pressure-gradient forcing, rough-wall lower boundary, and periodic horizontal directions. The purpose is not a short deterministic CPU/GPU bitwise check; it is to confirm that the GPU port still produces a physically turbulent channel-flow solution.

### Case Setup

| Item | CPU Run | GPU Run |
|---|---:|---:|
| Grid | `128 x 128 x 128` | `128 x 128 x 128` |
| Active physics | Default dynamic/Lagrangian SGS | Default dynamic/Lagrangian SGS |
| Turbines | Off | Off |
| Runtime | `50,000` steps | `50,000` steps |
| Averaging window | `25,000-50,000` | `25,000-50,000` |
| Hardware layout | 32 MPI ranks | 2 MPI ranks / 2 GPUs |

### Scalar Checks

| Run | Final Divergence | Final KE | Bottom Wall Stress |
|---|---:|---:|---:|
| CPU, 32 MPI | `0.2325891E-12` | `0.2335050E+03` | `0.9475399E+00` |
| GPU, 2 MPI / 2 GPU | `0.3059036E-06` | `0.2330924E+03` | `0.9105967E+00` |

These values are close enough for a turbulent long-run validation. The instantaneous trajectory is expected to decorrelate because small floating-point differences grow chaotically in turbulence.

### Mean Velocity

The mean velocity profile is compared against the rough-wall log-law trend. CPU and GPU are shown on identical axes, with `U+` plotted across the full wall-normal height.

<div class="lesgo-image-frame">
  <img src="../../assets/default-channel-128-mean-velocity.png" alt="CPU and GPU mean velocity profiles for the default 128 cubed half-channel case">
</div>

| Metric | Value |
|---|---:|
| Mean velocity L1 difference | `4.93354E-02` |
| Mean velocity relative L2 difference | `2.71536E-03` |

### Reynolds Stresses

Second-order statistics converge more slowly than the mean profile. A few-percent difference in `u'u'` is therefore normal for this averaging window, provided that the component shapes and near-wall behavior remain consistent.

<div class="lesgo-image-frame">
  <img src="../../assets/default-channel-128-reynolds-stress.png" alt="CPU and GPU Reynolds-stress profiles for the default 128 cubed half-channel case">
</div>

| Metric | Value |
|---|---:|
| `u'u'` L1 difference | `5.43758E-02` |
| `u'u'` relative L2 difference | `3.50556E-02` |
| `-u'w'` L1 difference | `9.21853E-03` |
| `-u'w'` relative L2 difference | `2.61361E-02` |

### Instantaneous Z-Plane And PDF

The mid-plane contours compare the instantaneous `u'` field at `z/H = 0.5` and step `50,000`. These are not expected to match pointwise after a long chaotic turbulent integration. The contours are therefore used only to check that both runs show physically turbulent structures, while the normalized PDF compares the instantaneous fluctuation distribution more directly.

<div class="lesgo-image-frame">
  <img src="../../assets/default-channel-128-zplane-contours.png" alt="CPU and GPU instantaneous z-plane velocity fluctuation contours for the default 128 cubed half-channel case">
</div>

| Instantaneous metric | CPU | GPU |
|---|---:|---:|
| `u'` RMS on `z/H=0.5` plane | `1.38334` | `1.78827` |
| Normalized PDF skewness | `-0.341666` | `-0.389028` |
| Normalized PDF kurtosis | `2.98154` | `2.63843` |
| Plane file | `vel.z-0.50000.50000.c15.bin` | `vel.z-0.50000.50000.c0.bin` |

| PDF Agreement Metric | Value |
|---|---:|
| L1 distance between normalized PDFs | `9.19189E-02` |

### Interpretation

The GPU result passes the current physical validation gate: the mean profile follows the expected log-law trend, the Reynolds-stress profiles have the correct structure, and the instantaneous mid-plane field shows developed turbulent streaks and patches rather than laminar behavior.

## 480x240x240 ATM Benchmark

This is the short no-I/O verification case for the actuator turbine model at `480 x 240 x 240`. The comparison uses the same case setup and reports compute time only.

### Test Setup

| Item | Setting |
|---|---|
| Case | `test-cases/actuator_turbine_model` |
| Grid | `Nx=480`, `Ny=240`, `Nz=240` |
| Active module | `USE_ATM=ON` |
| Output policy | Heavy domain/plane output disabled for timing runs |
| CPU sweep | 24, 40, 60, 80, 120 MPI ranks; 3 steps |
| GPU timing | A100 runs, average of steps 2-10 |
| GPU configurations | 1 GPU / 1 MPI and 2 GPUs / 2 MPI measured on same-node A100 runs |

### Runtime Summary

| Run | Step Time | Speedup vs Best CPU | Notes |
|---|---:|---:|---|
| Best CPU | `0.634 s/step` | `1.0x` | 120 MPI ranks |
| 1 GPU / 1 MPI | `0.103 s/step` | `6.1x` | A100, optimized default path |
| 2 GPUs / 2 MPI | `0.061 s/step` | `10.4x` | Same-node A100 run |

<div class="lesgo-image-frame">
  <img src="../../assets/benchmark-480-step-times.svg" alt="480x240x240 step time over iterations">
</div>

<div class="lesgo-image-frame">
  <img src="../../assets/benchmark-480-gpu-scaling-2gpu.svg" alt="GPU scaling chart for the 480 workload">
</div>

### CPU Sweep

The CPU baseline is selected from this short rank sweep.

<div class="lesgo-image-frame">
  <img src="../../assets/benchmark-480-cpu-sweep.svg" alt="CPU line sweep for the 480 workload">
</div>

### Module Breakdown

<div class="lesgo-image-frame">
  <img src="../../assets/benchmark-480-module-breakdown-2gpu.svg" alt="CPU and GPU module timing breakdown for the 480 workload">
</div>

### Flow-Field Verification

The figure compares the `z=2.5` velocity plane at step 10. The left and center panels show the CPU and GPU `u` field; the right panel shows the absolute difference.

<div class="lesgo-image-frame">
  <img src="../../assets/benchmark-480-flow-compare.svg" alt="CPU and GPU flow-field comparison on the z=2.5 plane">
</div>

| Component | L1 Mean Error | L2 Error | Max Error |
|---|---:|---:|---:|
| `u` | `4.97E-16` | `6.60E-16` | `3.11E-15` |
| `v` | `1.57E-16` | `2.06E-16` | `9.98E-16` |
| `w` | `7.75E-17` | `1.02E-16` | `5.06E-16` |

### Scalar Checks

| Run | Divergence | KE | Bot Wall Stress |
|---|---:|---:|---:|
| CPU, 2 MPI, step 10 | `0.2681714E-03` | `0.4998491E+00` | `0.8686115E-05` |
| 1 GPU / 1 MPI, step 10 | `0.2681679E-03` | `0.4998491E+00` | `0.8686115E-05` |
| 2 GPUs / 2 MPI, step 10 | `0.2681714E-03` | `0.4998491E+00` | `0.8686115E-05` |

### Reproduce

```bash
cd /glade/u/home/wchen/lesgo-gpu-test/test-cases/actuator_turbine_model
qsub job_compare_cpu120.pbs
qsub job_compare_gpu1_noio.pbs
qsub job_compare_gpu2_noio.pbs
```
