---
name: authoring-skill-frontmatter
description: "Choose invocation gates, inline vs context: fork, and structure when authoring a new skill. Use when writing a new SKILL.md, deciding which gate (disable-model-invocation vs user-invocable), or how a skill should activate."
when_to_use: "User asks which gate to use (disable-model-invocation vs user-invocable), inline vs fork, how to phrase a skill's body, or how to split SKILL.md across supporting files. For per-field syntax lookup, see frontmatter-reference.md."
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
model: sonnet
color: cyan
---

# Skill: Authoring Skill Frontmatter

**PURPOSE**
Decision guide for the *choices* an author makes when writing a skill: which gate, inline or forked, how to phrase the body, when to split into supporting files. For per-field syntax lookup (every frontmatter field, substitutions, permissions, namespacing), load [frontmatter-reference.md](frontmatter-reference.md).

If an existing skill is misbehaving (not triggering, not loading, runtime errors), use `/troubleshooting-skills` instead.

---

## INVOCATION GATES — pick a combination

Three independent controls. The combination determines who can invoke and whether Claude can even see the skill.

| `disable-model-invocation` | `user-invocable` | `/` works | Claude auto-loads | In context |
|---|---|---|---|---|
| (default) | (default) | yes | yes | yes |
| `true` | (default) | yes | no | no |
| (default) | `false` | no | yes | yes |
| `true` | `false` | no | no | dead skill — don't ship |

`allowed-tools` is a separate axis — it pre-approves tools while the skill is active. **It grants, never denies.** Settings-level deny rules still apply.

When to pick which:

- **(default both)** — most skills.
- **`disable-model-invocation: true`** — actions with side effects (`/deploy`, `/commit`, `/release`) where you don't want Claude triggering them.
- **`user-invocable: false`** — background knowledge skills (conventions, glossaries) that aren't actionable as a slash command.

---

## INLINE vs `context: fork`

| Pattern | What runs | When to use |
|---|---|---|
| Inline (default) | Skill body is added to the current conversation as one message | Reference content, conventions, procedures the main agent applies in-context |
| `context: fork` + `agent: <type>` | Skill body becomes the **prompt** for a subagent of the chosen type | Self-contained research / analysis tasks where the skill IS the task |

A `context: fork` skill with no actionable instruction (only "use these conventions…") returns nothing useful — the subagent has no task. If the body reads like reference, don't fork it.

The dual pattern (subagent declaring `skills:`) is different: the subagent has its own prompt, and skills are preloaded reference. Use that when a long-running custom agent needs the skill as background, not as a task.

---

## CONTENT LIFECYCLE — write standing rules, not one-time steps

The rendered `SKILL.md` enters the conversation as **one message** and stays. Claude does **not** re-read the file on later turns. Implications:

- Phrase guidance as standing rules ("whenever X, do Y"), not one-time steps ("first do this, then…"). One-time steps fire once and won't re-apply.
- Auto-compaction keeps the first 5,000 tokens of each invoked skill, with a 25,000-token combined budget across skills, filled most-recent-first.
- If a long-running session loses skill influence, re-invoke it.

---

## SUPPORTING FILES — when to split

Keep `SKILL.md` ≤200 lines preferred, ≤500 hard ceiling. Spill into siblings when content grows:

```
my-skill/
├── SKILL.md            # decision guide + navigation
├── reference.md        # per-field syntax / lookup tables
├── examples.md         # worked patterns
└── scripts/helper.py   # executed, not loaded as text
```

Boundary rule: `SKILL.md` holds what drives **decisions**; siblings hold what authors **look up**. If a section appears in both, one of them is wrong.

Link siblings with a loading hint so Claude knows what's there: *"For per-field syntax, see [frontmatter-reference.md](frontmatter-reference.md)."* Use `${CLAUDE_SKILL_DIR}` in `` !`cmd` `` blocks for paths to bundled scripts regardless of cwd.

---

## ANTI-PATTERNS

- **Description-as-summary.** Wrong: "This skill formats commits." Right: "Format git commit messages following Conventional Commits when staging or amending." The description IS the trigger phrase.
- **One-time procedural steps in `SKILL.md`.** Loaded once; "step 3 next" semantics break. Use `disable-model-invocation: true` to gate behind `/command`, or rephrase as standing rules.
- **Listing tools in `allowed-tools` to forbid them.** That field grants only — use settings deny rules.
- **`Agent` in `allowed-tools`.** Not a real tool. Use `Task` for delegation, or `context: fork` on the skill itself.
- **Stacking `disable-model-invocation: true` + `user-invocable: false`.** Nobody can invoke it.
- **`context: fork` on a reference skill.** No task = no output.
- **`$name` placeholder without a matching `arguments:` declaration.** Silent failure — placeholder stays literal.

---

## ADDITIONAL RESOURCES

- [frontmatter-reference.md](frontmatter-reference.md) — every frontmatter field, every substitution, dynamic `` !`cmd` `` injection syntax, permission syntax, plugin namespacing, live-reload rules, "ultrathink" keyword. Loaded on demand.
- `/troubleshooting-skills` — when an existing skill doesn't trigger, doesn't load, or fails at runtime.
