# v8 추가 검증 보고서 (ver5)

## — 49개 항목 Source Mapping 1차 검증 및 Provenance Layer 설계 보고서 (설계 승인본)

> **버전 이력**: ver1(v8 RDF 구조검증) → ver2(49개 항목 URL 팩트체크 초안) → ver3(Claim/Evidence/Source 분리, 상태값 이원화) → ver4(김좌진 정정, Claim 추가 분해, status vocabulary 3층+flag 구조) → **ver5(date_value_status 정의 명확화, review_flag 다중값 명시, Evidence↔Claim 다대다 허용, 오산학교 source_conflict 유보, 49개 상태표를 보조지표로 재정의, v9 데이터 생성 규칙 8개 신설)**

---

# 0. 핵심 설계 원칙 (유지)

```text
Claim status  ≠  Date status
Claim         ≠  Event date
Source        ≠  Evidence
Evidence      ≠  Claim
Negative evidence  ≠  Contradiction
Old value     ≠  Deleted value
```

ver5에서 다음 원칙을 추가한다.

```text
정밀도를 낮춘 표현  ≠  값을 추정한 것
날짜가 inferred라는 사실  ≠  Claim 전체가 validation_hold라는 뜻
review_flag        =  다중값(multi-valued)
```

---

# 0-1. ver4 → ver5 변경 요약

이번 피드백의 결론에서 제시한 5개 필수 수정과, 본문에서 함께 제안된 보완 규칙을 반영했다.

| No | 변경 내용 | 근거 |
|---|---|---|
| 1 | 오산학교 review_flag에서 `source_conflict` 제거, `relationship_issue`만 유지 | 설립/개교가 서로 다른 사건일 가능성이 있는 상태에서 곧바로 "충돌"로 단정하면 안 됨 |
| 2 | `date_value_status`를 `provisional/final` → `source_stated / provisional / unresolved`로 재정의, "대표값 채택 여부"와 "출처 검증 상태(date_status)"가 독립임을 명문화 | provisional·final이 verified와 모순되게 읽히는 문제 해소 |
| 3 | `review_flag`가 **다중값(list)**임을 명시, CSV 표기법(`\|` 구분)과 RDF 표기법(다중 트리플) 제시 | 오산학교처럼 두 flag가 동시에 붙는 경우를 스키마 차원에서 정의 |
| 4 | Evidence–Claim 관계를 1:1이 아니라 **1 Source→N Evidence→N Claim, 1 Evidence→N Claim**의 다대다로 재정의 | 김좌진 사례(하나의 문장이 두 Claim을 지지)처럼 실제로는 다대다가 흔함 |
| 5 | §7 제목을 「49개 항목 재분류」→「49개 항목 Source Mapping 작업 현황(보조 지표)」로 변경, "Claim 단위가 권위값" 원칙을 표 바로 아래 명시 | 항목 단위 표가 최종 판정표로 오독되는 것을 방지 |
| 6 | `verification_status`의 세 값을 "무엇을 확인했는가" 기준으로 명확히 재정의, `claim_status`와 독립적으로 조합될 수 있음을 예시로 명시 | "재검증에서 URL을 못 찾았지만 과거엔 confirmed였다" 같은 audit trail 표현 가능하게 함 |
| 7 | `has_estimation` 보완: "정밀도를 낮춘 표현"과 "값을 추정한 것"을 구분하는 예시 추가 | 원자료가 제공한 해상도를 그대로 저장한 경우까지 추정으로 오분류되는 것을 방지 |
| 8 | `claim_status = validation_hold`의 부여 기준을 "Claim 문장 자체의 강도"로 명시, 날짜가 inferred라는 이유만으로 자동으로 validation_hold가 되지 않음을 명문화 | 참여 사실(confirmed)과 참여일(validation_hold)의 확신도를 혼동하지 않기 위함 |
| 9 | 이동휘 CLM-LEE-A의 "선임/취임"처럼 **슬래시(/)로 서로 다른 event type을 묶지 않는다**는 원칙을 v9 규칙으로 명문화 | 선임과 취임이 서로 다른 사건일 수 있음을 반영 |
| 10 | 참고문헌 건수를 재검산(36건: 계승 33건 + ver4 신규 3건, 계산 일치 확인), Source count/Evidence count/Claim count를 별도 지표로 분리 관리하도록 명시 | "출처 개수 ≠ 49개 항목 개수 ≠ Claim 개수"라는 bookkeeping 원칙 반영 |
| 11 | 신설: **§12 v9 데이터 생성 규칙(8개)** — 위 8·9번 등 산발적으로 언급된 원칙을 규칙 목록으로 통합 | v9 CSV 작성 시 바로 참조할 수 있는 단일 규칙집 필요 |

