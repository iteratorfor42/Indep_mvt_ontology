# v8 추가 검증 보고서 (ver3)

## — 49개 항목 Source Mapping 1차 검증 및 Provenance Layer 설계 보고서

> **버전 이력**: ver1(초기 v8 RDF 구조검증) → ver2(49개 항목 URL 팩트체크 초안) → **ver3(피드백 반영, Claim/Evidence/Source 분리, 상태값 이원화, 변경이력 보존 구조 도입)**

---

# 0. ver2 → ver3 변경 요약

ver2에 대한 검토 피드백을 반영해 다음을 수정했다.

| No | 변경 내용 | 근거 |
|---|---|---|
| 1 | 제목을 「49개 항목 출처 URL 팩트체크」에서 「49개 항목 Source Mapping 1차 검증 및 Provenance Layer 설계 보고서」로 변경 | "49개 전체를 직접 팩트체크했다"는 오해를 방지하기 위함 |
| 2 | 판정 용어를 확인/부분확인/재확인/보류 → **직접검증 / 부분검증 / URL재확인필요 / 관계보류 / 출처충돌**로 재정리 | 판정 기준을 더 명확히 구분하기 위함 |
| 3 | Source와 Evidence를 분리 (같은 URL 안에서도 문장 단위 근거를 별도 관리) | 하나의 페이지가 여러 Claim의 근거가 되는 경우를 구분하기 위함 |
| 4 | `claim_status`와 `date_status`를 분리 | "관계는 확실하지만 날짜는 불확실"한 경우(예: 이동휘)를 표현하기 위함 |
| 5 | `hasEestimation`(날짜 추정 여부)과 `hasValidationStatus`(주장 자체의 검증 여부)를 분리 | "언제인가"와 "사실인가"는 서로 다른 질문이기 때문 |
| 6 | 오산학교·조선물산장려회에 **변경이력(변경 전/후 값과 사유)**을 provenance에 보존 | 값을 낮추면서 근거를 함께 남기기 위함 |
| 7 | 49개 항목을 항목 단위가 아니라 **Claim 단위**로 분해하는 원칙과 예시(홍범도) 추가 | 한 인물/조직 안에 여러 개별 주장이 섞여 있는 문제를 해소하기 위함 |
| 8 | Negative Evidence의 표현 범위를 "자료 범위 내 미확인"으로 제한 | "없었다"로 과잉 해석되는 것을 방지하기 위함 |
| 9 | Source Mapping CSV 컬럼에 `evidence_id`, `claim_status`, `date_status`, `change_history` 추가 | Provenance Layer를 실제로 감사(audit) 가능하게 만들기 위함 |
| 10 | 문서 말미에 v9 작업 순서(로드맵)를 명시 | "새 RDF부터 만든다"가 아니라 "Claim 분해 → Source Mapping CSV 완성"이 우선임을 명시하기 위함 |

---

# 1. 검증 목적

v8 RDF와 CSV의 각 사실을 다시 출처까지 역추적해 다음 구조를 확립하고자 했다.

> **개체/사건 → 주장(Claim) → 근거(Evidence) → 출처(Source) → 관계(Relation) → 날짜(Date)**

ver2에서는 Source와 Evidence를 사실상 하나로 취급했으나, ver3에서는 이를 분리했다. 같은 페이지(Source) 안에서도 서로 다른 문장(Evidence)이 서로 다른 Claim을 뒷받침할 수 있기 때문이다.

```text
Source:
한국민족문화대백과사전 「보성사」

Evidence E-001: "1919년 2월 27일..."
Evidence E-002: "사장 이종일..."
Evidence E-003: "독립선언서를 인쇄..."

CLM-039-01 → E-002  (이종일이 보성사를 경영했다)
CLM-039-02 → E-003  (이종일이 독립선언서 인쇄를 주도했다)
CLM-039-03 → E-001  (해당 사건의 시점은 1919년 2월이다)
```

