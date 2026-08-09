# Build and Runtime

The source repository keeps compilation and submission separate. Every public
case provides:

- `compile_derecho.sh`: configure, compile, and install a case-local executable;
- `submit_derecho.pbs`: request resources and run that executable;
- `lesgo.conf`: define the grid, decomposition, timestep, and physics inputs.

## Complete Derecho example

```bash
git clone https://github.com/wychen97/lesgo-gpu-porting.git
cd lesgo-gpu-porting/test-cases/channel_flow

./compile_derecho.sh gpu
qsub submit_derecho.pbs
```

The compile command creates a build directory outside the tracked case inputs
and installs `lesgo-run-exe-gpu` in the case directory. To build the matched CPU
baseline instead:

```bash
./compile_derecho.sh cpu
```

This produces `lesgo-run-exe-cpu`. The submit script selects the executable
through its documented profile variable.

## What the compile script sets

The root `CMakeLists.txt` declares all valid options and neutral defaults. The
case compile script passes the feature combination needed by that case. Command
line `-D...` values override CMake defaults; there is no second independent
module definition at runtime.

For a typical GPU channel case, the effective configure command includes:

```bash
FC=ftn cmake -S "$SOURCE_DIR" -B "$BUILD_DIR" \
  -Dhostname=derecho \
  -DUSE_MPI=ON \
  -DUSE_CPU_BUILD=OFF \
  -DUSE_LES_GPU=ON \
  -DUSE_GPU_AWARE_MPI=AUTO \
  -DUSE_TURBINES=OFF \
  -DUSE_ATM=OFF \
  -DUSE_CPS=OFF \
  -DUSE_SCALARS=OFF \
  -DUSE_SCALARS_GPU=OFF \
  -DUSE_LVLSET=OFF \
  -DUSE_LVLSET_GPU=OFF \
  -DUSE_HIT=OFF

cmake --build "$BUILD_DIR" --parallel 8
```

Use the checked-in case script rather than copying this fragment when running a
published example. The script also loads the validated modules and installs the
correct executable name.

## MPI and GPU counts

GPU cases use one MPI rank per GPU. Three values must agree:

1. the PBS resource request in `submit_derecho.pbs`;
2. `MPI_RANKS` and `MPI_PPN` in the same file;
3. `nproc` in `lesgo.conf`.

For four GPUs on one Derecho node:

```bash
#PBS -l select=1:ncpus=32:mpiprocs=4:ngpus=4:mem=220gb:gpu_type=a100

MPI_RANKS=4
MPI_PPN=4
```

and:

```text
nproc=4
```

For multi-node work, preserve the per-node rank/GPU ratio. The concurrent
precursor example documents its red/blue domain exception separately.

## Runtime environment

On Cray MPICH systems, the submit script enables GPU-aware MPI:

```bash
export MPICH_GPU_SUPPORT_ENABLED=1
export MPICH_GPU_MANAGED_MEMORY_SUPPORT_ENABLED=1
```

The second setting enables MPI runtime handling; it does not change LESGO's
NVHPC build from `mem:separate` to managed allocation.

`USE_GPU_AWARE_MPI=AUTO` selects the Cray GTL route when available. Use `ON`
only for a known CUDA-aware MPI stack that needs no extra GTL library, or `OFF`
to select the host-staged fallback.

## Outputs

Tracked inputs stay in the case directory. Submit scripts place queue logs and
generated fields under case-local `runs/` or `run-archives/` directories. The
repository ignores cluster-specific binaries and generated simulation output.
