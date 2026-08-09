# CMake and Environment

## CMake options

The root `CMakeLists.txt` is the option registry. Case scripts select a valid
combination with command-line `-D` arguments.

| Option | Meaning |
| --- | --- |
| `USE_MPI` | MPI domain decomposition |
| `USE_LES_GPU` | Explicit-residency GPU LES core |
| `USE_CPU_BUILD` | Matched NVHPC CPU baseline; cannot be combined with `USE_LES_GPU` |
| `USE_GPU_AWARE_MPI` | `AUTO`, `ON`, or `OFF` device-buffer communication policy |
| `USE_TURBINES` | Actuator disk model |
| `USE_ATM` | Actuator line/section turbine model |
| `USE_SCALARS` | Scalar transport equations |
| `USE_SCALARS_GPU` | GPU scalar path; requires `USE_SCALARS=ON` and `USE_LES_GPU=ON` |
| `USE_CPS` | Concurrent precursor; requires MPI |
| `USE_HIT` | Homogeneous isotropic turbulence input |
| `USE_LVLSET` | Level Set immersed-surface model |
| `USE_LVLSET_GPU` | GPU Level Set path; requires `USE_LVLSET=ON` and `USE_LES_GPU=ON` |
| `USE_DYN_TN` | Dynamic Lagrangian averaging timescale |
| `USE_SAFETYMODE` | Additional runtime checks |
| `USE_CGNS` | CGNS output support and external dependency |

For GPU scalar transport, both scalar options must be enabled:

```bash
-DUSE_SCALARS=ON -DUSE_SCALARS_GPU=ON -DUSE_LES_GPU=ON
```

For GPU Level Set, both Level Set options must be enabled:

```bash
-DUSE_LVLSET=ON -DUSE_LVLSET_GPU=ON -DUSE_LES_GPU=ON
```

CMake rejects invalid combinations during configuration.

## Derecho environment

The latest documented Derecho profile uses:

```bash
module --force purge
module load nvhpc/26.1 cuda/12.9.0 \
  cray-mpich/8.1.32 fftw/3.3.10 cmake/3.31.8

export FFTW_ROOT="$NCAR_ROOT_FFTW"
export MPICH_GPU_SUPPORT_ENABLED=1
export MPICH_GPU_MANAGED_MEMORY_SUPPORT_ENABLED=1
```

Use `ftn` as the Fortran compiler wrapper. The Derecho GPU profile compiles
with FP64 and `-gpu=mem:separate,cc80,lineinfo`.

## Delta RH96 environment

The Level Set validation matrix also passed on Delta's RH96 environment using
the RH96 login node and reservation:

```bash
ssh dt-login04.delta.ncsa.illinois.edu

module reset
module swap PrgEnv-gnu PrgEnv-nvidia
module load nvidia/26.5 cudatoolkit/26.5_13.2 \
  cray-mpich/9.1.0 cray-fftw/3.3.10.11 cmake/3.31.8

export MPICH_GPU_SUPPORT_ENABLED=1
export MPICH_GPU_MANAGED_MEMORY_SUPPORT_ENABLED=1
```

Delta RH96 jobs use `#SBATCH --reservation=RH96`. Cluster module names change
over time, so the checked-in scripts remain the reference for a recorded test;
on another Cray/NVHPC cluster, replace the module block and scheduler header,
then keep the CMake feature combination and rank decomposition unchanged.

## Portability rules

- Select the compiler with `FC` or `-DCMAKE_Fortran_COMPILER`; do not edit the
  detected CMake compiler ID.
- Load an MPI-compatible FFTW library before configuration.
- Use the MPI compiler wrapper supplied by the cluster.
- Keep one rank per GPU unless a new layout is measured and validated.
- Set `USE_GPU_AWARE_MPI=OFF` when the MPI implementation cannot consume device
  buffers directly.
- Enable CGNS only after its HDF5/MPI-compatible installation is available.

The source uses broad `use mpi` imports for compatibility with Cray/NVHPC MPI
module implementations that do not expose all nonblocking routines through an
`only` list. This is intentional portability code, not a physics change.
