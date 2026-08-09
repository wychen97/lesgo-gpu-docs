# SGS and Stresses

The SGS path combines full-domain tensor work, filtering, model-specific
updates, and halo exchange. The release covers the disabled SGS path and all
supported runtime model values `1` through `5`; it is not limited to the
Lagrangian scale-dependent `sgs=5` case.

## Main source files

| File group | Role |
| --- | --- |
| `sgs_stag_util.f90` | strain, eddy viscosity, stress construction, and halos |
| `std_dynamic.f90`, `scaledep_dynamic.f90` | dynamic SGS models |
| `lagrange_Ssim.f90`, `lagrange_Sdep.f90` | Lagrangian averaging updates |
| `interpolag_Ssim.f90`, `interpolag_Sdep.f90` | Lagrangian interpolation |
| `divstress_uv.f90`, `divstress_w.f90` | stress divergence |
| `wallstress.f90`, `iwmles.f90` | wall-stress and optional wall-model support |

Regular tensor and interpolation loops execute on the GPU. Halo exchange uses
packed buffers and follows the selected GPU-aware or host-staged MPI route.
Test-filter calls are imported explicitly so the same source compiles with the
Cray/NVHPC MPI and module interfaces used on Derecho and Delta.

## Validation

The channel and turbine cases exercise the common SGS configurations. Repository
readiness checks also audit dispatch coverage so adding an optimized branch for
one `sgs` value cannot silently leave another supported value on an obsolete
path.

Useful diagnostics include velocity divergence, kinetic energy, bottom wall
stress, mean profiles, Reynolds stresses, and model/stress timing. Diagnostic
timers should remain off for release performance measurements.