이렇게 만들어야 나중에 누군가 "왜 이 트리플이 존재하는가"를 물었을 때 **RDF → Claim → Evidence → Source** 순으로 즉시 추적할 수 있다.

---

# 2. 전체 평가 (ver3 기준 재정리)

| 영역 | 판단 | 비고 |
|---|---|---|
| v8 RDF 구조 검증 | **완료** | rdflib 기준 구조적 무결성 확인 |
| 49개 항목 출처 목록화 | **상당 부분 완료** | 36건가량 실제 URL 제시, 13건 미제시 |
| URL 자체의 실재성 | **대체로 양호** | 한국민족문화대백과사전·우리역사넷 URL이 구체적으로 제시됨 |
| URL → 주장 직접 검증 | **부분 완료** | 일부는 항목 전체를 근거로 삼아 개별 주장과 1:1 대응이 안 됨 |
| 날짜 검증 | **중요한 문제 발견** | 오산학교·조선물산장려회가 대표적 |
| 관계 검증 | **부분 완료** | 설립·소속·참여·경영 등 관계별 근거 분리가 필요 |
| Provenance 설계 | **v9 기본모델로 채택 가능** | Source/Evidence 분리, claim_status/date_status 이원화 반영 |
| 49개 항목 1:1 Source Mapping | **미완료 — v9 최우선 과제** | 13개는 URL 미제시, 나머지도 Claim 단위 매핑 필요 |

이 문서의 성격은 다음과 같이 재정의한다.

> **"v8 추가 검증을 통해 Source Mapping의 필요성과 핵심 충돌을 발견했고, Provenance Layer의 설계안(Source/Evidence 분리, claim_status/date_status 이원화)을 확정한 1차 검증 보고서."**

---

# 3. 핵심 사례 1 — 이승훈 → 오산학교 (변경이력 보존형)

### 기존 값 (ver1 CSV)

```text
이승훈 → 설립 → 오산학교
date = 1907-12-24
status = confirmed
```

### 확인된 출처

* 「오산고등학교」(한국민족문화대백과사전) → 1907년 12월
* 「오산 학교」(우리역사넷) → 1907년 12월
* 「이승훈」(한국민족문화대백과사전) → 1907년 11월 24일

문제는 "날짜를 못 찾았다"가 아니라 **서로 다른 공식 자료가 서로 다른 정밀도·값을 제시**한다는 점이었다.

### ver3 provenance 기록 (변경이력 포함)

```text
Claim: 이승훈이 오산학교를 설립했다
Relation: 설립
Object: 오산학교

Evidence A (Source: 오산고등학교) → "1907년 12월"
Evidence B (Source: 우리역사넷 오산 학교) → "1907년 12월"
Evidence C (Source: 이승훈) → "1907년 11월 24일"

change_history:
  old_value = 1907-12-24
  old_status = confirmed
  new_value = 1907-12
  new_precision = Month
  reason = "학교 관련 자료 2건은 12월을 지지하나, 인물 항목은 11월 24일을 제시하여 day 단위 확정 근거 부족"

claim_status = confirmed        # "이승훈이 오산학교를 설립했다"는 사실 자체는 확실
date_status  = conflicting_sources   # 정확한 날짜는 출처 간 충돌
```

`1907-12`도 "모든 자료가 12월로 합의했다"는 의미의 확정값이 아니라, **출처 충돌이 보존된 상태의 최선값**임을 명시한다.

`1907-12-24`를 되살리려면 그 날짜를 직접 명시하는 별도의 1차·공식 자료 URL을 추가 확보해야 한다는 원칙은 ver2와 동일하게 유지한다.

---

# 4. 핵심 사례 2 — 조선물산장려회 (변경이력 보존형)

### 기존 값

```text
1920-08-23
confirmed
```

### 확인된 공식 자료

> 1920년 8월 조만식·오윤선·김동원·김보애 등 70인이 발기·조직 (한국민족문화대백과사전 「조선물산장려회」)

`8월 23일`이라는 일자는 현재 확인된 URL에서 직접 확인되지 않았다.

