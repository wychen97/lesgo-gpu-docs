<section class="lesgo-hero">
  <div class="lesgo-kicker">CUDA Fortran | GPU-aware MPI | FP64</div>
  <h1>LESGO GPU Porting Guide</h1>
  <p>A concise engineering handoff for the CUDA Fortran port of LESGO: what changed, how to build it, how the GPU/MPI paths are validated, and where each Fortran file fits.</p>
  <div class="lesgo-actions">
    <a class="lesgo-button primary" href="gpu/">Read The Guide</a>
    <a class="lesgo-button" href="gpu/cmake-environment/">Build Setup</a>
    <a class="lesgo-button" href="gpu/validation-performance/">480 Benchmark</a>
    <a class="lesgo-button" href="gpu/file-audit/">File Audit</a>
  </div>
</section>

<div class="lesgo-grid">
  <div class="lesgo-card"><strong>Porting Map</strong><span>Main timestep sections, ownership, and module-level GPU status.</span></div>
  <div class="lesgo-card"><strong>Validation Data</strong><span>CPU/GPU timing, module breakdowns, and flow-field comparison plots.</span></div>
  <div class="lesgo-card"><strong>Source Audit</strong><span>Generated inventory of Fortran files, procedures, GPU markers, and runtime relevance.</span></div>
</div>

## Quick Links

| Need | Page |
|---|---|
| Build the GPU code | [CMake And Environment](gpu/cmake-environment/) |
| Understand timestep modules | [Main Timestep Flow](gpu/main-flow/) |
| Review GPU/MPI architecture | [GPU Architecture](gpu/architecture/) |
| View benchmark plots | [Validation And Performance](gpu/validation-performance/) |
| Inspect every Fortran file | [File-By-File GPU Audit](gpu/file-audit/) |

<div class="lesgo-affiliation-logo">
  <img src="assets/rosei-logo-horizontal-blue.png" alt="Johns Hopkins Ralph O'Connor Sustainable Energy Institute">
</div>
