---
description: Manage insight chain - health check, clear, view
argument-hint: <health|clear|view|consolidate>
allowed-tools: Bash, Read
---

# /insight - 인사이트 체인 관리

$ARGUMENTS 작업을 수행합니다.

---

## 사용법

```
/imlazy:insight health      # 체인 상태 확인
/imlazy:insight view        # 현재 체인 내용 보기
/imlazy:insight clear       # 새 태스크 시작 전 초기화
/imlazy:insight consolidate # 10개 초과 시 통합
```

---

## 명령 실행

### health (기본값)

```bash
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/insight-manager.sh health
```

출력 결과를 해석하여 사용자에게 알려줘:
- `status: empty` → "인사이트 체인이 비어 있습니다. /think 또는 개별 모드 명령어로 시작하세요."
- `status: active` + `count: N` → "현재 N개의 인사이트가 있습니다."
- `warning: approaching-limit` → "⚠️ 인사이트가 7개를 초과했습니다. 곧 통합이 필요합니다."
- `warning: consolidation-needed` → "🔴 인사이트가 10개를 초과했습니다. `/imlazy:insight consolidate`로 통합하세요."

---

### view

```bash
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/insight-manager.sh load
```

내용이 있으면 마크다운으로 보여주고, 없으면 "인사이트 체인이 비어 있습니다."

---

### clear

```bash
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/insight-manager.sh clear
```

출력:
```
✅ 인사이트 체인을 초기화했습니다.
백업 위치: ~/.imlazy/insight-history/
```

---

### consolidate

인사이트 체인을 통합합니다:

1. 현재 체인 로드
```bash
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/insight-manager.sh load
```

2. 통합 인사이트 생성:
```markdown
## Consolidated Insight: [핵심 요약]
Type: consolidated
Content: [여러 인사이트를 2-3문장으로 요약]
Covers: [통합된 인사이트 제목들 나열]
Preserved:
  - [유지해야 할 개별 인사이트 1]
  - [유지해야 할 개별 인사이트 2]
```

통합 기준:
- **같은 Type의 인사이트**: 하나로 합침
- **high confidence**: 우선 보존
- **gap 타입**: 개별 유지 (해결 추적 필요)
- **최신 evidence**: 우선 보존

3. 저장
```bash
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/insight-manager.sh save "[통합된 내용]"
```

---

## 인수 없이 실행 시

`/imlazy:insight` 만 실행하면 `health`를 실행합니다.
