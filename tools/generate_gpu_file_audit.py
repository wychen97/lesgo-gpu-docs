#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "gpu" / "file-audit.md"
FORTRAN_SUFFIXES = {".f90", ".F90", ".f", ".F", ".f03", ".F03"}

ROLE_MAP = {
    "main.f90": ("Main driver", "Timestep orchestration, timing, CPU/GPU comparison output", "Runtime"),
    "initialize.f90": ("Initialization", "Startup allocation and setup", "Initialization"),
    "finalize.f90": ("Finalization", "Shutdown and cleanup", "Finalization"),
    "param.f90": ("Configuration", "Global parameters and CMake/runtime option state", "Setup"),
    "input_util.f90": ("Configuration", "Input parsing helpers", "I/O/setup"),
    "param_output.f90": ("Output", "Output configuration", "I/O/setup"),
    "io.f90": ("Output", "Output and optional CGNS paths", "I/O"),
    "types.f90": ("Shared types", "Core precision and type definitions", "Shared"),
    "messages.f90": ("Messages", "User-facing message helpers", "Setup"),
    "string_util.f90": ("Utility", "String parsing helpers", "Setup"),
    "clocks.f90": ("Timing", "Wall-clock timers", "Runtime support"),
    "init_random_seed.f90": ("Initialization", "Random seed control", "Setup"),
    "pid.f90": ("Utility", "PID/control helper", "Setup"),
    "grid.f90": ("Grid", "Grid metadata and coordinates", "Runtime data"),
    "sim_param.f90": ("Configuration", "Simulation parameters", "Setup"),
    "stat_defs.f90": ("Statistics", "Statistics definitions", "Runtime support"),
    "fft.f90": ("FFT", "FFT plan/state support", "Runtime support"),
    "emul_complex.f90": ("Math utility", "Complex arithmetic compatibility", "Shared"),
    "linear_simple.f90": ("Math utility", "Linear helper routines", "Shared"),
    "stability.f90": ("Stability", "Stability helper routines", "Runtime support"),
    "cuda_mpi_debug.f90": ("MPI/GPU debug", "Concise CUDA-aware MPI pointer/sync diagnostics", "Debug support"),
    "mpi_defs.f90": ("MPI", "MPI decomposition, rank/GPU binding, communication helpers", "Runtime"),
    "mpi_transpose_mod.f90": ("MPI transpose", "Transpose support used by pressure and spectral paths", "Runtime"),
    "derivatives.f90": ("Derivatives", "GPU spatial derivative kernels", "Runtime hot path"),
    "test_filtermodule.f90": ("Filtering", "GPU test-filter support for dynamic SGS", "Runtime hot path"),
    "convec.f90": ("Convection", "Production GPU convection path", "Runtime hot path"),
    "press_stag_array.f90": ("Pressure", "GPU pressure RHS, halos, cuFFT orchestration", "Runtime hot path"),
    "tridag_array.f90": ("Pressure", "GPU tridiagonal solve and transpose-Thomas helper", "Runtime hot path"),
    "sgs_stag_util.f90": ("SGS", "GPU SGS model/stress construction and halos", "Runtime hot path"),
    "sgs_param.f90": ("SGS", "SGS parameters", "Setup/runtime support"),
    "std_dynamic.f90": ("SGS", "Standard dynamic SGS model support", "Runtime"),
    "scaledep_dynamic.f90": ("SGS", "Scale-dependent dynamic SGS model support", "Runtime"),
    "interpolag_Ssim.f90": ("SGS", "Lagrangian scale-sim interpolation", "Runtime"),
    "interpolag_Sdep.f90": ("SGS", "Lagrangian scale-dependent interpolation", "Runtime"),
    "lagrange_Ssim.f90": ("SGS", "Lagrangian scale-sim averaging", "Runtime"),
    "lagrange_Sdep.f90": ("SGS", "Lagrangian scale-dependent averaging", "Runtime"),
    "divstress_uv.f90": ("SGS/divstress", "GPU horizontal stress divergence", "Runtime hot path"),
    "divstress_w.f90": ("SGS/divstress", "GPU vertical stress divergence", "Runtime hot path"),
    "forcing.f90": ("Forcing/projection", "GPU forcing, applied force reset, projection timing", "Runtime hot path"),
    "actuator_turbine_model.f90": ("ATM", "Turbine physics, yaw/rotation, blade force logic", "Runtime hot path when USE_ATM"),
    "atm_lesgo_interface.f90": ("ATM", "GPU LESGO/ATM interface, sampling, gather, point-owner LB", "Runtime hot path when USE_ATM"),
    "atm_base.f90": ("ATM", "ATM type definitions", "Setup/runtime support"),
    "atm_input_util.f90": ("ATM", "ATM input parsing", "I/O/setup"),
    "turbines.f90": ("Turbines", "Optional actuator disk/turbine routines", "Optional runtime"),
    "turbines_gpu.f90": ("Turbines", "GPU helper routines for optional turbine paths", "Optional runtime"),
    "turbine_indicator.f90": ("Turbines", "Turbine indicator setup/runtime helpers", "Optional setup/runtime"),
    "wallstress.f90": ("Wall model", "GPU wall-stress related loops and diagnostics", "Runtime"),
    "iwmles.f90": ("Wall model", "Integral wall model support", "Runtime"),
    "rmsdiv.f90": ("Diagnostics", "GPU divergence metric/reduction", "Runtime diagnostic"),
    "cfl_util.f90": ("Diagnostics", "GPU CFL reduction", "Runtime diagnostic"),
    "functions.f90": ("Utility", "Shared GPU-enabled helper loops and math", "Shared/runtime"),
    "initial.f90": ("Initialization", "Initial condition setup and device state", "Initialization"),
    "inflow.f90": ("Inflow", "GPU inflow forcing/runtime loops", "Runtime"),
    "shifted_inflow.f90": ("Inflow", "Shifted inflow support", "Runtime"),
    "fringe.f90": ("Inflow", "Fringe-region support", "Runtime"),
    "sponge.f90": ("Boundary", "GPU sponge damping loops", "Runtime"),
    "coriolis.f90": ("Forcing", "GPU Coriolis forcing loops", "Runtime"),
    "hit_inflow.f90": ("HIT", "Optional HIT input/reference path", "Optional"),
    "hit_inflow_gpu.f90": ("HIT", "GPU HIT inflow helpers", "Optional runtime"),
    "scalars.f90": ("Scalars", "Optional scalar transport GPU loops", "Optional runtime"),
    "concurrent_precursor.f90": ("CPS", "Concurrent precursor coordination", "Optional runtime"),
    "time_average.f90": ("Statistics", "Time averaging and output accumulation", "Runtime/I/O"),
    "level_set.f90": ("Level set", "Optional level-set runtime loops", "Optional runtime"),
    "level_set_base.f90": ("Level set", "Level-set shared definitions", "Optional setup"),
    "trees_base_ls.f90": ("Level set", "Tree geometry base data", "Optional setup"),
    "trees_global_fmask_ls.f90": ("Level set", "Tree/fmask preprocessing", "Optional setup"),
    "trees_io_ls.f90": ("Level set", "Tree I/O", "Optional I/O"),
    "trees_pre_ls.f90": ("Level set", "Tree preprocessing", "Optional setup"),
    "trees_setup_ls.f90": ("Level set", "Tree setup", "Optional setup"),
}

