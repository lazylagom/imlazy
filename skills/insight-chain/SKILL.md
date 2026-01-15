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

## 체인 규칙

### 생성 규칙
1. **모드당 1-3개 인사이트** - 더 많으면 핵심이 아님
2. **인사이트당 1-3문장** - 더 길면 문서화하고 있는 것
3. **Source 필수** - 근거 없는 인사이트는 추측

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
