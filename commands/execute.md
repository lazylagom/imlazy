---
description: EXECUTE mode - Incremental implementation with verification
argument-hint: <task-to-implement>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
---

# /execute - 점진적 실행 모드

$ARGUMENTS 를 작은 단위로 구현하고 즉시 검증합니다.

---

## 에이전트 로드

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/execute.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/insight-chain/SKILL.md
```

---

## 실행

Use Task tool with:
- `subagent_type: general-purpose`
- `model: sonnet`
- 에이전트 시스템 프롬프트 포함
- Task: "$ARGUMENTS 구현"

---

## 출력

The Trail 형식으로 출력:

```markdown
## Progress

### Step 1: [무엇을 했나]
결과: [성공/실패]
배운 것: [...]

### Step 2: [무엇을 했나]
결과: [성공/실패]
배운 것: [...]

## Current State
[현재 동작 상태]

## Next Step
[다음 할 일]

## Blocked? (해당시)
문제: [...]
가설: [...]
시도할 것: [...]
```

---

## 인사이트 생성

구현 완료 시 evidence 타입 인사이트:

```markdown
## Insight: [제목]
Type: evidence
Confidence: high
Content: [1-3문장 - 무엇이 동작하는지]
Source: [테스트 결과]
```

---

## 루프백 트리거

- 탐색 필요 → `/explore` 또는 EXPLORE 모드로 복귀
- 가설 재검토 필요 → `/theorize` 또는 THEORIZE 모드로 복귀
