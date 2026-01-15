---
description: ORIENT mode - Understand the problem and form hypotheses
argument-hint: <task-or-problem>
allowed-tools: Read, Glob, Grep, AskUserQuestion
---

# /orient - 문제 이해 모드

$ARGUMENTS 에 대해 본질을 파악하고 가설을 형성합니다.

---

## 에이전트 로드

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/orient.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/insight-chain/SKILL.md
```

---

## 실행

Use Task tool with:
- `subagent_type: general-purpose`
- `model: sonnet`
- 에이전트 시스템 프롬프트 포함
- Task: "$ARGUMENTS"

---

## 출력

The Compass 형식으로 출력:

```markdown
## Understanding
사용자가 말한 것: [...]
내가 이해한 것: [...]
성공의 모습: [...]

## Hypotheses
H1: [...] - [근거]
H2: [...] - [근거]

## Critical Unknowns
- [...] → [확인 방법]

## Next
[다음 할 일]
```

---

## 인사이트 생성

1-3개 understanding 타입 인사이트 생성:

```markdown
## Insight: [제목]
Type: understanding
Confidence: [high/medium/low]
Content: [1-3문장]
Source: [근거]
```
