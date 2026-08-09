# Overview

The GPU port keeps the original LESGO equations, timestep order, input format,
and z-slab MPI decomposition. The main changes are implementation changes:
loop-heavy timestep work runs on GPUs, active arrays remain device-resident,
and supported MPI stacks exchange device buffers directly.

The public release is maintained on the `main` branch of
[`wychen97/lesgo-gpu-porting`](https://github.com/wychen97/lesgo-gpu-porting).
It replaces the older `gpu-explicit-residency-wip` development branch.

## Scope

| Area | Current state |
| --- | --- |
| LES core | GPU path for derivatives, convection, SGS/stresses, pressure, projection, and forcing |
| SGS selection | Disabled path and runtime models `1` through `5` covered |
| Turbines | ADM and ATM paths, including the optional ATM structural solver |
| Optional physics | Scalar transport, concurrent precursor, HIT/shifted inflow, Coriolis/sponge, and Level Set examples |
| MPI | GPU-aware path with a host-staged fallback selected by CMake |
| Restart | CPU/GPU continuation checks, including ATM history fields and Level Set restart matrices |
| I/O and setup | Host-side where the work is outside the regular timestep hot path |

## Reading order

1. [Current Release](explicit-residency.md) defines what is supported.
2. [Public Test Cases](test-cases.md) lists the runnable examples.
3. [Build and Runtime](build-runtime.md) gives an exact Derecho build and submit sequence.
4. [GPU Architecture](architecture.md) records data ownership and MPI rules.
5. [Validation and Performance](validation-performance.md) separates current release checks from historical benchmark results.

Any new feature should add a small CPU/GPU case, preserve the original input
contract where possible, and update the source audit in the code repository.
