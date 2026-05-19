# CMake And Environment

This page shows the recommended way to build the GPU branch. The short version is: use the build script when possible, pass CMake options through the command line, and keep `lesgo.conf` consistent with the MPI layout used at runtime.

## Recommended Derecho Build

```bash
cd /glade/u/home/wchen/lesgo-gpu-test
BUILD_JOBS=8 ./derecho_build_gpu.sh
```

The script loads the GPU toolchain, configures CMake, builds the executable, and installs it into the ATM test case as:

```text
test-cases/actuator_turbine_model/lesgo-mpi-ATM
```

## Environment Loaded By The Build Script

```bash
module --force purge
module load ncarenv/25.10 craype/2.7.34 nvhpc/25.9 cuda/12.9.0             cray-mpich/8.1.32 cmake/3.31.8 fftw/3.3.10
export FFTW_ROOT="$NCAR_ROOT_FFTW"
```

For `USE_CGNS=ON`, the script also loads HDF5-MPI and points CMake to the user-side CGNS install:

```bash
module load hdf5-mpi/1.14.6
export CGNS_ROOT=/glade/u/home/wchen/local/cgns/4.5.2-nvhpc-hdf5mpi
```

## Core CMake Options

| Option | Recommended ATM GPU setting | Notes |
|---|---|---|
| `USE_MPI` | `ON` | Production path |
| `USE_ATM` | `ON` | Actuator turbine model case |
| `USE_CPS` | `OFF` | Optional precursor mode |
| `USE_HIT` | `OFF` | Optional HIT input |
| `USE_LVLSET` | `OFF` | Optional level-set path |
| `USE_TURBINES` | `OFF` | Optional actuator disk model |
| `USE_CGNS` | `OFF` | Output dependency; enable only when CGNS is configured |
| `USE_SCALARS` | `OFF` | Optional scalar transport |
| `USE_SAFETYMODE` | `ON` | Keep enabled unless testing release performance carefully |

Equivalent manual configure command:

```bash
FC=ftn cmake -S . -B bld-derecho-a100   -DCMAKE_Fortran_COMPILER=ftn   -DUSE_MPI=ON   -DUSE_ATM=ON   -DUSE_CPS=OFF   -DUSE_HIT=OFF   -DUSE_LVLSET=OFF   -DUSE_TURBINES=OFF   -DUSE_CGNS=OFF   -DUSE_SCALARS=OFF
cmake --build bld-derecho-a100 -j 8
```

## Testing Other CMake Options

Use `LESGO_CMAKE_ARGS` instead of editing `CMakeLists.txt` for one-off builds:

```bash
LESGO_CMAKE_ARGS="-DUSE_SCALARS=ON" BUILD_DIR=/glade/u/home/wchen/lesgo-gpu-test/bld-option-USE_SCALARS ./derecho_build_gpu.sh
```

This keeps the default ATM build clean while making option-specific testing reproducible.

## Runtime Environment

For GPU-aware MPI runs:

```bash
export MPICH_GPU_SUPPORT_ENABLED=1
export MPICH_GPU_MANAGED_MEMORY_SUPPORT_ENABLED=1
```

For one GPU:

```bash
mpiexec -n 1 -ppn 1 set_gpu_rank ./lesgo-mpi-ATM
```

For two GPUs on one node:

```bash
mpiexec -n 2 -ppn 2 set_gpu_rank ./lesgo-mpi-ATM
```

Make sure the `nproc` value in `lesgo.conf` matches the MPI rank count.


## Common Mistakes

| Symptom | Likely cause |
|---|---|
| Build cannot find FFTW | `FFTW_ROOT` or module environment is missing |
| CGNS build cannot find `cgns.mod` | `CGNS_ROOT`/HDF5-MPI not configured |
| Multi-GPU run gives wrong communication behavior | `MPICH_GPU_SUPPORT_ENABLED=1` missing or rank/GPU binding wrong |
| Runtime stops early or uses wrong decomposition | `lesgo.conf` `nproc` does not match MPI rank count |
| Accidentally benchmarking I/O | `domain_calc`, plane output, or ATM output interval still active |
