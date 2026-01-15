# imlazy

> **Stay Lazy, Think Crazy**

개발자처럼 사고하는 인지 모드 기반 에이전트 시스템. Claude Code 플러그인.

## 핵심 철학

기존 SDLC 워터폴 방식 대신 **개발자의 실제 사고 패턴**을 반영:

- **가설-검증 루프**: 추측하고, 테스트하고, 수정
- **점진적 이해**: 필요한 만큼만 탐색
- **적응형 플로우**: 상황에 따라 단계 스킵/반복

## Installation

```bash
claude --plugin-dir /path/to/imlazy
```

## Commands

### 자동 플로우
| Command | Description |
|---------|-------------|
| `/imlazy:think <task>` | 적응형 인지 워크플로우 (권장) |

### 개별 모드
| Command | Description | Model |
|---------|-------------|-------|
| `/imlazy:orient <task>` | 문제 이해, 가설 형성 | Sonnet |
| `/imlazy:explore <area>` | 점진적 코드 탐색 | Haiku |
| `/imlazy:theorize <goal>` | 해결책 가설 수립 | Opus |
| `/imlazy:execute <task>` | 단계별 구현 + 검증 | Sonnet |
| `/imlazy:verify <what>` | 원래 의도와 비교 검증 | Sonnet |

## 인지 모드 시스템

```
ORIENT → EXPLORE → THEORIZE → EXECUTE → VERIFY
   ↑         ↑         ↑         ↑         ↓
   └─────────┴─────────┴─────────┴─────────┘
           (언제든 루프백 가능)
```

### ORIENT (이해)
- "사용자가 진짜 원하는 게 뭐지?"
- 가설 형성, 성공의 모습 정의
- Critical Unknown 식별

### EXPLORE (탐색)
- 필요한 만큼만 점진적 탐색
- 패턴 발견 시 멈춤
- 전체 분석 X, 충분한 이해 O

### THEORIZE (가설)
- "X를 하면 Y가 될 것이다"
- Minimal Viable Test 정의
- 실패 시 대안 준비

### EXECUTE (실행)
- 한 번에 하나, 바로 확인
- 에러 = 정보 (무시 X)
- 막히면 이전 모드로 복귀

### VERIFY (검증)
- ORIENT의 "성공 모습"과 비교
- 적대적 테스트 (깨뜨리기 시도)
- Gap 발견 시 EXECUTE로 복귀

## 인사이트 체인

모드 간 **간결한 인사이트**로 맥락 전달:

```markdown
## Insight: 세션 기반 인증 적합
Type: hypothesis
Confidence: medium
Content: JWT보다 세션이 단순. express-session 설치됨.
Source: EXPLORE에서 package.json 확인
```

- 인사이트당 최대 3문장
- 상세 문서 X, 핵심만 O

## 사용 예시

```
# 자동 플로우 (권장)
/imlazy:think 사용자 인증 추가

# 탐색만 필요할 때
/imlazy:explore src/auth

# 가설 수립만
/imlazy:theorize 캐싱 전략

# 구현 + 검증
/imlazy:execute passport.js 미들웨어 추가
/imlazy:verify 인증 기능
```

## 플로우 예시

### 단순 버그 수정
```
ORIENT → EXPLORE → EXECUTE → VERIFY
(THEORIZE 스킵 - 원인 명확)
```

### 복잡 기능 추가
```
ORIENT → EXPLORE → THEORIZE → EXECUTE(실패)
  → EXPLORE(추가 탐색) → THEORIZE(수정)
  → EXECUTE → VERIFY
```

## Project Structure

```
imlazy/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── think.md          # 자동 적응형 플로우
│   ├── orient.md          # 개별 모드
│   ├── explore.md
│   ├── theorize.md
│   ├── execute.md
│   └── verify.md
├── agents/
│   ├── orient.md          # 이해 에이전트
│   ├── explore.md         # 탐색 에이전트
│   ├── theorize.md        # 가설 에이전트
│   ├── execute.md         # 실행 에이전트
│   └── verify.md          # 검증 에이전트
├── skills/
│   └── insight-chain/     # 인사이트 체인 시스템
└── hooks/
    └── ...
```

## vs 기존 SDLC 워크플로우

| 기존 | 새로운 |
|------|--------|
| 고정 5단계 순차 실행 | 적응형 루프백/스킵 |
| 템플릿 채우기 | 실제 사고 과정 |
| 상세 문서 전달 | 간결한 인사이트 |
| FR-1, NFR-1 번호 매기기 | 가설과 증거 |

## License

MIT