OPTION_HINTS = [
    ("ATM", "USE_ATM"), ("Turbines", "USE_TURBINES"), ("Level set", "USE_LVLSET"),
    ("Scalars", "USE_SCALARS"), ("HIT", "USE_HIT"), ("CPS", "USE_CPS"),
]


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", "<br>")


def short_list(items, limit=7):
    items = [i for i in items if i]
    if not items:
        return "-"
    if len(items) > limit:
        return ", ".join(items[:limit]) + f", +{len(items)-limit} more"
    return ", ".join(items)


def status_for(text: str, file: str, area: str) -> str:
    lower = text.lower()
    gpu = any(tok in lower for tok in ["enable_cuda", "!$cuf", "attributes(global)", "device", "cudafor", "cufft", "cuda"])
    if "reference" in area.lower() or file.endswith("-cpu.f90"):
        return "Reference/fallback"
    if gpu:
        return "GPU-enabled"
    if any(w in area.lower() for w in ["input", "output", "i/o", "setup", "configuration", "shared types", "messages"]):
        return "CPU acceptable: setup/I/O"
    return "Review if runtime-active"


def option_for(area: str, file: str, text: str) -> str:
    found = []
    combined = f"{area} {file} {text[:4000]}"
    for key, opt in OPTION_HINTS:
        if key.lower() in combined.lower() or opt in text:
            found.append(opt)
    return ", ".join(sorted(set(found))) if found else "default/core"


def note_for(file: str, status: str, area: str, switches) -> str:
    if file in {"press_stag_array.f90", "tridag_array.f90"}:
        return "Pressure math and zero-mode handling are release-sensitive; validate divergence and wall stress after edits."
    if file == "sgs_stag_util.f90":
        return "Do not change SGS formulas while editing timing or halo paths; validate tau/wall-stress behavior."
    if file == "atm_lesgo_interface.f90":
        return "Legacy ATM path is default; point-owner LB remains experimental and must validate force sums."
    if "Reference" in status:
        return "Kept for comparison or fallback; not the production hot path."
    if "CPU acceptable" in status:
        return "CPU is acceptable unless this path becomes repeated inside the timestep."
    if switches:
        return "Retained switch should be documented before changing behavior."
    if "GPU-enabled" in status:
        return "Runtime loops have GPU coverage; preserve device-resident data flow."
    return "Audit before using in a new active configuration."


