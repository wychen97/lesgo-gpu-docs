# Main Timestep Flow

The GPU release keeps the original LESGO timestep ordering. Porting changes
execution location and data movement, not the sequence of physical operators.

## Timestep order

```text
forcing and turbine phase 1
derivatives
SGS model and stress construction
convection and stress divergence
turbine force application
pressure solve
pressure-gradient update
velocity projection
diagnostics and scheduled output
```

| Section | Main files | GPU status |
| --- | --- | --- |
| Forcing and turbines | `forcing.f90`, `atm_lesgo_interface.f90`, `actuator_turbine_model.f90` | ADM/ATM sampling and force paths covered |
| Derivatives and filtering | `derivatives.f90`, `test_filtermodule.f90` | Full-domain GPU kernels |
| SGS and stresses | `sgs_stag_util.f90`, dynamic/Lagrangian SGS files, `divstress_*.f90` | Disabled SGS and models `1` to `5` covered |
| Convection | `convec.f90` | GPU hot path |
| Pressure | `press_stag_array.f90`, `tridag_gpu.f90`, transpose support | cuFFT, GPU tridiagonal work, GPU-aware MPI path |
| Projection | `forcing.f90` and pressure-gradient helpers | GPU hot path |
| Optional transport/geometry | `scalars.f90`, CPS, inflow/forcing, Level Set files | Covered by dedicated compact cases |
| Diagnostics and output | `main.f90`, `io.f90`, output helpers | Host-visible by design |

Periodic output, statistics, or model updates can make a printed timestep slower
than adjacent ordinary steps. Performance comparisons therefore use a window of
ordinary steps and report periodic work separately; a single multiple-of-50
step is not a solver-average measurement.

## Ownership

`sim_param.f90` owns the principal field arrays. GPU modules expect these arrays
to be present throughout the timestep. MPI routines consume packed device
buffers on a GPU-aware stack and compact host buffers on the fallback path.

ATM is split into two ordered phases: sampling/model updates before the LES
operators, then force deposition/application at the original forcing site.
Level Set follows the same rule: host geometry setup precedes persistent device
work during the timestep.

## Release diagnostics

Changes to active solver paths are checked with divergence, kinetic energy,
wall stress, field norms/differences, and model-specific quantities such as
turbine force, thrust, torque, and power. Restart tests are required when the
changed routine owns state carried between runs.
