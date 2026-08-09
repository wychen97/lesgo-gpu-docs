# GPU Architecture

The port preserves LESGO's equations, timestep order, and z-slab MPI
decomposition. GPU work is organized around explicit data ownership rather than
a second solver implementation.

## Design rules

| Rule | Consequence |
| --- | --- |
| Preserve the CPU numerical method | CPU/GPU comparisons remain meaningful |
| Keep hot arrays resident | Full fields are not copied during an ordinary timestep |
| Use explicit communication buffers | MPI does not depend on noncontiguous Fortran sections |
| Synchronize at real dependencies | Kernel-wide synchronization is not added only for timing convenience |
| Keep setup and I/O on the host | One-time work does not complicate the timestep path |
| Retain a correct host-staged MPI route | The same source can run where device-buffer MPI is unavailable |

## Memory model

NVHPC GPU builds use separate host and device memory:

```text
-gpu=mem:separate
```

Derecho A100 builds also specify `cc80` and `lineinfo`. Core fields declared in
`sim_param.f90` have persistent device mirrors in the GPU configuration.
Timestep modules use `present(...)` regions or persistent CUDA device arrays.

Full-field host/device updates belong only at named boundaries:

- initial conditions and restart input;
- output and validation snapshots;
- diagnostics that explicitly consume host data;
- documented compatibility bridges for optional model operations.

Adding an unmarked `update self` to a regular timestep routine is a performance
and correctness risk under separate-memory compilation.

## MPI model

Each MPI rank owns a z slab and normally maps to one GPU. Halo exchanges and the
pressure pipeline use contiguous buffers. With `USE_GPU_AWARE_MPI=AUTO`, CMake
selects the Cray GTL route on supported Cray systems. A host-staged fallback is
compiled when GPU-aware communication is disabled or unavailable.

The pressure solver performs its internal transpose/tridiagonal work without
changing the outer solver decomposition. A full pencil decomposition is not
part of the current release: at the validated problem sizes, the additional
transpose, memory, and implementation cost has not justified replacing the
existing slab layout.

## Synchronization

Synchronization is required before MPI or the host consumes pending device
data. Diagnostic event synchronization is enabled only when that diagnostic is
requested. `LESGO_MPI_CUDA_SYNC=1` adds stricter synchronization for debugging
and is not a production performance setting.

## Mixed CPU/GPU boundaries

ATM keeps blade and force exchange data on the device for the normal path, while
parts of turbine control and structural mechanics remain host model code.
Level Set geometry is initialized on the host, then geometry, overlap buffers,
interpolation workspaces, and regular forcing operations remain device-resident
when `USE_LVLSET_GPU=ON`.

These boundaries are deliberate. They should be changed only with a matched
CPU/GPU case and a restart check when persistent state is involved.
