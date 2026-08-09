# ATM and Forcing

The actuator turbine model is split between LES field operations and turbine
model state. The normal GPU path batches velocity sampling, induced-velocity
correction, force gathering, and force deposition while preserving the original
two-phase call order in `main.f90`.

## Main source files

| File | Role |
| --- | --- |
| `atm_lesgo_interface.f90` | LES/ATM exchange, batched sampling, force gathering and deposition |
| `actuator_turbine_model.f90` | blade aerodynamics, controls, power, restart, and structural model |
| `forcing.f90` | LES forcing application and auxiliary forcing |
| `atm_input_util.f90` | ATM configuration input |

Atharva's exact-panel induced-velocity correction is integrated in the batched
GPU ATM path. Rigid and structural configurations use that same correction; GPU
selection is not conditional on the structural solver being disabled.

The structural model is enabled with `LESGO_ATM_STRUCTURE=1`. Structural state,
load history, induced-velocity history, and the corresponding restart metadata
are checked so a continuation does not silently cold-start those terms.

## Maintained controls

| Variable | Purpose |
| --- | --- |
| `LESGO_ATM_STRUCTURE` | Enable structural coupling |
| `LESGO_ATM_STRUCTURE_VEL_FEEDBACK` | Control structural velocity feedback |
| `LESGO_ATM_STRUCTURE_ALPHA_FEEDBACK` | Control structural angle-of-attack feedback |
| `LESGO_ATM_STRUCTURE_TIMING` | Report structural timing |
| `LESGO_ATM_STRUCTURE_DIAG` | Write structural diagnostics |
| `LESGO_ATM_POWER_STDOUT` | Print turbine power in addition to normal files |

Historical point-owner load-balancing and shadow/mirror experiment branches were
removed after validation did not justify carrying their complexity. The release
uses the maintained batched ATM route.

Any ATM change should compare force sums, thrust, torque, power, blade state,
and downstream flow fields. Restart checks must cover both rigid and structural
state when those paths are affected.
