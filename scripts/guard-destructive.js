#!/usr/bin/env node
// PreToolUse guard for Bash/PowerShell: flags irreversible commands.
// On a hit it prints a PreToolUse JSON decision with permissionDecision "ask" (exit 0),
// so Claude Code asks the user to confirm that one command; otherwise exit 0 silently.
// Opt out for one session with SSE_GUARD=off.
const DANGER_PATH = String.raw`(\/\*?|~\/?|\.\/?|\*|\$HOME\/?|\$\{HOME\}\/?)`;
const RULES = [
  [/\bgit\s+push\b[^\n]*\s(--force(?!-with-lease)\b|-f\b|\+\S)/, 'git force-push (use --force-with-lease after user approval)'],
  [/\bgit\s+reset\b[^\n]*\s--hard\b/, 'git reset --hard discards local work'],
  [/\bgit\s+clean\b[^\n]*\s(-[a-zA-Z]*f|--force\b)/, 'git clean -f deletes untracked files'],
  // Some token is a recursive flag (-r, -rf, -fR, --recursive) and some token is a root/home/cwd/wildcard path.
  [new RegExp(String.raw`\brm\s+(?=(?:\S+\s+)*?(?:-[a-zA-Z]*[rR][a-zA-Z]*|--recursive)(?:\s|$))(?:\S+\s+)*?["']?${DANGER_PATH}["']?(?=\s|$)`),
    'recursive delete of a root/home/wildcard path'],
  [/\bRemove-Item\b(?=[^\n]*\s-r(ec(urse)?)?\b)[^\n]*\s["']?([\\/]|[A-Z]:[\\/]?|~[\\/]?|\*|\$HOME[\\/]?)["']?(?=\s|$)/i,
    'recursive delete of a root/home/wildcard path'],
  [/\b(DROP\s+(DATABASE|SCHEMA|TABLE)|TRUNCATE\s+TABLE)\b/i, 'destructive SQL (DROP/TRUNCATE)'],
  [/\bDELETE\s+FROM\s+[\w.`[\]]+\s*(;|["']|$)/im, 'DELETE without WHERE'],
  [/\bterraform\s+(destroy|apply\b[^\n]*-auto-approve)/, 'terraform destroy / auto-approved apply'],
  [/\bkubectl\s+delete\b[^\n]*(namespace|ns|--all)\b/, 'kubectl bulk/namespace delete'],
  [/\bhelm\s+uninstall\b/, 'helm uninstall'],
  [/\bdocker\s+system\s+prune\b[^\n]*-a/, 'docker system prune -a'],
];
// Commands that only record, print or search text: quoted arguments are data, not commands.
const TEXT_ONLY = new Set(['git', 'grep', 'egrep', 'fgrep', 'rg', 'echo', 'printf', 'select-string']);

// Split on ; & | and newlines outside quotes. Each segment keeps its raw text and a copy
// with quoted contents blanked, so a commit message or grep pattern is not mistaken for a command.
function segments(cmd) {
  const out = [];
  let raw = '', bare = '', quote = '';
  const flush = () => { if (raw.trim()) out.push({ raw, bare }); raw = bare = ''; };
  for (let i = 0; i < cmd.length; i++) {
    const c = cmd[i];
    if (quote) {
      if (quote === '"' && c === '\\' && cmd[i + 1] === '"') { raw += c + cmd[++i]; continue; }
      raw += c;
      if (c === quote) { quote = ''; bare += c; }
    } else if (c === '"' || c === "'") {
      quote = c; raw += c; bare += c;
    } else if (';&|\n'.includes(c)) {
      flush();
    } else {
      raw += c; bare += c;
    }
  }
  flush();
  return out;
}

// Quote-stripped text is always checked; the raw text (quotes included, e.g. mysql -e "DROP ...",
// bash -c "...") is checked too unless the segment starts with a text-only command.
function check(cmd) {
  for (const { raw, bare } of segments(cmd)) {
    const first = ((bare.trim().split(/\s+/)[0] || '').split(/[\\/]/).pop() || '').toLowerCase().replace(/\.exe$/, '');
    const texts = TEXT_ONLY.has(first) ? [bare] : [bare, raw];
    const hit = RULES.find(([re]) => texts.some((t) => re.test(t)));
    if (hit) return hit[1];
  }
  return null;
}

let input = '';
process.stdin.on('data', (c) => (input += c));
process.stdin.on('end', () => {
  if ((process.env.SSE_GUARD || '').toLowerCase() === 'off') process.exit(0);
  let cmd = '';
  try {
    cmd = (JSON.parse(input || '{}').tool_input || {}).command || '';
  } catch {
    process.exit(0); // never break the session on malformed input
  }
  if (typeof cmd !== 'string') process.exit(0);
  const reason = check(cmd);
  // No process.exit() after writing: stdout pipes are async on Windows and could be truncated.
  if (reason) {
    process.stdout.write(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        permissionDecision: 'ask',
        permissionDecisionReason: `[sse-plugin] ${reason}. Confirm only if this is intended.`,
      },
    }));
  }
});
