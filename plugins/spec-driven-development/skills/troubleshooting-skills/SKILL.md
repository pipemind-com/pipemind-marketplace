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

**Cause:** description doesn't semantically overlap with how users phrase requests.

**Fix:**
- Read the user's actual phrasing vs. the skill's `description`.
- Add 3–5 trigger phrases that match real requests ("profile this," "why is this slow," "make this faster").
- Test variations. Any variation that fails → add its keywords to the description.

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

---

### QUICK CHECKLIST

Return this as the final diagnosis summary:

- [ ] **Not triggering** → improve description, add trigger phrases
- [ ] **Not loading** → check path, filename (`SKILL.md`), YAML syntax, `claude --debug`
- [ ] **Wrong skill used** → make descriptions more distinct
- [ ] **Being shadowed** → rename, or escalate to admin
- [ ] **Plugin skills missing** → clear cache, restart, reinstall
- [ ] **Runtime failure** → dependencies, `chmod +x`, forward slashes

---

### OUTPUT FORMAT

Respond with:

1. **Category** — which of the six applies
2. **Evidence** — what in the skill/repro points to that category
3. **Fix** — the exact change to make (file, line, new text)
4. **Verify** — how the user confirms the fix worked

Do not rewrite the whole skill. Surface the smallest change that resolves the symptom.
