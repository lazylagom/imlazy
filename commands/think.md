---
description: Adaptive cognitive workflow - thinks like a developer
argument-hint: <task-description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite, AskUserQuestion
---

# /think - 개발자처럼 사고하기

$ARGUMENTS 태스크를 개발자의 사고 방식으로 해결합니다.

---

## 인지 모드 시스템

```
ORIENT → EXPLORE → THEORIZE → EXECUTE → VERIFY
   ↑         ↑         ↑         ↑         ↓
   └─────────┴─────────┴─────────┴─────────┘
           (언제든 루프백 가능)
```

---

## 핵심 자료

```
Read: ${CLAUDE_PLUGIN_ROOT}/skills/insight-chain/SKILL.md
```

인사이트 체인을 사용하여 모드 간 맥락을 전달합니다.

---

## 플로우 실행

**중요: 각 모드 시작 시 반드시 아래 형식으로 현재 모드를 표시하라:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧭 ORIENT 모드 (sonnet)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Phase 1: ORIENT (이해)

**먼저 출력:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧭 ORIENT 모드 (sonnet)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/orient.md
```

Use Task tool with:
- `subagent_type: general-purpose`
- `model: sonnet`
- 에이전트 시스템 프롬프트 + 인사이트 체인 스킬 포함
- Task: "$ARGUMENTS"

**ORIENT 완료 후 결정:**
- 태스크가 명확하고 단순한가? → EXPLORE로
- 더 명확히 해야 할 것이 있나? → AskUserQuestion 사용
- Critical Unknown이 있나? → 먼저 해결

---

### Phase 2: EXPLORE (탐색)

**먼저 출력:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 EXPLORE 모드 (haiku)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/explore.md
```

Use Task tool with:
- `subagent_type: general-purpose`
- `model: haiku`
- 에이전트 시스템 프롬프트 + 이전 인사이트 포함
- Task: ORIENT 인사이트 기반 탐색

**EXPLORE 완료 후 결정:**
- 패턴을 발견했나? → THEORIZE로
- 더 탐색이 필요한가? → EXPLORE 계속
- 해결책이 명확한가? → THEORIZE 스킵하고 EXECUTE로

---

### Phase 3: THEORIZE (가설)

**먼저 출력:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 THEORIZE 모드 (opus)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/theorize.md
```

Use Task tool with:
- `subagent_type: general-purpose`
- `model: opus`
- 에이전트 시스템 프롬프트 + 이전 인사이트 포함
- Task: ORIENT + EXPLORE 인사이트 기반 가설 수립

**THEORIZE 완료 후:**
- Minimal Viable Test 정의됨 → EXECUTE로
- 가설에 확신이 없다면 → EXPLORE로 복귀하여 더 탐색

**스킵 조건:**
- 단순 버그 수정: 원인이 명확하면 바로 EXECUTE
- 작은 변경: 패턴이 명확하면 바로 EXECUTE

---

### Phase 4: EXECUTE (실행)

**먼저 출력:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ EXECUTE 모드 (sonnet)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/execute.md
```

Use Task tool with:
- `subagent_type: general-purpose`
- `model: sonnet`
- 에이전트 시스템 프롬프트 + 이전 인사이트 포함
- Task: THEORIZE의 가설 또는 직접 구현

**EXECUTE 중 결정:**
- 단계별 성공 → 계속 진행
- 에러 발생 → 분석 후 수정 또는 백트랙
- 막힘 → EXPLORE 또는 THEORIZE로 복귀

**루프백 트리거:**
- "이 부분이 어떻게 동작하는지 모르겠다" → EXPLORE
- "내 접근 방식이 틀린 것 같다" → THEORIZE
- "요구사항을 잘못 이해한 것 같다" → ORIENT

---

### Phase 5: VERIFY (검증)

**먼저 출력:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ VERIFY 모드 (sonnet)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/verify.md
```

Use Task tool with:
- `subagent_type: general-purpose`
- `model: sonnet`
- 에이전트 시스템 프롬프트 + 전체 인사이트 체인 포함
- Task: ORIENT의 성공 기준과 비교 검증

**VERIFY 완료 후:**
- 모든 의도 충족 + Critical 갭 없음 → 완료
- Critical 갭 발견 → EXECUTE로 복귀
- 의도 자체가 잘못됨 → ORIENT로 복귀

---

## 적응형 플로우 예시

### 단순 버그 수정
```
ORIENT: "로그인 안 됨" → 가설: 최근 변경 관련
EXPLORE: git log + 관련 코드 추적 → 원인 발견
EXECUTE: 수정 + 테스트 (THEORIZE 스킵)
VERIFY: 로그인 동작 확인
```

### 복잡한 기능 추가
```
ORIENT: 요구사항 이해 + 가설 형성
EXPLORE: 관련 코드 탐색 + 패턴 발견
THEORIZE: 가설 수립 + MVT 정의
EXECUTE: 구현 시도 → 실패
  → EXPLORE 복귀: 더 탐색 필요
  → THEORIZE 복귀: 새 가설
EXECUTE: 재시도 → 성공
VERIFY: 전체 검증
```

---

## 인사이트 체인 관리

각 모드 완료 시:
1. 1-3개 핵심 인사이트 생성
2. 이전 인사이트와 통합
3. 다음 모드에 전달

인사이트 체인이 10개 초과 시:
- 통합 인사이트로 압축
- 핵심만 유지

---

## 완료 조건

- [ ] ORIENT의 "성공의 모습" 달성
- [ ] VERIFY에서 Critical 갭 없음
- [ ] 사용자 의도 충족 확인

---

## 요약 출력

모든 모드 완료 후:

```markdown
## 결과 요약

### 이해 (ORIENT)
[핵심 인사이트 요약]

### 발견 (EXPLORE)
[핵심 발견 요약]

### 가설 (THEORIZE)
[선택한 접근 방식]

### 구현 (EXECUTE)
[구현 내용 요약]

### 검증 (VERIFY)
[검증 결과 + 남은 갭]

### 인사이트 체인
[전체 인사이트 목록]
```
