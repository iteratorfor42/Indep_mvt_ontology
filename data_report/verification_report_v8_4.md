# v8 추가 검증 보고서 (ver4)

## — 49개 항목 Source Mapping 1차 검증 및 Provenance Layer 설계 보고서

> **버전 이력**: ver1(v8 RDF 구조검증) → ver2(49개 항목 URL 팩트체크 초안) → ver3(Claim/Evidence/Source 분리, 상태값 이원화, 변경이력 보존 도입) → **ver4(김좌진 정정, Claim 추가 분해, status vocabulary 3층+flag 구조로 재정리, naming convention 통일)**

---

# 0. 핵심 설계 원칙 (v9까지 관통하는 5원칙)

```text
Claim status  ≠  Date status
Claim         ≠  Event date
Source        ≠  Evidence
Evidence      ≠  Claim
Negative evidence  ≠  Contradiction
Old value     ≠  Deleted value
```

이 여섯 줄이 ver4 전체 구조의 근거다. 아래 모든 사례 재작성과 상태값 재설계는 이 원칙을 실제 데이터에 적용한 결과다.

---

# 0-1. ver3 → ver4 변경 요약

| No | 변경 내용 | 근거 |
|---|---|---|
| 1 | **김좌진–신민회를 관계보류 → confirmed로 정정** | 「김좌진」 항목 본문에 "신민회에 가입하였다"는 직접 서술 확인 |
| 2 | 오산학교: `date_status`와 별도로 `date_value_status = provisional` 필드 신설, 설립/개교를 별개 Claim으로 분리 | "값을 낮춰 채택"과 "값이 확정됨"을 구별하기 위함 |
| 3 | 이동휘: CLM-A(선임/취임, 1919-08말)와 CLM-B(통합임시정부 합동 취임식, 1919-11-03)로 Claim 분리 | 두 날짜가 같은 종류의 사건인지 먼저 판단해야 함 |
| 4 | 조선물산장려회: "1920년 8월 조직"과 "1920-08-23 조직"을 별개 Claim으로 분리 | claim_status를 날짜 단위까지 섞어 쓰지 않기 위함 |
| 5 | 홍범도: 참여 Claim / 사건 Claim / 참여일 Claim 3단으로 재정리, 참여일 Claim은 `validation_hold`로 하향 | "참여는 확정, 참여일은 미확정"을 더 정확히 표현 |
| 6 | 이종일–보성사: "사장이었다" Claim과 "인쇄를 주도했다" Claim을 분리 | Evidence 문장과 Claim을 1:1로 맞추기 위함 |
| 7 | `claim_status` / `date_status` / `verification_status`를 세 개의 독립 층위로 재정의 | 세 필드가 서로 겹치던 문제 해소 |
| 8 | `관계보류`·`출처충돌`을 verification_status에서 분리해 별도의 `review_flag`로 이동 | 진행상태(검증 프로세스)와 발견문제(판정)를 구분 |
| 9 | `hasEestimation` 오타를 `hasEstimation`(RDF)/`has_estimation`(CSV)으로 통일, naming convention 명시 | 표기 일관성 확보 |
| 10 | `has_estimation`의 정의를 "원자료에 없는 값을 연구자가 추론/범위화한 경우"로 한정 | `date_status`와의 중복 축소 |
| 11 | Negative Evidence 예시에서 김좌진 사례 제거, 추상 템플릿으로 대체하고 실제 사례는 v9 작업 큐로 이관 | 검증되지 않은 사실을 예시로 남기지 않기 위함 |
| 12 | 참고문헌에 출처 인벤토리 태그(ver2 계승 / ver4 신규) 추가, 신규 출처 3건 반영 | 어떤 출처가 이번에 새로 편입됐는지 추적 가능하게 함 |
| 13 | §8(49개 항목 재분류)을 "항목 단위는 보조 지표, Claim 단위가 권위값"이라는 원칙으로 재정의 | 항목 하나가 "직접검증"이어도 내부 개별 Claim은 상태가 다를 수 있음을 명시 |

---

# 1. 검증 목적 (유지)

v8 RDF와 CSV의 각 사실을 다시 출처까지 역추적해 다음 구조를 확립하고자 했다.

> **개체/사건 → 주장(Claim) → 근거(Evidence) → 출처(Source) → 관계(Relation) → 날짜(Date)**

