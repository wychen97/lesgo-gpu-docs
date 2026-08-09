# Optional Modules

Optional modules are compiled only when their CMake options are enabled. The
public examples keep each feature isolated enough to show its build and runtime
contract.

| Module | Options | Example | Current evidence |
| --- | --- | --- | --- |
| Scalar transport | `USE_SCALARS`, `USE_SCALARS_GPU` | `scalar_transport` | Passive and active CPU/GPU checks on Derecho |
| Concurrent precursor | `USE_CPS` | `concurrent_precursor` | Velocity and scalar-coupled CPU/GPU checks on Derecho |
| HIT input | `USE_HIT` | `inflow_and_forcing` | Compact CPU/GPU check on Derecho |
| Shifted inflow | Case input/build variant | `inflow_and_forcing` | Compact CPU/GPU check on Derecho |
| Coriolis and sponge | Case input/build variant | `inflow_and_forcing` | Compact CPU/GPU check on Derecho |
| Level Set | `USE_LVLSET`, `USE_LVLSET_GPU` | `level_set_cubes` | Derecho and Delta CPU/GPU matrix and restart checks |
| Dynamic SGS timescale | `USE_DYN_TN` | No standalone public case | Implemented; broader production validation remains appropriate |
| CGNS output | `USE_CGNS` | No standalone public case | Host I/O feature; requires compatible CGNS/HDF5/MPI libraries |

For GPU scalar transport, `USE_SCALARS=ON` alone is not enough;
`USE_SCALARS_GPU=ON` and `USE_LES_GPU=ON` are also required. The same dependency
applies to Level Set: `USE_LVLSET_GPU=ON` requires both `USE_LVLSET=ON` and
`USE_LES_GPU=ON`.

The compact optional-module cases establish compilation, execution, numerical
parity, and restart behavior where applicable. They do not establish
production-scale speedup or statistical convergence.
