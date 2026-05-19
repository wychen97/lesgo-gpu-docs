<div class="lesgo-hero">
  <h1>GPU Migration Overview</h1>
  <p>This guide explains the production GPU branch at a practical level: build configuration, timestep flow, module changes, validation, and the generated file audit.</p>
  <div class="lesgo-actions">
    <a class="lesgo-button primary" href="cmake-environment/">Build Setup</a>
    <a class="lesgo-button" href="main-flow/">Main Flow</a>
    <a class="lesgo-button" href="validation-performance/">480 Benchmark</a>
    <a class="lesgo-button" href="file-audit/">File Audit</a>
  </div>
</div>

## Essential Pages

| Topic | Page |
|---|---|
| Correct CMake options and environment variables | [CMake And Environment](cmake-environment.md) |
| Main timestep ownership and module timing | [Main Timestep Flow](main-flow.md) |
| GPU memory, synchronization, and MPI rules | [GPU Architecture](architecture.md) |
| 480x240x240 CPU/GPU comparison | [Validation And Performance](validation-performance.md) |
| Generated 75-file audit matrix | [File Audit](file-audit.md) |

## Scope

The GPU branch keeps the original LESGO equations and timestep order. Runtime timestep loops are GPU-enabled where they matter; I/O, parsing, and one-time setup can remain CPU-side when they do not affect timestep performance.

Regenerate the file audit after source changes:

```bash
cd /glade/u/home/wchen/lesgo-gpu-test
python3 tools/generate_gpu_file_audit.py
```