Source와 Evidence는 분리했다. 같은 페이지(Source) 안에서도 서로 다른 문장(Evidence)이 서로 다른 Claim을 뒷받침할 수 있기 때문이다.

---

# 2. 상태값 체계 v4 — 3층 + review_flag 구조

ver3까지는 `claim_status`, `date_status`, `verification_status`가 실질적으로 겹치는 문제가 있었다. ver4에서는 세 필드의 층위를 명확히 분리하고, "관계보류/출처충돌"처럼 발견된 문제를 나타내는 값은 별도의 `review_flag`로 뺐다.

## 2-1. claim_status — 역사적 주장 자체의 상태

```text
confirmed              # 주장 자체가 직접 근거로 확인됨
confirmed_indirect      # 간접 근거(명단 등)로 확인됨
validation_hold        # 근거 부족·충돌로 보류
contradicted           # 근거와 모순됨
```

## 2-2. date_status — 날짜의 상태

```text
verified               # 날짜가 1차/공식 자료로 직접 확인됨
inferred               # 상위 사건의 날짜에서 유추, 개인 참여일에 자동 적용 금지
estimated              # 범위 추정
conflicting_sources    # 출처마다 날짜가 다름
not_directly_verified  # 날짜 근거 자체가 아직 확인되지 않음
```

## 2-3. verification_status — 이번 검증 프로세스가 무엇을 했는가 (진행 상태만)

```text
directly_verified       # Evidence를 직접 찾아 확인함
partially_verified      # URL은 확인했으나 세부 주장 일부만 확인됨
url_recheck_required    # 실제 URL을 아직 확보하지 못함
```

## 2-4. review_flag — 검증 중 발견된 문제 (신설, verification_status에서 분리)

```text
none                 # 특이사항 없음
relationship_issue    # 관계의 성격/동일성 자체를 추가 검토해야 함 (예: 설립 vs 개교가 같은 사건인지)
source_conflict       # 복수의 공식 출처가 서로 다른 값을 제시
provenance_gap        # 기존 CSV 값의 최초 출처를 역추적하지 못함
```

> `claim_status` = 지식그래프의 판단 / `date_status` = 날짜의 판단 / `verification_status` = 이번 검증 작업의 진행 상태 / `review_flag` = 발견된 문제의 종류. 네 필드는 서로 독립적으로 부여한다.

---

# 3. Naming Convention 통일

ver3까지 `hasEestimation`(오타), `has_estimation`(CSV)이 혼재했다. ver4에서 다음과 같이 통일했다.

```text
RDF 속성 (PascalCase 프로퍼티명, has- 접두):
  :hasEstimation
  :hasValidationStatus
  :hasReviewFlag

CSV 컬럼 (snake_case):
  has_estimation
  claim_status
  date_status
  verification_status
  review_flag
```

## 3-1. has_estimation의 재정의

`date_status`(estimated 등)와 중복되지 않도록 범위를 좁혔다.

```text
has_estimation = true
  → 원자료에 명시된 날짜가 아니라, 연구자가 상위 사건 날짜 등에서 추론하거나
    범위화(예: ±2개월)하여 만든 값인 경우에만 true
```

원자료에 날짜가 직접 쓰여 있으면 `date_precision`만으로 표현하고 `has_estimation`은 false로 둔다.

---

# 4. 핵심 사례 재작성

## 4-1. 김좌진 — 신민회 (정정: 관계보류 → confirmed)

### ver3까지의 판정 (오류)

```text
김좌진–신민회 = 관계보류
negative_evidence = "신민회 공식 명단에서 김좌진을 확인하지 못함"
```

### ver4 정정

한국민족문화대백과사전 「김좌진」 항목 본문에 다음이 직접 서술되어 있었다.

> "계몽운동에 적극 나섰다. 신민회에 가입하였고 청년학우회에서도 활동하였다."

```text
CLM-KIM-01
Claim: 김좌진이 신민회에 가입하였다
Source: 한국민족문화대백과사전 「김좌진」 (신규 출처, https://encykorea.aks.ac.kr/Article/E0010528)
Evidence: "신민회에 가입하였고 청년학우회에서도 활동하였다"

claim_status = confirmed
date_status = not_directly_verified   # 가입 시점의 구체적 일자는 미확인
verification_status = directly_verified
review_flag = none
```