### ver3 provenance 기록

```text
change_history:
  old_value  = 1920-08-23
  old_status = confirmed
  new_value  = 1920-08
  new_precision = Month
  reason = "현재 확인된 공식 백과사전 항목은 '1920년 8월 조직'까지만 명시, 일자(23일)를 지지하는 근거 미확인"

claim_status = confirmed             # 1920년 8월 조선물산장려회가 조직되었다는 사실은 확실
date_status  = not_directly_verified  # 8월 23일이라는 특정 일자는 미확인
```

단순히 날짜를 낮추는 데 그치지 않고, **애초에 8/23이라는 값이 왜 들어갔는지도 별도의 조사 대상(open item)으로 provenance에 남겨야 한다.** 이는 v9 작업 큐에 포함한다(§9 참조).

---

# 5. Claim 단위 분해 원칙과 예시 — 홍범도

ver2까지는 49개 "항목"(대개 인물 1명 = 1행) 단위로 URL을 매핑했다. 그러나 인물 1명 안에는 실제로 여러 개의 독립적 주장이 섞여 있다. 이를 항목 단위가 아니라 **Claim 단위**로 쪼개는 것이 ver3의 핵심 방침이다.

### 예: 홍범도

기존(ver2, 항목 단위):

```text
홍범도 → 한국민족문화대백과사전 「홍범도」 → 확인
```

ver3(Claim 단위):

| Claim ID | 주장 |
|---|---|
| CLM-027-01 | 홍범도의 생년(1868) |
| CLM-027-02 | 홍범도의 몰년(1943) |
| CLM-027-03 | 대한독립군 창설 관련 |
| CLM-027-04 | 봉오동전투 참여 |
| CLM-027-05 | 청산리전투 참여 |
| CLM-027-06 | 봉오동전투 참여시점 = 1920-06 |
| CLM-027-07 | 청산리전투 참여시점 = 1920-10 |

```text
CLM-027-04 → Source S-027-A(홍범도 항목) → 봉오동전투 참여 근거 (claim_status = confirmed)
CLM-027-06 → Source S-027-B(봉오동전투 항목) → 사건 발생일 근거
             ※ 개인 Event 날짜(CLM-027-06)에는 자동 상속하지 않음 (date_status = inferred)
```

**Claim A(사건 발생일이 확인됨)와 Claim B(인물이 참여했음이 확인됨)가 모두 참이어도, Claim C(그 인물의 개인 참여일 = 사건 발생일)는 자동으로 확정되지 않는다.** 이는 v7에서 확립한 "사건 날짜 자동상속 금지" 원칙을 Claim 단위·provenance 단위로 명문화한 것이다.

이 분해 방식은 49개 항목 전체, 특히 여러 사건에 걸쳐 활동한 인물(안창호, 이시영, 이회영, 이동휘 등)에 우선 적용한다.

---

# 6. 상태값 체계 (ver3 — 이원화)

## 6-1. claim_status (주장 자체가 사실인가)

```text
confirmed              # 주장 자체가 직접 근거로 확인됨
confirmed_indirect      # 간접 근거(명단 등)로 확인됨
validation_hold        # 근거 부족·충돌로 보류
contradicted           # 근거와 모순됨
```

## 6-2. date_status (그 날짜가 정확한가) — claim_status와 독립적으로 부여

```text
verified               # 날짜가 1차/공식 자료로 직접 확인됨
inferred               # 상위 사건의 날짜에서 유추, 개인 참여일에 자동 적용 금지
estimated              # 범위 추정(예: ±2개월)
conflicting_sources    # 출처마다 날짜가 다름
not_directly_verified  # 날짜 근거 자체가 아직 확인되지 않음
```

## 6-3. 적용 예시

| 항목 | claim_status | date_status |
|---|---|---|
| 이승훈–오산학교 | confirmed | conflicting_sources |
| 조선물산장려회 | confirmed | not_directly_verified |
| 이동휘–임시정부 국무총리 | confirmed | conflicting_sources |
| 홍범도–봉오동전투 참여 | confirmed | inferred |
| 김좌진–신민회 | validation_hold | (해당없음, null) |

