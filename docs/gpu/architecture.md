# GPU Architecture

The GPU migration follows a conservative rule: preserve LESGO numerics and module ordering, then move repeated timestep work to the GPU. The code uses CUDA Fortran, CUF kernel loops, cuFFT, and GPU-aware MPI.

## Core Design Rules

| Rule | Reason |
|---|---|
| Keep the original solver equations | Makes validation against CPU LESGO meaningful |
| Keep the z-slab MPI decomposition | Limits architectural risk and preserves existing MPI assumptions |
| Use GPU kernels for timestep loops | Removes CPU bottlenecks without changing physics |
| Use persistent contiguous device buffers for MPI | Avoids non-contiguous managed-memory MPI hazards |
| Keep I/O and one-time parsing on CPU | They do not dominate timestep performance |
| Keep fallback switches only for core risk areas | Reduces code clutter while preserving debugging ability |

## Memory Model

The build uses NVHPC CUDA Fortran and managed/device allocations where appropriate. The most important performance rule is to avoid accidental host touches of large managed arrays inside the timestep. Host reductions and diagnostics can silently trigger migration and create false bottlenecks.

Prefer full-domain kernels for regular loops:

```fortran
!$cuf kernel do(3) <<<*,*>>>
do k = kstart, kend
  do j = 1, n2m
    do i = 1, n1m
      field(i,j,k) = ...
    end do
  end do
end do
```

Use explicit CUDA Fortran kernels when CUF kernel loops create poor launch geometry, too many small launches, or excessive integer flattening overhead.

## MPI And GPU Awareness

The production multi-GPU path assumes GPU-aware MPI:

```bash
export MPICH_GPU_SUPPORT_ENABLED=1
```

The main MPI safety points are:

| Communication Area | Current Pattern |
|---|---|
| SGS tau halo | Combined contiguous device halo for the 2-rank path |
| SGS dwdz halo | Device-buffer path retained; further MPI variants were not beneficial |
| Pressure RHS halo | Combined contiguous device halo for the 2-rank path |
| Pressure transpose | Specialized nproc==2 transpose-Thomas helper |
| ATM point-owner LB | Experimental targeted device exchange path |

## Synchronization Policy

| Synchronization Type | Policy |
|---|---|
| Before MPI consumes GPU data | Required |
| After diagnostic GPU events | Only when timing is enabled |
| Per-small-kernel strict sync | Disabled by default |
| Global debug sync | Available through `LESGO_MPI_CUDA_SYNC` |

When adding a new MPI exchange, pack into a contiguous device buffer, synchronize once before MPI if necessary, exchange, unpack on GPU, and validate with divergence, KE, wall stress, and module-specific checks.