이 정정 자체가 ver3가 강조한 "Claim 단위 검증"의 실제 사례다 — 조직의 **명단** 자료만으로 관계를 판단하지 않고, **인물 항목의 직접 서술**도 Evidence로 함께 검색해야 한다는 교훈을 남겼다.

---

## 4-2. 이승훈 — 오산학교 (설립/개교 Claim 분리)

### 문제의 재정의

기존에는 "설립일"이라는 하나의 값을 두고 두 출처(12월/11월 24일)가 경쟁하는 것처럼 다뤘다. 그러나 실제로는 서로 다른 종류의 서술이었다.

* 「오산고등학교」: 학교 연혁 기준 **1907년 12월 설립**
* 「이승훈」: 인물 활동 연혁 기준 **1907년 11월 24일 개교**

### ver4 Claim 분리

```text
CLM-OSAN-01
Claim: 이승훈이 오산학교를 설립하였다
Source: 「오산고등학교」
Evidence: "1907년 12월 … 오산학교로 설립"
date_value = 1907-12
date_precision = Month
claim_status = confirmed
date_status = verified
date_value_status = provisional   # 신설: "현재 채택한 최선값"이라는 뜻이며 "확정"과는 다름

CLM-OSAN-02
Claim: 이승훈이 오산학교를 개교하였다
Source: 「이승훈」
Evidence: "이 해 11월 24일 … 오산학교를 개교"
date_value = 1907-11-24
date_precision = Day
claim_status = confirmed
date_status = verified

Entity-level:
review_flag(이승훈-오산학교) = relationship_issue + source_conflict
  # ① 설립일과 개교일이 동일 사건을 가리키는지 여부가 아직 검토되지 않음
  # ② 두 Claim의 날짜값 자체가 서로 다름
```

`date_value_status = provisional`을 신설한 이유는, "값을 낮춰 저장한다"와 "그 값이 사실상 확정됐다"가 서로 다른 주장이기 때문이다. `1907-12`는 CLM-OSAN-01 안에서는 `verified`이지만, 엔티티 전체로 보면 `review_flag = source_conflict`가 함께 붙어 "최선값이되 잠정값"임을 표시한다.

기존 change_history는 그대로 유지했다.

```text
change_history:
  old_value = 1907-12-24
  old_status = confirmed
  new_value = 1907-12 (CLM-OSAN-01 기준)
  reason = "학교 연혁 자료는 12월까지만 지지, 24일이라는 일자의 직접 근거 미확인.
            단, 인물 항목은 11월 24일 개교를 별도로 명시하므로 동일 사건 여부 자체를 재검토 대상으로 둠"
```

---

## 4-3. 조선물산장려회 (월 단위 Claim / 일 단위 Claim 분리)

```text
CLM-JOSEON-01
Claim: 1920년 8월 조선물산장려회가 조직되었다
Source: 「조선물산장려회」
Evidence: "조만식·오윤선·김동원·김보애 등 70인이 발기·조직"
date_value = 1920-08
date_precision = Month
claim_status = confirmed
date_status = verified
verification_status = directly_verified
review_flag = none

CLM-JOSEON-02
Claim: 조선물산장려회가 1920년 8월 23일에 조직되었다
date_value = 1920-08-23
date_precision = Day
claim_status = validation_hold        # 날짜가 포함된 별도 Claim으로 취급
date_status = not_directly_verified
verification_status = url_recheck_required
review_flag = provenance_gap          # 기존 CSV에 8/23이 어떻게 들어갔는지 출처 역추적 필요

change_history:
  old_value = 1920-08-23 (CLM 전체가 confirmed였던 상태)
  new_structure = "월 단위 Claim(confirmed)과 일 단위 Claim(validation_hold)으로 분리"
```

---

## 4-4. 이동휘 (선임 Claim / 공식 취임식 Claim 분리)

기존에는 "임시정부 국무총리 취임일"을 하나의 conflicting_sources 값으로 뭉뚱그렸다. 그러나 확인된 자료는 사실 서로 다른 종류의 사건을 가리킬 가능성이 있었다.

* 한국민족문화대백과사전 「고려공산당」: 1919년 8월 말 상해 도착, 임시정부 초대 국무총리 취임
* 국사편찬위원회 한국 근대 사료 DB(대한민국임시정부자료집): 1919년 11월 3일 국무총리 이동휘 등의 **합동 취임식**