---

# 1. 검증 목적 (유지)

v8 RDF와 CSV의 각 사실을 다시 출처까지 역추적해 다음 구조를 확립하고자 했다.

> **개체/사건 → 주장(Claim) → 근거(Evidence) → 출처(Source) → 관계(Relation) → 날짜(Date)**

---

# 2. 상태값 체계 v5

## 2-1. claim_status — 역사적 주장 자체의 상태

```text
confirmed
confirmed_indirect
validation_hold
contradicted
```

**부여 기준(ver5 명확화)**: `claim_status`는 **Claim 문장 자체가 얼마나 강하게 근거로 뒷받침되는지**를 기준으로 부여한다. 연결된 `date_status`가 `inferred`/`estimated`라는 이유만으로 상위 Claim의 `claim_status`가 자동으로 `validation_hold`가 되지 않는다.

예:

```text
Claim: 홍범도는 1920년 봉오동전투에 참여하였다.
→ Source가 직접 서술 → claim_status = confirmed, date_status = verified

Claim: 홍범도의 정확한 봉오동전투 참여일은 1920-06이다.
→ 사건 날짜에서 유추한 별도 Claim → claim_status = validation_hold, date_status = inferred
```

즉 두 문장은 **서로 다른 Claim**이며, 하나가 confirmed라고 해서 다른 하나가 자동으로 confirmed가 되지 않는다(§0의 원칙과 동일).

## 2-2. date_status — 날짜의 상태

```text
verified
inferred
estimated
conflicting_sources
not_directly_verified
```

## 2-3. date_value_status — 저장된 날짜값의 채택 단계 (ver5 재정의)

```text
source_stated        # 해당 값이 특정 출처에 그대로 명시되어 있음
provisional          # 복수 출처를 종합해 대표값으로 잠정 채택함 (최종 확정 아님)
unresolved           # 아직 대표값을 선택하지 못함 (예: 근거 미확보 상태의 legacy 값)
```

> **정의**: `date_value_status`는 해당 Claim에 저장된 날짜값이 연구용 대표값으로서 어느 단계에 있는지를 나타내며, 출처가 그 값을 실제로 뒷받침하는지를 나타내는 `date_status`와는 **독립적인 축**이다. 예를 들어 `date_status = verified`이면서 `date_value_status = source_stated`인 것이 표준 조합이며 — 이는 "그 출처가 실제로 그렇게 말했고(source_stated), 그 진술 자체는 확인되었다(verified)"는 뜻이다. 반대로 여러 출처를 종합해 대표값을 임시로 고른 경우에는 `date_value_status = provisional`을 쓰되, 그 값 자체가 개별 Claim 단위로는 `source_stated`일 수도 있다 — `provisional`은 주로 **엔티티(예: 이승훈–오산학교) 수준에서 "여러 Claim 중 어느 것을 대표로 쓸지 아직 정하지 못했다"**는 뜻으로 사용한다.

## 2-4. has_estimation — 재정의 보완 (ver5)

```text
has_estimation = true
  → 원자료에 없는 값을 상위 사건의 날짜 등에서 추론·복사하여 만든 경우에만 true
```

**중요한 구분(ver5 추가)**: **정밀도를 낮추어 표현한 것 ≠ 값을 추정한 것**이다.

* 원자료: "1919년 8월 말" → 저장값: `1919-08` (Month) → `has_estimation = false`
  (원자료 자체가 그 해상도의 정보를 제공했고, 단지 저장 형식이 day 단위를 표현하지 않을 뿐)
* Event 날짜(`1920-06`)를 그대로 복사해 개인 참여 Claim의 날짜로 사용 → `has_estimation = true`, `date_status = inferred`
  (원자료가 개인의 참여일을 직접 말하지 않았는데, 상위 사건 날짜를 가져다 쓴 경우)

## 2-5. verification_status — 이번 검증 프로세스의 결과 (ver5 정의 명확화)

```text
directly_verified
  = 실제 Source를 확인했고, Evidence를 특정하여 해당 Claim과 명시적으로 연결함

partially_verified
  = Source는 확인했으나 Claim의 일부 요소만 Evidence로 확인됨

url_recheck_required
  = 기존 기록(CSV 등)에는 출처가 있다고 되어 있으나,
    이번 검증에서 실제 Source를 확보·확인하지 못함
```

