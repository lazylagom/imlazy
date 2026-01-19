---
description: imlazy cognitive workflow - cyclic agent orchestration
argument-hint: <task-description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite, AskUserQuestion
---

# /imlazy:think - Cognitive Agent Loop Architecture

$ARGUMENTS 태스크를 imlazy 인지 워크플로우로 해결합니다.

---

## 아키텍처

```
                    ┌──────────────────────────────────────────┐
                    │                                          │
                    ▼                                          │
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ PLANNER │───▶│ REASONER│───▶│  CODER  │───▶│VERIFIER │───▶│REFLECTOR│
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
   (sonnet)      (opus)        (sonnet)       (haiku)        (opus)
                                                  │
                                                  ▼
                                            ┌───────────┐
                                            │CONSOLIDATOR│
                                            └───────────┘
                                               (haiku)
```

---

## Step 1: 상태 초기화

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py init
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py set user_query "$ARGUMENTS"
```

---

## Step 2: PLANNER 노드

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 PLANNER 노드 (sonnet)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**에이전트 로드:**
```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/planner.md
```

Use Task tool:
- `subagent_type: general-purpose`
- `model: sonnet`
- 에이전트 시스템 프롬프트 포함
- Task: 메모리 검색 + 문제 분석 + 해결책 생성

**PLANNER 출력 확인:**
- `problem_reflection` 작성됨
- `possible_solutions` 2-3개 생성
- `selected_solution` 선택됨

**전환:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py transition REASONER
```

---

## Step 3: REASONER 노드

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 REASONER 노드 (opus)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**에이전트 로드:**
```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/reasoner.md
```

Use Task tool:
- `subagent_type: general-purpose`
- `model: opus`
- 에이전트 시스템 프롬프트 + 현재 상태 포함
- Task: Tree of Thoughts + 구현 계획 수립

**REASONER 출력 확인:**
- `thought_trace`에 ToT 기록
- `current_plan` 상세 계획 작성됨

**전환:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py transition CODER
```

**스킵 조건:**
- 단순 버그 수정 (원인 명확)
- 패턴 기반 변경 (이미 검증됨)

---

## Step 4: CODER 노드

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ CODER 노드 (sonnet)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**에이전트 로드:**
```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/coder.md
```

Use Task tool:
- `subagent_type: general-purpose`
- `model: sonnet`
- 에이전트 시스템 프롬프트 + 현재 상태 포함
- Task: 코드 구현 + Anchor Test 관리

**CODER 핵심 규칙:**
1. Anchor test 실패 시 즉시 revert
2. 새 테스트 통과 시 anchor에 추가
3. 점진적 구현 (한 번에 많이 바꾸지 않음)

**전환:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py transition VERIFIER
```

---

## Step 5: VERIFIER 노드

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ VERIFIER 노드 (haiku)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**에이전트 로드:**
```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/verifier.md
```

Use Task tool:
- `subagent_type: general-purpose`
- `model: haiku`
- 에이전트 시스템 프롬프트 포함
- Task: 전체 테스트 실행 + 결과 수집

**VERIFIER 판정:**
- **PASS**: → CONSOLIDATOR로 전환
- **FAIL**: → REFLECTOR로 전환

```bash
# On PASS
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py transition CONSOLIDATOR

# On FAIL
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py transition REFLECTOR
```

---

## Step 6a: REFLECTOR 노드 (실패 시)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 REFLECTOR 노드 (opus)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**에이전트 로드:**
```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/reflector.md
```

Use Task tool:
- `subagent_type: general-purpose`
- `model: opus`
- 에이전트 시스템 프롬프트 + 에러 로그 포함
- Task: 5 Whys 분석 + 자기 비판 + 수정 제안

**REFLECTOR 라우팅:**

```bash
# 상태 확인
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py get retry_count
```

| 상황 | 라우팅 |
|------|--------|
| 단순 코드 버그 | → CODER |
| 계획 수정 필요 | → REASONER |
| 문제 재분석 필요 | → PLANNER |
| retry_count >= 3 | → 사용자 에스컬레이션 |

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py transition [TARGET_NODE]
```

**루프백 후:**
Step 2, 3, 또는 4로 돌아가서 해당 노드부터 재실행.

---

## Step 6b: CONSOLIDATOR 노드 (성공 시)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 CONSOLIDATOR 노드 (haiku)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**에이전트 로드:**
```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/consolidator.md
```

Use Task tool:
- `subagent_type: general-purpose`
- `model: haiku`
- Task: 메모리 통합 + 에피소드 아카이브

**CONSOLIDATOR 작업:**
```bash
# 에피소드 저장
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/memory-manager.py consolidate
```

---

## 완료 출력

```markdown
## imlazy Episode Complete

### 문제
$ARGUMENTS

### 해결책
[selected_solution 요약]

### 구현
[변경된 파일 목록]
[주요 변경 사항]

### 테스트
- Public: X/Y passed
- AI Tests: X/Y passed
- Anchor Tests: X/Y passed

### 인지 경로
PLANNER → REASONER → CODER → VERIFIER → CONSOLIDATOR
[실제 경로 + retry 횟수]

### 학습
[procedural memory에 저장된 주요 학습]

### Episode ID
[episode_id]
```

---

## 플로우 제어 규칙

### Retry 정책
- `max_retries: 3`
- 각 REFLECTOR 방문 시 `retry_count++`
- 초과 시 사용자에게 에스컬레이션

### Anchor Test 불변성
- 통과한 테스트는 anchor가 됨
- Anchor 실패 시 반드시 revert
- Anchor는 절대 제거하지 않음

### 노드 스킵
- REASONER: 단순 버그, 명확한 패턴
- 다른 노드는 스킵 불가

### 라우팅 우선순위
1. Anchor violation → REFLECTOR (무조건)
2. Test failure → REFLECTOR
3. Success → CONSOLIDATOR
4. retry_count >= 3 → User escalation

---

## 상태 확인

언제든 현재 상태 확인:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py dump
```
