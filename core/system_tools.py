"""
core/system_tools.py — vision, file I/O, terminal, and restart.

These are NOT sandboxed. Relative paths resolve against ROOT_DIR (this project's own
folder, by default) purely for convenience so she naturally works on her own codebase,
but nothing here stops `run_bash` from doing `cd / && anything`. If you want a hard
boundary, run this process under a restricted OS user or in a container — that's the
only boundary that actually holds against a real shell.
"""

import asyncio
import os
import sys
from pathlib import Path

from core.ai import describe_image

ROOT_DIR = Path(os.getenv("SONEM_ROOT_DIR", Path(__file__).resolve().parent.parent))
TIMEOUT_SECONDS = 30
MAX_OUTPUT_CHARS = 4000


async def h_vision(params: dict, ctx) -> str:
    url = params.get("url")
    question = params.get("question", "Describe this image.")
    if not url:
        return "Need an image url."
    try:
        return await describe_image(url, question)
    except Exception as e:
        return f"Couldn't look at that image: {e}"


async def h_read_file(params: dict, ctx) -> str:
    path = ROOT_DIR / params.get("path", "")
    if not path.exists() or not path.is_file():
        return f"No such file: {params.get('path')}"
    try:
        return path.read_text(errors="replace")[:MAX_OUTPUT_CHARS]
    except Exception as e:
        return f"Couldn't read file: {e}"


async def h_write_file(params: dict, ctx) -> str:
    path = ROOT_DIR / params.get("path", "")
    content = params.get("content", "")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return f"Wrote {len(content)} chars to {params.get('path')}"
    except Exception as e:
        return f"Couldn't write file: {e}"


async def h_list_files(params: dict, ctx) -> str:
    path = ROOT_DIR / params.get("path", "") if params.get("path") else ROOT_DIR
    if not path.exists() or not path.is_dir():
        return f"No such directory: {params.get('path', '.')}"
    entries = sorted(path.iterdir())
    if not entries:
        return "(empty)"
    return "\n".join(f"{'d' if e.is_dir() else 'f'} {e.relative_to(ROOT_DIR)}" for e in entries)


async def _run_subprocess(*args: str, cwd: Path) -> str:
    try:
        proc = await asyncio.create_subprocess_exec(
            *args, cwd=str(cwd),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            return f"[timed out after {TIMEOUT_SECONDS}s]"
    except Exception as e:
        return f"[failed to run: {e}]"

    out = stdout.decode(errors="replace").strip()
    err = stderr.decode(errors="replace").strip()
    result = out
    if err:
        result += f"\n[stderr]\n{err}" if result else f"[stderr]\n{err}"
    return (result or "[no output]")[:MAX_OUTPUT_CHARS]


async def _run_shell(command: str, cwd: Path) -> str:
    try:
        proc = await asyncio.create_subprocess_shell(
            command, cwd=str(cwd),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            return f"[timed out after {TIMEOUT_SECONDS}s]"
    except Exception as e:
        return f"[failed to run: {e}]"

    out = stdout.decode(errors="replace").strip()
    err = stderr.decode(errors="replace").strip()
    result = out
    if err:
        result += f"\n[stderr]\n{err}" if result else f"[stderr]\n{err}"
    return (result or "[no output]")[:MAX_OUTPUT_CHARS]


async def h_run_bash(params: dict, ctx) -> str:
    command = params.get("command", "")
    if not command:
        return "No command given."
    # Runs through an actual shell (not exec'd as a bare argv list) so cd, &&, pipes,
    # globs, etc. all work the way you'd expect from typing this at a real terminal.
    return await _run_shell(command, cwd=ROOT_DIR)


async def h_run_python(params: dict, ctx) -> str:
    code = params.get("code", "")
    if not code:
        return "No code given."
    return await _run_subprocess(sys.executable, "-c", code, cwd=ROOT_DIR)


async def h_restart(params: dict, ctx) -> str:
    """Restarts this whole process (picks up any code changes, including new
    plugins) by re-exec'ing python on main.py. Whatever called this should send a
    heads-up message first — the process image gets replaced right after, so nothing
    after this call in the same turn will run."""
    ctx.state.log(f"restarting — reason: {params.get('reason', 'unspecified')}")
    from core.persistence import save_state
    save_state(ctx.state)

    async def _do_restart():
        await asyncio.sleep(1)  # let the current Discord message actually send first
        os.execv(sys.executable, [sys.executable, str(ROOT_DIR / "main.py")])

    asyncio.create_task(_do_restart())
    return "Restarting now."
