# CodeXRay

CodeXRay | Turn your feedback into guidance for the next time AI writes code.

CodeXRay captures your explicit feedback on code explanations, implementation, debugging, and reviews. Let useful feedback build up, so you spend less time repeating the same corrections.

[中文说明](Readme-CN.md)

## Quick start in Codex

Cloning this repository into an arbitrary directory only downloads the skill. Install it into a skill directory before invoking it. Python 3 is required for the feedback storage helper.

### Install with Codex

Send the following in a Codex chat, not in your terminal:

```text
$skill-installer Install the skill from https://github.com/qiuchenmeng/CodeXRay. The skill path is the repository root (.), and the installed name should be codexray.
```

Once installation completes, try it on your next turn. If it does not appear in the skill selector, restart Codex.

Open the code project you want to work on and send:

```text
$codexray Explain this project's code structure.
```

### Install manually for all your projects

Use one of the following in a terminal. Both install into your own home directory, so they do not depend on the author's username or checkout location. Git is required.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME/.agents/skills" | Out-Null
git clone https://github.com/qiuchenmeng/CodeXRay.git "$HOME/.agents/skills/codexray"
```

macOS / Linux / WSL (Bash):

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/qiuchenmeng/CodeXRay.git "$HOME/.agents/skills/codexray"
```

The resulting layout must include:

```text
~/.agents/skills/codexray/
  SKILL.md
  scripts/append_feedback.py
  references/derive-preferences.md
```

If the destination already exists, inspect that installation instead of cloning over it. If you use WSL or a remote environment, install in the environment where Codex runs.

### Install for one project instead

From the root of the code project you want to use with CodeXRay, run:

```bash
git clone https://github.com/qiuchenmeng/CodeXRay.git .agents/skills/codexray
```

Then open that project in Codex and invoke the installed skill. The skill directory belongs inside the target code project; a sibling checkout is not a project installation.

## Invocation and verification

- In Codex CLI / IDE, use `/skills` or type `$` to select the installed `codexray` skill, then submit your coding question. These are chat inputs, not shell commands.
- In ChatGPT, type `@` and select an installed skill. Writing `@codexray` as plain text does not install a local Git checkout into ChatGPT. Follow that host's installation flow first.
- If the selector does not show `codexray`, check the installation path and restart Codex. A response that merely repeats the skill's name is not verification that the host discovered it.
- After the skill appears in the selector, a minimal smoke check is to ask it to run its `scripts/append_feedback.py --paths` helper. This reports storage paths without creating feedback files. Python 3 must be available.

Feedback is stored separately from the installation, in `~/.codexray` by default or in `CODEXRAY_HOME` when configured. CodeXRay learns from explicit feedback and synthesizes a personalized prompt when requested; a code question alone does not create feedback.

See [OpenAI Docs: Build skills](https://learn.chatgpt.com/docs/build-skills) for discovery paths and invocation rules. For distribution through the shared plugin directory, package the skill as a plugin using the official plugin workflow; cloning this repository is a local installation option.
