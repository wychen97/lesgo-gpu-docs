# Build And Runtime

## Derecho Build

```bash
cd /glade/u/home/wchen/lesgo-gpu-test
BUILD_JOBS=8 ./derecho_build_gpu.sh
```

The helper installs the executable here:

```text
/glade/u/home/wchen/lesgo-gpu-test/test-cases/actuator_turbine_model/lesgo-mpi-ATM
```

## Primary CMake Options

| Option | Current Role |
|---|---|
| `USE_MPI=ON` | Main production mode |
| `USE_ATM=ON` | Actuator turbine model; active in validation case |
| `USE_LES_GPU=ON` | Experimental explicit-residency LES route in `gpu-explicit-residency-wip` |
| `USE_SAFETYMODE=ON` | Extra safety checks retained |
| `USE_LVLSET=OFF` | Optional level-set path; GPU coverage documented separately |
| `USE_TURBINES=OFF` | Optional actuator disk path |
| `USE_CPS=OFF` | Concurrent precursor path |
| `USE_HIT=OFF` | Homogeneous isotropic turbulence input |
| `USE_CGNS=OFF` | Optional CGNS output dependency |
| `USE_SCALARS=OFF` | Optional scalar transport |

## Retained GPU Environment Checkpoints

| Switch | Default | Purpose |
|---|---|---|
| `LESGO_SGS_HALO_COMBINED` | on | Use optimized combined SGS tau halo path |
| `LESGO_SGS_CALCSIJ_EXPLICIT` | on | Use explicit CUDA Fortran calc_Sij interior path |
| `LESGO_SGS_STAGE_TIMING` | off | Enable SGS diagnostic stage timing |
| `LESGO_SGS_STRICT_SYNC` | off | Re-enable strict per-stage sync for diagnosis |
| `LESGO_PRESS_RHS_HALO_COMBINED` | on | Use optimized combined pressure RHS halo |
| `LESGO_PRESS_TRANSPOSE_GENERIC` | off | Force generic pressure transpose fallback |
| `LESGO_PRESS_DIRECT_THOMAS_OUT` | on | Use direct Thomas output path |
| `LESGO_PRESS_STAGE_TIMING` | off | Enable pressure stage timing |
| `LESGO_PRESS_TRANSPOSE_TIMING` | off | Enable transpose-Thomas helper timing |
| `LESGO_PROJECT_STAGE_TIMING` | off | Enable projection timing details |
| `LESGO_ATM_DIAG_TIMING` | off | Enable detailed ATM timing |
| `LESGO_ATM_POINT_OWNER_LB` | off | Experimental point-owner ATM load balance path |
| `LESGO_ATM_POINT_OWNER_TARGETED` | off | Experimental targeted ATM exchange path |
| `LESGO_ATM_LB_AUTO_SELECT` | off | Probe legacy vs LB and choose faster path |
| `LESGO_ATM_LB_VALIDATE` | off | Compare ATM LB path against legacy quantities |
| `LESGO_MPI_CUDA_DEBUG` | off | Print CUDA/MPI pointer and environment diagnostics |
| `LESGO_MPI_CUDA_SYNC` | off | Force CUDA sync around debug MPI wrappers |

CPU reference timing checkpoints are intentionally preserved but not counted as GPU debug controls:

| Switch | Purpose |
|---|---|
| `LESGO_CPU_REF_TIME_TOTAL` | Optional CPU total reference for reporting `Other` speedup |
| `LESGO_CPU_REF_TIME_FORCING` | Optional CPU forcing reference for reporting |

System probes such as `CUDA_VISIBLE_DEVICES` and `MPICH_GPU_SUPPORT_ENABLED` are inspected for diagnostics but are not LESGO-owned checkpoints.

## Explicit-Residency WIP Build

For collaborator testing of the explicit-residency route, build with:

```bash
FC=ftn cmake -S . -B build_acc_residency \
  -DCMAKE_Fortran_COMPILER=ftn \
  -DUSE_MPI=ON \
  -DUSE_ATM=ON \
  -DUSE_LES_GPU=ON
cmake --build build_acc_residency -j 8
```

This produces:

```text
lesgo-mpi-ATM-lesgpu
```

Important caveat: this route is not fully managed-free yet. It enables explicit-residency code paths such as `PPLES_GPU`, `PPSGS_GPU`, `PPPRESS_GPU`, `PPCONVEC_GPU`, and `PPDERIVS_GPU`, but the build still preserves `-gpu=mem:managed` until all remaining managed-memory islands are removed and validated.
