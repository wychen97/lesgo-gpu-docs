<div class="lesgo-hero">
  <h1>LESGO GPU Migration Guide</h1>
  <p>Concise documentation for the CUDA Fortran and GPU-aware MPI version of LESGO: how to build it, what changed, how it is validated, and where each Fortran file fits.</p>
  <div class="lesgo-actions">
    <a class="lesgo-button primary" href="gpu/">Start Reading</a>
    <a class="lesgo-button" href="gpu/cmake-environment/">Build Setup</a>
    <a class="lesgo-button" href="gpu/validation-performance/">480 Benchmark</a>
    <a class="lesgo-button" href="gpu/file-audit/">File Audit</a>
  </div>
</div>

<div class="lesgo-grid">
  <div class="lesgo-card"><strong>GPU source handoff</strong><span>Architecture and module notes for developers familiar with CPU LESGO.</span></div>
  <div class="lesgo-card"><strong>480x240x240 benchmark</strong><span>CPU sweep, 1-GPU, and 2-GPU short-run comparison with plots.</span></div>
  <div class="lesgo-card"><strong>69-file audit</strong><span>Generated inventory of Fortran files, procedures, GPU markers, and runtime relevance.</span></div>
</div>

## Quick Links

| Need | Page |
|---|---|
| Build the GPU code | [CMake And Environment](gpu/cmake-environment/) |
| Understand timestep modules | [Main Timestep Flow](gpu/main-flow/) |
| Review GPU/MPI architecture | [GPU Architecture](gpu/architecture/) |
| View benchmark plots | [Validation And Performance](gpu/validation-performance/) |
| Inspect every Fortran file | [File-By-File GPU Audit](gpu/file-audit/) |