**`claim_status`와 독립적으로 조합 가능**(ver5 강조): 예를 들어 `claim_status = confirmed`이면서 `verification_status = url_recheck_required`인 조합도 유효하다 — 이는 "과거 검증 또는 선행 연구에서는 confirmed였지만, 이번 ver5 재검증 과정에서 그 근거 URL을 다시 확보하지 못했다"는 audit trail을 표현한다.

## 2-6. review_flag — 다중값(list) (ver5 명시)

```text
none
relationship_issue    # 관계/사건의 동일성 자체를 추가 검토해야 함
source_conflict        # 동일 사건에 대해 복수의 공식 출처가 서로 다른 값을 제시 (동일 사건임이 확인된 경우에만 부여)
provenance_gap          # 기존 CSV 값의 최초 출처를 역추적하지 못함
```

`review_flag`는 **단일 enum이 아니라 다중값**이다.

* CSV 표기: 파이프(`|`)로 구분 — 예) `relationship_issue|provenance_gap`
* RDF 표기: 다중 트리플 — 예)
  ```text
  :오산학교이승훈설립 :hasReviewFlag :RelationshipIssue .
  :오산학교이승훈설립 :hasReviewFlag :SourceConflict .
  ```

**`source_conflict` 부여 기준(ver5, 오산학교 사례로 확정)**: 두 값이 **동일 사건**을 가리키는 것으로 확인된 경우에만 `source_conflict`를 부여한다. 동일 사건 여부가 아직 미확인이면 `relationship_issue`만 부여한다.

---

# 3. Naming Convention (유지)

```text
RDF: :hasEstimation  :hasValidationStatus  :hasReviewFlag
CSV: has_estimation   claim_status          review_flag (다중값)
```

---

# 4. 핵심 사례 재작성 (ver5 수정분 반영)

## 4-1. 김좌진 — 신민회 (Evidence 다대다 사례 추가)

```text
CLM-KIM-01
Claim: 김좌진이 신민회에 가입하였다
claim_status = confirmed
date_status = not_directly_verified
verification_status = directly_verified
review_flag = [none]

CLM-KIM-02  (ver5 신설 — Evidence 1건이 두 Claim을 지지하는 사례)
Claim: 김좌진이 청년학우회에서 활동하였다
claim_status = confirmed
date_status = not_directly_verified
verification_status = directly_verified
review_flag = [none]

Evidence E-KIM-01 (공통)
"신민회에 가입하였고 청년학우회에서도 활동하였다"
→ E-KIM-01 → CLM-KIM-01
→ E-KIM-01 → CLM-KIM-02   (1 Evidence → N Claim의 실제 사례)
```

## 4-2. 이승훈 — 오산학교 (review_flag 조정)

```text
CLM-OSAN-01
Claim: 이승훈이 오산학교를 설립하였다
date_value = 1907-12
date_precision = Month
claim_status = confirmed
date_status = verified
date_value_status = source_stated   # 「오산고등학교」가 직접 명시한 값 그대로

CLM-OSAN-02
Claim: 이승훈이 오산학교를 개교하였다
date_value = 1907-11-24
date_precision = Day
claim_status = confirmed
date_status = verified
date_value_status = source_stated   # 「이승훈」이 직접 명시한 값 그대로

Entity-level (ver5 수정):
review_flag = [relationship_issue]
  # 설립일과 개교일이 동일 사건을 가리키는지 아직 확인되지 않았으므로
  # source_conflict는 아직 부여하지 않는다.
  # → v9에서 동일 사건으로 확인될 경우:
  #    review_flag = [relationship_issue, source_conflict]로 갱신
```

change_history는 ver4와 동일하게 유지한다.

## 4-3. 조선물산장려회 (date_value_status 적용)

```text
CLM-JOSEON-01
Claim: 1920년 8월 조선물산장려회가 조직되었다
date_value = 1920-08
claim_status = confirmed
date_status = verified
date_value_status = source_stated
verification_status = directly_verified
review_flag = [none]

CLM-JOSEON-02
Claim: 조선물산장려회가 1920년 8월 23일에 조직되었다
date_value = 1920-08-23
claim_status = validation_hold
date_status = not_directly_verified
date_value_status = unresolved       # legacy CSV 값, 대표값으로 아직 채택 못함
verification_status = url_recheck_required
review_flag = [provenance_gap]
```

## 4-4. 이동휘 (event type 분리 원칙 적용)

기존 CLM-LEE-A는 "선임/취임"을 슬래시로 묶고 있었다. ver5에서는 원칙(§0, §12 Rule G-01)에 따라 정리했다. 다만 현재 확보된 Source(「고려공산당」)가 "선임"과 "취임"을 구분하지 않고 서술하므로, 근거 없이 인위적으로 둘로 쪼개지는 않았다 — 대신 Claim 문장에서 슬래시 표기를 제거하고 Source의 표현을 그대로 따랐다.

