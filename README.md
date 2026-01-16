# imlazy

> **Stay Lazy, Think Crazy**

A cognitive mode-based agent system that thinks like a developer. Claude Code plugin.

## Core Philosophy

Instead of traditional SDLC waterfall approaches, this reflects **how developers actually think**:

- **Hypothesis-Verification Loop**: Guess, test, fix
- **Progressive Understanding**: Explore only as much as needed
- **Adaptive Flow**: Skip/repeat phases based on context

## Installation

### Marketplace (Recommended)

In Claude Code:
```
# Add marketplace
/plugin marketplace add lazylagom/lazy-marketplace

# Install plugin
/plugin install imlazy
```

### Verify Installation

In Claude Code:
```
# List installed plugins
/plugin list
```

## Commands

### Automatic Flow
| Command | Description |
|---------|-------------|
| `/imlazy:think <task>` | Adaptive cognitive workflow (recommended) |

### Individual Modes
| Command | Description | Model |
|---------|-------------|-------|
| `/imlazy:orient <task>` | Understand problem, form hypotheses | Sonnet |
| `/imlazy:explore <area>` | Progressive code exploration | Haiku |
| `/imlazy:theorize <goal>` | Establish solution hypothesis | Opus |
| `/imlazy:execute <task>` | Step-by-step implementation + verification | Sonnet |
| `/imlazy:verify <what>` | Validate against original intent | Sonnet |

## Cognitive Mode System

```
ORIENT → EXPLORE → THEORIZE → EXECUTE → VERIFY
   ↑         ↑         ↑         ↑         ↓
   └─────────┴─────────┴─────────┴─────────┘
           (Loop back anytime)
```

### ORIENT (Understand)
- "What does the user really want?"
- Form hypotheses, define what success looks like
- Identify Critical Unknowns

### EXPLORE (Search)
- Progressive exploration, only as much as needed
- Stop when patterns are found
- Not complete analysis, but sufficient understanding

### THEORIZE (Hypothesize)
- "If I do X, Y will happen"
- Define Minimal Viable Test
- Prepare alternatives for failure

### EXECUTE (Implement)
- One at a time, verify immediately
- Error = Information (don't ignore)
- Return to previous mode when blocked

### VERIFY (Validate)
- Compare against ORIENT's "success definition"
- Adversarial testing (try to break it)
- Return to EXECUTE when gaps are found

## Insight Chain

Pass context between modes with **concise insights**:

```markdown
## Insight: Session-based auth is suitable
Type: hypothesis
Confidence: medium
Content: Sessions are simpler than JWT. express-session is installed.
Source: Checked package.json in EXPLORE
```

- Maximum 3 sentences per insight
- Not detailed docs, just the essentials

## Usage Examples

```
# Automatic flow (recommended)
/imlazy:think add user authentication

# When only exploration is needed
/imlazy:explore src/auth

# Just hypothesis building
/imlazy:theorize caching strategy

# Implementation + verification
/imlazy:execute add passport.js middleware
/imlazy:verify authentication feature
```

## Flow Examples

### Simple Bug Fix
```
ORIENT → EXPLORE → EXECUTE → VERIFY
(Skip THEORIZE - cause is obvious)
```

### Complex Feature Addition
```
ORIENT → EXPLORE → THEORIZE → EXECUTE(fail)
  → EXPLORE(additional search) → THEORIZE(revise)
  → EXECUTE → VERIFY
```

## Project Structure

```
imlazy/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── think.md          # Automatic adaptive flow
│   ├── orient.md          # Individual modes
│   ├── explore.md
│   ├── theorize.md
│   ├── execute.md
│   └── verify.md
├── agents/
│   ├── orient.md          # Understanding agent
│   ├── explore.md         # Exploration agent
│   ├── theorize.md        # Hypothesis agent
│   ├── execute.md         # Execution agent
│   └── verify.md          # Verification agent
├── skills/
│   └── insight-chain/     # Insight chain system
└── hooks/
    ├── hooks.json         # Hook configuration
    └── scripts/
        ├── auto-formatter.sh   # Auto-format on file save
        ├── bash-validator.py   # Block dangerous commands
        └── file-protector.py   # Protect sensitive files
```

## Hooks

Automated safety mechanisms:

| Hook | Trigger | Description |
|------|---------|-------------|
| **auto-formatter** | PostToolUse | Auto-run prettier/black |
| **bash-validator** | PreToolUse | Block `rm -rf /`, `git push -f` |
| **file-protector** | PreToolUse | Block editing `.env`, `*.lock` |

## vs Traditional SDLC Workflow

| Traditional | New |
|-------------|-----|
| Fixed 5-step sequential execution | Adaptive loopback/skip |
| Template filling | Actual thought process |
| Detailed document handoff | Concise insights |
| FR-1, NFR-1 numbering | Hypotheses and evidence |

## License

MIT
