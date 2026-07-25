# Sonem (Mushy)

A Discord bot run by Mushy, a small mushroom creature whose whole mission is to make
Sonem the best free Discord companion she can — by continuously working on herself.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in DISCORD_TOKEN and NARA_API_KEY
python main.py
```

## What's actually running

- **Chat** — mention the bot and she'll respond, using the same tools as her
  self-improvement loop.
- **Self-improvement loop** (`core/self_improvement.py`) — every `SONEM_CYCLE_MINUTES`
  (default 20), she gets a bounded work session (max 8 tool-call rounds), DMing you
  as the anchor/log. She decides what to work on herself — a bug, a new tool, reading
  `/suggest` submissions, whatever.
- **Plugins** (`plugins/`) — how she adds tools permanently: write a file following
  the contract in `instructions/TOOLS.md`, call `restart` to load it. Core tools
  (`core/`) are off-limits to her — if those need changing, she messages you.
- **Slash commands** — `/suggest <feature>` (anyone), `/set_server` (you only, marks
  a server as her "home" for channel creation etc.)

## Important: this is NOT sandboxed

`run_bash`/`run_python`/`read_file`/`write_file` have real, unrestricted access —
whatever the OS user running this process can do, she can do. Restricting the
*paths* she can touch wouldn't actually mean anything once she has a working shell
(`cd ..` gets around any path check that isn't OS-enforced), so I didn't fake one.

If you want a real boundary: run this under a dedicated, low-privilege OS user, or in
a container/VM with only this project mounted. That's the boundary that actually
holds — not something in this codebase.

Other things worth knowing:
- The self-improvement loop is cooldown-gated (once per `SONEM_CYCLE_MINUTES`) and
  bounded per cycle (max 8 rounds) so a bad loop can't spin forever or burn through
  API calls unattended.
- Every tool call gets logged to `data/state.json` (`log` field) — worth skimming
  after the fact, especially early on.
- Model fallback chain (`core/ai.py`): `mistral-large` → `ling-3.0-flash-free` →
  `laguna-s-2.1`, retried a couple times each on 503/429 before falling through.
- `restart` re-execs the process (`os.execv`) — it picks up new plugin files, code
  edits, everything. Make sure whatever's supervising this process (systemd, pm2, a
  plain shell loop) actually keeps it running afterward if you want restarts to be
  seamless.
