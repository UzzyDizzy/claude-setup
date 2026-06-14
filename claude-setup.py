#!/usr/bin/env python3
"""
claude-setup.py — one-shot local setup for a Claude Code research project.

What it does:
  1. Creates .claude/skills/ in the current project.
  2. Clones the 5 skill repos (gstack, gsd, superpowers, anthropic, custom-skills),
     hoisting the ones that ship their skills inside a subfolder.
  3. Runs gstack's ./setup (POSIX only).
  4. Installs the global codebase tools (graphify, understand-anything) if missing.

Safe to re-run. By default it skips a repo whose folder already exists; pass --force to re-clone.
Cross-platform (Linux / macOS / Windows). Global-tool install is non-fatal: if it can't install,
it prints exact manual steps and keeps going.

Usage:
    python claude-setup.py                 # full setup
    python claude-setup.py --force         # re-clone all repos
    python claude-setup.py --skip-global   # repos only, no global tools
    python claude-setup.py --skip-clone    # global tools only
    python claude-setup.py --root /path    # target a different project root
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# CONFIG — edit the two global-tool URLs/commands to match your real tools.
# ──────────────────────────────────────────────────────────────────────────────

GIT_FLAGS = ["--single-branch", "--depth", "1"]

# Each repo: (folder_name, git_url, hoist_subdir_or_None, run_setup_bool)
#   hoist_subdir: clone to a temp dir, then copy <temp>/<subdir> -> .claude/skills/<folder_name>.
#                 Use it for repos that keep their skills one level down (anthropic, custom-skills).
REPOS = [
    ("gstack",       "https://github.com/garrytan/gstack.git",            None,     True),
    ("gsd",          "https://github.com/open-gsd/gsd-core.git",          None,     False),
    ("superpowers",  "https://github.com/obra/superpowers.git",           None,     False),
    ("anthropic",    "https://github.com/anthropics/skills.git",          "skills", False),
    # Your own repo. NOTE: your original command pointed at ".../claude-setup/custom-skills.git",
    # which isn't a valid clone URL — clone the repo and hoist its top-level `skills/` folder:
    ("custom-skills","https://github.com/UzzyDizzy/claude-setup.git",     "skills", False),
]

# Global CLI tools installed once, system-wide. Installed only if the `check` command is not on PATH.
#   ⚠️ CONFIRM these install commands — I can't verify graphify / understand-anything's real
#   install method. pipx is a good cross-platform default for global Python CLIs (isolated, on PATH).
#   If they're npm/cargo/etc., swap the command lists. Each tool tries its commands in order.
GLOBAL_TOOLS = {
    "graphify": {
        "check": "graphify",  # executable name expected on PATH after install
        "install": [
            ["pipx", "install", "graphify"],                       # preferred (edit if wrong)
            ["pip", "install", "--user", "graphify"],              # fallback
        ],
        "manual": "Install graphify globally and ensure `graphify` is on PATH.",
    },
    "understand-anything": {
        "check": "understand-anything",
        "install": [
            ["pipx", "install", "understand-anything"],
            ["pip", "install", "--user", "understand-anything"],
        ],
        "manual": "Install understand-anything globally and ensure its command is on PATH.",
    },
}

# ──────────────────────────────────────────────────────────────────────────────
# Logging helpers (plain tags — no color deps, works in every terminal)
# ──────────────────────────────────────────────────────────────────────────────

def log(tag: str, msg: str) -> None:
    print(f"[{tag:^4}] {msg}", flush=True)

def ok(m):   log("OK", m)
def skip(m): log("SKIP", m)
def warn(m): log("WARN", m)
def fail(m): log("FAIL", m)
def step(m): print(f"\n=== {m} ===", flush=True)


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> int:
    """Run a command, streaming output. Returns the exit code."""
    printable = " ".join(cmd)
    log("RUN", printable + (f"   (cwd={cwd})" if cwd else ""))
    try:
        proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    except FileNotFoundError:
        fail(f"command not found: {cmd[0]}")
        if check:
            raise
        return 127
    if check and proc.returncode != 0:
        fail(f"exited {proc.returncode}: {printable}")
        raise subprocess.CalledProcessError(proc.returncode, cmd)
    return proc.returncode


def require_git() -> None:
    if shutil.which("git") is None:
        fail("git is not installed or not on PATH. Install git and re-run.")
        sys.exit(1)


# ──────────────────────────────────────────────────────────────────────────────
# Repo cloning
# ──────────────────────────────────────────────────────────────────────────────

def is_nonempty_dir(p: Path) -> bool:
    return p.is_dir() and any(p.iterdir())


def clone_repo(name: str, url: str, hoist: str | None, run_setup: bool,
               skills_dir: Path, force: bool) -> None:
    dest = skills_dir / name

    if is_nonempty_dir(dest):
        if not force:
            skip(f"{name} already present at {dest} (use --force to re-clone)")
            return
        warn(f"--force: removing existing {dest}")
        shutil.rmtree(dest, ignore_errors=True)

    if hoist:
        # Clone to a temp dir, then lift <temp>/<hoist> into place.
        with tempfile.TemporaryDirectory(prefix=f"{name}-") as tmp:
            tmp_path = Path(tmp) / "repo"
            run(["git", "clone", *GIT_FLAGS, url, str(tmp_path)])
            src = tmp_path / hoist
            if not src.is_dir():
                fail(f"{name}: expected '{hoist}/' inside the repo but it's missing — "
                     f"check the repo layout / URL.")
                return
            shutil.copytree(src, dest)
        ok(f"{name}: hoisted '{hoist}/' -> {dest}")
    else:
        run(["git", "clone", *GIT_FLAGS, url, str(dest)])
        ok(f"{name}: cloned -> {dest}")

    if run_setup:
        run_gstack_setup(dest)


def run_gstack_setup(repo_dir: Path) -> None:
    """gstack ships a POSIX ./setup. Run it on Unix; warn on Windows."""
    setup = repo_dir / "setup"
    if not setup.exists():
        skip("gstack: no ./setup found, nothing to run")
        return
    if platform.system() == "Windows":
        warn("gstack: ./setup is a POSIX script — run it from Git Bash / WSL manually:")
        warn(f"      cd {repo_dir} && ./setup")
        return
    try:
        os.chmod(setup, 0o755)
    except OSError:
        pass
    # Prefer an explicit shell so a missing exec bit doesn't break it.
    sh = shutil.which("bash") or shutil.which("sh") or "sh"
    code = run([sh, "./setup"], cwd=repo_dir, check=False)
    (ok if code == 0 else warn)(f"gstack ./setup exited {code}")


# ──────────────────────────────────────────────────────────────────────────────
# Global tools
# ──────────────────────────────────────────────────────────────────────────────

def install_global_tool(name: str, spec: dict) -> None:
    if shutil.which(spec["check"]):
        skip(f"{name}: already on PATH")
        return
    log("INFO", f"{name}: not found — attempting install (confirm the command in CONFIG)")
    for cmd in spec["install"]:
        if shutil.which(cmd[0]) is None:
            warn(f"{name}: installer '{cmd[0]}' not available, trying next")
            continue
        code = run(cmd, check=False)
        if code == 0 and shutil.which(spec["check"]):
            ok(f"{name}: installed via {cmd[0]}")
            return
        warn(f"{name}: '{' '.join(cmd)}' didn't put '{spec['check']}' on PATH")
    fail(f"{name}: could not auto-install. Manual step: {spec['manual']}")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="Set up Claude Code skills + global tools.")
    ap.add_argument("--root", default=".", help="project root (default: current dir)")
    ap.add_argument("--force", action="store_true", help="re-clone repos that already exist")
    ap.add_argument("--skip-clone", action="store_true", help="don't clone skill repos")
    ap.add_argument("--skip-global", action="store_true", help="don't install global tools")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    skills_dir = root / ".claude" / "skills"

    step(f"Project root: {root}")
    skills_dir.mkdir(parents=True, exist_ok=True)
    ok(f"ensured {skills_dir}")

    if not args.skip_clone:
        require_git()
        step("Cloning skill repos")
        for name, url, hoist, run_setup in REPOS:
            try:
                clone_repo(name, url, hoist, run_setup, skills_dir, args.force)
            except subprocess.CalledProcessError:
                fail(f"{name}: clone failed — continuing with the rest")
    else:
        skip("clone step skipped (--skip-clone)")

    if not args.skip_global:
        step("Global tools (graphify, understand-anything)")
        for name, spec in GLOBAL_TOOLS.items():
            install_global_tool(name, spec)
    else:
        skip("global-tool step skipped (--skip-global)")

    step("Done")
    ok("Skills are under .claude/skills/. Start research by invoking ml-research-queries.")
    print("    Reminder: confirm the graphify / understand-anything install commands in CONFIG "
          "if they didn't install cleanly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