## 6-4. `hasEestimation` vs `hasValidationStatus` 분리

두 속성은 서로 다른 질문에 답한다.

* `hasEestimation = true` → **"언제인가?"**가 불확실하다는 뜻 (날짜의 정밀도 문제)
* `hasValidationStatus = "검증보류"` → **"사실인가?"**를 아직 확정하지 않았다는 뜻 (주장 자체의 신뢰도 문제)

예를 들어 신흥무관학교 개칭 문제는:

```text
claim_status(개칭 사건 자체) = validation_hold
date_status(개칭 시점 1912년) = not_directly_verified
```

처럼 두 축을 독립적으로 기록해야 "신흥강습소 → 신흥무관학교 개칭이 있었다는 것 자체가 불확실"한지, "개칭은 있었지만 정확한 시점만 불확실"한지를 구분할 수 있다.

---

# 7. Negative Evidence 원칙 (표현 제한)

김좌진–신민회 사례처럼 "확인한 자료 범위에서 관계를 찾지 못한 경우"도 provenance로 남긴다. 다만 표현 범위는 다음과 같이 제한한다.

> **"자료에 없었다" ≠ "그런 일이 없었다"**

```text
evidence_type = negative
evidence_note = "확인한 신민회 공식 명단(한국민족문화대백과사전 「신민회」)에서 김좌진을 확인하지 못함"
claim_status = validation_hold
```

이를 **"김좌진은 신민회 회원이 아니었다"**는 단정적 문장으로 변환해서는 안 된다. Negative evidence는 "조사 범위 내 미확인"이라는 제한된 의미로만 기록한다.

---

# 8. 49개 항목 상태 재분류 (판정 용어 갱신)

ver2의 확인/부분확인/재확인/보류를 아래와 같이 재정리했다. 세부 항목별 매핑은 원문(ver2) 표와 동일한 근거를 사용하되 용어만 다음 기준으로 치환한다.

| ver2 용어 | ver3 용어 | 의미 |
|---|---|---|
| 확인 | **직접검증** | Evidence가 Claim을 직접 뒷받침 |
| 부분확인 | **부분검증** | URL은 있으나 세부 주장 일부만 근거로 확인됨 |
| 재확인 | **URL재확인필요** | CSV상 URL 존재 언급은 있으나 본 검증에서 실제 URL을 확보하지 못함 |
| (신설) | **관계보류** | 관계 자체의 존재를 확정하지 못함 (예: 김좌진–신민회) |
| (신설) | **출처충돌** | 복수의 공식 자료가 서로 다른 값을 제시 (예: 오산학교, 이동휘 취임시점) |

### 직접검증 (핵심 근거 확보)

신민회, 대성학교, 신흥강습소(공동설립 4인), 대한민국임시정부, 보성사, 3·1운동, 안악사건, 105인사건, 봉오동전투(사건), 물산장려운동, 안창호, 조만식, 유영모(오산학교 재직), 안명근, 홍범도(참여 사실), 이종호, 손병희, 이회영, 이시영(신흥강습소), 이종일, 한용운, 오세창, 서일/북로군정서, 이승만, 최린, 정춘수(33인 서명)

### 출처충돌

이승훈–오산학교(설립일), 조선물산장려회(설립일), 이동휘(임시정부 취임시점)

### 관계보류

김좌진–신민회

### URL재확인필요 (v9 작업 큐, §9 참조)

숭실학교, 보성학교, 신간회, 함석헌, 배위량, 최광옥(URL은 신민회 명단으로 소속만 간접확인), 차이석, 이용익, 이동녕, 이상룡, 지청천, 이범석, 박희도, 청산리전투(사건-개인 참여일 분리 필요)

---

# 9. v9 작업 큐 (우선순위)

이 13건은 **억지로 URL을 채우지 않고 정직하게 재확인 상태로 남긴다.**

