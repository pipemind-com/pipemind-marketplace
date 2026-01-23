#!/bin/bash
# bootstrap-agentic.sh
# One-command setup for complete agentic workflow (planner + builder + task system)
# Usage: ./bootstrap-agentic.sh

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                            ║${NC}"
echo -e "${CYAN}║           🤖  AGENTIC WORKFLOW BOOTSTRAP  🚀              ║${NC}"
echo -e "${CYAN}║                                                            ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if in git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Not in a git repository. Run 'git init' first.${NC}"
    exit 1
fi

# Check if Claude CLI is available
if ! command -v claude &> /dev/null; then
    echo -e "${YELLOW}⚠️  Claude CLI not found. Install from: https://github.com/anthropics/claude-code${NC}"
    exit 1
fi

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Phase 1: Creating Directory Structure${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Create directory structure
mkdir -p tasks/backlog tasks/completed .claude/agents

echo -e "${GREEN}✓${NC} Created tasks/, tasks/backlog/, tasks/completed/"
echo -e "${GREEN}✓${NC} Created .claude/agents/"

# Create .gitkeep files
touch tasks/backlog/.gitkeep tasks/completed/.gitkeep

echo -e "${GREEN}✓${NC} Created .gitkeep files"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Phase 2: Copying Task System Templates${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEMPLATE_DIR="$SCRIPT_DIR/templates"

# Check if template directory exists
if [ ! -d "$TEMPLATE_DIR" ]; then
    echo -e "${YELLOW}⚠️  Template directory not found at: $TEMPLATE_DIR${NC}"
    echo -e "${YELLOW}    Looking for:${NC}"
    echo -e "${YELLOW}      - templates/tasks-TEMPLATE.md${NC}"
    echo -e "${YELLOW}      - templates/tasks-README.md${NC}"
    echo -e "${YELLOW}      - templates/tasks-000-example-task.md${NC}"
    echo ""
    echo -e "${YELLOW}    Please ensure templates/ directory exists with the required files.${NC}"
    exit 1
fi

# Copy template files
if [ -f "$TEMPLATE_DIR/tasks-TEMPLATE.md" ]; then
    cp "$TEMPLATE_DIR/tasks-TEMPLATE.md" tasks/TEMPLATE.md
    echo -e "${GREEN}✓${NC} Copied tasks/TEMPLATE.md"
else
    echo -e "${YELLOW}⚠️  Missing: templates/tasks-TEMPLATE.md${NC}"
    exit 1
fi

if [ -f "$TEMPLATE_DIR/tasks-README.md" ]; then
    cp "$TEMPLATE_DIR/tasks-README.md" tasks/README.md
    echo -e "${GREEN}✓${NC} Copied tasks/README.md"
else
    echo -e "${YELLOW}⚠️  Missing: templates/tasks-README.md${NC}"
    exit 1
fi

if [ -f "$TEMPLATE_DIR/tasks-000-example-task.md" ]; then
    cp "$TEMPLATE_DIR/tasks-000-example-task.md" tasks/000-example-task.md
    echo -e "${GREEN}✓${NC} Copied tasks/000-example-task.md (placeholder)"
else
    echo -e "${YELLOW}⚠️  Missing: templates/tasks-000-example-task.md${NC}"
    exit 1
fi
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Phase 3: Generating Architecture Documentation (Claude)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${CYAN}Running: claude --agent agent-author /creating-claude-settings...${NC}"
echo ""

claude --agent agent-author -p "/creating-claude-settings"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} CLAUDE.md created"
else
    echo -e "${YELLOW}⚠️  CLAUDE.md generation had issues. Review manually.${NC}"
fi
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Phase 4: Generating Planner Agent (Claude)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${CYAN}Running: claude --agent agent-author /creating-planner-agent...${NC}"
echo ""

claude --agent agent-author -p "/creating-planner-agent"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} .claude/agents/planner.md created"
else
    echo -e "${YELLOW}⚠️  planner.md generation had issues. Review manually.${NC}"
fi
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Phase 5: Generating Builder Agent (Claude)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${CYAN}Running: claude --agent agent-author /creating-builder-agent...${NC}"
echo ""

claude --agent agent-author -p "/creating-builder-agent"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} .claude/agents/builder.md created"
else
    echo -e "${YELLOW}⚠️  builder.md generation had issues. Review manually.${NC}"
