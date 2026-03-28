#!/usr/bin/env bash
# Structural validator for a completed scientific-method research directory.
# Usage: ./validate-research.sh <problem-dir>
#
# Checks file existence, required sections, and structural invariants.
# Exit 0 = all checks pass, exit 1 = failures found.

set -euo pipefail

dir="${1:?Usage: validate-research.sh <problem-dir>}"
dir="${dir%/}"
fails=0

pass() { printf "  \033[32m✓\033[0m %s\n" "$1"; }
fail() { printf "  \033[31m✗\033[0m %s\n" "$1"; fails=$((fails + 1)); }
section_exists() { rg -q "^## $2" "$1" 2>/dev/null; }
heading() { printf "\n\033[1m%s\033[0m\n" "$1"; }

# --- problem.md ---
heading "problem.md"
if [[ -f "$dir/problem.md" ]]; then
  pass "exists"
  if rg -q "Novelty required: (yes|no)" "$dir/problem.md"; then
    pass "Novelty required is set (not TBD)"
  else
    fail "Novelty required is still TBD or missing"
  fi
  for sec in "Problem Statement" "Scope" "Success Criteria" "Background"; do
    if section_exists "$dir/problem.md" "$sec"; then
      pass "has ## $sec"
    else
      fail "missing ## $sec"
    fi
  done
else
  fail "problem.md not found"
fi

# --- hypothesis files ---
heading "Hypotheses"
hyp_files=("$dir"/hypothesis-*.md)
if [[ -e "${hyp_files[0]}" ]]; then
  count=${#hyp_files[@]}
  if [[ $count -ge 4 ]]; then
    pass "$count hypothesis files (>= 4 minimum)"
  else
    fail "$count hypothesis files (expected >= 4)"
  fi

  for f in "${hyp_files[@]}"; do
    name=$(basename "$f")
    # Required sections from generating-hypotheses
    for sec in "Status" "Statement" "Rationale"; do
      if section_exists "$f" "$sec"; then
        pass "$name: has ## $sec"
      else
        fail "$name: missing ## $sec"
      fi
    done

    # Status should not be 'pending' if pipeline completed
    status=$(rg -A1 "^## Status" "$f" 2>/dev/null | tail -1 | tr -d '[:space:]')
    if [[ "$status" == "pending" ]]; then
      fail "$name: status still pending (pipeline incomplete?)"
    else
      pass "$name: status = $status"
    fi
  done
else
  fail "no hypothesis-*.md files found"
fi

# --- references.md ---
heading "references.md"
if [[ -f "$dir/references.md" ]]; then
  pass "exists"
  ref_count=$(rg -c "^## REF-" "$dir/references.md" 2>/dev/null || echo 0)
  if [[ $ref_count -gt 0 ]]; then
    pass "$ref_count references indexed"
  else
    fail "no REF-NNN entries found"
  fi
else
  fail "references.md not found"
fi

# --- findings.md ---
heading "findings.md"
if [[ -f "$dir/findings.md" ]]; then
  pass "exists"
  for sec in "Outcome" "What was ruled out" "Open questions" "Publishability Assessment"; do
    if section_exists "$dir/findings.md" "$sec"; then
      pass "has ## $sec"
    else
      fail "missing ## $sec"
    fi
  done
else
  fail "findings.md not found"
fi

# --- article-abstract.md ---
heading "article-abstract.md"
if [[ -f "$dir/article-abstract.md" ]]; then
  pass "exists"
  for sec in "Background" "Methods" "Results" "Conclusions"; do
    if section_exists "$dir/article-abstract.md" "$sec"; then
      pass "has ## $sec"
    else
      fail "missing ## $sec"
    fi
  done
  # Word count check (200-350 target)
  wc=$(wc -w < "$dir/article-abstract.md")
  if [[ $wc -ge 100 && $wc -le 500 ]]; then
    pass "word count $wc (within tolerance)"
  else
    fail "word count $wc (expected ~200-350)"
  fi
else
  fail "article-abstract.md not found"
fi

# --- refinement addendum (only if multiple iterations) ---
heading "Refinement addenda"
addendum_count=$(rg -c "^## Refinement Addendum:" "$dir/problem.md" 2>/dev/null || echo 0)
pass "$addendum_count refinement addenda in problem.md"

# --- invariant checks ---
heading "Invariants"

# No TBD leftovers
if rg -q "TBD" "$dir/problem.md" 2>/dev/null; then
  fail "problem.md still contains TBD placeholder"
else
  pass "no TBD placeholders in problem.md"
fi

# Hypothesis numbering is sequential
if [[ -e "${hyp_files[0]}" ]]; then
  expected=1
  sequential=true
  for f in $(printf '%s\n' "${hyp_files[@]}" | sort); do
    num=$(basename "$f" | sed 's/hypothesis-0*//' | sed 's/\.md//')
    if [[ "$num" -ne "$expected" ]]; then
      sequential=false
      break
    fi
    expected=$((expected + 1))
  done
  if $sequential; then
    pass "hypothesis numbering is sequential"
  else
    fail "hypothesis numbering has gaps"
  fi
fi

# --- summary ---
printf "\n"
if [[ $fails -eq 0 ]]; then
  printf "\033[32mAll checks passed.\033[0m\n"
  exit 0
else
  printf "\033[31m%d check(s) failed.\033[0m\n" "$fails"
  exit 1
fi
