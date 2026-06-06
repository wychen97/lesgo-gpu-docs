# ATM And Forcing

The actuator turbine model is active in the main validation case and was one of the most complex migration areas. It combines turbine control, blade kinematics, velocity sampling, force calculation, MPI aggregation, and force application to the flow grid.

## Primary Files

| File | Role |
|---|---|
| `forcing.f90` | Top-level forcing and projection-adjacent force application |
| `atm_lesgo_interface.f90` | Interface between LESGO flow arrays and ATM data structures |
| `actuator_turbine_model.f90` | Turbine model physics and blade/nacelle force logic |
| `atm_base.f90`, `atm_input_util.f90` | ATM types and input parsing |
| `turbines.f90`, `turbines_gpu.f90`, `turbine_indicator.f90` | Optional turbine/indicator support |

## Implemented GPU Changes

| Area | Change |
|---|---|
| Velocity sampling | GPU paths for interpolation and on-the-fly w sampling |
| Blade force | GPU-enabled blade/nacelle force calculations |
| Force reset and application | GPU kernels for force array reset and scatter/apply operations |
| Gather/reduction | Packed reductions reduce latency relative to many small reductions |
| Explicit residency WIP | Device force-field shadows plus blade point/force mirrors in `gpu-explicit-residency-wip` |
| Point-owner LB | Experimental load-balanced ownership model retained behind switches |
| Auto-select | Optional short probe can choose legacy vs point-owner LB path |

## Retained Controls

| Switch | Purpose |
|---|---|
| `LESGO_ATM_DIAG_TIMING` | Detailed ATM timing |
| `LESGO_ATM_POINT_OWNER_LB` | Experimental decoupled point-owner load balance path |
| `LESGO_ATM_POINT_OWNER_TARGETED` | Experimental targeted point-owner exchange |
| `LESGO_ATM_LB_AUTO_SELECT` | Probe legacy vs LB and choose faster path |
| `LESGO_ATM_LB_VALIDATE` | Validate LB path against legacy force quantities |

The legacy ATM path remains the default for the current 2-turbine validation case. The point-owner LB algorithm remains experimental and should be enabled by default only after strict same-step force, thrust, torque, power, and flow-field comparisons are completed.

## Explicit-Residency ATM Notes

The `gpu-explicit-residency-wip` branch adds the following ATM-specific residency work:

| Data area | WIP storage strategy |
|---|---|
| Force-field metadata | Flattened persistent GPU shadow arrays |
| Blade points | Explicit device mirror `atm_bladePoints_d` |
| Blade forces | Explicit device mirror `atm_bladeForces_d` |
| Slim gather blade-force exchange | Device mirror pack/unpack path |
| Nacelle scratch | Small explicit device scratch buffer with scalar copy-back |

This reduces managed-memory dependence in the active ATM path, but it does not remove all managed memory from ATM. Fallback helpers, full diagnostic gather paths, and some point-owner LB paths still need review before `-gpu=mem:managed` can be removed.