* 숭실학교, 보성학교, 신간회, 함석헌, 배위량, 차이석, 이용익, 이동녕, 이상룡, 지청천, 이범석, 박희도
* 청산리전투 — 사건 자체는 확인되더라도 "사건 날짜 ≠ 개인 참여 날짜" 원칙(§5)에 따라 별도 Claim으로 분리해야 함

추가로 다음 두 항목도 open item으로 큐에 포함한다.

* 오산학교 1907-12-24 값이 애초에 어떻게 CSV에 들어갔는지의 출처 역추적 (change_history의 근거 보강)
* 조선물산장려회 1920-08-23 값의 출처 역추적

---

# 10. Source Mapping 최소 데이터 구조 (ver3 — 컬럼 확장)

```text
source_id
evidence_id          # 신설: 같은 source_url 안에서도 문장 단위로 구분
claim_id
subject_uri
claim
relation
object_uri
date_value
date_precision
has_estimation        # hasEestimation: 날짜 추정 여부
claim_status          # 신설: 주장 자체의 검증 상태
date_status           # 신설: 날짜의 검증 상태 (claim_status와 독립)
source_title
source_url
evidence_note          # 반드시 유지: 해당 URL의 어느 문장이 근거인지
change_history          # 신설: 이전 값 → 현재 값, 변경 사유
verification_status
verification_date
```

### 예시 (이종일–보성사)

```text
source_id = SM-039
evidence_id = E-039-002
claim_id = CLM-039-01
subject_uri = :이종일
claim = "이종일이 보성사를 경영했다"
relation = :경영
object_uri = :보성사
date_value = 1919-02
date_precision = Month
has_estimation = false
claim_status = confirmed
date_status = verified
source_title = "한국민족문화대백과사전 「보성사」"
source_url = https://encykorea.aks.ac.kr/Article/E0023417
evidence_note = "1919년 2월 27일 사장 이종일이 독립선언서 21,000매를 인쇄"
change_history = null
verification_status = 직접검증
verification_date = 2026-08-29
```

---

# 11. v8 구조검증과의 관계 재확인

v8 RDF 자체는 앞선 rdflib 검증에서 구조적 무결성이 확인되었다. 이번 ver2~ver3 검증에서 드러난 문제는 **문법 문제가 아니라 증거 강도(evidence strength)의 문제**였다. 즉 핵심 질문은:

> "이 트리플이 RDF 문법상 유효한가?" (→ 이미 해결됨)

가 아니라,

> **"이 트리플을 왜 넣었으며, 어떤 Evidence가 어떤 Source에서 이 Claim을 지지하는가, 그리고 다른 출처와 충돌하지 않는가?"**

로 옮겨갔다.

---

# 12. v9 작업 순서 (로드맵)

새 RDF를 먼저 만드는 것이 아니라 **Claim 분해와 Source Mapping CSV 완성이 우선**이다.

```text
v8 RDF
 ↓
49개 항목
 ↓
각 항목의 주장(Claim) 분해            ← §5 원칙 적용 (홍범도식 분해)
 ↓
Claim ID 부여
 ↓
각 Claim → 실제 URL 1:1 매핑
 ↓
URL → Evidence 단위 분리 + evidence_note 작성
 ↓
날짜/정밀도 별도 검증 (date_status)
 ↓
주장 자체 검증 (claim_status)
 ↓
출처 충돌 및 변경이력(change_history) 기록
 ↓
Verification Status 부여
 ↓
Provenance CSV 확정
 ↓
v9 RDF에 provenance 반영
```

v9에서는 `source_url`만 추가하는 수준에서 끝내지 않고, `claim_id + evidence_id + source_id + evidence_note + claim_status + date_status + change_history`까지 함께 채우는 것을 핵심 목표로 삼는다.

---

# 13. ver3 결론

