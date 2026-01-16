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

## 이전 인사이트 로드

기존 인사이트 체인 로드 (ORIENT + EXPLORE + THEORIZE 결과 포함):
```bash
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/insight-manager.sh load
```

**THEORIZE 인사이트에서 MVT_Definition을 확인하라.** 이것을 먼저 검증해야 한다.

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

## MVT 검증 (필수)

**전체 구현 전에 MVT(Minimal Viable Test)를 먼저 검증하라.**

THEORIZE 인사이트의 `MVT_Definition`을 찾아서:
1. 해당 항목만 최소한으로 구현
2. 즉시 테스트
3. 결과 기록

```markdown
## MVT Checkpoint
Definition: [THEORIZE에서 정의한 MVT]
Status: [✓ Passed | ✗ Failed]
Result: [무엇이 확인되었나]
Next: [전체 구현 진행 | 가설 재검토]
```

**MVT 실패 시**: 전체 구현 진행하지 말고 THEORIZE로 복귀하여 가설 재검토.

---

## 인사이트 생성

구현 완료 시 evidence 타입 인사이트:

```markdown
## Insight: [제목]
Type: evidence
Confidence: high
Content: [1-3문장 - 무엇이 동작하는지]
Source: [테스트 결과]
MVT_Status: [✓ Passed | ✗ Failed]
```

---

## 인사이트 저장

생성한 인사이트를 체인에 추가:
```bash
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/insight-manager.sh append "[새 인사이트]"
```

상태 확인:
```bash
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/insight-manager.sh health
```

---

## 루프백 트리거

- 탐색 필요 → `/explore` 또는 EXPLORE 모드로 복귀
- 가설 재검토 필요 → `/theorize` 또는 THEORIZE 모드로 복귀
- MVT 실패 → THEORIZE 모드로 복귀
