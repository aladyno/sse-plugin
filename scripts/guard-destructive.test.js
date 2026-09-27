#!/usr/bin/env node
// Plain-node tests for guard-destructive.js: node scripts/guard-destructive.test.js
const { spawnSync } = require('child_process');
const path = require('path');
const HOOK = path.join(__dirname, 'guard-destructive.js');

// Returns 'ask' when the hook asks for confirmation, 'allow' when it stays silent.
function run(stdin, env = {}) {
  const r = spawnSync(process.execPath, [HOOK], { input: stdin, encoding: 'utf8', env: { ...process.env, SSE_GUARD: '', ...env } });
  if (r.status !== 0) return `exit ${r.status}: ${r.stderr}`;
  if (!r.stdout.trim()) return 'allow';
  const d = JSON.parse(r.stdout).hookSpecificOutput || {};
  return d.hookEventName === 'PreToolUse' && d.permissionDecision === 'ask' && /^\[sse-plugin\] /.test(d.permissionDecisionReason) ? 'ask' : `bad output: ${r.stdout}`;
}
const cmd = (c) => JSON.stringify({ tool_input: { command: c } });

const ASK = [
  'git push --force origin main',
  'git push -f',
  'git push origin +main',
  'git reset --hard HEAD~1',
  'bash -c "git reset --hard"',
  'git clean -fd',
  'rm -rf /',
  'rm -r -f /',
  'rm -rf ~',
  'rm -rf ~/',
  'rm -rf .',
  'rm -rf ./',
  'rm -rf *',
  'rm -rf $HOME',
  'rm -rf $HOME/',
  'rm --recursive --force /',
  'cd x && rm -rf ~/',
  'Remove-Item -Recurse -Force C:\\',
  'Remove-Item C:\\ -Recurse',
  'Remove-Item -Recurse -Force ~',
  'Remove-Item -Recurse /',
  'Remove-Item -Recurse *',
  'DROP TABLE users;',
  'DELETE FROM db.users;',
  'DELETE FROM `db`.`users`;',
  'mysql -e "DROP TABLE x"',
  "psql -c 'TRUNCATE TABLE t'",
  'mysql -e "DELETE FROM users"',
  'terraform destroy',
  'terraform apply -auto-approve',
  'kubectl delete ns foo',
  'helm uninstall x',
  'docker system prune -a',
];
const ALLOW = [
  'git push --force-with-lease',
  'git push origin main',
  'git status',
  'rm -rf ./build',
  'rm -rf /tmp/foo',
  'rm -rf node_modules',
  'rm -f /',
  'Remove-Item -Recurse C:\\temp\\build',
  'DELETE FROM users WHERE id=1;',
  'git commit -m "remove DROP TABLE usage"',
  'grep -rn "git reset --hard" docs',
  'git commit -m "a; DROP TABLE x"',
  'echo "DROP TABLE x"',
  'terraform plan',
  'kubectl get ns',
  'docker system prune',
];

let fail = 0;
const expect = (name, got, want) => {
  if (got !== want) { fail++; console.log(`FAIL [${want}] ${name} -> ${got}`); }
};
for (const c of ASK) expect(c, run(cmd(c)), 'ask');
for (const c of ALLOW) expect(c, run(cmd(c)), 'allow');
expect('SSE_GUARD=off bypass', run(cmd('git reset --hard'), { SSE_GUARD: 'off' }), 'allow');
expect('malformed input', run('{not json'), 'allow');
expect('empty input', run(''), 'allow');

const total = ASK.length + ALLOW.length + 3;
console.log(`${total - fail}/${total} passed`);
process.exit(fail ? 1 : 0);