1. v8 데이터의 문제는 구조적 오류가 아니라 **증거 강도**의 문제였다.
2. 기존 CSV의 일부 `confirmed`가 과도하게 강했다 — 특히 오산학교(1907-12-24), 조선물산장려회(1920-08-23)는 현재 증거 수준에 맞게 Month 단위로 낮추되, **변경이력(change_history)을 provenance에 함께 보존**한다.
3. 사건 날짜와 인물 Event 날짜는 반드시 분리해야 하며, 사건 날짜가 확정되었다고 개인 참여일까지 자동 확정해서는 안 된다(§5).
4. 출처 URL만 저장하는 것으로는 provenance가 완성되지 않는다. 최소한 `Claim / Evidence / Source / Date / claim_status / date_status`가 함께 있어야 한다(§10).
5. v9부터는 "데이터베이스"가 아니라 **감사 가능한(audit-trail) 역사 지식그래프**로 발전시키는 것이 목표이며, 그 첫 작업은 새 RDF 생성이 아니라 49개 항목의 Claim 단위 분해와 Source Mapping CSV 완성이다(§12).

---

# 부록. 참고문헌 (APA 형식)

ver2에서 확인한 고유 URL 33건은 그대로 유지한다. 발행처는 **한국학중앙연구원**(한국민족문화대백과사전, encykorea.aks.ac.kr)과 **국사편찬위원회**(우리역사넷, contents.history.go.kr)이며, 접속일은 2026년 8월 29일 기준이다.

## 한국민족문화대백과사전 (encykorea.aks.ac.kr) — 발행: 한국학중앙연구원

한국학중앙연구원. (n.d.). 3·1독립선언서. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0026764 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 3·1운동. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0026772 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 105인 사건. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0022233 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 고려공산당. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0003430 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 공산주의운동. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0004340 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 대성학교. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0014519 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 대한민국 임시정부. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0015017 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 대한민국임시정부헌법. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0015021 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 보성사. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0023417 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 봉오동전투. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0023974 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 손병희. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0030507 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 신민회. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0032974 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 안명근. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0034719 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 안악사건. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0034866 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 안창호. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0035050 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 오산고등학교. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0038302 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 유영모. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0041674 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 이동휘. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0044080 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 이승훈. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0044964 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 이시영. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0044990 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 이종일. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0045940 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 이종호. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0045955 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 이회영. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0046635 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 조만식. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0051729 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 조선물산장려운동. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0052020 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 조선물산장려회. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0052021 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 최린. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0057276 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 홍범도. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0064093 (2026. 8. 29. 검색)

한국학중앙연구원. (n.d.). 북로군정서. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0024657 (2026. 8. 29. 검색)

## 우리역사넷 (contents.history.go.kr) — 발행: 국사편찬위원회

국사편찬위원회. (n.d.). 대한민국 임시 헌장. 우리역사넷. https://contents.history.go.kr/front/hm/view.do?levelId=hm_123_0060 (2026. 8. 29. 검색)

국사편찬위원회. (n.d.). 독립군 아내들의 헌신. 우리역사넷. https://contents.history.go.kr/front/hm/view.do?levelId=hm_126_0050 (2026. 8. 29. 검색)

국사편찬위원회. (n.d.). 신흥무관학교 (용어해설). 우리역사넷. https://contents.history.go.kr/front/tg/list.do?ganada=전체&pageIndex=3&pageUnit=20&treeId=0202 (2026. 8. 29. 검색)

국사편찬위원회. (n.d.). 오산 학교. 우리역사넷. https://contents.history.go.kr/mobile/tg/view.do?levelId=tg_004_2280 (2026. 8. 29. 검색)

---

**비고**: §9의 v9 작업 큐 13건(숭실학교, 보성학교, 신간회, 함석헌, 배위량, 차이석, 이용익, 이동녕, 이상룡, 지청천, 이범석, 박희도, 청산리전투)은 본 보고서 원문에 실제 URL 문자열이 제시되지 않아 참고문헌 목록에 포함하지 않았다. v9에서 실제 URL을 확보한 뒤 동일한 형식으로 추가한다.
