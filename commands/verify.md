---
description: VERIFY mode - Validate against original intent
argument-hint: <what-to-verify>
allowed-tools: Read, Glob, Grep, Bash
---

# /verify - 검증 모드

$ARGUMENTS 가 원래 의도대로 동작하는지 검증합니다.

---

## 에이전트 로드

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/verify.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/insight-chain/SKILL.md
```

---

## 실행

Use Task tool with:
- `subagent_type: general-purpose`
- `model: sonnet`
- 에이전트 시스템 프롬프트 포함
- Task: "$ARGUMENTS 검증"

---

## 출력

The Verdict 형식으로 출력:

```markdown
## Original Intent
[성공의 모습 - ORIENT에서 정의한 것]

## Verification

### Intent 1: [측면]
테스트: [...]
결과: [Pass/Fail]
증거: [...]

### Intent 2: [측면]
...

## Adversarial Tests
- [공격 시나리오]: [결과]

## Gaps Found
- [갭]: [심각도] - [해결 방안]

## Confidence
[High/Medium/Low] - [이유]

## Verdict
[Ship / Fix X first / Back to EXECUTE]
```

---

## 인사이트 생성

검증 결과에 따라:

성공 시:
```markdown
## Insight: [검증 완료]
Type: evidence
Confidence: high
Content: [무엇이 검증되었는지]
Source: [테스트 결과]
```

갭 발견 시:
```markdown
## Insight: [갭 제목]
Type: gap
Confidence: high
Content: [무엇이 부족한지]
Source: [어떻게 발견했는지]
```

---

## 후속 조치

- Critical 갭 → `/execute` 로 수정
- 의도 불일치 → `/orient` 로 재이해
- 모두 통과 → 완료