```text
CLM-LEE-A
Claim: 이동휘가 임시정부 국무총리로 선임/취임하였다
Source: 「고려공산당」
date_value = 1919-08 (말)
date_precision = Month
claim_status = confirmed
date_status = verified

CLM-LEE-B
Claim: 이동휘가 포함된 통합임시정부 국무원 합동 취임식이 거행되었다
Source: 한국 근대 사료 DB — 대한민국임시정부자료집 (신규 출처,
        https://db.history.go.kr/modern/level.do?levelId=ij_045_0020_00010_0090)
date_value = 1919-11-03
date_precision = Day
claim_status = confirmed
date_status = verified

Entity-level:
review_flag(이동휘-임시정부) = relationship_issue
  # CLM-LEE-A(선임/부임)와 CLM-LEE-B(통합정부 공식 합동취임식)가
  # 같은 종류의 사건인지, 아니면 "선임"과 "취임식"이라는 서로 다른 단계인지
  # 아직 판단하지 않음 → v9 작업 큐로 이관
```

이전 버전의 `date_status = conflicting_sources` 판정은 성급했다. 실제로는 날짜가 "충돌"하는 것이 아니라 **서로 다른 사건을 가리킬 가능성**이 있으므로 Claim을 분리하는 것이 ver3가 제시한 원칙(§5, 사건 날짜 자동상속 금지)의 올바른 적용이다.

---

## 4-5. 홍범도 (참여 Claim / 사건 Claim / 참여일 Claim 3단 구조)

```text
CLM-027-04
Claim: 홍범도가 봉오동전투에 참여하였다
claim_status = confirmed
date_status = null            # 참여 사실 자체에는 날짜 속성을 부여하지 않음
verification_status = directly_verified

CLM-EVENT-027
Claim: 봉오동전투는 1920년 6월에 발생하였다
Source: 「봉오동전투」
claim_status = confirmed
date_status = verified

CLM-027-06
Claim: 홍범도의 봉오동전투 참여일 = 1920-06
claim_status = validation_hold      # "참여했다"는 confirmed이지만 "그 시점이 사건일과 정확히 같다"는 아직 미확정
date_status = inferred
verification_status = partially_verified
review_flag = none
```

이전 ver3에서는 CLM-027-06의 `claim_status`를 명시하지 않고 `date_status = inferred`만 두었는데, 이는 "참여 사실"과 "참여일"의 확신도 차이를 흐리게 만든다. ver4에서는 참여일 Claim 자체의 `claim_status`를 `validation_hold`로 낮춰, "인물의 참여 사실은 확정할 수 있어도 참여일은 자동으로 확정하지 않는다"는 원칙을 명시적으로 반영했다.

---

## 4-6. 이종일 — 보성사 (경영 Claim / 인쇄 Claim 분리)

```text
CLM-039-01
Claim: 이종일은 1919년 당시 보성사 사장이었다
Source A: 「보성사」 (https://encykorea.aks.ac.kr/Article/E0023417)
Source B: 「이종일」 (https://encykorea.aks.ac.kr/Article/E0045940)
claim_status = confirmed
date_status = verified (1919-02 시점 기준)

CLM-039-02
Claim: 이종일이 1919년 2월 27일 보성사에서 독립선언서 인쇄를 주도하였다
Source A: 「보성사」 — "사장 이종일 … 독립선언서를 인쇄"
Source C: 우리역사넷 「사료로 본 한국사 — 3·1 독립 선언서」 (신규 출처,
          https://contents.history.go.kr/mobile/hm/view.do?levelId=hm_123_0040)
          — "보성사 사장 이종일이 1919년 2월 27일 밤부터 21,000부를 인쇄"
date_value = 1919-02-27
date_precision = Day
claim_status = confirmed
date_status = verified
```

Evidence와 Claim을 1:1로 맞추면 "경영했다"(직함/역할)와 "인쇄를 주도했다"(구체적 행위)를 분리해서 관리할 수 있다.

---

# 5. Negative Evidence 원칙 (원칙 유지, 예시 교체)

원칙은 그대로 유지했다.

> **"자료에 없었다" ≠ "그런 일이 없었다"**

