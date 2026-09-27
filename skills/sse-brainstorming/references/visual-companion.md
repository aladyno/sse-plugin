# Visual Companion Guide

Browser-based companion for `sse-brainstorming`: shows mockups, diagrams and visual options while
the design conversation stays in the terminal. Rules for *when* to offer it live in
[`../SKILL.md` → Visual companion](../SKILL.md#visual-companion); this file is the operating manual.

`SKILL_DIR` below means this skill's base directory — `${CLAUDE_PLUGIN_ROOT}/skills/sse-brainstorming`
(Claude Code also prints it as "Base directory for this skill" when the skill loads). Always quote it:
the path may contain spaces.

**Approval first.** Start the server only after the user accepted the companion, and stop it when
the design is done or the user asks (Expert Entity Contract §6 hybrid exception).

## When to use

Decide per question, not per session. The test: **would the user understand this better by seeing
it than reading it?**

**Use the browser** when the content itself is visual:

- **UI mockups** — wireframes, layouts, navigation structures, component designs
- **Architecture diagrams** — system components, data flow, relationship maps (C4 container/component zoom)
- **Side-by-side visual comparisons** — two layouts, two colour schemes, two design directions
- **Design polish** — look and feel, spacing, visual hierarchy
- **Spatial relationships** — state machines, flowcharts, entity relationships rendered as diagrams

**Use the terminal** when the content is text or tabular:

- **Requirements and scope questions** — "what does X mean?", "which features are in scope?"
- **Conceptual A/B/C choices** — picking between approaches described in words
- **Trade-off lists** — pros/cons, comparison tables
- **Technical decisions** — API design, data modelling, architectural approach selection
- **Clarifying questions** — anything where the answer is words, not a visual preference

A question *about* a UI topic is not automatically a visual question. "What kind of wizard do you
want?" is conceptual — terminal. "Which of these wizard layouts feels right?" is visual — browser.

## How it works

The server (`scripts/server.cjs`, Node only, no dependencies) watches a directory for HTML files and
serves the newest one. You write HTML into `screen_dir`; the user sees it in the browser and can click
to select options. Clicks are recorded to `state_dir/events`, which you read on your next turn.

**Content fragments vs full documents:** if the HTML file starts with `<!DOCTYPE` or `<html`, the
server serves it as-is (it only injects the helper script). Otherwise it wraps the content in the
frame template — header, theme CSS, connection status and all interactive infrastructure. **Write
fragments by default.** Write full documents only when you need complete control of the page.

The companion makes **no outbound network requests** of its own; it binds to `127.0.0.1` by default.

## Starting a session

### Claude Code on macOS / Linux / Windows (Bash tool = Git Bash)

```bash
# Start AFTER the user approves the companion. --open auto-opens their browser on the first
# screen; --project-dir persists mockups and enables same-port restart.
bash "$SKILL_DIR/scripts/start-server.sh" --project-dir "/path/to/project" --open

# Prints: {"type":"server-started","pid":12345,"port":52341,
#          "url":"http://localhost:52341/?key=ab12…",
#          "screen_dir":"/path/to/project/.sse-brainstorming/<session>/content",
#          "state_dir":"/path/to/project/.sse-brainstorming/<session>/state", …}
```

- **macOS / Linux:** the script backgrounds the server itself and returns the JSON.
- **Windows (Git Bash):** the script detects MSYS/Cygwin and runs in the **foreground** (Git Bash
  reaps detached processes). Run the Bash tool call with `run_in_background: true`, then on the next
  step read `<state_dir>/server-info` (or the background task output) to get the URL. Paths in the
  JSON come back as native Windows paths — use them as-is with the file-writing tool.

### Windows without Git Bash (PowerShell tool)

The `.sh` helpers need bash. Without it, launch Node directly — this is the same server, only the
wrapper differs:

```powershell
$skill   = "$env:CLAUDE_PLUGIN_ROOT\skills\sse-brainstorming"   # or the skill's base directory
$project = "C:\path\to\project"
$session = Join-Path $project (".sse-brainstorming\" + [DateTimeOffset]::Now.ToUnixTimeSeconds())
New-Item -ItemType Directory -Force (Join-Path $session 'state') | Out-Null
$env:BRAINSTORM_DIR        = $session
$env:BRAINSTORM_PORT_FILE  = Join-Path $project '.sse-brainstorming\.last-port'
$env:BRAINSTORM_TOKEN_FILE = Join-Path $project '.sse-brainstorming\.last-token'
$env:BRAINSTORM_OPEN       = '1'            # omit to skip auto-opening the browser
Start-Process node -ArgumentList "`"$skill\scripts\server.cjs`"" -WindowStyle Hidden `
  -RedirectStandardOutput (Join-Path $session 'state\server.log')
# Then poll for <session>\state\server-info and read it (ConvertFrom-Json) for url/pid/screen_dir.
```

`Start-Process` detaches the server, so it survives across turns. Optional environment variables:
`BRAINSTORM_HOST`, `BRAINSTORM_URL_HOST`, `BRAINSTORM_IDLE_TIMEOUT_MS`.

### Options (start-server.sh)

| Flag | Meaning |
|---|---|
| `--project-dir <path>` | Store sessions under `<path>/.sse-brainstorming/` (persist after stop; reuse port + key on restart). Without it, sessions go to the temp dir and are deleted on stop. |
| `--open` | Open the browser on the first pushed screen (only after the user approved the companion). |
| `--host <bind>` / `--url-host <host>` | Bind a non-loopback interface (remote/container setups) / hostname printed in the URL. |
| `--idle-timeout-minutes <n>` | Auto-exit after n idle minutes (default 240). |
| `--foreground` / `--background` | Force the run mode instead of auto-detection. |

Remind the user to add `.sse-brainstorming/` to `.gitignore` if it is not there — never edit it
yourself without asking.

### Session key

The URL carries a session key (`?key=…`); the server rejects requests without it. Always give the
user the **complete** URL from the `url` field — never strip the query string or hand out a bare
`http://host:port`. After the first load the browser keeps the key in a cookie, so reloads work.
`server-info` contains the key and is written owner-only; don't paste it into tickets or commits.

### Windows notes (verified on Windows 11, Node 24, Git Bash)

- Random ports that fall inside Windows' reserved ("excluded") port ranges fail with `EACCES`; the
  server retries other random ports automatically (`netsh interface ipv4 show excludedportrange
  protocol=tcp` lists them).
- Session paths containing 8.3 short names (e.g. `C:\Users\JOHNDO~1\AppData\Local\Temp`) are
  expanded to long paths before watching, so the file watcher does not abort.

## The loop

1. **Check the server is alive, then write HTML** to a new file in `screen_dir`:
   - **Required:** before referring to the URL or pushing a screen, check `<state_dir>/server-info`
     exists and `<state_dir>/server-stopped` does not. If it has stopped, restart it with the **same
     `--project-dir`** — it reuses the port and key, so the user's open tab reconnects by itself
     (it shows a "paused" overlay while the server is down). The server auto-exits after 4 h idle.
   - Semantic filenames: `platform.html`, `visual-style.html`, `layout.html`.
   - **Never reuse filenames** — each screen is a fresh file; iterations get `layout-v2.html`.
   - Use the file-creation tool — **never cat/heredoc** (it dumps noise into the terminal).
   - The server serves the newest file by modification time.
2. **Tell the user what to expect and end your turn:**
   - Repeat the URL (every step, not only the first).
   - One-line summary of what is on screen ("Showing 3 layout options for the homepage").
   - Ask them to answer in the terminal: "Take a look and tell me what you think. Click to select
     an option if you like."
3. **On your next turn**, after the user replies in the terminal:
   - Read `<state_dir>/events` if it exists — JSON lines of browser clicks/selections.
   - Merge with the terminal text; the terminal message is the primary feedback.
4. **Iterate or advance** — feedback changes the screen → write a new version. Move to the next
   question only when the current step is validated.
5. **Unload when returning to the terminal** — when the next step needs no browser, push a waiting
   screen so the user isn't staring at a resolved choice:

   ```html
   <!-- filename: waiting.html (or waiting-2.html, etc.) -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">Continuing in terminal...</p>
   </div>
   ```

6. Repeat until the design is approved.

## Writing content fragments

Write only the content that goes inside the page; the server wraps it.

```html
<h2>Which layout works better?</h2>
<p class="subtitle">Consider readability and visual hierarchy</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Single Column</h3>
      <p>Clean, focused reading experience</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>Two Column</h3>
      <p>Sidebar navigation with main content</p>
    </div>
  </div>
</div>
```

No `<html>`, no CSS, no `<script>` needed.

## CSS classes available

### Options (A/B/C choices)

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Title</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

**Multi-select:** add `data-multiselect` to the container; each click toggles the item.

```html
<div class="options" data-multiselect>
  <!-- same option markup — users can select/deselect multiple -->
</div>
```

### Cards (visual designs)

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- mockup content --></div>
    <div class="card-body">
      <h3>Name</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

### Mockup container

```html
<div class="mockup">
  <div class="mockup-header">Preview: Dashboard Layout</div>
  <div class="mockup-body"><!-- your mockup HTML --></div>
</div>
```

### Split view (side by side)

```html
<div class="split">
  <div class="mockup"><!-- left --></div>
  <div class="mockup"><!-- right --></div>
</div>
```

### Pros / cons

```html
<div class="pros-cons">
  <div class="pros"><h4>Pros</h4><ul><li>Benefit</li></ul></div>
  <div class="cons"><h4>Cons</h4><ul><li>Drawback</li></ul></div>
</div>
```

### Mock elements (wireframe building blocks)

```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display: flex;">
  <div class="mock-sidebar">Navigation</div>
  <div class="mock-content">Main content area</div>
</div>
<button class="mock-button">Action Button</button>
<input class="mock-input" placeholder="Input field">
<div class="placeholder">Placeholder area</div>
```

### Typography and sections

- `h2` — page title · `h3` — section heading
- `.subtitle` — secondary text below the title
- `.section` — content block with bottom margin
- `.label` — small uppercase label text

## Browser events format

Clicks are appended to `<state_dir>/events`, one JSON object per line; the file is cleared when you
push a new screen.

```jsonl
{"type":"click","choice":"a","text":"Option A - Simple Layout","timestamp":1706000101}
{"type":"click","choice":"c","text":"Option C - Complex Grid","timestamp":1706000108}
{"type":"click","choice":"b","text":"Option B - Hybrid","timestamp":1706000115}
```

The last choice is usually the final selection, but the click path can reveal hesitation worth
asking about. No `events` file → the user didn't interact; use only their terminal text.

## Design tips

- **Scale fidelity to the question** — wireframes for layout, polish for polish questions.
- **State the question on each page** — "Which layout feels more professional?", not "Pick one".
- **Iterate before advancing** — feedback changes the screen → new version.
- **2–4 options max** per screen.
- **Real content when it matters** — placeholder text hides design problems. External images make
  the *browser* fetch from the internet; prefer local files served via `/files/<name>` from
  `screen_dir` when the project is confidential.
- **Keep mockups simple** — layout and structure, not pixel perfection.

## Cleaning up

Bash (macOS / Linux / Git Bash):

```bash
bash "$SKILL_DIR/scripts/stop-server.sh" "<session_dir>"   # session_dir = parent of screen_dir
# → {"status":"stopped"} | {"status":"not_running"} | {"status":"stale_pid"}
```

PowerShell (server started with `Start-Process`):

```powershell
$info = Get-Content "<state_dir>\server-info" -Raw | ConvertFrom-Json
Stop-Process -Id $info.pid
Remove-Item "<state_dir>\server-info"
Set-Content "<state_dir>\server-stopped" '{"reason":"Stop-Process"}'
```

`--project-dir` sessions keep their mockups in `.sse-brainstorming/` for later reference; temp-dir
sessions are deleted by `stop-server.sh`. `stop-server.sh` refuses to signal a PID it cannot prove
is this session's server (stale PID file after a reboot) and reports `stale_pid`.

## Reference

- Frame template (CSS reference): [`../scripts/frame-template.html`](../scripts/frame-template.html)
- Client helper: [`../scripts/helper.js`](../scripts/helper.js)
- Server: [`../scripts/server.cjs`](../scripts/server.cjs) — launchers
  [`start-server.sh`](../scripts/start-server.sh) / [`stop-server.sh`](../scripts/stop-server.sh)
