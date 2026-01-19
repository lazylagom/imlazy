---
description: Manage imlazy 4-tier memory system
argument-hint: <search|store|recall|stats|prune> [args]
allowed-tools: Bash
---

# /imlazy:memory - 메모리 관리

imlazy 4중 메모리 시스템을 관리합니다.

---

## 사용법

### 메모리 검색

```bash
# 에피소드 메모리에서 유사한 문제 검색
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/memory-manager.py search episodic "검색어"

# 시맨틱 메모리에서 패턴 검색
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/memory-manager.py search semantic "패턴 키워드"

# 절차적 메모리에서 전략 검색
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/memory-manager.py search procedural "전략 키워드"

# 결과 제한
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/memory-manager.py search episodic "query" --limit 3
```

---

### 메모리 저장

```bash
# 시맨틱 지식 저장
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/memory-manager.py store semantic '{"pattern":"...", "context":"..."}' --tags pattern,domain

# 절차적 학습 저장
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/memory-manager.py store procedural '{"learning":"...", "situation":"..."}' --tags learning
```

**Note:** Episodic 메모리는 `/imlazy:think` 완료 시 자동으로 consolidate됩니다.

---

### 특정 메모리 조회

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/memory-manager.py recall <memory-id>
```

---

### 통계 확인

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/memory-manager.py stats
```

출력 예시:
```json
{
  "memory_home": "/Users/you/.imlazy",
  "types": {
    "working": {"count": 1, "size_human": "2.1 KB"},
    "episodic": {"count": 15, "size_human": "45.3 KB"},
    "semantic": {"count": 8, "size_human": "12.1 KB"},
    "procedural": {"count": 23, "size_human": "28.7 KB"}
  }
}
```

---

### 오래된 메모리 정리

```bash
# 30일 이상 접근 없는 메모리 정리
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/memory-manager.py prune --days 30
```

---

## 메모리 유형

| 유형 | 내용 | 예시 |
|------|------|------|
| **working** | 현재 에피소드 상태 | state.json |
| **episodic** | 과거 문제-해결 쌍 | "로그인 버그를 JWT 검증으로 해결" |
| **semantic** | 도메인 지식, 패턴 | "이 코드베이스는 Repository 패턴 사용" |
| **procedural** | 학습한 전략, 수정 | "null 체크 전에 항상 타입 확인" |

---

## 자동 저장

- **REFLECTOR**: 수정 사항 → procedural memory
- **CONSOLIDATOR**: 완료된 에피소드 → episodic memory
- **PLANNER**: 발견한 패턴 → semantic memory

---

## Arguments

```
$ARGUMENTS
```

위 명령어를 참고하여 적절한 메모리 작업을 수행하세요.
