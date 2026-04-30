# TODO

## Skill authoring follow-ups (deferred from agent-author self-improvement, 2026-04-29)

### Restructure `troubleshooting-skills` Category 1

**Source:** agent-author second-pass introspection.

Category 1 (`Skill Doesn't Trigger`) has grown into a 5-item checklist with its own ordering, breaking the "classify-then-apply" model that Categories 2–5 follow (3–5 lines each). Diagnostic accuracy improved, but shape is uneven.

**Options:**
- Split into two categories: "Not visible to Claude" (`disable-model-invocation`, `paths:` mismatch, 1,536-char cap, global listing budget) vs "Visible but description doesn't match user phrasing" (the original semantic-overlap fix).
- Or: keep one category but reorder so the cheap binary checks (`disable-model-invocation`, `paths:`) come before the semantic work, and label the sub-checks 1a/1b/1c instead of nesting a flat numbered list.

File: `plugins/spec-driven-development/skills/troubleshooting-skills/SKILL.md`

### Make cross-references to `/authoring-skill-frontmatter` consistent in `troubleshooting-skills`

**Source:** agent-author second-pass introspection.

Currently the pointer `"For the full set of frontmatter semantics, see /authoring-skill-frontmatter"` appears at the end of Category 1 only. Categories 6 and 7 also reference frontmatter behavior (`${CLAUDE_SKILL_DIR}` semantics, `context: fork`) without the same pointer.

**Decision needed:** repeat the pointer per category that touches frontmatter, or drop it entirely (the agent-author already routes both ways from its main flow). Avoid the current inconsistent middle.

File: `plugins/spec-driven-development/skills/troubleshooting-skills/SKILL.md`
