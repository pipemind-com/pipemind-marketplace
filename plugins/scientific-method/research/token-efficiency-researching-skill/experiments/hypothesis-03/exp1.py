"""
Experiment 1: Manual Redundancy Audit of All Eight SKILL.md Files
Hypothesis 03: Can SKILL.md files be reduced 40% without behavioral drift?

Counts word counts per file and categorizes structural redundancy.
"""
import os
import re

SKILLS_DIR = os.path.expanduser(
    "~/.claude-equine/plugins/marketplaces/pipemind-marketplace"
    "/plugins/scientific-method/skills"
)
SKILLS = [
    "designing-experiments",
    "drawing-conclusions",
    "generating-hypotheses",
    "refining-hypothesis",
    "refining-problem",
    "researching",
    "researching-literature",
    "running-experiments",
]

def wc(text):
    return len(text.split())

files = {}
for skill in SKILLS:
    path = os.path.join(SKILLS_DIR, skill, "SKILL.md")
    with open(path) as f:
        files[skill] = f.read()

print("=== WORD COUNTS PER FILE ===")
total_words = 0
for skill in SKILLS:
    w = wc(files[skill])
    total_words += w
    print(f"  {skill}: {w} words")
print(f"  TOTAL: {total_words} words")
print()

print("=== TEMPLATE BLOCK WORD COUNTS ===")
for skill in SKILLS:
    blocks = re.findall(r"```[\s\S]*?```", files[skill])
    template_words = sum(wc(b) for b in blocks)
    print(f"  {skill}: {len(blocks)} blocks, {template_words} words")
print()

# -------------------------------------------------------
# Redundancy categories with estimated removable words
# -------------------------------------------------------
redundancy_items = [
    # Category A: Repeated template examples
    ("A1", "drawing-conclusions", "Two Conclusion templates sharing ~99 words of structure (unified = save ~84w)", 84),
    ("A2", "refining-hypothesis", "Two near-identical Task prompt templates (17+26 words, save ~17w)", 17),
    ("A3", "designing-experiments", "Experiment template Experiment 2 placeholder padding (~20w)", 20),
    ("A4", "researching", "article-abstract.md template verbose field descriptions (~40w saveable)", 40),
    # Category B: Restated guiding principles
    ("B1", "multiple (7 skills)", "Step 0 idempotency rationale repeated (10w per file × 7 = 70w)", 70),
    ("B2", "running-experiments", "Guiding Principles section (184w) collapsible to imperatives, save ~80w", 80),
    ("B3", "drawing-conclusions", "Outcome definitions (confirmed/refuted/inconclusive) ~195w verbose, save ~80w", 80),
    ("B4", "researching", "CRITICAL note (56w) → ~20w, save ~36w", 36),
    ("B5", "refining-problem", "CRITICAL autonomous note (48w) → ~20w, save ~28w", 28),
    ("B6", "generating-hypotheses", "Quality check sub-section (32w) restates criteria above, save ~22w", 22),
    # Category C: Verbose workflow descriptions
    ("C1", "researching", "Publishability Assessment Content (143w) over-specified, save ~71w", 71),
    ("C2", "researching-literature", "MCP vs WebSearch branching text (45w) collapsible, save ~15w", 15),
    ("C3", "researching-literature", "WebSearch path (181w) mirrors MCP path, save ~60w", 60),
    # Category D: Duplicated format specs
    ("D1", "multiple (3 skills)", '"Use Edit to append -- never overwrite" repeated 3×, save ~20w', 20),
]

print("=== REDUNDANCY INVENTORY ===")
total_removable = 0
for item in redundancy_items:
    rid, skill, desc, removable = item
    print(f"  [{rid}] {skill}")
    print(f"        {desc}")
    print(f"        Removable: {removable} words")
    total_removable += removable

print()
print("=== COMPRESSIBILITY RESULT ===")
ratio = total_removable / total_words
threshold = 0.40
print(f"  Total removable words: {total_removable}")
print(f"  Total words:           {total_words}")
print(f"  Compressibility ratio: {ratio:.1%}")
print(f"  40% threshold requires: {int(total_words * 0.40)} removable words")
print()
if ratio >= threshold:
    print("  RESULT: Hypothesis SUPPORTED — structural redundancy >= 40%")
else:
    print(f"  RESULT: Hypothesis REFUTED — structural redundancy is {ratio:.1%}, well below 40% threshold")
    print(f"  Gap: {int(total_words * 0.40) - total_removable} additional words would need to be removable to reach 40%")
