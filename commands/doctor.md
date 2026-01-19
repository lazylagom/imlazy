---
description: Diagnose imlazy plugin health and configuration
allowed-tools: Read, Glob, Bash
---

# /imlazy:doctor - 플러그인 진단

imlazy 플러그인의 상태를 점검합니다.

---

## 진단 항목

### 1. 에이전트 파일 및 모델 확인

각 에이전트 파일을 읽어서 `model:` 필드를 확인:

```
Read: ${CLAUDE_PLUGIN_ROOT}/agents/planner.md
Read: ${CLAUDE_PLUGIN_ROOT}/agents/reasoner.md
Read: ${CLAUDE_PLUGIN_ROOT}/agents/coder.md
Read: ${CLAUDE_PLUGIN_ROOT}/agents/verifier.md
Read: ${CLAUDE_PLUGIN_ROOT}/agents/reflector.md
Read: ${CLAUDE_PLUGIN_ROOT}/agents/consolidator.md
```

기대값:
| Agent | Model | 역할 |
|-------|-------|------|
| planner | sonnet | 메모리 검색 + AlphaCodium 전처리 |
| reasoner | opus | Tree of Thoughts 심층 사고 |
| coder | sonnet | 코드 작성 + Anchoring |
| verifier | haiku | 테스트 실행 |
| reflector | opus | Reflexion 자기 수정 |
| consolidator | haiku | 메모리 통합 |

---

### 2. 커맨드 파일 확인

필수 커맨드 파일 존재 여부:

```
Glob: ${CLAUDE_PLUGIN_ROOT}/commands/*.md
```

필수 목록:
- [ ] think.md (메인 오케스트레이션)
- [ ] memory.md (메모리 관리)
- [ ] state.md (상태 확인)
- [ ] doctor.md (헬스 체크)

---

### 3. 스킬 파일 확인

필수 스킬 존재 여부:

```
Glob: ${CLAUDE_PLUGIN_ROOT}/skills/*/SKILL.md
```

필수 목록:
- [ ] cognitive-state/SKILL.md
- [ ] memory-system/SKILL.md
- [ ] alphacodium-flow/SKILL.md

---

### 4. 훅 스크립트 확인

```
Glob: ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/*.py
Glob: ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/*.sh
```

필수 목록:
- [ ] state-manager.py
- [ ] memory-manager.py
- [ ] reflection-trigger.py
- [ ] bash-validator.py
- [ ] file-protector.py
- [ ] init-session.sh
- [ ] auto-formatter.sh

---

### 5. 메모리 디렉토리 확인

```bash
ls -la ~/.imlazy/
```

필수 디렉토리:
- [ ] ~/.imlazy/working/
- [ ] ~/.imlazy/episodic/
- [ ] ~/.imlazy/semantic/
- [ ] ~/.imlazy/procedural/

---

### 6. 플러그인 설정 확인

```
Read: ${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json
```

확인 항목:
- name: "imlazy"
- version 존재
- description 존재

---

### 7. 상태 관리자 테스트

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py init
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/state-manager.py dump
```

---

### 8. 메모리 관리자 테스트

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/memory-manager.py stats
```

---

## 출력 형식

```markdown
## imlazy Doctor Report

### Agents & Models
| Agent | Status | Model |
|-------|--------|-------|
| planner | ✓ | sonnet |
| reasoner | ✓ | opus |
| coder | ✓ | sonnet |
| verifier | ✓ | haiku |
| reflector | ✓ | opus |
| consolidator | ✓ | haiku |

### Commands
✓ think.md
✓ memory.md
✓ state.md
✓ doctor.md

### Skills
✓ cognitive-state/SKILL.md
✓ memory-system/SKILL.md
✓ alphacodium-flow/SKILL.md

### Hooks
✓ state-manager.py
✓ memory-manager.py
✓ reflection-trigger.py

### Memory System
✓ ~/.imlazy/ directories exist
✓ state-manager.py functional
✓ memory-manager.py functional

### Plugin Config
✓ plugin.json valid

---

## Status: [HEALTHY / ISSUES FOUND]

[문제가 있다면 해결 방법 제안]
```

---

## 문제 해결 제안

| 문제 | 해결 방법 |
|------|-----------|
| 에이전트 파일 없음 | 해당 파일 재생성 필요 |
| 커맨드 파일 없음 | 해당 파일 재생성 필요 |
| 스킬 파일 없음 | 해당 스킬 재생성 필요 |
| 메모리 디렉토리 없음 | `state-manager.py init` 실행 |
| 스크립트 오류 | Python 3 설치 확인, 권한 확인 |
| plugin.json 오류 | 설정 파일 검토 필요 |

---

## 실행

위 모든 항목을 순서대로 확인하고 결과를 보고합니다.
