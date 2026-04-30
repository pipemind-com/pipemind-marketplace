---
name: troubleshooting-skills
description: "Diagnose and fix skills that don't trigger, don't load, get shadowed, or fail at runtime. Use when a skill isn't working as expected."
user-invocable: true
argument-hint: "skill name, path, or symptom (e.g., 'foo-skill not triggering', 'path/to/SKILL.md')"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
model: sonnet
color: red
---

# Skill: Troubleshooting Skills

**PURPOSE**
Systematically diagnose a broken or misbehaving skill. Classify the failure into one of six categories, then apply the matching fix. Return a diagnosis + concrete change — not a rewrite of the whole skill.

---

### TRIAGE ORDER

Run checks in this order — cheap structural checks first, semantic reasoning last.

1. **Validator** — run the skills validator if available (`uvx agent-skills-verifier` or equivalent). It catches structural problems before anything else.
2. **Classify the symptom** — pick the category below that matches what the user reports.
3. **Apply the category's fix** — don't guess across categories.

If the user hasn't said what's wrong, ask one question: *"What's the observed behavior — not appearing in `/help`, not triggering on requests, wrong skill activating, or erroring mid-execution?"*

---

### CATEGORY 1 — Skill Doesn't Trigger

**Symptom:** skill exists, passes validation, but Claude doesn't activate it when expected.

**Check in this order:**

1. **`disable-model-invocation: true`** — if set, Claude can't see the description and won't auto-trigger. The `/` menu still works. Either remove the flag or invoke manually.
2. **`paths:` mismatch** — if the skill declares `paths:`, Claude only auto-loads it when the current file matches. Confirm the file you're editing matches a glob, or drop `paths:`.
3. **Description-trigger overlap** — read the user's phrasing vs. the skill's `description`. Add 3–5 trigger phrases that match real requests ("profile this," "why is this slow," "make this faster"). Use `when_to_use:` for example phrases — it's appended to `description` in the listing.
4. **1,536-char cap** — combined `description` + `when_to_use` is truncated at 1,536 chars per skill in the listing. If the skill has a long description, the trigger phrases at the end may be cut off. Front-load the primary use case.
5. **Global listing budget** — across many skills the total listing is capped (1% of context window, fallback 8,000 chars). Raise `SLASH_COMMAND_TOOL_CHAR_BUDGET`, or trim other skills' descriptions.

For the full set of frontmatter semantics, see `/authoring-skill-frontmatter`.

---

### CATEGORY 2 — Skill Doesn't Load

**Symptom:** skill doesn't appear in the available-skills list at all.

**Checks (in order):**
1. `SKILL.md` is inside a **named directory**, not at the skills root.
2. Filename is exactly `SKILL.md` — uppercase `SKILL`, lowercase `md`.
3. YAML frontmatter parses cleanly (no tab indents, required fields present).
4. Run `claude --debug` and grep the output for the skill name — the loader usually logs the exact failure.

---

### CATEGORY 3 — Wrong Skill Gets Used

**Symptom:** Claude activates a similar skill instead of the intended one, or seems to toggle between them.

**Cause:** descriptions are too semantically similar.

**Fix:**
- Diff the two descriptions. Look for overlapping verbs/nouns.
- Make each description **specific about scope**: what it handles *and* what it explicitly doesn't.
- Add disambiguating clauses: "Use for X. Not for Y — use `/other-skill` instead."

---

### CATEGORY 4 — Skill Is Shadowed (Priority Conflict)

**Symptom:** personal skill is ignored; a same-named skill from elsewhere wins.

**Cause:** enterprise/plugin skill with the same name takes precedence.

**Fix (preferred):** rename the personal skill to something more distinct. This is almost always faster than renegotiating priority.

**Fix (alternative):** if the shadowing skill is org-managed, escalate to the admin.

**Note:** plugin skills are namespaced as `plugin-name:skill-name` and do **not** conflict with personal/project/enterprise skills. If you suspect a plugin is shadowing, check that you're actually invoking the unnamespaced form.

---

### CATEGORY 5 — Plugin Skills Not Appearing

**Symptom:** installed a plugin, but its skills don't show up.

**Fix sequence:**
1. Clear the Claude Code cache.
2. Restart Claude Code.
3. Reinstall the plugin.
4. If still missing, run the validator on the plugin's skill directory — the structure is likely wrong (missing `SKILL.md`, wrong nesting, malformed manifest).

---

### CATEGORY 6 — Runtime Errors

**Symptom:** skill loads and activates, but fails during execution.

**Common causes:**
| Cause | Check | Fix |
|---|---|---|
| Missing dependencies | Does the skill call external packages? | Install them; document required deps in the skill description so Claude knows what's needed. |
| Permission issues | Does the skill invoke a script? | `chmod +x` on every referenced script. |
| Path separators | Any hardcoded `\` in paths? | Use forward slashes everywhere — even on Windows. |
| `$name` arguments stay literal | Does `arguments:` declare every `$name` referenced in the body? | Add the missing names to `arguments:` (positional, ordered) or switch to `$ARGUMENTS` / `$N`. Mismatches are silent. |
| `${CLAUDE_SKILL_DIR}` resolves wrong | Did you assume it's the plugin root? | It's the skill's own directory (the one containing `SKILL.md`), not the plugin root. Adjust paths to bundled scripts accordingly. |
| `` !`cmd` `` blocks not running | Settings have `"disableSkillShellExecution": true`? | Each command is replaced with `[shell command execution disabled by policy]`. Either lift the policy, or move the work into a tool call inside the skill body. Bundled/managed skills are exempt from this setting. |
| `shell: powershell` ignored | `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` set? | Required for PowerShell mode; otherwise `bash` is used. |

---

### CATEGORY 7 — `context: fork` Skill Returns Nothing

**Symptom:** skill is invoked, runs, finishes — but produces no useful output, or the response is generic.

**Cause:** the skill body has no actionable instruction. With `context: fork`, the body becomes the **prompt** for the subagent. A skill that only states conventions ("use these API patterns…") gives the subagent no task to perform, so it returns immediately with nothing.

**Fix:**
- Either remove `context: fork` (run inline so Claude uses the body as reference) and leave the conventions as standing rules.
- Or add an actionable directive at the end: *"Now research X, find Y, and return Z."* The body must read like a self-contained task description.
- Confirm the picked `agent:` type has the tools needed for the task (e.g., `Explore` for read-only codebase research).

---

### QUICK CHECKLIST

Return this as the final diagnosis summary:

- [ ] **Not triggering** → check `disable-model-invocation`, `paths:`, description+`when_to_use` ≤1,536 chars, trigger phrases match user phrasing
- [ ] **Not loading** → check path, filename (`SKILL.md`), YAML syntax, `claude --debug`
- [ ] **Wrong skill used** → make descriptions more distinct
- [ ] **Being shadowed** → rename, or escalate to admin (plugin skills are namespaced and don't conflict)
- [ ] **Plugin skills missing** → clear cache, restart, reinstall
- [ ] **Runtime failure** → deps, `chmod +x`, forward slashes, `arguments:` declared, `${CLAUDE_SKILL_DIR}` semantics, shell-execution policy
- [ ] **`context: fork` empty output** → body must be an actionable task, not just conventions

---

### OUTPUT FORMAT

Respond with:

1. **Category** — which of the six applies
2. **Evidence** — what in the skill/repro points to that category
3. **Fix** — the exact change to make (file, line, new text)
4. **Verify** — how the user confirms the fix worked

Do not rewrite the whole skill. Surface the smallest change that resolves the symptom.