```text
CLM-LEE-A
Claim: 이동휘가 임시정부 국무총리에 취임하였다   # "선임/취임" 슬래시 제거, Source 표현(취임)을 그대로 채택
Source: 「고려공산당」
date_value = 1919-08
date_precision = Month
claim_status = confirmed
date_status = verified
date_value_status = source_stated

CLM-LEE-B
Claim: 이동휘가 포함된 통합임시정부 국무원 합동 취임식이 거행되었다
Source: 한국 근대 사료 DB — 대한민국임시정부자료집
date_value = 1919-11-03
date_precision = Day
claim_status = confirmed
date_status = verified
date_value_status = source_stated

Entity-level:
review_flag = [relationship_issue]
  # CLM-LEE-A(취임)와 CLM-LEE-B(통합정부 합동 취임식)가
  # 같은 사건의 다른 단계인지, 서로 다른 사건인지 아직 미확인
```

## 4-5. 홍범도 (claim_status 부여 기준 명시 반영)

```text
CLM-027-04
Claim: 홍범도가 봉오동전투에 참여하였다
claim_status = confirmed        # Claim 문장 자체가 Source로 직접 확인됨
date_status = null
has_estimation = false

CLM-EVENT-027
Claim: 봉오동전투는 1920년 6월에 발생하였다
claim_status = confirmed
date_status = verified
date_value_status = source_stated

CLM-027-06
Claim: 홍범도의 봉오동전투 참여일은 1920-06이다
claim_status = validation_hold   # 문장 자체가 사건날짜를 개인에게 복사한 것이므로 강도가 낮음
date_status = inferred
has_estimation = true            # 원자료에 없는 값을 사건 날짜에서 가져온 경우
date_value_status = provisional
```

## 4-6. 이종일 — 보성사 (Evidence-Claim 다대다 표현 수정)

```text
CLM-039-01
Claim: 이종일은 1919년 당시 보성사 사장이었다
claim_status = confirmed
date_status = verified

CLM-039-02
Claim: 이종일이 1919년 2월 27일 보성사에서 독립선언서 인쇄를 주도하였다
date_value = 1919-02-27
claim_status = confirmed
date_status = verified
date_value_status = source_stated
```

**Evidence-Claim 관계(ver5 수정)**: 「보성사」 항목의 "사장 이종일 … 독립선언서를 인쇄"라는 한 문장이 CLM-039-01과 CLM-039-02 두 Claim을 동시에 지지할 수 있다. Evidence와 Claim은 1:1로 고정하지 않고, **1 Source → N Evidence → N Claim, 1 Evidence → N Claim**의 다대다 관계로 기록한다(§9 스키마 참조).

---

# 5. Negative Evidence 원칙 (유지)

원칙과 추상 템플릿은 ver4와 동일하게 유지한다. 실제 사례 발굴은 v9 작업 큐(§8)에서 계속 진행한다.

---

# 6. 항목 단위 vs Claim 단위 (재확인)

* **항목 단위 상태**(§7)는 **보조 지표**로만 사용한다.
* **개별 Claim의 `claim_status`/`date_status`가 권위값**이며, 항목 단위 상태와 불일치할 경우 Claim 단위가 우선한다.

---

# 7. 49개 항목 Source Mapping 작업 현황 (보조 지표)

> **본 표는 항목 단위의 진행 현황을 나타내는 보조 지표이며, 개별 Claim의 상태를 대표하지 않는다. 최종 판정은 §4의 Claim 단위 레코드가 우선한다.**

### verification_status = directly_verified (핵심 근거 확보)

신민회, 대성학교, 신흥강습소(공동설립 4인), 대한민국임시정부, 보성사/이종일(§4-6), 3·1운동, 안악사건, 105인사건, 봉오동전투(사건 자체), 물산장려운동, 안창호, 조만식, 유영모(오산학교 재직), 안명근, 홍범도(참여 사실, §4-5), 이종호, 손병희, 이회영, 이시영(신흥강습소), 한용운, 오세창, 서일/북로군정서, 이승만, 최린, 정춘수(33인 서명), 김좌진(§4-1)

### verification_status = directly_verified, review_flag = [relationship_issue]

* 이승훈–오산학교 (§4-2)
* 이동휘–임시정부 (§4-4)

### verification_status = directly_verified(월 단위)/url_recheck_required(일 단위), review_flag = [provenance_gap]

* 조선물산장려회 (§4-3)

### verification_status = url_recheck_required (v9 작업 큐)

