# Insight Chain: 맥락 전달 시스템

## 개요

Insight Chain은 모드 간 맥락을 전달하는 경량 시스템입니다. 상세한 문서 대신 **핵심 인사이트**만 전달합니다.

## 왜 인사이트인가?

### 기존 문제
```
ORIENT → "Requirements Analysis" 문서 (50줄)
  ↓
CODE ANALYST → 앞 문서 파싱 + 자기 문서 (80줄)
  ↓
ARCHITECT → 앞 문서들 파싱 + 자기 문서 (100줄)
  ↓
... 맥락 폭발, 핵심 정보 희석
```

### 인사이트 접근
```
ORIENT → 3개 인사이트 (핵심만)
  ↓
EXPLORE → 2개 인사이트 추가
  ↓
THEORIZE → 1개 가설 인사이트
  ↓
... 맥락 유지, 핵심 보존
```

## 인사이트 형식

```markdown
## Insight: [짧은 제목]
Type: [understanding | discovery | hypothesis | evidence | gap]
Confidence: [high | medium | low]
Content: [1-3문장 - 핵심만]
Source: [어디서 이 인사이트가 나왔나]
```

### Type 설명

| Type | 의미 | 예시 |
|------|------|------|
| understanding | 문제/요구사항 이해 | "사용자는 간단한 팀용 인증을 원함" |
| discovery | 코드베이스 발견 | "이 프로젝트는 미들웨어 패턴 사용" |
| hypothesis | 해결책 가설 | "세션 기반 인증이 JWT보다 적합" |
| evidence | 검증된 사실 | "보호 라우트 테스트 통과" |
| gap | 발견된 격차 | "토큰 만료 처리 미구현" |
| loopback | 모드 복귀 결정 | "API 구조 재탐색 필요 → EXPLORE" |
| escalation | 진행 불가, 사용자 결정 필요 | "환경 설정 문제로 실행 불가" |

### Confidence 기준

| Confidence | 기준 |
|------------|------|
| high | 코드로 확인됨 / 사용자가 명시함 |
| medium | 패턴에서 추론됨 / 합리적 가정 |
| low | 추측 / 더 확인 필요 |

## 예시: 인증 기능 추가

### ORIENT 생성
```markdown
## Insight: 팀 내부 도구용 간단한 인증
Type: understanding
Confidence: high
Content: 사용자는 외부 노출 없는 팀 도구에 기본 인증이 필요. OAuth 불필요.
Source: 사용자 "내부 팀 도구에 간단한 로그인"

## Insight: 성공 = 비인가 접근 차단
Type: understanding
Confidence: high
Content: 로그인 없이 접근 시 401, 로그인 후 접근 허용이 핵심 요구사항.
Source: 사용자 "권한 없는 사람이 못 들어오게"
```

### EXPLORE 추가
```markdown
## Insight: Express 미들웨어 패턴 사용
Type: discovery
Confidence: high
Content: 프로젝트는 express 미들웨어로 cross-cutting concern 처리. logger, cors 미들웨어 존재.
Source: middleware/logger.ts, app.ts:15-20

## Insight: express-session 이미 설치됨
Type: discovery
Confidence: high
Content: package.json에 express-session 존재. 세션 기반 인증 인프라 준비됨.
Source: package.json dependencies
```

### THEORIZE 추가
```markdown
## Insight: Passport.js 로컬 전략 적합
Type: hypothesis
Confidence: medium
Content: passport-local로 username/password 인증 구현. 기존 미들웨어 패턴과 호환.
Source: EXPLORE 발견 + passport.js 일반 패턴
```

### EXECUTE 추가
```markdown
## Insight: 기본 인증 플로우 동작 확인
Type: evidence
Confidence: high
Content: /login POST → 세션 생성, /protected GET → 인증 시 200/미인증 시 401.
Source: curl 테스트 결과
```

### VERIFY 추가
```markdown
## Insight: 토큰 만료 처리 미구현
Type: gap
Confidence: high
Content: 세션 만료 후 재로그인 유도 로직 없음. UX 개선 필요하나 보안상 문제는 아님.
Source: 세션 만료 시나리오 테스트
```

## Loopback 기록

모드 간 복귀(loopback) 발생 시 반드시 기록:

