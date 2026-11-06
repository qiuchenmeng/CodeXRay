# CodeXRay

Turn your feedback into guidance for the next time AI writes code. CodeXRay captures explicit feedback on code explanations, implementation, debugging, and reviews, then synthesizes a personalized coding prompt when requested.

[中文说明](Readme-CN.md)

## Quick start

Requires Git, Python 3, and a Codex version with `codex plugin` support.

Run in your terminal:

```sh
git clone https://github.com/qiuchenmeng/CodeXRay.git
cd CodeXRay
codex plugin marketplace add .
codex plugin add codexray@codexray
```

The last two commands register the marketplace and install the plugin. Run them using the same Codex environment/profile as the app where you will use CodeXRay. Cloning alone does not register a plugin.

Start a new Codex chat, open your code project, and send:

```text
@codexray Explain this project's code structure.
```

If your client uses `$` for skill selection, select `codexray` with that selector. Check that `codexray:codexray` appears in the available skills; restart Codex if the installed plugin has not appeared yet.

Verify the plugin installation in your terminal:

```sh
codex plugin list --marketplace codexray --json
```

The plugin should be installed and enabled. To check its helper without creating feedback, ask CodeXRay to run its bundled `scripts/append_feedback.py --paths` from the installed skill directory.

## Install directly from GitHub

Once this plugin layout is published to the repository, users can install without a separate checkout:

```sh
codex plugin marketplace add https://github.com/qiuchenmeng/CodeXRay.git
codex plugin add codexray@codexray
```

## Plugin layout

```text
.codex-plugin/plugin.json       Codex plugin manifest
.claude-plugin/plugin.json      Claude-compatible plugin manifest
.claude-plugin/marketplace.json Marketplace entry
skills/codexray/
  SKILL.md
  scripts/append_feedback.py
  references/derive-preferences.md
```

The manifests point to the same skill resources. For standalone skill installation, use the `skills/codexray` folder, not the repository root.

Feedback lives in `~/.codexray`, or in `CODEXRAY_HOME` when set. Installing or updating the plugin does not replace that private state. CodeXRay records explicit feedback; ordinary coding questions do not become preference records. Ask it to synthesize a personalized prompt when you want to update your coding guidance.