숭실학교, 보성학교, 신간회, 함석헌, 배위량, 최광옥(confirmed_indirect), 차이석, 이용익, 이동녕, 이상룡, 지청천, 이범석, 박희도, 청산리전투(사건-개인 참여일 분리 필요, §4-5와 동일 원칙 적용)

---

# 8. v9 작업 큐

1. 오산학교: 설립(CLM-OSAN-01)/개교(CLM-OSAN-02) 동일 사건 여부 1차 사료로 재검토 → 확인되면 review_flag에 source_conflict 추가
2. 조선물산장려회: `1920-08-23`의 최초 출처 역추적
3. 이동휘: "취임"(CLM-LEE-A)과 "합동 취임식"(CLM-LEE-B)이 임시정부사에서 통상 구분되는 개념인지 재검토
4. 나머지 13건 URL 확보, 청산리전투는 사건/개인 참여일 분리 설계로 시작
5. Negative Evidence 실제 사례 1건 이상 확정
6. **49개 항목 전체를 Claim 단위로 재작성**(§4의 6개 사례를 표준 패턴으로 확산 적용) — v9 본 작업
7. Source count / Evidence count / Claim count / Verified Claim count / Unmapped Claim count를 별도 지표로 산출 (§10)

---

# 9. Source Mapping 최소 데이터 구조 (ver5)

```text
source_id
evidence_id            # 1 Source : N Evidence
claim_id                 # 1 Evidence : N Claim (다대다 허용)
subject_uri
claim
relation
object_uri
date_value
date_precision
date_value_status         # source_stated / provisional / unresolved
has_estimation              # 추론값에만 true (정밀도 축소와 구분)
claim_status                 # confirmed / confirmed_indirect / validation_hold / contradicted
date_status                   # verified / inferred / estimated / conflicting_sources / not_directly_verified
verification_status            # directly_verified / partially_verified / url_recheck_required
review_flag                     # 다중값, '|' 구분: none | relationship_issue | source_conflict | provenance_gap
source_title
source_url
evidence_note
change_history
verification_date
```

---

# 10. 지표 분리 (ver5 신설)

다음 카운트는 서로 다른 층위이며 혼동해서는 안 된다.

```text
Source count            # 참고문헌 URL 개수
Evidence count           # 문장 단위 근거 개수 (Source보다 많을 수 있음)
Claim count                # 개별 주장 개수 (49개 항목보다 훨씬 많음)
Verified Claim count         # claim_status = confirmed 또는 confirmed_indirect인 Claim 수
Unmapped Claim count           # 아직 Claim ID조차 부여되지 않은 항목 (v9 착수 전 상태)
```

참고문헌(부록) 재검산 결과: **Source count = 36건** (ver2 계승 33건 + ver4 신규 3건, 합계 일치 확인). 이는 49개 항목 수, Claim 수와는 별개의 지표이므로 "49개 항목 중 33건 확인"처럼 서로 다른 분모를 섞어 말하지 않는다.

---

# 11. v9 작업 순서 (로드맵)

```text
① 김좌진 정정                           ← 완료 (ver4)
② 이동휘 Claim 분해 (event type 분리)    ← 완료 (ver5, §4-4)
③ 오산학교 Claim 분해 + review_flag 조정 ← 완료 (ver5, §4-2)
④ status vocabulary 정규화(3층+flag,
   다중값·정의 명확화)                   ← 완료 (ver5, §2)
⑤ 49개 전체 Claim CSV 작성               ← v9 본 작업 (미착수)
```

---

# 12. v9 데이터 생성 규칙 (신설 — 8개 규칙집)

v9에서 49개 항목을 Claim 단위로 전개할 때 아래 규칙을 그대로 적용한다.

**Rule G-01.** Claim 문장 안에 서로 다른 event type을 슬래시(`/`)로 묶지 않는다. Source가 두 event를 구분하지 않고 서술하면 Source의 표현을 그대로 따르는 단일 Claim으로 두고, 구분 가능성이 있으면 별개 Claim으로 분리한다(§4-4).

**Rule G-02.** Event의 날짜는 해당 Event에 직접 연결된 Claim에만 귀속되며, Person–Event participation Claim의 개인 활동일로 자동 상속하지 않는다(§4-5).

**Rule G-03.** 정밀도를 낮추어 원자료의 해상도 그대로 저장한 것과, 원자료에 없는 값을 추론·복사한 것은 다르다. `has_estimation`은 후자에만 true(§2-4).

**Rule G-04.** `claim_status`는 Claim 문장 자체의 근거 강도로 정하며, 연결된 `date_status`가 inferred/estimated라는 이유만으로 자동으로 `validation_hold`가 되지 않는다(§2-1).

