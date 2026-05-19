<div class="lesgo-hero">
  <h1>GPU Migration Overview</h1>
  <p>This guide is for developers who already know CPU LESGO and need to understand the CUDA Fortran, cuFFT, and GPU-aware MPI changes quickly.</p>
  <div class="lesgo-actions">
    <a class="lesgo-button primary" href="main-flow/">Main Flow</a>
    <a class="lesgo-button" href="architecture/">Architecture</a>
    <a class="lesgo-button" href="file-audit/">File Audit</a>
  </div>
</div>

<div class="lesgo-grid">
  <div class="lesgo-card"><strong>Production GPU path</strong><span>Validated GPU implementations are enabled by default.</span></div>
  <div class="lesgo-card"><strong>Conservative numerics</strong><span>The migration preserves LESGO's equations and timestep ordering.</span></div>
  <div class="lesgo-card"><strong>Small debug surface</strong><span>Only core fallback and timing checkpoints remain.</span></div>
</div>

## What This Guide Covers

| Topic | Where To Read |
|---|---|
| Main timestep ownership and timings | [Main Timestep Flow](main-flow.md) |
| GPU memory, synchronization, and MPI rules | [GPU Architecture](architecture.md) |
| Derecho build and runtime controls | [Build And Runtime](build-runtime.md) |
| Correctness checks and benchmark policy | [Validation And Performance](validation-performance.md) |
| How to safely edit GPU kernels | [Developer Guide](developer-guide.md) |
| Generated 75-file audit matrix | [File Audit](file-audit.md) |

## Current Default Philosophy

The GPU branch is no longer a collection of independent experiments. The validated GPU implementation is the default execution path. Fallback switches are kept only where they are useful for isolating numerical or MPI/GPU issues.

The remaining GPU checkpoint count is intentionally small: 17 LESGO-owned GPU environment switches, excluding CPU reference timing and system probes such as `CUDA_VISIBLE_DEVICES` and `MPICH_GPU_SUPPORT_ENABLED`.

## How To Regenerate The File Audit

```bash
cd /glade/u/home/wchen/lesgo-gpu-test
python3 tools/generate_gpu_file_audit.py
```

This refreshes `docs/gpu/file-audit.md` with the current file list, procedure inventory, GPU markers, retained switches, and developer notes.
