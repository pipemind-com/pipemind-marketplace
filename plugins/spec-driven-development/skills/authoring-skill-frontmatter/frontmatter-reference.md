# Skill Frontmatter Reference

Complete field-by-field reference. Loaded on demand from `SKILL.md` — do not paraphrase from memory.

All fields are optional unless noted. Order doesn't matter.

---

## name

Display name and slug. Lowercase letters, numbers, hyphens. Max 64 characters. If omitted, the directory name is used.

```yaml
name: reviewing-code
```

## description

What the skill does and when to use it. Claude matches user requests against this string. If omitted, the first paragraph of markdown content is used.

**Front-load the primary use case** — combined with `when_to_use`, the listing entry is truncated at **1,536 characters per skill**. Across many skills, the global listing budget is 1% of the context window (fallback 8,000 chars), overridable via the `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable.

The description IS the trigger phrase. Don't write a summary of the skill — write what Claude should match against.

```yaml
description: "Format git commits following Conventional Commits. Use when staging, amending, or about to commit."
```

## when_to_use

Supplementary trigger context — example phrases or canonical user requests. Appended to `description` in the listing. Counts toward the 1,536-char cap.

```yaml
when_to_use: "User says 'commit this', 'wrap it up', or stages files manually."
```

## argument-hint

Autocomplete hint shown after `/skill-name`. Bracket-token style.

```yaml
argument-hint: "[issue-number] [--dry-run]"
```

## arguments

Named positional arguments. Names map to `$name` substitutions in declaration order. Accepts a list or a space-separated string.

```yaml
arguments: [component, from, to]
# In SKILL.md body: Migrate $component from $from to $to.
```

Mismatch between this list and `$name` references in the body is silent — the placeholder will stay literal. Verify both sides.

## allowed-tools

Tools Claude can use without per-call approval **while this skill is active**. Pre-approval, not restriction. Every other tool stays callable; settings-level deny rules still apply.

```yaml
allowed-tools:
  - "Bash(git add *)"
  - "Bash(git commit *)"
  - Read
  - Edit
```

Use `Bash(<pattern>)` for command-pattern pre-approval; bare `Bash` grants all bash. To block a tool while the skill runs, use settings deny rules — not this field.

## disable-model-invocation

`true` removes the skill from Claude's context entirely. The `/` menu still works for the user. Also blocks the skill from being preloaded into subagents that opt into skill preloading.

```yaml
disable-model-invocation: true
```

## user-invocable

`false` hides from the `/` menu. Claude can still load and use the skill via auto-trigger.

```yaml
user-invocable: false
```

For the combined effect of `disable-model-invocation` + `user-invocable` and which combination to pick, see the truth table in `SKILL.md` (`INVOCATION GATES`).

## model

Override the session model for this skill's turn only. The session model resumes on the next prompt — this is not persisted to settings.

```yaml
model: opus       # or sonnet, haiku, inherit
```

`inherit` keeps the active model — useful as an explicit no-op for clarity.

## effort

Override session effort level. Available levels depend on model.

```yaml
effort: high      # low | medium | high | xhigh | max
```

## context

`fork` runs the skill body as the prompt for a forked subagent. Without `fork`, the skill runs inline in the current context.

```yaml
context: fork
agent: Explore
```

A `context: fork` skill with no actionable task returns nothing useful — the subagent has no instructions. Use this only when the skill body is a self-contained task description.

## agent

Which subagent type to spawn when `context: fork`. Defaults to `general-purpose`. Built-ins: `Explore`, `Plan`, `general-purpose`. Custom subagents from `.claude/agents/` work too.

The subagent's system prompt comes from the agent type. The skill body becomes the user-message prompt.

## paths

Glob patterns. When set, Claude auto-loads the skill **only** when working with files matching the patterns. User invocation via `/skill-name` is unaffected.

```yaml
paths:
  - "**/*.sql"
  - "migrations/**"
```

Same syntax as path-specific memory rules. If the skill isn't auto-triggering when you expect it to, check that the file you're working on actually matches a pattern.

## hooks

Skill-scoped hooks (run only while this skill is active). See the hooks reference for format.

## shell

Shell for `` !`cmd` `` blocks: `bash` (default) or `powershell`. PowerShell mode requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` in the environment.

---

## String substitutions

| Variable | Description |
|---|---|
| `$ARGUMENTS` | Full literal argument string. |
| `$ARGUMENTS[N]` | Indexed argument, 0-based, shell-quoted. |
| `$N` | Shorthand for `$ARGUMENTS[N]`. |
| `$name` | Named argument from `arguments:` list. |
| `${CLAUDE_SESSION_ID}` | Current session ID. |
| `${CLAUDE_EFFORT}` | Current effort level. |
| `${CLAUDE_SKILL_DIR}` | Directory containing this skill's `SKILL.md`. For plugin skills, the skill subdirectory — not the plugin root. |

Indexed arguments use shell-style quoting, so wrap multi-word values in quotes to pass them as one arg: `/my-skill "hello world" second` → `$0` = `hello world`, `$1` = `second`.

`$ARGUMENTS` always expands to the full literal string as typed. If `$ARGUMENTS` is absent from the body, supplied arguments are appended as `ARGUMENTS: <value>` so Claude still sees them.

---

## Dynamic context injection

`` !`<command>` `` runs before the skill content reaches Claude. Output replaces the placeholder.

Multi-line form (fenced block opened with ` ```! `):

````markdown
```!
gh pr diff
gh pr view --comments
```
````

Disable globally with `"disableSkillShellExecution": true` in settings. Each command is replaced with `[shell command execution disabled by policy]` instead of running. Bundled and managed skills are not affected — most useful in managed settings where users cannot override.

---

## Permission syntax

Settings rules referencing skills:

- `Skill(name)` — exact match
- `Skill(name *)` — name with any arguments

Use these in deny rules to block specific skills, or in allow rules to grant access.

To disable all skills, deny the bare `Skill` tool in `/permissions`.

---

## Plugin namespacing

Plugin skills are addressed as `plugin-name:skill-name`. They never collide with personal/project/enterprise skills — different namespace.

---

## Live change detection

Edits under `~/.claude/skills/`, project `.claude/skills/`, or `.claude/skills/` inside an `--add-dir` directory take effect mid-session without restart. Creating a new top-level skills directory mid-session requires restart so the new directory can be watched.

Working in a subdirectory auto-discovers nested skills: editing in `packages/frontend/` also loads `packages/frontend/.claude/skills/`.

---

## "ultrathink" keyword

The literal token `ultrathink` anywhere in the rendered skill content enables extended thinking mode for that turn.
