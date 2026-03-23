---
name: conducting-post-mortem
description: "Extracts lessons from completed task and proposes CLAUDE.md updates. Use at the end of a task session to capture gotchas."
user-invocable: true
argument-hint: "none required - reviews current conversation"
allowed-tools:
  - Read
  - Grep
  - Glob
model: sonnet
color: yellow
---

# Conducting Post-Mortem

Analyzes the current conversation to identify lessons learned and proposes specific updates to CLAUDE.md to prevent future issues.

## When Invoked

This skill automatically reviews the current conversation context to extract actionable insights.

## Arguments

**None required** - Automatically analyzes the current conversation history and context.

**Optional**: Path to a completed task file
- If provided: Read that file as additional context alongside conversation history to improve gotcha identification quality
- If omitted: Rely on conversation history alone

## Process

Now that we are done with the task:
1. Review our conversation history. If a task file path was provided, read that file as additional context.
2. Identify up to 3 "Unknown Unknowns" or "Gotchas" we encountered (e.g., a library quirk, a missing permission, a tricky type error). Rank them by potential impact on future sessions — most impactful first.
3. For each gotcha not already in `./CLAUDE.md`, propose specific markdown content: describe the problem, the solution, and suggest where in CLAUDE.md to add it.

## Output Format

Format the output as a numbered list, one entry per proposed gotcha, ranked by impact (most impactful first):

```markdown
## PROPOSED CLAUDE.MD UPDATES

### 1. [Gotcha Title] *(highest impact)*
**Problem**: [What went wrong or was surprising]
**Solution**: [The fix or pattern to remember]
**Suggested location**: CLAUDE.md → [section path]

### 2. [Gotcha Title]
...

### 3. [Gotcha Title] *(lowest impact)*
...
```

Include only gotchas not already covered in CLAUDE.md. If fewer than 3 novel gotchas were found, include only those found.

## Examples

**Usage:**
```
/conducting-post-mortem
```

**Sample Output:**
```markdown
## PROPOSED CLAUDE.MD UPDATE

### Gotcha: Supabase Edge Functions Require Explicit CORS Headers

**Problem**: Edge functions were returning 200 but browser blocked responses due to missing CORS headers.

**Solution**: Always include in Edge Function responses:
```typescript
return new Response(JSON.stringify(data), {
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  },
})
```

**Where to Add**: CLAUDE.md → Supabase → Edge Functions section
```

## Error Handling

- **No CLAUDE.md**: WARN — still propose the update content, note that CLAUDE.md needs to be created first
- **No meaningful gotchas found**: Report "No novel gotchas identified in this session" and stop
