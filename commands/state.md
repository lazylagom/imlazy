---
description: View and manage imlazy cognitive state
argument-hint: [dump|get|set|transition|reset]
allowed-tools: Bash
---

# /imlazy:state - 상태 관리

imlazy CognitiveState를 조회하고 관리합니다.

---

## 사용법

### 전체 상태 조회

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py dump
```

---

### 특정 필드 조회

```bash
# 현재 노드
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py get current_node

# 문제 분석
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py get problem_reflection

# 중첩 필드
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py get problem_reflection.goal

# 테스트 결과
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py get test_results.anchor_tests

# 에러 로그
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py get error_log

# retry 횟수
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py get retry_count
```

---

### 값 설정

```bash
# 단순 값
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py set user_query "새 기능 추가"

# 중첩 값
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py set problem_reflection.goal "사용자 인증 구현"

# JSON 객체
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py set possible_solutions '[{"name":"A","approach":"JWT"},{"name":"B","approach":"Session"}]'
```

---

### 리스트에 추가

```bash
# 사고 추적에 추가
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py update thought_trace '{"type":"decision","content":"JWT 선택"}'

# 에러 로그에 추가
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py update error_log '{"type":"test_failure","test":"login_test"}'
```

---

### 노드 전환

```bash
# 유효한 노드: PLANNER, REASONER, CODER, VERIFIER, REFLECTOR, CONSOLIDATOR
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py transition REASONER
```

전환 시 자동으로 `thought_trace`에 기록됩니다.

---

### 상태 초기화

```bash
# 새 에피소드 시작
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py init

# 현재 프로젝트 컨텍스트 유지하며 리셋
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py reset
```

---

## 상태 스키마

```yaml
CognitiveState:
  # 태스크
  user_query: string
  problem_reflection:
    goal: string
    inputs: list
    outputs: list
    constraints: list
    edge_cases: list

  # 사고 과정
  current_plan: list
  thought_trace: list
  critiques: list
  possible_solutions: list
  selected_solution: string

  # 실행 컨텍스트
  file_context: dict
  test_results:
    public_tests: list
    ai_tests: list
    anchor_tests: list
  error_log: list

  # 사이클 제어
  current_node: string         # PLANNER|REASONER|CODER|VERIFIER|REFLECTOR|CONSOLIDATOR
  retry_count: int             # 0-3
  max_retries: 3

  # 메타
  episode_id: string
  project_hash: string
  created_at: string
  updated_at: string
```

---

## Arguments

```
$ARGUMENTS
```

위 명령어를 참고하여 적절한 상태 작업을 수행하세요.

기본 동작 (인수 없음): `dump` - 전체 상태 출력
