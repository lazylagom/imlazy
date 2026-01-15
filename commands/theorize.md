---
description: THEORIZE mode - Form solution hypothesis with test plan
argument-hint: <problem-or-goal>
allowed-tools: Read, Glob, Grep, Write
---

# /theorize - 가설 수립 모드

$ARGUMENTS 에 대한 해결책 가설을 수립하고 검증 계획을 세웁니다.

---

## 에이전트 로드

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/theorize.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/insight-chain/SKILL.md
```

---

## 실행

Use Task tool with:
- `subagent_type: general-purpose`
- `model: opus`
- 에이전트 시스템 프롬프트 포함
- Task: "$ARGUMENTS 에 대한 가설 수립"

---

## 출력

The Theory 형식으로 출력:

```markdown
## Hypothesis
[한 문단: 무엇을 어떻게 할 것인지]

## Why This Should Work
- Evidence: [코드베이스 근거]
- Pattern: [알려진 패턴]
- Logic: [논리적 추론]

## Riskiest Assumption
[가장 위험한 가정]
→ Test by: [검증 방법]

## Minimal Viable Test
목표: [MVT 목표]
단계:
1. [...]
2. [...]
3. [확인 방법]

## If Hypothesis Fails
- Alternative A: [...]
- Alternative B: [...]
```

---

## 인사이트 생성

1개 hypothesis 타입 인사이트 생성:

```markdown
## Insight: [제목]
Type: hypothesis
Confidence: [high/medium/low]
Content: [1-3문장]
Source: [추론 근거]
```