fi
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Phase 6: Validating Setup (Claude)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${CYAN}Running: claude (validation check)...${NC}"
echo ""

claude --prompt "Validate the agentic setup by checking all files that were just created:

1. **CLAUDE.md completeness**:
   - [ ] Development commands present
   - [ ] Architecture overview with clear layers
   - [ ] Data flow diagrams for key workflows
   - [ ] Integration points documented
   - [ ] Key patterns with code examples
   - [ ] Anti-patterns table exists
   - [ ] Deployment strategy with order explained
   - [ ] Testing strategy for each layer
   - [ ] Common gotchas with examples

2. **Task system** (directory structure):
   - [ ] tasks/ directory exists
   - [ ] tasks/backlog/ exists
   - [ ] tasks/completed/ exists
   - [ ] TEMPLATE.md has all required sections (Planner, Builder, Status)
   - [ ] README.md explains naming, lifecycle, responsibilities
   - [ ] Example task (000-example-task.md) exists

3. **Planner agent** (.claude/agents/planner.md):
   - [ ] YAML frontmatter with name, description, tools, model
   - [ ] Mission statement emphasizes task files as primary output
   - [ ] Workflow is clear (read CLAUDE.md → analyze → explore → design → write)
   - [ ] \"Before Creating Task\" section lists REQUIRED preparation steps
   - [ ] Task file requirements are comprehensive and specific
   - [ ] Quality standards include good/bad examples with code
   - [ ] \"After Creating Task\" includes verification checklist
   - [ ] Optimal detail level examples (too little / too much / just right)
   - [ ] References TEMPLATE.md and CLAUDE.md appropriately

4. **Builder agent** (.claude/agents/builder.md):
   - [ ] YAML frontmatter with name, description, tools, model
   - [ ] Scope covers all relevant tech stacks/layers
   - [ ] Coding guidelines reference CLAUDE.md patterns
   - [ ] Architecture pattern explanation with code examples
   - [ ] Task workflow clearly documented (0-7 steps)
   - [ ] \"When Invoked\" section includes proactive testing (step 3)
   - [ ] Task completion includes updating Builder section (step 7)
   - [ ] Testing standards include code examples for each layer
   - [ ] Task completion checklist is comprehensive
   - [ ] References tasks/ and TEMPLATE.md appropriately

5. **Integration** (cross-references):
   - [ ] Planner references CLAUDE.md for architecture understanding
   - [ ] Builder references CLAUDE.md for coding patterns
   - [ ] Planner references TEMPLATE.md for task structure
   - [ ] Builder references TEMPLATE.md for task completion
   - [ ] Planner and Builder have clear, non-overlapping responsibilities
   - [ ] Task system (TEMPLATE.md) aligns with both agent definitions

6. **Quality checks**:
   - [ ] All files use consistent terminology
   - [ ] Code examples are complete and realistic
   - [ ] Instructions are actionable (not vague)
   - [ ] Workflow steps are numbered and sequential
   - [ ] Checklists are comprehensive
   - [ ] Anti-patterns are clearly marked with ❌ and ✅

Output a validation report with:
- ✅ for items that are complete and high-quality
- ⚠️ for items that exist but need improvement (explain what's missing)
- ❌ for missing items (explain what needs to be added)

Provide specific, actionable recommendations for any issues found.

If major issues are found, offer to fix them."

echo ""

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅  AGENTIC WORKFLOW BOOTSTRAP COMPLETE!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${CYAN}Files created:${NC}"
echo "  📁 tasks/"
echo "     ├── TEMPLATE.md"
echo "     ├── README.md"
echo "     ├── 000-example-task.md"
echo "     ├── backlog/"
echo "     └── completed/"
echo "  📁 .claude/agents/"
echo "     ├── planner.md"
echo "     └── builder.md"
echo "  📄 CLAUDE.md"
echo ""
echo -e "${CYAN}Next steps:${NC}"
echo "  1. Review the generated files (especially validation report above)"
echo "  2. Customize for project-specific needs if needed"
echo "  3. Test planner: ${BLUE}claude --agent planner -p 'Create a task for <feature>'${NC}"
echo "  4. Test builder: ${BLUE}claude --agent builder -p 'Implement task 001'${NC}"
echo ""
echo -e "${YELLOW}Tip:${NC} The validation report above will identify any gaps or improvements needed."
echo ""