**Rule G-05.** `verification_status`와 `claim_status`는 서로 다른 시점·층위의 판단일 수 있다. 예: 과거 confirmed였으나 이번 재검증에서 URL을 재확보하지 못한 경우 `claim_status = confirmed`, `verification_status = url_recheck_required` 조합이 가능하다(§2-5).

**Rule G-06.** `review_flag`는 다중값이다. CSV는 `|` 구분, RDF는 다중 트리플로 표기한다(§2-6).

**Rule G-07.** Evidence와 Claim은 1:1이 아니라 **1 Source→N Evidence→N Claim, 1 Evidence→N Claim**의 다대다 관계로 기록한다(§4-1, §4-6).

**Rule G-08.** `review_flag`의 `source_conflict`는 두 값이 **동일 사건**을 가리키는 것으로 확인된 경우에만 부여한다. 동일 사건 여부가 미확인이면 `relationship_issue`만 부여한다(§2-6, §4-2).

---

# 13. ver5 결론

| 영역 | 판정 |
|---|---|
| Claim/Evidence/Source 분리 | 통과 |
| claim_status/date_status/verification_status/review_flag 4층 분리 | 통과 (ver5에서 정의 명확화 완료) |
| review_flag 다중값 | 통과 (ver5 신설) |
| Evidence↔Claim 다대다 관계 | 통과 (ver5 반영) |
| date_value_status 정의 | 통과 (ver5 재정의: source_stated/provisional/unresolved) |
| 오산학교 review_flag | 통과 (source_conflict 유보, relationship_issue만 유지) |
| has_estimation 보완(정밀도 vs 추정 구분) | 통과 |
| claim_status 부여 기준(문장 강도 기준) | 통과 |
| 이동휘 event type 분리 원칙 | 통과 (슬래시 표현 제거) |
| 49개 상태표의 위상 | 통과 (보조 지표로 재정의) |
| 지표 분리(Source/Evidence/Claim count) | 통과 (ver5 신설) |
| v9 데이터 생성 규칙집 | 통과 (ver5 신설, 8개 규칙) |
| 49개 전체 Claim CSV 작성 | 미완료 — v9 본 작업 |

**ver5는 설계 승인 단계로 간주한다.** 남은 것은 §11-⑤, 즉 49개 항목 전체를 §4의 6개 표준 패턴과 §12의 8개 규칙에 따라 Claim 단위 CSV로 전개하는 v9 본 작업이다. 이 단계부터는 새 RDF를 먼저 만들지 않고, `claim_id → evidence_id → source_id`가 채워진 CSV를 먼저 완성한 뒤 그 CSV를 기준으로 v9 RDF를 생성한다.

---

# 부록. 참고문헌 (APA 형식) — 본문 인용 대응표

이전 버전(ver2~ver4)의 부록은 발행처별·가나다순으로 나열되어 있어, 각 출처가 본문의 **어느 절·어느 Claim**을 뒷받침하는지 역추적하기 어려웠다. ver5의 부록은 이를 교정하여 **본문에 실제로 등장하는 순서(§4-1 → §4-6 → §7)대로, 각 출처가 정확히 어느 인용 위치를 뒷받침하는지 1:1로 표기**한다.

**정리 원칙**

1. 모든 항목에 `S-번호`(source ID)를 부여하고, 같은 출처가 본문 여러 곳에서 재사용되는 경우에도 항목은 **한 번만** 싣되 `인용 위치`란에 해당하는 모든 절·Claim ID를 함께 표기한다(§9 Rule G-07의 1 Source–N Claim 원칙과 동일한 논리).
2. 반대로, **현재 ver5 본문에서 실제로 인용되지 않는 출처는 부록에서 제외**한다. 대조 결과 아래 4건이 이전 버전 부록에는 있었으나 ver5 본문(§4의 재구성된 Claim, §7의 항목 목록)에서는 더 이상 직접 인용되지 않아 제외했다.
   * 「공산주의운동」(E0004340) — §4-4 이동휘 Claim이 「고려공산당」과 한국 근대 사료 DB 두 건으로 재구성되며 더 이상 인용되지 않음
   * 「이동휘」(E0044080) — 위와 같은 이유로 인물 개인 항목 대신 「고려공산당」이 CLM-LEE-A의 Source로 채택됨
   * 우리역사넷 「신흥무관학교(용어해설)」 — §7에서 "신흥강습소"만 직접검증 항목으로 남고 별도 인용되지 않음
   * 우리역사넷 「오산 학교」(tg_004_2280) — §4-2 CLM-OSAN-01의 Source가 「오산고등학교」 단일 출처로 재구성됨