```markdown
## Insight: [복귀 이유 요약]
Type: loopback
From: [현재 모드]
To: [복귀할 모드]
Reason: [왜 복귀하는지 1-2문장]
What_Changed: [기존 가설/이해에서 무엇이 달라지는지]
Attempt: [몇 번째 시도인지 - 예: 1st, 2nd]
```

### Loopback 예시

```markdown
## Insight: API 응답 구조 불일치로 재탐색 필요
Type: loopback
From: EXECUTE
To: EXPLORE
Reason: API가 배열이 아닌 객체를 반환. 문서와 실제 동작 불일치.
What_Changed: 기존 "배열 순회" 가설 폐기, 객체 키 접근 방식 탐색
Attempt: 1st
```

**Loopback 인사이트의 가치:**
- 같은 실수 반복 방지
- 어떤 가설이 왜 폐기됐는지 추적
- 다음 유사 문제에서 참고

---

## 체인 규칙

### 생성 규칙
1. **모드당 1-3개 인사이트** - 더 많으면 핵심이 아님
2. **인사이트당 1-3문장** - 더 길면 문서화하고 있는 것
3. **Source 필수** - 근거 없는 인사이트는 추측
4. **Loopback 시 필수 기록** - 복귀 이유 없이 모드 전환 금지

### 소비 규칙
1. **전체 체인 읽기** - 이전 모든 인사이트 확인
2. **충돌 확인** - 새 발견이 기존 인사이트와 모순되면 수정
3. **참조 가능** - "ORIENT에서 정의한 성공 기준에 따르면..."

### 통합 규칙 (10개 초과 시)
```markdown
## Consolidated Insight: [통합 제목]
Type: consolidated
Content: [여러 인사이트 요약]
Covers: [통합된 인사이트 제목들]
```

## 인사이트 vs 문서

| 상황 | 인사이트 | 문서 |
|------|----------|------|
| 다음 모드에 전달 | ✓ | ✗ |
| 나중에 참고 | ✗ | ✓ |
| 핵심 결정사항 | ✓ | ✗ |
| 상세 구현 내용 | ✗ | ✓ |

인사이트는 **결정과 발견**을, 문서는 **상세 내용**을 담는다.

## Anti-patterns

- "## Insight: Code Analysis" → 섹션 제목이 아님
- 10줄 넘는 Content → 문서로 분리
- Source 없는 인사이트 → 추측일 가능성
- 모든 것을 인사이트로 → 핵심 희석

---

## 세션 간 전달 (Persistence)

인사이트 체인은 세션 간에도 유지됩니다. `~/.imlazy/insight-chain.md` 파일에 자동 저장됩니다.

### 스크립트 사용

```bash
# 현재 인사이트 체인 불러오기
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/insight-manager.sh load

# 인사이트 체인 저장하기
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/insight-manager.sh save "내용"

# 인사이트 추가하기
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/insight-manager.sh append "## Insight: 새 인사이트"

# 체인 상태 확인 (개수, 통합 필요 여부)
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/insight-manager.sh health

# 체인 초기화 (히스토리에 백업 후)
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/insight-manager.sh clear
```

### 자동 관리 규칙

1. **모드 시작 시**: 기존 체인 자동 로드
2. **모드 종료 시**: 새 인사이트 자동 저장
3. **7개 초과 시**: "approaching-limit" 경고
4. **10개 초과 시**: "consolidation-needed" 경고 → 통합 필수

### 개별 명령어 사용 시

`/imlazy:orient` → `/imlazy:explore` 처럼 개별 명령어를 순차 실행할 때:

```
/imlazy:orient "인증 추가"
→ 인사이트 생성됨 (자동 저장)

/imlazy:explore "인증 코드 탐색"
→ 이전 인사이트 자동 로드 + 새 인사이트 추가
```

수동으로 체인을 관리하려면:

```
/imlazy:insight health   # 상태 확인
/imlazy:insight clear    # 새 태스크 시작 전 초기화
```

### 히스토리

모든 인사이트 체인은 `~/.imlazy/insight-history/`에 타임스탬프와 함께 백업됩니다.
과거 의사결정을 추적하거나 참조할 때 유용합니다.
