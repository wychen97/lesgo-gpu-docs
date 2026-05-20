# SGS And Stresses

The SGS module was one of the largest GPU porting targets because it contains repeated full-domain tensor work plus MPI halo exchange.

## Primary Files

| File | Role |
|---|---|
| `sgs_stag_util.f90` | SGS tensor construction, dynamic model helpers, calc_Sij, Nu_t, tau handling |
| `divstress_uv.f90` | Divergence of horizontal stress components |
| `divstress_w.f90` | Divergence of vertical stress components |
| `std_dynamic.f90`, `scaledep_dynamic.f90` | Dynamic SGS model support |
| `interpolag_Ssim.f90`, `interpolag_Sdep.f90`, `lagrange_Ssim.f90`, `lagrange_Sdep.f90` | Lagrangian dynamic model support |

## Implemented GPU Changes

| Area | Change |
|---|---|
| `calc_Sij` | GPU path with explicit CUDA Fortran interior kernel option |
| Nu_t and tau loops | GPU kernels for repeated full-domain operations |
| Tau halo | Combined contiguous device halo path for nproc==2 |
| dwdz halo | Device-buffer path audited; further micro-variants were not beneficial |
| Stage timing | Non-strict timing mode avoids charging queued work to the wrong stage |
| Default half-channel SGS path | `sgs_model=5` validation exercises the Lagrangian scale-dependent path, including the `F_NN`, `F_QN`, `F_MM`, and `F_LM` update work |

## Default Half-Channel Validation Note

The `128^3` default half-channel case uses the Lagrangian scale-dependent SGS model after the dynamic model initializes. For that validation, the GPU path covers the runtime loops in `sgs_stag_util.f90`, `scaledep_dynamic.f90`, `interpolag_Sdep.f90`, and `lagrange_Sdep.f90`. The retained optimized defaults are the explicit `calc_Sij` interior kernel and the combined two-rank tau halo; diagnostic timers remain off unless explicitly enabled.

## Retained Controls

| Switch | Purpose |
|---|---|
| `LESGO_SGS_HALO_COMBINED` | Fallback-safe control for combined tau halo |
| `LESGO_SGS_CALCSIJ_EXPLICIT` | Fallback-safe control for explicit calc_Sij interior path |
| `LESGO_SGS_STAGE_TIMING` | Enable SGS diagnostic timing |
| `LESGO_SGS_STRICT_SYNC` | Restore strict sync behavior for debugging |

Do not change SGS formulas or array bounds while optimizing communication. For SGS changes, validate divergence, kinetic energy, bottom wall stress, mean velocity, Reynolds stresses, SGS model/stress build timing, divstress timing, and tau halo behavior on 2 MPI / 2 GPU.
