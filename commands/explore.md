---
description: EXPLORE mode - Progressive codebase exploration
argument-hint: <area-or-keyword>
allowed-tools: Read, Glob, Grep, Bash
---

# /explore - 점진적 탐색 모드

$ARGUMENTS 관련 코드를 점진적으로 탐색합니다.

---

## 에이전트 로드

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/explore.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/insight-chain/SKILL.md
```

---

## 실행

Use Task tool with:
- `subagent_type: general-purpose`
- `model: haiku`
- 에이전트 시스템 프롬프트 포함
- Task: "$ARGUMENTS 관련 코드 탐색"

---

## 출력

The Map Fragment 형식으로 출력:

```markdown
## Explored
시작점: [file:line] - [이유]

## Discoveries
- [패턴/발견]: [설명]

## Mental Model
[2-3문장 요약]

## Integration Points
- 연결할 곳: [file:function]
- 수정할 곳: [file:function]

## Intentionally Unexplored
- [영역] - [이유]
```

---

## 인사이트 생성

1-3개 discovery 타입 인사이트 생성:

```markdown
## Insight: [제목]
Type: discovery
Confidence: [high/medium/low]
Content: [1-3문장]
Source: [file:line 또는 패턴]
```
