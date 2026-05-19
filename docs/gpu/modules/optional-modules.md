# Optional Modules

The production validation path is ATM-focused, but the repository also contains optional modules controlled by CMake options and runtime configuration. The GPU migration policy is to GPU-enable loop-heavy timestep work, while allowing I/O and one-time setup to remain CPU-side when it does not affect timestep performance.

| Module / Option | Main Files | GPU Policy |
|---|---|---|
| `USE_HIT` | `hit_inflow.f90`, `hit_inflow_gpu.f90` | GPU helper retained for runtime inflow work; setup can remain CPU |
| `USE_SCALARS` | `scalars.f90` | Loop-heavy scalar transport paths should remain GPU-enabled when option is active |
| `USE_TURBINES` | `turbines.f90`, `turbines_gpu.f90`, `turbine_indicator.f90` | Runtime turbine loops and indicator operations GPU-enabled where relevant; initialization may remain CPU |
| `USE_LVLSET` | `level_set.f90`, `trees_*_ls.f90`, `level_set_base.f90` | Timestep-level level-set loops require GPU coverage; tree/fmask preprocessing is setup unless repeated |
| `USE_CPS` | `concurrent_precursor.f90` | MPI/precursor coordination remains mostly communication/control logic |
| `USE_CGNS` | `io.f90`, CGNS output paths | Output dependency and I/O path; not a timestep compute target |
| `USE_DYN_TN` | Lagrangian dynamic model files | Dynamic timescale update should use existing GPU/Lagrangian paths if active |

When enabling an optional module for a new case, build with the CMake option enabled, run a minimal smoke case, check the file audit for CPU-heavy uncovered loops, add GPU coverage only for repeated runtime cost, and document any intentionally CPU initialization or I/O loops.
