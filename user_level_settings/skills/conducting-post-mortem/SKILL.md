---
name: conducting-post-mortem
description: Extracts lessons from task and proposes CLAUDE.md updates
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

## Process

Now that we are done with the task:
1. Review our conversation history.
2. Identify ONE "Unknown Unknown" or "Gotcha" we encountered (e.g., a library quirk, a missing permission, a tricky type error).
3. If this "Gotcha" is not already in `./CLAUDE.md`, generate a specific update to prevent this in the future.

## Output Format

Format the output as:
```markdown
## PROPOSED CLAUDE.MD UPDATE
[The Markdown content to add]
```

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