다만 김좌진 사례는 §4-1에서 confirmed로 정정되었으므로 더 이상 negative evidence 예시로 쓸 수 없다. ver4에서는 실제로 검증되지 않은 특정 인물을 단정적으로 예시화하는 대신, 추상 템플릿으로 원칙만 제시하고 **실제 사례 발굴은 v9 작업 큐(§7)로 이관**한다.

```text
(추상 템플릿)
evidence_type = negative
evidence_note = "확인한 [출처 X, 출처 Y]에서 [인물]–[조직] 관계를 확인하지 못함"
claim_status = validation_hold
review_flag = provenance_gap
```

> 실제 negative evidence 사례는 §8의 "URL재확인필요" 13건을 Claim 단위로 조사하는 과정에서 자연스럽게 발견될 것이며, 발견 즉시 인물 항목 본문까지 교차검색한 뒤 확정한다(§4-1의 교훈 적용).

---

# 6. §8 관련 원칙 — 항목 단위는 보조 지표, Claim 단위가 권위값

"홍범도 → 직접검증"처럼 항목 단위로 쓰면 그 인물의 모든 주장이 검증되었다는 인상을 준다. 그러나 실제로는 §4-5처럼 한 인물 안에 `confirmed`, `validation_hold`가 섞여 있을 수 있다.

따라서 v9 CSV에서는:

* **항목 단위 상태**(아래 §7의 표)는 **보조 지표**로만 사용한다 (대략적인 진행 현황 파악용).
* **개별 Claim의 `claim_status`/`date_status`가 권위값(authoritative)**이며, 항목 단위 상태와 불일치할 경우 Claim 단위가 우선한다.

---

# 7. 49개 항목 재분류 (verification_status + review_flag 모델 적용)

### verification_status = directly_verified (핵심 근거 확보, review_flag = none 다수)

신민회, 대성학교, 신흥강습소(공동설립 4인), 대한민국임시정부, 보성사/이종일(§4-6), 3·1운동, 안악사건, 105인사건, 봉오동전투(사건 자체), 물산장려운동, 안창호, 조만식, 유영모(오산학교 재직), 안명근, 홍범도(참여 사실, §4-5), 이종호, 손병희, 이회영, 이시영(신흥강습소), 한용운, 오세창, 서일/북로군정서, 이승만, 최린, 정춘수(33인 서명), **김좌진(신민회 가입, §4-1로 정정)**

### verification_status = directly_verified, review_flag = source_conflict / relationship_issue

* 이승훈–오산학교 (§4-2: 설립/개교 Claim 분리 필요)
* 이동휘–임시정부 (§4-4: 선임/취임식 Claim 분리 필요)

### verification_status = directly_verified(월 단위) / url_recheck_required(일 단위), review_flag = provenance_gap

* 조선물산장려회 (§4-3)

### verification_status = url_recheck_required (v9 작업 큐, §8)

숭실학교, 보성학교, 신간회, 함석헌, 배위량, 최광옥(현재는 신민회 명단으로 소속만 간접확인 → confirmed_indirect), 차이석, 이용익, 이동녕, 이상룡, 지청천, 이범석, 박희도, 청산리전투(사건-개인 참여일 분리 필요, §4-5와 동일 원칙 적용)

---

# 8. v9 작업 큐 (갱신)

1. 오산학교: 설립(CLM-OSAN-01)과 개교(CLM-OSAN-02)가 동일 사건인지 1차 사료로 재검토
2. 조선물산장려회: `1920-08-23`이 기존 CSV에 어떻게 들어갔는지 최초 출처 역추적 (`provenance_gap`)
3. 이동휘: "선임/취임"과 "합동 취임식"이 임시정부사에서 통상 구분되는 개념인지 재검토
4. 나머지 13건(§7) URL 확보 — 특히 청산리전투는 사건 날짜와 개인 참여 날짜를 처음부터 별도 Claim으로 설계
5. Negative Evidence 실제 사례 1건 이상 확정 (§5 템플릿 적용)
6. 49개 항목 전체를 Claim 단위로 재작성 (§4의 6개 사례를 표준 패턴으로 확산 적용)

---

# 9. Source Mapping 최소 데이터 구조 (ver4)

