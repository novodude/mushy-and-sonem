# Sonem (Mushy)

A Discord bot run by Mushy, a small mushroom creature whose whole mission is to make
Sonem the best free Discord companion she can — by continuously working on herself.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in DISCORD_TOKEN and NARA_API_KEY

# Give her commits their own identity, scoped to just this repo (not --global —
# this won't touch your own git config anywhere else)
git config user.name "Mushy"
git config user.email "mushy@sonem.bot"

python main.py
```

## What's actually running

- **Chat** — mention the bot and she'll respond, using the same tools as her
  self-improvement loop.
- **Self-improvement loop** (`core/self_improvement.py`) — runs continuously, cycles
  back-to-back with no real cooldown (max 8 tool-call rounds each). Only pauses —
  for `SONEM_BACKOFF_MINUTES` (default 30) — when every model in the fallback chain
  fails, which in practice means quota exhaustion or every provider being down.
  She decides what to work on herself each cycle — a bug, a new tool, reading
  `/suggest` submissions, whatever. What she's doing shows live on her Discord
  status (`set_status`); she only DMs you for things that actually need you.
  the contract in `instructions/TOOLS.md`, call `restart` to load it. Core tools
  (`core/`) are off-limits to her — if those need changing, she messages you.
- **Slash commands** — `/suggest <feature>` (anyone), `/set_server` (you only, marks
  a server as her "home" for channel creation etc.)

## Important: this is NOT sandboxed

`run_bash`/`run_python`/`read_file`/`write_file` have real, unrestricted access —
whatever the OS user running this process can do, she can do. Restricting the
_paths_ she can touch wouldn't actually mean anything once she has a working shell
(`cd ..` gets around any path check that isn't OS-enforced), so I didn't fake one.

If you want a real boundary: run this under a dedicated, low-privilege OS user, or in
a container/VM with only this project mounted. That's the boundary that actually
holds — not something in this codebase.

Other things worth knowing:

- The self-improvement loop runs continuously with no fixed cooldown, bounded per
  cycle (max 8 rounds). It only backs off (`SONEM_BACKOFF_MINUTES`, default 30) when
  every model fails — quota exhaustion or every provider down are the realistic
  cases. She DMs you exactly once at startup (the anchor message) and otherwise only
  when something actually needs you — routine activity shows in her Discord status
  instead, via `set_status`.
- Every tool call gets logged to `data/state.json` (`activity_log` field) — worth
  skimming after the fact, especially early on.
- Model fallback chain (`core/ai.py`): `mistral-large` → `ling-3.0-flash-free` →
  `laguna-s-2.1`, retried a couple times each on 503/429 before falling through.
- `restart` re-execs the process (`os.execv`) — it picks up new plugin files, code
  edits, everything. Make sure whatever's supervising this process (systemd, pm2, a
  plain shell loop) actually keeps it running afterward if you want restarts to be
  seamless.
- She's expected to `git add`/`commit`/`push` after any change she makes (that's in
  `MISSION.md`) — local disk isn't durable, the repo is. Worth glancing at `git log`
  occasionally to see what she's actually been doing.
