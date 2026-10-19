---
name: codexray
description: "Learn reusable preferences from explicit feedback on code explanations, implementation, debugging, and review; capture feedback per user and synthesize a personalized coding prompt on request. Use for CodeXRay sessions and coding-preference synthesis, not paper-reading preferences."
---

# CodeXRay

Adapt code assistance to the user's explicit feedback. This skill handles preference capture and synthesis; it contains no default prompt or starter preferences.

## Session and storage

Accept a CodeXRay request with a repository, file, snippet, coding task, or feedback. Resolve code paths against the user's workspace and the helper script against this SKILL.md. Follow the project's instructions and inspect relevant code before explaining or changing it. Separate observed behavior, verified results, and hypotheses; preference learning does not authorize additional changes, commands, or repository operations.

Private state lives in `CODEXRAY_HOME` when set (expand environment variables and `~`), otherwise `~/.codexray`. It contains `reference.json` and, only after synthesis, `runtime-prompt-personalized.md`. This state is independent of PaperXRay. Never save personal state in the installed skill directory or import paper-reading preferences.

1. Run `python scripts/append_feedback.py --paths` once to resolve the absolute state paths without creating files. Use an explicitly supplied coding prompt if present; otherwise read the saved personalized prompt when available.
2. If there is no personalized prompt, proceed with the user's task and project conventions. Do not generate a substitute default or invent preferences. If a selected file is empty or unreadable, disclose that it was not loaded and continue with current instructions.
3. Apply current requests and explicit feedback before older learned preferences, subject to host/project requirements and task correctness. Repository-specific preferences remain scoped to that repository. Reuse the loaded prompt during follow-ups; reload when the user selects a different prompt or synthesis saves a revision.

## Capture feedback during code work

Capture an explicit evaluation of an answer/change or a stated reusable preference: explanation depth, code locations, examples, patch size, abstractions, naming, dependencies, debugging evidence, review format, or validation scope. These are possible topics, not assumed user preferences. A correction of a code fact is not automatically a general preference.

Ordinary coding requests, clarifying questions, and generic thanks are not feedback. Do not infer that acceptance endorses every implementation detail. Apply feedback immediately; if a message also contains a new task, attempt to save the feedback first, then continue the task.

Use `scripts/append_feedback.py` to append a concise record:

```sh
python scripts/append_feedback.py --query "<evaluated task>" --negative "<explicitly unwanted aspect>" --preference "<transferable rule>" --scope "<task type and any repository/language limits>"
```

`--positive` and `--negative` are repeatable. Omit aspects the user did not express. For quotes, multiline text, or shell-sensitive content, write one record to a temporary UTF-8 JSON file and pass `--file`; do not interpolate untrusted text into shell commands.

Records contain `user_query`, `positive`, `negative`, `preference`, and `scope`. Preserve scope and evidence; avoid full code, entire answers, proprietary implementation details, credentials, or paper-specific facts. Existing records are preserved and exact duplicates skipped. An actual stored record must contain explicit helpful/unwanted evidence or a stated preference.

Verify the script's success and report the absolute feedback file path briefly when a record is saved. If permissions or file access prevent saving, explain that it remains pending, provide a ready-to-save record, and continue applying it in-session. Do not claim persistence from acknowledgment alone or ask for a rating.

## Synthesize on request

Requests such as “总结我的代码反馈偏好”, “根据反馈更新代码 prompt”, or “生成 CodeXRay 新版偏好” trigger synthesis. Requests to summarize code, explain a method, or finish a coding task do not; feedback capture alone does not regenerate the prompt.

1. Save pending feedback first. If saving fails, report it and do not claim the pending evidence was persisted.
2. Run `python scripts/append_feedback.py --init` to initialize an empty feedback file if necessary and resolve its paths. Read the private `reference.json` as `{{FEEDBACK_JSON}}`. If it has no feedback, explain that explicit feedback is needed; create no prompt.
3. Read [references/derive-preferences.md](references/derive-preferences.md) only now. Supply the explicitly active prompt or saved personalized prompt as `{{EXISTING_PROMPT}}`; use an empty string when neither exists. Infer only evidence-supported preferences and retain conditions and exceptions.
4. Write the candidate to a temporary UTF-8 file, then run `python scripts/append_feedback.py --save-prompt "<candidate-file>"`. The helper rejects empty candidates and absent feedback, atomically saves to the same private profile, and verifies the bytes. On failure, retain the previous saved prompt and provide the candidate as unsaved. Report unchanged results as unchanged.
5. Briefly report the absolute saved prompt path and use it for subsequent answers. Future CodeXRay sessions load this version; a separate static chat needs an explicit reload. Synthesis changes prompt instructions, not model weights.

Use `--list` to inspect stored records. Ordinary code questions use loaded preferences and relevant code; read the full feedback dataset and synthesis reference only for feedback inspection or synthesis. No default-prompt file is shipped or loaded.