```text
source_id
evidence_id
claim_id
subject_uri
claim
relation
object_uri
date_value
date_precision
date_value_status        # 신설: provisional / final
has_estimation            # 재정의: 연구자 추론값에만 true
claim_status               # confirmed / confirmed_indirect / validation_hold / contradicted
date_status                 # verified / inferred / estimated / conflicting_sources / not_directly_verified
verification_status          # directly_verified / partially_verified / url_recheck_required
review_flag                   # none / relationship_issue / source_conflict / provenance_gap
source_title
source_url
evidence_note
change_history
verification_date
```

---

# 10. v9 작업 순서 (로드맵, 우선순위 갱신)

피드백에서 제시된 순서를 그대로 채택했다.

```text
① 김좌진 정정 반영                     ← §4-1 (완료, 본 문서에 반영)
 ↓
② 이동휘 Claim 분해                    ← §4-4 (완료, 본 문서에 반영)
 ↓
③ 오산학교 Claim 분해                  ← §4-2 (완료, 본 문서에 반영)
 ↓
④ status vocabulary 정규화             ← §2, §3 (완료, 본 문서에 반영)
 ↓
⑤ 49개 전체 Claim CSV 작성             ← §8의 작업 큐, v9의 본 작업
```

①~④는 ver4에서 설계 수준까지 반영했다. ⑤(49개 전체를 Claim 단위 CSV로 전개하는 작업)가 v9의 실제 본 작업이다.

---

# 11. ver4 결론

| 영역 | 판정 |
|---|---|
| 전체 설계 방향 | 통과 |
| Claim/Evidence/Source 분리 | 통과 |
| claim_status/date_status/verification_status 3층 분리 | 통과 (ver4에서 재정의) |
| review_flag 분리 | 통과 (ver4 신설) |
| 사건 날짜 자동상속 금지 | 통과, §4-5·§4-4에서 실제 적용 |
| 변경이력 보존 | 통과 |
| 김좌진–신민회 | **정정 완료 (confirmed)** |
| 오산학교 | Claim 분리 완료, review_flag=relationship_issue+source_conflict로 재표시 |
| 조선물산장려회 | Claim 분리 완료 |
| 이동휘 | Claim 분리 완료 |
| 보성사/이종일 | Claim 분리 완료 |
| 홍범도 | 3단 Claim 구조로 재정리 완료 |
| hasEestimation 오타 | 수정 완료 (hasEstimation/has_estimation) |
| Negative Evidence 예시 | 김좌진 사례 제거, 추상 템플릿으로 대체, 실제 사례는 v9 큐로 이관 |
| 49개 Claim 단위 완성 | 미완료 — v9 본 작업 (§10-⑤) |

ver4는 "설계안"으로서는 사실상 완결되었다고 볼 수 있다. 남은 것은 §10-⑤, 즉 49개 항목 전체를 본 문서의 6개 표준 사례(§4-1~§4-6) 패턴에 따라 Claim 단위 CSV로 전개하는 작업이며, 이것이 v9의 실질적 본 작업이다.

---

# 부록. 참고문헌 (APA 형식)

발행처는 **한국학중앙연구원**(한국민족문화대백과사전, encykorea.aks.ac.kr), **국사편찬위원회**(우리역사넷 contents.history.go.kr / 한국사데이터베이스 db.history.go.kr)이며, 접속일은 2026년 8월 29일 기준이다. 각 항목에 출처 인벤토리 태그를 표기했다: `[ver2 계승]` = ver2에서부터 사용, `[ver4 신규]` = 이번 ver4 피드백 반영 과정에서 새로 확인·추가된 출처.

## 한국민족문화대백과사전 (encykorea.aks.ac.kr) — 발행: 한국학중앙연구원

한국학중앙연구원. (n.d.). 3·1독립선언서. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0026764 `[ver2 계승]`

한국학중앙연구원. (n.d.). 3·1운동. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0026772 `[ver2 계승]`

한국학중앙연구원. (n.d.). 105인 사건. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0022233 `[ver2 계승]`

한국학중앙연구원. (n.d.). 고려공산당. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0003430 `[ver2 계승]`

한국학중앙연구원. (n.d.). 공산주의운동. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0004340 `[ver2 계승]`

한국학중앙연구원. (n.d.). 김좌진. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0010528 `[ver4 신규]`

한국학중앙연구원. (n.d.). 대성학교. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0014519 `[ver2 계승]`

