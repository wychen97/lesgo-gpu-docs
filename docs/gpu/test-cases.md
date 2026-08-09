# Public Test Cases

The repository contains eight maintained examples under `test-cases/`. Each
case keeps its inputs, case-specific build script, Derecho submit script, and a
README in one directory.

| Case | Purpose | Main GPU options | Latest recorded check |
| --- | --- | --- | --- |
| `channel_flow` | LES core without turbine physics | `USE_LES_GPU=ON` | Derecho CPU/GPU pass, `240^3`, 200 steps |
| `adm_disk` | Actuator disk model | `USE_LES_GPU=ON`, `USE_TURBINES=ON` | Derecho CPU/GPU pass, `240^3`, 200 steps |
| `atm_line` | Actuator line 5 MW turbine | `USE_LES_GPU=ON`, `USE_ATM=ON` | Derecho rigid and structural CPU/GPU passes, `240^3` |
| `large_windfarm_3072x384x400_60turbines` | Large ATM benchmark | `USE_LES_GPU=ON`, `USE_ATM=ON` | Derecho CPU50/GPU16 pass, 50 steps |
| `level_set_cubes` | Immersed-surface Level Set | `USE_LVLSET=ON`, `USE_LVLSET_GPU=ON` | Derecho and Delta matrix/restart passes, 58 runtime tasks |
| `scalar_transport` | Passive scalar and active temperature/buoyancy | `USE_SCALARS=ON`, `USE_SCALARS_GPU=ON` | Derecho compact CPU/GPU passive and active passes, `64^3` |
| `concurrent_precursor` | Red/blue precursor exchange | `USE_CPS=ON`; scalar variant optional | Derecho compact CPU/GPU velocity and scalar passes, two `64^3` domains |
| `inflow_and_forcing` | HIT, shifted inflow, Coriolis, and sponge | Variant-specific options | Derecho compact CPU/GPU passes, `64^3` |

The `64^3` records check execution and numerical parity. They are not
production scaling results or statistically converged turbulence datasets.

## Derecho example

```bash
git clone https://github.com/wychen97/lesgo-gpu-porting.git
cd lesgo-gpu-porting/test-cases/channel_flow

# Build the case-specific GPU executable.
./compile_derecho.sh gpu

# Submit the already configured PBS job.
qsub submit_derecho.pbs
```

The build script installs `lesgo-run-exe-gpu` in the case directory. CPU builds
use `./compile_derecho.sh cpu` and produce `lesgo-run-exe-cpu`.

## Changing the parallel layout

GPU examples use one MPI rank per GPU. Keep these settings consistent:

| Setting | File | Requirement |
| --- | --- | --- |
| `select`, `mpiprocs`, `ngpus` | `submit_derecho.pbs` | Scheduler allocation |
| `MPI_RANKS`, `MPI_PPN` | `submit_derecho.pbs` | `mpiexec` layout |
| `nproc` | `lesgo.conf` | LESGO slab count |

The concurrent precursor case is the exception: its two-rank MPI world is split
between equal red and blue domains, so each input uses its local domain rank
count.

Case-specific variants and acceptance checks are documented in each case
README in the source repository.
