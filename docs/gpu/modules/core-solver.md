# Derivatives, Convection, Projection

## Derivatives and filtering

`derivatives.f90`, `test_filtermodule.f90`, and shared helpers provide the
spatial derivative and filtering work used by the LES and SGS paths. Repeated
three-dimensional loops run on the GPU; broad kernels are preferred to many
small per-plane launches.

## Convection

`convec.f90` is the maintained nonlinear convection implementation. Its active
timestep loops run on the GPU and consume device-resident velocity and
derivative fields. Temporary reference variants used during optimization are
not part of the release path.

## Projection

The projection and pressure-gradient updates run on the GPU after the pressure
solve. Their correctness is assessed through the divergence residual and the
matched CPU/GPU field comparison, not timing alone.

## Boundary and auxiliary flow work

`wallstress.f90`, `inflow.f90`, `shifted_inflow.f90`, `sponge.f90`,
`coriolis.f90`, and `rmsdiv.f90` include GPU coverage for timestep-relevant
loops. Parsing, initialization, and output remain host-side where they are not
regular timestep costs. The `inflow_and_forcing` case isolates HIT, shifted
inflow, Coriolis, and sponge configurations for compact CPU/GPU checks.
