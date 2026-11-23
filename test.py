#!/usr/bin/env python3
"""Runs a template's set-up for real, in a fresh Debian container, then its check.

    python3 test.py            every template
    python3 test.py node rust  only these

Needs Docker and the network. A template's check is the "# check:" line at its top.
"""
import pathlib, subprocess, sys

def steps(text):
    out, block = [], None
    lines = text.split('\n')
    start = next(i for i, l in enumerate(lines) if l.startswith('setup:'))
    for line in lines[start + 1:]:
        if line.startswith('  - '):
            if block is not None: out.append('\n'.join(block))
            rest = line[4:]
            block = [] if rest.strip() == '|' else [rest]
        elif line.startswith('    ') and block is not None:
            block.append(line[4:])
        elif line.strip() and not line.startswith(' '):
            break
    if block is not None: out.append('\n'.join(block))
    return out

def test(name, image='debian:trixie-slim'):
    text = pathlib.Path(name, 'annex.yml').read_text()
    check = next(l.split('check:', 1)[1].strip() for l in text.split('\n') if l.startswith('# check:'))
    script = 'set -e\ncd "$HOME"\n' + '\n'.join(f"sh -c {shq(s)}" for s in steps(text)) + f"\necho '--- check'\n{check}\n"
    r = subprocess.run(['docker', 'run', '--rm', image, 'sh', '-c', script], capture_output=True, text=True)
    tail = (r.stdout + r.stderr).strip().split('\n')[-3:]
    print(f"{'ok  ' if r.returncode == 0 else 'FAIL'} {name}: " + ' | '.join(tail), flush=True)
    return r.returncode == 0

def shq(s): return "'" + s.replace("'", "'\\''") + "'"

if __name__ == '__main__':
    names = sys.argv[1:] or sorted(p.parent.name for p in pathlib.Path('.').glob('*/annex.yml'))
    sys.exit(0 if all([test(n) for n in names]) else 1)