def parse_file(path: Path):
    text = path.read_text(errors="ignore")
    proc_re = re.compile(r"^\s*(?:subroutine|function|program|module)\s+([a-zA-Z_][\w]*)", re.I | re.M)
    procs = [m.group(1) for m in proc_re.finditer(text)]
    envs = sorted(set(re.findall(r"get_environment_variable\s*\(\s*'([^']+)'", text, re.I)))
    loop_count = len(re.findall(r"^\s*do\b", text, re.I | re.M))
    cuf_count = len(re.findall(r"!\$cuf|attributes\s*\(\s*global\s*\)", text, re.I))
    mpi_count = len(re.findall(r"\bMPI_", text, re.I))
    cuda_count = len(re.findall(r"cuda|cudafor|cufft|device", text, re.I))
    return text, procs, envs, loop_count, cuf_count, mpi_count, cuda_count


def main():
    files = sorted([p for p in ROOT.iterdir() if p.is_file() and (p.suffix in FORTRAN_SUFFIXES or p.suffix.lower() in FORTRAN_SUFFIXES)])
    generated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    rows = []
    total_envs = []
    for p in files:
        text, procs, envs, loop_count, cuf_count, mpi_count, cuda_count = parse_file(p)
        area, role, relevance = ROLE_MAP.get(p.name, ("Unclassified", "No curated role yet", "Review"))
        status = status_for(text, p.name, area)
        option = option_for(area, p.name, text)
        total_envs.extend(envs)
        note = note_for(p.name, status, area, envs)
        rows.append((p.name, area, role, relevance, option, status, procs, envs, loop_count, cuf_count, mpi_count, cuda_count, note))

    gpu_envs = sorted(set(e for e in total_envs if e.startswith("LESGO_") and not e.startswith("LESGO_CPU_REF_TIME_") and e != "LESGO_RANDOM_SEED"))
    cpu_envs = sorted(set(e for e in total_envs if e.startswith("LESGO_CPU_REF_TIME_")))
    system_envs = sorted(set(e for e in total_envs if e in {"CUDA_VISIBLE_DEVICES", "MPICH_GPU_SUPPORT_ENABLED"}))

    lines = [
        "# File-By-File GPU Audit",
        "",
        f"Generated by `tools/generate_gpu_file_audit.py` on {generated}.",
        "",
        "This page is a release-gate inventory for the GPU branch. It lists every top-level Fortran source, its runtime relevance, GPU status, retained environment switches, and developer notes. The status is generated from source markers plus curated role metadata; update the role map in the generator when ownership changes.",
        "",
        "## Summary",
        "",
        f"- Top-level Fortran files audited: `{len(files)}`",
        f"- LESGO-owned GPU checkpoints: `{len(gpu_envs)}`",
        f"- CPU reference checkpoints preserved but excluded from GPU count: `{len(cpu_envs)}`",
        f"- System probes: `{len(system_envs)}`",
        "",
        "### Retained GPU Checkpoints",
        "",
    ]
    lines += [f"- `{e}`" for e in gpu_envs]
    lines += ["", "### CPU Reference Checkpoints", ""]
    lines += [f"- `{e}`" for e in cpu_envs]
    lines += [
        "",
        "## Audit Matrix",
        "",
        "| File | Area | Role | Relevance | CMake/Option | GPU Status | Procedures | Switches | Loop Markers | GPU/MPI Markers | Developer Note |",
        "|---|---|---|---|---|---|---|---|---:|---|---|",
    ]

    for row in rows:
        file, area, role, relevance, option, status, procs, envs, loop_count, cuf_count, mpi_count, cuda_count, note = row
        markers = f"CUF/global={cuf_count}; CUDA/device={cuda_count}; MPI={mpi_count}"
        cells = [
            f"`{file}`", area, role, relevance, option, status,
            short_list([f"`{p}`" for p in procs], 6),
            short_list([f"`{e}`" for e in envs], 6),
            str(loop_count), markers, note,
        ]
        lines.append("| " + " | ".join(md_escape(c) for c in cells) + " |")

    lines += ["", "## Procedure Inventory", ""]
    for row in rows:
        file, area, role, relevance, option, status, procs, envs, loop_count, cuf_count, mpi_count, cuda_count, note = row
        lines += [
            f"### `{file}`",
            "",
            f"- Area: {area}",
            f"- Runtime relevance: {relevance}",
            f"- GPU status: {status}",
            f"- Procedures/modules found: {short_list([f'`{p}`' for p in procs], 30)}",
            f"- Retained switches: {short_list([f'`{e}`' for e in envs], 30)}",
            f"- Developer note: {note}",
            "",
        ]

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {DOC.relative_to(ROOT)}")
    print(f"Fortran files: {len(files)}")
    print(f"GPU checkpoints: {len(gpu_envs)}")


if __name__ == "__main__":
    main()
