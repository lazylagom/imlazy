# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

imlazy is a Claude Code plugin implementing an "Adaptive Cognitive Workflow System" - a developer-centric approach that mirrors how developers actually think (hypothesis-verification loops) rather than traditional SDLC waterfall methods.

**Core philosophy:** "Stay Lazy, Think Crazy" - Guess → Test → Fix, with adaptive phase skipping/looping based on context.

## Plugin Structure

```
.claude-plugin/plugin.json    # Plugin manifest
commands/                     # Slash commands (think.md is main entry)
agents/                       # Agent system prompts with YAML frontmatter
skills/insight-chain/         # Context-passing system between modes
hooks/                        # Automation hooks (safety + formatting)
```

## Development Commands

This is a Claude Code plugin (Markdown + YAML), not a buildable project. No npm/build steps.

**Testing the plugin locally:**
```bash
claude --plugin-dir /path/to/imlazy
```

**Verify plugin health:**
```
/imlazy:doctor
```

## Architecture: Five-Mode Cognitive Workflow

```
ORIENT → EXPLORE → THEORIZE → EXECUTE → VERIFY
   ↑         ↑         ↑         ↑         ↓
   └─────────┴─────────┴─────────┴─────────┘
           (Adaptive loopback)
```

| Mode | Purpose | Model | Key Output |
|------|---------|-------|------------|
| ORIENT | Understand problem, form hypotheses | Sonnet | "The Compass" |
| EXPLORE | Progressive codebase exploration | Haiku | "Map Fragment" |
| THEORIZE | Solution hypothesis + MVT plan | Opus | "The Theory" |
| EXECUTE | Incremental implementation | Sonnet | "Trail" |
| VERIFY | Validate against original intent | Sonnet | "Verdict" |

**Adaptive behaviors:**
- Simple bugs: Skip THEORIZE (cause is obvious)
- Blocked in EXECUTE: Loop back to EXPLORE or THEORIZE
- Misunderstood requirements: Loop back to ORIENT

## Insight Chain System

Lightweight context passing between modes using structured insights:

```markdown
## Insight: [Title]
Type: [understanding|discovery|hypothesis|evidence|gap]
Confidence: [high|medium|low]
Content: [1-3 sentences - essence only]
Source: [where this came from]
```

**Rules:**
- 1-3 insights per mode (more = not essential)
- 1-3 sentences per insight (longer = documentation, not insight)
- Source always required
- Consolidate when chain exceeds 10 insights

## Agent File Format

Each agent is Markdown with YAML frontmatter:

```yaml
---
name: agent-name
description: |
  Multi-line description with examples
model: sonnet|haiku|opus
color: terminal-color
tools: ["Read", "Grep", "Glob", ...]
---
```

## Key Anti-Patterns to Avoid

When modifying this plugin, avoid:
- FR-1, NFR-1 numbered requirements
- Comprehensive design documents before coding
- "Codebase Overview" sections
- Template-filling exercises
- Fixed 5-step sequential workflows

**Instead, embrace:**
- Hypothesis-first thinking
- Minimal Viable Tests (MVT)
- Progressive understanding ("enough" ≠ "complete")
- Error-as-information mindset
- Adaptive phase skipping/looping

## Hooks System

Configured in `hooks/hooks.json`:

| Hook | Trigger | Script |
|------|---------|--------|
| SessionStart | Plugin loads | init-session.sh |
| PreToolUse (Bash) | Before commands | bash-validator.py (blocks dangerous commands) |
| PreToolUse (Edit/Write) | Before file edits | file-protector.py (protects .env, *.lock) |
| PostToolUse (Edit/Write) | After file edits | auto-formatter.sh (prettier/black) |
