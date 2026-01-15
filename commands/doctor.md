---
description: Diagnose imlazy plugin health and configuration
allowed-tools: Read, Glob, Bash
---

# /doctor - 플러그인 진단

imlazy 플러그인의 상태를 점검합니다.

---

## 진단 항목

### 1. 에이전트 파일 및 모델 확인

각 에이전트 파일을 읽어서 `model:` 필드를 확인:

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/orient.md
Read: ${CLAUDE_PLUGIN_ROOT}/agents/explore.md
Read: ${CLAUDE_PLUGIN_ROOT}/agents/theorize.md
Read: ${CLAUDE_PLUGIN_ROOT}/agents/execute.md
Read: ${CLAUDE_PLUGIN_ROOT}/agents/verify.md
```

기대값:
| Agent | Model | 역할 |
|-------|-------|------|
| orient | sonnet | 빠른 이해, 사용자 질문 |
| explore | haiku | 빠른 검색과 패턴 매칭 |
| theorize | opus | 깊은 추론 |
| execute | sonnet | 균형잡힌 구현 |
| verify | sonnet | 검증과 적대적 사고 |

---

### 2. 커맨드 파일 확인

필수 커맨드 파일 존재 여부:

```
Glob: ${CLAUDE_PLUGIN_ROOT}/commands/*.md
```

필수 목록:
- [ ] think.md (자동 플로우)
- [ ] orient.md
- [ ] explore.md
- [ ] theorize.md
- [ ] execute.md
- [ ] verify.md

---

### 3. 스킬 파일 확인

필수 스킬 존재 여부:

```
Glob: ${CLAUDE_PLUGIN_ROOT}/skills/*/SKILL.md
```

필수 목록:
- [ ] insight-chain/SKILL.md

---

### 4. 플러그인 설정 확인

```
Read: ${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json
```

확인 항목:
- name, version, description 존재 여부
- commands, agents 경로 설정

---

## 출력 형식

```markdown
## imlazy Doctor Report

### Agents & Models
| Agent | Status | Model |
|-------|--------|-------|
| orient | ✓ | sonnet |
| explore | ✓ | haiku |
| theorize | ✓ | opus |
| execute | ✓ | sonnet |
| verify | ✓ | sonnet |

### Commands
✓ think.md
✓ orient.md
✓ explore.md
✓ theorize.md
✓ execute.md
✓ verify.md

### Skills
✓ insight-chain/SKILL.md

### Plugin Config
✓ plugin.json valid

---

## Status: [HEALTHY / ISSUES FOUND]

[문제가 있다면 해결 방법 제안]
```

---

## 문제 해결 제안

발견된 문제에 따라 해결 방법 제시:

| 문제 | 해결 방법 |
|------|-----------|
| 에이전트 파일 없음 | 해당 파일 재생성 필요 |
| 커맨드 파일 없음 | 해당 파일 재생성 필요 |
| 스킬 파일 없음 | insight-chain 스킬 재생성 필요 |
| plugin.json 오류 | 설정 파일 검토 필요 |

---

## 실행

위 모든 항목을 순서대로 확인하고 결과를 보고합니다.
