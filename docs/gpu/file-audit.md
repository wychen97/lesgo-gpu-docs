# Source Inventory

The source inventory is maintained with the code so it cannot drift from the
release it describes. For checkpoint
`f46eca2fbaad00793da140ce77de4830b3098026`, the repository audit covers 78
Fortran files and 401 subprograms. The GPU coverage audit identifies 104
timestep-relevant candidates, and the release readiness suite contains 56
checks.

## Authoritative records

| Record | Purpose |
| --- | --- |
| [`docs/gpu_static_full_inventory.md`](https://github.com/wychen97/lesgo-gpu-porting/blob/main/docs/gpu_static_full_inventory.md) | File and subprogram inventory |
| [`docs/gpu_port_coverage_audit.md`](https://github.com/wychen97/lesgo-gpu-porting/blob/main/docs/gpu_port_coverage_audit.md) | GPU status by active source area |
| [`docs/code_organization.md`](https://github.com/wychen97/lesgo-gpu-porting/blob/main/docs/code_organization.md) | Module ownership and edit boundaries |
| [`docs/environment_switches.md`](https://github.com/wychen97/lesgo-gpu-porting/blob/main/docs/environment_switches.md) | Maintained runtime controls |
| [`docs/level_set_gpu_validation_evidence.json`](https://github.com/wychen97/lesgo-gpu-porting/blob/main/docs/level_set_gpu_validation_evidence.json) | Derecho and Delta Level Set evidence |

## Source groups

| Group | Representative files |
| --- | --- |
| Solver state and orchestration | `main.f90`, `sim_param.f90`, `param.f90` |
| Derivatives and filtering | `derivatives.f90`, `test_filtermodule.f90` |
| SGS and stresses | `sgs_stag_util.f90`, dynamic/Lagrangian files, `divstress_*.f90` |
| Convection | `convec.f90` |
| Pressure and MPI transpose | `press_stag_array.f90`, `tridag_gpu.f90`, `mpi_transpose_mod.f90` |
| Turbines | `turbines.f90`, `atm_lesgo_interface.f90`, `actuator_turbine_model.f90` |
| Optional transport and inflow | `scalars.f90`, CPS, HIT, shifted inflow, sponge, Coriolis |
| Level Set | `level_set.f90`, `level_set_base.f90`, `level_set_gpu.f90` |
| Input, output, restart | `input_util.f90`, `io.f90`, model-specific restart routines |

## Maintenance checks

The repository's `tools/check_branch_readiness.py` entry point runs the static
coverage, environment-switch, testcase, restart, architecture, and documentation
checks used before publication. Source changes should update the authoritative
record in the same commit rather than regenerating a separate website-only
inventory.
