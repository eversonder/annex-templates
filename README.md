# Annex templates

Ready-made starting points for [Annex](https://annex.eversonder.com) sandboxes. A template is one small file, `annex.yml`, that says what a sandbox starts with. Copy one, change what you like, and every sandbox you start from it arrives with the tools already installed, on any provider.

| Template | What's on the machine |
|---|---|
| [node](node/annex.yml) | Node, npm, pnpm, TypeScript and git |
| [python-data](python-data/annex.yml) | Python with pandas, numpy, scipy and matplotlib |
| [browser](browser/annex.yml) | Playwright with headless Chromium |
| [rust](rust/annex.yml) | Rust (stable, from rustup) and a C toolchain |
| [go](go/annex.yml) | Go and git |
| [claude-code](claude-code/annex.yml) | Claude Code, git and the GitHub command |

## Use one

With the [`annex` command](https://github.com/eversonder/annex-cli) installed and signed in:

```sh
curl -fsSLO https://raw.githubusercontent.com/eversonder/annex-templates/main/node/annex.yml
annex start          # saves the template, then starts a sandbox from it
```

or save it without starting anything, and use it by name later:

```sh
annex template apply
annex start --template node
```

The same file works over the API and in the dashboard under **Templates**. The full guide is at [annex.eversonder.com/docs/templates](https://annex.eversonder.com/docs/templates).

## How a template behaves

- The set-up commands run in the first sandbox started from it. Annex then saves the files they changed and puts them back in later sandboxes, so the install happens once.
- A template names no provider and no image, so the same file works on every provider and on your own machines.
- Whatever a start asks for wins: `annex start --template rust --vcpu 8` starts the template with 8 vCPU.
- Add `default: true` and every sandbox in the workspace starts from it unless it names another.
- If a set-up starts a program that must keep running, add `always_run: true`: a saved result holds files, not running programs.

## What these assume

- A Debian or Ubuntu sandbox, which is what most providers start. They install with `apt-get`.
- Either the root user or `sudo` without a password. Each command works out which.

Every template here was run for real in a fresh Debian 13 container before it was added, and its `# check:` line passed. They have not each been run on every provider.

## Add yours

Open a pull request with a folder holding an `annex.yml`:

- Start it with a comment saying what it is, and a `# check:` line: one command that proves the set-up worked.
- Keep every command safe to run twice.
- Run `python3 test.py your-template` (needs Docker). It runs the set-up in a fresh container, then the check.

## Licence

MIT. See [LICENSE](LICENSE).