3. 이 결과 **본문 실제 인용 출처는 총 32건**이다(§10 지표 원칙에 따라 이 숫자는 49개 항목 수·Claim 수와는 별개의 지표).

---

## §4-1. 김좌진–신민회 (CLM-KIM-01, CLM-KIM-02)

**S-01** 한국학중앙연구원. (n.d.). 김좌진. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0010528 `[ver4 신규]`
— 인용 위치: §4-1 (CLM-KIM-01 "신민회 가입", CLM-KIM-02 "청년학우회 활동" — Evidence 1건이 두 Claim을 지지, §9 Rule G-07)

---

## §4-2. 이승훈–오산학교 (CLM-OSAN-01, CLM-OSAN-02)

**S-02** 한국학중앙연구원. (n.d.). 오산고등학교. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0038302 `[ver2 계승]`
— 인용 위치: §4-2 (CLM-OSAN-01 "설립", 1907-12)

**S-03** 한국학중앙연구원. (n.d.). 이승훈. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0044964 `[ver2 계승]`
— 인용 위치: §4-2 (CLM-OSAN-02 "개교", 1907-11-24)

---

## §4-3. 조선물산장려회 (CLM-JOSEON-01, CLM-JOSEON-02)

**S-04** 한국학중앙연구원. (n.d.). 조선물산장려회. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0052021 `[ver2 계승]`
— 인용 위치: §4-3 (CLM-JOSEON-01 "1920년 8월 조직")
— *CLM-JOSEON-02("1920-08-23")는 근거 미확보(`verification_status = url_recheck_required`)로 인용 출처 없음 — §8 v9 작업 큐 2번*

---

## §4-4. 이동휘 (CLM-LEE-A, CLM-LEE-B)

**S-05** 한국학중앙연구원. (n.d.). 고려공산당. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0003430 `[ver2 계승]`
— 인용 위치: §4-4 (CLM-LEE-A "국무총리 취임", 1919-08)

**S-06** 국사편찬위원회. (n.d.). 대한민국임시정부자료집 — 국무원 합동 취임식. 한국 근대 사료 DB. https://db.history.go.kr/modern/level.do?levelId=ij_045_0020_00010_0090 `[ver4 신규]`
— 인용 위치: §4-4 (CLM-LEE-B "합동 취임식", 1919-11-03)

---

## §4-5. 홍범도 (CLM-027-04, CLM-EVENT-027, CLM-027-06)

**S-07** 한국학중앙연구원. (n.d.). 홍범도. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0064093 `[ver2 계승]`
— 인용 위치: §4-5 (CLM-027-04 "봉오동전투 참여"; CLM-027-06의 참여일은 이 Source가 아니라 CLM-EVENT-027의 사건일에서 유추한 값이므로 별도 근거 없음 — §9 Rule G-02)

**S-08** 한국학중앙연구원. (n.d.). 봉오동전투. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0023974 `[ver2 계승]`
— 인용 위치: §4-5 (CLM-EVENT-027 "사건 발생일", 1920-06)

---

## §4-6. 이종일–보성사 (CLM-039-01, CLM-039-02)

**S-09** 한국학중앙연구원. (n.d.). 보성사. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0023417 `[ver2 계승]`
— 인용 위치: §4-6 (CLM-039-01 "보성사 사장", CLM-039-02 "인쇄 주도")

**S-10** 한국학중앙연구원. (n.d.). 이종일. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0045940 `[ver2 계승]`
— 인용 위치: §4-6 (CLM-039-01, CLM-039-02)

**S-11** 국사편찬위원회. (n.d.). 3·1 독립 선언서. 사료로 본 한국사, 우리역사넷. https://contents.history.go.kr/mobile/hm/view.do?levelId=hm_123_0040 `[ver4 신규]`
— 인용 위치: §4-6 (CLM-039-02 "1919-02-27 인쇄" 보강 근거)

---

## §7. 기타 직접검증 항목 (Claim ID 미부여, 항목명 기준 대응 — v9에서 §4식 Claim으로 전개 예정)

**S-12** 한국학중앙연구원. (n.d.). 신민회. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0032974 `[ver2 계승]`
— 인용 위치: §7 "신민회" 항목, "최광옥(confirmed_indirect)" 항목의 소속 근거로 재사용

**S-13** 한국학중앙연구원. (n.d.). 대성학교. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0014519 `[ver2 계승]`
— 인용 위치: §7 "대성학교" 항목

