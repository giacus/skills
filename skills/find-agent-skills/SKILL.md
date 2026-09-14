---
name: find-agent-skills
description: Find and compare installable agent skills when the user requests skill discovery or an identified capability gap needs it. Do not divert ordinary how-to or implementation requests into discovery when available capabilities suffice.
---

# Find Agent Skills

This skill helps you discover and install skills from the open agent skills ecosystem.

## When to Use This Skill

Use for explicit requests to find, compare, or install skills, or when a concrete
capability gap calls for discovery. First consider capabilities already available
for an ordinary task. Skill discovery alone does not authorize installation or
execution of the underlying workflow.

## What is the Skills CLI?

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands:**

- `npx skills find [query] [--owner <owner>]` - Search for skills interactively or by keyword, optionally scoped to a GitHub owner
- `npx skills add <package>` - Install a skill from GitHub or other sources
- `npx skills update` - Update all installed skills

**Browse skills at:** https://skills.sh/

## How to Help Users Find Skills

### Step 1: Understand What They Need

Once discovery is warranted, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

### Optional discovery sources

Use a targeted CLI search, a known relevant source, or the [skills.sh directory](https://skills.sh/) as appropriate. Popularity can help discovery but does not establish quality or safety.

### Step 2: Search for Skills

For keyword discovery, run:

```bash
npx skills find [query] [--owner <owner>]
```

For example:

- User asks "find a skill for React performance" → `npx skills find react performance`
- User asks "find a PR review skill" → `npx skills find pr review`
- User asks "find a changelog skill" → `npx skills find changelog`

### Step 3: Verify Quality Before Recommending

**Do not recommend a skill based solely on search results.** Always verify:

1. **Fit** — inspect activation boundaries and the actual workflow.
2. **Provenance and maintenance** — identify the source, revision, license, and update history.
3. **Behavior** — review referenced instructions, scripts, dependencies, and requested access before recommending installation. Stars or install counts are context, not proof of trustworthiness.

### Step 4: Present Options to the User

When you find relevant skills, present them to the user with:

1. The skill name and what it does
2. The verified source and relevant limitations
3. The install command they can run
4. A link to learn more at skills.sh

Example response:

```
I found a skill that might help! The "react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.

To install it:
npx skills add vercel-labs/agent-skills@react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### Step 5: Install When Authorized

When installation is requested or already authorized, install the selected, reviewed skill without asking again. For discovery-only requests, present options before installation:

```bash
npx skills add <owner/repo@skill> -g -y
```

The `-g` flag installs globally (user-level) and `-y` skips confirmation prompts.

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`

## When No Skills Are Found

If no relevant skill exists, report the gap. When the underlying task was
already requested and available capabilities can handle it, continue that task
without asking again. If the user requested discovery only, report the result
and possible alternatives without expanding into unrequested implementation.
