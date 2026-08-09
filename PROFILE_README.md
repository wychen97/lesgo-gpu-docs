# Wenyuan Chen

## LESGO GPU port

I maintain a GPU-enabled version of LESGO, a Fortran/MPI large-eddy simulation
solver. The public implementation uses NVHPC, explicit device residency,
GPU-aware MPI where available, and FP64 arithmetic.

Current work includes the LES core, ADM and ATM turbine models, scalar
transport, concurrent precursor, inflow/forcing options, and Level Set. The
repository includes small CPU/GPU cases for build and numerical validation, plus
larger benchmark configurations.

- Documentation: https://wychen97.github.io/lesgo-gpu-docs/
- Source and test cases: https://github.com/wychen97/lesgo-gpu-porting
- Validation notes: https://wychen97.github.io/lesgo-gpu-docs/gpu/validation-performance/

`Fortran` | `MPI` | `CUDA Fortran` | `OpenACC` | `NVHPC` | `cuFFT` |
`GPU-aware MPI` | `Large-Eddy Simulation` | `Wind Turbine Modeling`
