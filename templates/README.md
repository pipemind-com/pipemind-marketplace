# Agentic Workflow Templates

This directory contains template files used by the `bootstrap-agentic.sh` script to set up the agentic workflow in new projects.

## Files

### Task System Templates

- **`tasks-TEMPLATE.md`**: Template for creating new task files. Copied to `tasks/TEMPLATE.md` during bootstrap.
  - Defines the structure planners use when creating tasks
  - Includes sections for: Planner (requirements, analysis, implementation), Builder (implementation notes), Status

- **`tasks-README.md`**: Documentation for the task file system. Copied to `tasks/README.md` during bootstrap.
  - Explains task naming conventions, lifecycle, and responsibilities
  - Documents planner vs builder roles
  - Provides quality standards

- **`tasks-000-example-task.md`**: Placeholder example task. Copied to `tasks/000-example-task.md` during bootstrap.
  - Serves as a reference example until real tasks are completed
  - Should be replaced with a real example from the first completed task

## Usage

These templates are automatically copied by the bootstrap script:

```bash
./bootstrap-agentic.sh
```

The script will:
1. Create the `tasks/` directory structure
2. Copy these templates to their respective locations
3. Generate agent definitions using Claude Code

## Customization

To customize the agentic workflow for a specific project:

1. **Edit templates here** before running the bootstrap script
2. Modify the structure, sections, or examples to match your project needs
3. Run the bootstrap script to apply your customized templates

## Version Control

These templates should be:
- ✅ Committed to version control (they define the workflow structure)
- ✅ Shared across projects (ensures consistency)
- ✅ Updated when workflow improvements are discovered

The bootstrap script is designed to be portable - copy the entire `templates/` directory and `bootstrap-agentic.sh` to new projects.