**S-14** 국사편찬위원회. (n.d.). 독립군 아내들의 헌신. 우리역사넷. https://contents.history.go.kr/front/hm/view.do?levelId=hm_126_0050 `[ver2 계승]`
— 인용 위치: §7 "신흥강습소" 항목, "이회영" 항목의 공동설립 근거로 재사용

**S-15** 한국학중앙연구원. (n.d.). 이시영. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0044990 `[ver2 계승]`
— 인용 위치: §7 "신흥강습소" 항목, "이시영" 항목

**S-16** 한국학중앙연구원. (n.d.). 대한민국 임시정부. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0015017 `[ver2 계승]`
— 인용 위치: §7 "대한민국임시정부" 항목, "이승만" 항목에서 재사용

**S-17** 국사편찬위원회. (n.d.). 대한민국 임시 헌장. 우리역사넷. https://contents.history.go.kr/front/hm/view.do?levelId=hm_123_0060 `[ver2 계승]`
— 인용 위치: §7 "대한민국임시정부" 항목

**S-18** 한국학중앙연구원. (n.d.). 3·1운동. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0026772 `[ver2 계승]`
— 인용 위치: §7 "3·1운동" 항목, "손병희"·"한용운"·"오세창"·"최린"·"정춘수" 항목에서 재사용

**S-19** 한국학중앙연구원. (n.d.). 안악사건. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0034866 `[ver2 계승]`
— 인용 위치: §7 "안악사건" 항목

**S-20** 한국학중앙연구원. (n.d.). 105인 사건. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0022233 `[ver2 계승]`
— 인용 위치: §7 "105인사건" 항목

**S-21** 한국학중앙연구원. (n.d.). 조선물산장려운동. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0052020 `[ver2 계승]`
— 인용 위치: §7 "물산장려운동" 항목 (§4-3의 「조선물산장려회」 S-04와는 별개 항목)

**S-22** 한국학중앙연구원. (n.d.). 안창호. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0035050 `[ver2 계승]`
— 인용 위치: §7 "안창호" 항목

**S-23** 한국학중앙연구원. (n.d.). 조만식. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0051729 `[ver2 계승]`
— 인용 위치: §7 "조만식" 항목

**S-24** 한국학중앙연구원. (n.d.). 유영모. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0041674 `[ver2 계승]`
— 인용 위치: §7 "유영모(오산학교 재직)" 항목

**S-25** 한국학중앙연구원. (n.d.). 안명근. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0034719 `[ver2 계승]`
— 인용 위치: §7 "안명근" 항목

**S-26** 한국학중앙연구원. (n.d.). 이종호. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0045955 `[ver2 계승]`
— 인용 위치: §7 "이종호" 항목

**S-27** 한국학중앙연구원. (n.d.). 손병희. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0030507 `[ver2 계승]`
— 인용 위치: §7 "손병희" 항목 (S-18과 병기)

**S-28** 한국학중앙연구원. (n.d.). 이회영. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0046635 `[ver2 계승]`
— 인용 위치: §7 "이회영" 항목 (S-14와 병기)

**S-29** 한국학중앙연구원. (n.d.). 3·1독립선언서. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0026764 `[ver2 계승]`
— 인용 위치: §7 "오세창" 항목 (S-18과 병기)

**S-30** 한국학중앙연구원. (n.d.). 북로군정서. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0024657 `[ver2 계승]`
— 인용 위치: §7 "서일/북로군정서" 항목

**S-31** 한국학중앙연구원. (n.d.). 대한민국임시정부헌법. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0015021 `[ver2 계승]`
— 인용 위치: §7 "이승만" 항목 (S-16과 병기)

**S-32** 한국학중앙연구원. (n.d.). 최린. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0057276 `[ver2 계승]`
— 인용 위치: §7 "최린" 항목 (S-18과 병기)

---

**비고 1**: §7의 `url_recheck_required` 13건(숭실학교, 보성학교, 신간회, 함석헌, 배위량, 차이석, 이용익, 이동녕, 이상룡, 지청천, 이범석, 박희도, 청산리전투)은 본문에 실제 URL이 제시되지 않으므로 본 부록에도 대응 항목을 두지 않는다. v9에서 실제 Source를 확보하면 `S-33`부터 이어서 `[ver5 신규]` 태그로 추가한다.

**비고 2**: 위 4건(공산주의운동, 이동휘 개인 항목, 신흥무관학교 용어해설, 우리역사넷 오산 학교)은 완전히 폐기된 것이 아니라, 향후 §8 v9 작업 큐(오산학교 동일사건 검토, 이동휘 event type 재검토 등)에서 필요 시 재인용될 수 있는 후보 출처로 §12 change_history 개념에 준해 별도 관리한다.