한국학중앙연구원. (n.d.). 대한민국 임시정부. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0015017 `[ver2 계승]`

한국학중앙연구원. (n.d.). 대한민국임시정부헌법. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0015021 `[ver2 계승]`

한국학중앙연구원. (n.d.). 보성사. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0023417 `[ver2 계승]`

한국학중앙연구원. (n.d.). 봉오동전투. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0023974 `[ver2 계승]`

한국학중앙연구원. (n.d.). 손병희. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0030507 `[ver2 계승]`

한국학중앙연구원. (n.d.). 신민회. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0032974 `[ver2 계승]`

한국학중앙연구원. (n.d.). 안명근. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0034719 `[ver2 계승]`

한국학중앙연구원. (n.d.). 안악사건. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0034866 `[ver2 계승]`

한국학중앙연구원. (n.d.). 안창호. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0035050 `[ver2 계승]`

한국학중앙연구원. (n.d.). 오산고등학교. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0038302 `[ver2 계승]`

한국학중앙연구원. (n.d.). 유영모. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0041674 `[ver2 계승]`

한국학중앙연구원. (n.d.). 이동휘. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0044080 `[ver2 계승]`

한국학중앙연구원. (n.d.). 이승훈. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0044964 `[ver2 계승]`

한국학중앙연구원. (n.d.). 이시영. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0044990 `[ver2 계승]`

한국학중앙연구원. (n.d.). 이종일. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0045940 `[ver2 계승]`

한국학중앙연구원. (n.d.). 이종호. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0045955 `[ver2 계승]`

한국학중앙연구원. (n.d.). 이회영. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0046635 `[ver2 계승]`

한국학중앙연구원. (n.d.). 조만식. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0051729 `[ver2 계승]`

한국학중앙연구원. (n.d.). 조선물산장려운동. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0052020 `[ver2 계승]`

한국학중앙연구원. (n.d.). 조선물산장려회. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0052021 `[ver2 계승]`

한국학중앙연구원. (n.d.). 최린. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0057276 `[ver2 계승]`

한국학중앙연구원. (n.d.). 홍범도. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0064093 `[ver2 계승]`

한국학중앙연구원. (n.d.). 북로군정서. 한국민족문화대백과사전. https://encykorea.aks.ac.kr/Article/E0024657 `[ver2 계승]`

## 우리역사넷 (contents.history.go.kr) — 발행: 국사편찬위원회

국사편찬위원회. (n.d.). 대한민국 임시 헌장. 우리역사넷. https://contents.history.go.kr/front/hm/view.do?levelId=hm_123_0060 `[ver2 계승]`

국사편찬위원회. (n.d.). 독립군 아내들의 헌신. 우리역사넷. https://contents.history.go.kr/front/hm/view.do?levelId=hm_126_0050 `[ver2 계승]`

국사편찬위원회. (n.d.). 신흥무관학교 (용어해설). 우리역사넷. https://contents.history.go.kr/front/tg/list.do?ganada=전체&pageIndex=3&pageUnit=20&treeId=0202 `[ver2 계승]`

국사편찬위원회. (n.d.). 오산 학교. 우리역사넷. https://contents.history.go.kr/mobile/tg/view.do?levelId=tg_004_2280 `[ver2 계승]`

국사편찬위원회. (n.d.). 3·1 독립 선언서. 사료로 본 한국사, 우리역사넷. https://contents.history.go.kr/mobile/hm/view.do?levelId=hm_123_0040 `[ver4 신규]`

## 한국사데이터베이스 (db.history.go.kr) — 발행: 국사편찬위원회

국사편찬위원회. (n.d.). 대한민국임시정부자료집 — 국무원 합동 취임식. 한국 근대 사료 DB. https://db.history.go.kr/modern/level.do?levelId=ij_045_0020_00010_0090 `[ver4 신규]`

---

**비고**: §7의 url_recheck_required 13건(숭실학교, 보성학교, 신간회, 함석헌, 배위량, 차이석, 이용익, 이동녕, 이상룡, 지청천, 이범석, 박희도, 청산리전투)은 본 보고서 원문에 실제 URL 문자열이 제시되지 않아 참고문헌 목록에 포함하지 않았다. v9에서 실제 URL을 확보한 뒤 동일한 형식(태그 `[ver5 신규]` 등)으로 추가한다.