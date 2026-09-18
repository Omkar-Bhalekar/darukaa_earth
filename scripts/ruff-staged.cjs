const { spawnSync } = require('child_process');

const files = process.argv.slice(2).filter((file) => file.endsWith('.py'));
if (!files.length) {
  process.exit(0);
}

const result = spawnSync('python', ['-m', 'ruff', 'check', '--fix', ...files], {
  encoding: 'utf8',
});
const output = `${result.stdout || ''}${result.stderr || ''}`;
if (output.includes('No module named ruff')) {
  console.warn('ruff is not installed; skipping Python lint on this machine');
  process.exit(0);
}
if (result.stdout) process.stdout.write(result.stdout);
if (result.stderr) process.stderr.write(result.stderr);
process.exit(result.status ?? 0);
