<div class="lesgo-hero">
  <h1>LESGO GPU Migration Guide</h1>
  <p>A focused engineering handoff for the CUDA Fortran and GPU-aware MPI version of LESGO. The guide explains what changed, why it changed, and how to keep the GPU branch correct and maintainable.</p>
  <div class="lesgo-actions">
    <a class="lesgo-button primary" href="gpu/">Start Reading</a>
    <a class="lesgo-button" href="gpu/file-audit/">File Audit</a>
    <a class="lesgo-button" href="gpu/validation-performance/">Validation Plan</a>
  </div>
</div>

<div class="lesgo-grid">
  <div class="lesgo-card"><strong>75 Fortran files audited</strong><span>Generated directly from the current GPU source tree.</span></div>
  <div class="lesgo-card"><strong>17 GPU checkpoints</strong><span>Debug and fallback controls were reduced to a small core set.</span></div>
  <div class="lesgo-card"><strong>FP64 production target</strong><span>The official GPU release path focuses on double precision correctness.</span></div>
  <div class="lesgo-card"><strong>MPI + CUDA Fortran</strong><span>The branch keeps LESGO's z-slab MPI layout while using GPU-aware exchanges.</span></div>
</div>

## What To Read First

| If you want to... | Go here |
|---|---|
| Understand the main timestep changes | [Main Timestep Flow](gpu/main-flow/) |
| Learn the GPU/MPI rules | [GPU Architecture](gpu/architecture/) |
| See retained runtime switches | [Build And Runtime](gpu/build-runtime/) |
| Review validation strategy | [Validation And Performance](gpu/validation-performance/) |
| Inspect every Fortran file | [File-By-File GPU Audit](gpu/file-audit/) |
