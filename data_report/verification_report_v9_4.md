# v9.4 검증 보고서

## — Claim 문장·subject/object URI·relation 의미 정합성 검증

> 본 보고서는 「v8 추가검증보고서(ver5, 설계 승인본)」의 형식을 준용하여, v9.3에서 구조적으로는 완결됐으나 의미론적 정합성이 남아 있던 문제를 실제 파일 대조를 통해 검토·수정한 v9.4의 작업 내용과 검증 결과를 정리한다.

---

## 0. 이 보고서가 검증하는 대상

- **입력**: v9.3의 34 Core + 5 Hold + 16 Exclusion
- **출력**:
  - `v9.4_claim_core.csv` (34건)
  - `v9.4_claim_hold.csv` (5건)
  - `v9.4_exclusion_manifest.csv` (16건)
  - `v9.4_gwanhak_claims.ttl`
  - `v9.4_data_dictionary.md`
- **목적**: v9.3까지의 검증이 행 수·CURIE 형식·날짜 형식 등 기계적으로 확인 가능한 정합성에 머물렀던 것을, Claim 문장이 실제 `subject_uri → relation → object_uri` 방향과 일치하는가라는 의미론적 정합성까지 확장한다.

> v9.5와 v8 그리고 c5 csv 파일을 제외한 나머지는 전부 로컬에서 관리하고, git에서는 생략한다.

---

## 1. 문제의 성격 — 형식은 맞지만 의미가 어긋나는 경우

v9.3까지의 자동검증은 CURIE 형식이나 날짜 포맷처럼 구문(syntax) 수준에서 확인 가능한 항목을 대상으로 했다. 실제 파일을 행 단위로 다시 읽은 결과, `claim` 자연어 문장과 `subject_uri`·`object_uri`·`relation` 사이에 의미론적 불일치가 발견됐다.

이러한 문제는 필드 형식만 검사하는 스크립트로는 충분히 검출하기 어렵다. 문장의 실제 주어와 관계 방향, 대상 엔티티가 구조화된 필드와 일치하는지를 사람이 직접 검토해야 하는 유형이다.

---

## 2. 발견·수정한 의미 정합성 문제 7건 (P0)

### 2-1. CLM-014 — subject는 인물인데 문장의 주어는 사건

**문제**

`subject_uri=:안명근`으로 지정되어 있었지만, Claim 문장은 "안명근 사건은 105인 사건의 계기가 된 사건으로 연결된다"는 취지였다. 문장의 실제 주어는 안명근이라는 인물이 아니라 그를 둘러싼 사건이었다.

**수정**

- `subject_uri`를 `:안악사건`으로 정정했다. 해당 URI는 CLM-007에서 사용하던 사건 엔티티 URI를 재사용한다.
- `object_uri`에 `:105인사건`을 지정했다. 해당 URI는 CLM-008에서 사용하던 URI를 재사용한다.
- `relation=related_to`의 대상을 명시했다.
- `item_no`와 `item_name`(26/안명근)은 원본 매핑 출처를 나타내므로 유지했다.
- subject 엔티티가 원본 인물 매핑과 다르다는 사실은 `change_history`에 기록했다.

### 2-2. CLM-003 — 수동태 문장과 subject 방향의 불일치

**문제**

`subject_uri=:이회영`, `relation=설립`, `object_uri=:신흥강습소`였으나 Claim 문장은 "신흥강습소가 … 설립되었다"는 수동태로 신흥강습소를 문장의 주어로 삼고 있었다.

**수정**

Claim 문장을 "이회영 등이 신흥강습소를 설립하였다"로 바꿔 구조화된 방향에 맞췄다. 공동설립자 전원을 주어에 넣으면 다중 주체 문제가 생길 수 있으므로 "등"으로 대표 표기했다. 개별 공동설립자별 Claim은 후속 확장 과제로 남겼다.

### 2-3. CLM-022b — 문장의 복수 주체와 단일 object의 불일치

**문제**

문장에는 "서일·김좌진 등이 주도한"이라고 복수 인물이 등장했지만 `object_uri`는 `:김좌진` 하나뿐이었다.

**검토한 선택지**

- A안: 문장을 김좌진 중심으로 축소한다.
- B안: 서일과 김좌진의 관계를 별도 Claim으로 분리한다. 이 경우 Claim 수가 55건에서 56건으로 증가한다.

**결정 및 수정**

A안을 채택했다. "서일·"을 제거하고 "북로군정서는 김좌진이 주도한 독립군 조직이다"로 정리했다. 서일과 북로군정서의 관계는 별도 Claim인 CLM-022a(item 43)가 다루고 있으므로, 해당 문장에서 서일을 제거해도 이 관계를 다루는 Claim 자체가 사라지는 것은 아니다.

### 2-4~2-7. CLM-046 / CLM-016 / CLM-018 / CLM-019 — relation=`소속`과 문장의 "활동" 사이 의미 간극

**문제**

양기탁(CLM-046), 이종호(CLM-016), 이회영(CLM-018), 이시영(CLM-019) 4건 모두 `relation=소속`으로 되어 있었으나 문장은 "핵심/중심 인물로 활동하였다"는 더 넓은 의미를 표현했다.

Evidence가 소속 관계 자체를 뒷받침하는 것으로 검토됐으므로, relation을 약화하기보다 문장을 relation에 맞춰 명확히 하기로 했다.

**수정**

- CLM-046: "양기탁은 신민회에 소속되어 핵심 인물로 활동하였다."
- CLM-016: "이종호는 신민회에 소속되어 중심 인물로 활동하였다."
- CLM-018: "이회영은 신민회에 소속되어 중심 인물로 활동하였다."
- CLM-019: "이시영은 신민회에 소속되어 중심 인물로 활동하였다."

수정 과정에서 발견한 조사 오류인 "이회영는"→"이회영은", "이시영는"→"이시영은"도 함께 바로잡았다.

---

## 3. date_status 정밀화 (P1) — 6건 중 실제 버그는 1건

v9.3에서 `date_value`가 비어 있으면서 `date_status`가 채워진 6건을 재검토했다.

| Claim | 기존 `date_status` | 판정 |
|---|---|---|
| CLM-010 | `verified` | 버그 — 날짜값이 없는데 검증됨으로 기록한 논리 오류 |
| CLM-046, CLM-035, CLM-KIM-01, CLM-KIM-02, CLM-047 | `not_directly_verified` | 정상 — 날짜가 있을 수 있는 Claim이나 날짜를 직접 확인하지 못했다는 의미로 타당 |

이번 검토에서 다음 두 상태를 구분하는 원칙을 확정했다.

- `not_directly_verified`: 날짜가 있을 수 있으나 직접 확인하지 못함
- `not_applicable`: 해당 Claim이 날짜 assertion 자체를 요구하지 않음

`date_status` 어휘에 `not_applicable`을 추가하고 CLM-010에 적용했다. 나머지 5건은 변경하지 않았다.

---

## 4. exclusion manifest 용어 충돌 해소

`exclusion_manifest.csv`의 `disposition` 값이 v9.3까지 `보류`였으나, `claim_hold.csv`의 "보류"와 혼동될 수 있었다. 이에 16건 전체의 값을 `excluded_from_ttl`로 통일했다.

| 파일 | 의미 |
|---|---|
| `claim_core.csv` | TTL 반영, 판정은 core |
| `claim_hold.csv` | TTL 반영, 판정은 hold |
| `exclusion_manifest.csv` | TTL 미반영, `disposition=excluded_from_ttl`; 삭제가 아님 |

---

## 5. 자동검증 8개

```text
[1] claim_id unique                         : OK (39건)
[2] source_id ↔ title/url 정합성            : OK
[3] source_url 형식                          : OK
[4] CURIE 형식                               : OK
[5] date_value ↔ date_precision 일치         : OK
[6] controlled vocabulary(not_applicable 포함): OK
[7] date_value 없이 verified인 잔존 오류     : OK — 0건
[8] exclusion disposition 통일               : OK — 16건 전부 excluded_from_ttl

[coverage] 49개 item_no 전체 커버             : OK
[coverage] core 34 + hold 5 + exclusion 16    : 55건, OK
```

---

## 6. TTL 재생성 결과

```text
Claim(core+hold) : 39 (core=34, hold=5; claimDecision으로 구분)
트리플 수(rdflib) : 972
TTL claim count = CSV claim count : 39 = 39 (일치)
```

---

## 7. 데이터 사전 신설 및 예시의 시점 관리

`v9.4_data_dictionary.md`를 별도로 작성해 다음 사항을 명문화했다.

- `claim_status`, `verification_status`, `date_status`는 서로 다른 질문에 답하는 독립 필드다.
- `not_directly_verified`와 `not_applicable`은 구분된다.
- `review_flag`와 판정(decision)은 같은 개념이 아니다.
- v1~v8 TTL 본체의 `hasEestimation`과 v9 계열의 `has_estimation`은 이름이 비슷하지만 독립적으로 설계된 속성이다.
- CSV 22개 컬럼은 v9.1부터 고정되어 있으므로 컬럼을 늘리지 않고 별도 문서에서 의미를 보강한다.

### 7-1. 실제 Claim을 예시로 사용할 때의 시점 표시

데이터 사전에서 실제 Claim ID와 필드값을 예시로 인용하는 경우, 해당 예시가 특정 릴리스 시점의 스냅샷임을 표시한다. 예시는 이후 데이터 변경에 따라 현재 CSV 값과 달라질 수 있다.

v9.4 데이터 사전의 CLM-OSAN-01/02 예시는 v9.4 시점의 사례로 취급한다. 후속 릴리스에서 동일 Claim의 `review_flag`가 바뀌더라도, 그것만으로 과거 문서가 당시의 기록을 잘못 설명했다고 단정하지 않는다. 다만 현재 상태를 설명하는 문서처럼 읽히지 않도록 시점을 명시해야 한다.

---

## 8. 의도적으로 손대지 않은 것 (P2, 후속 과제)

- `related_to`, `해당`, `조직`, `조직관계` 등 relation vocabulary의 전면 정규화
- `decision`을 별도 machine-readable 컬럼으로 분리할지 여부
- CLM-002/CLM-011의 대성학교 설립 주장 통합 여부 — 동일 Claim과 복수 Evidence로 통합할지 검토
- SHACL 셰이프를 통한 수동 검사의 자동화
- master Claim registry 기반 파이프라인 전환 — CLM-023의 반복 재발이 드러낸 재현성 문제의 근본 해법
- 실제 Claim 예시와 릴리스 데이터의 시점 일치 여부를 점검하는 절차의 도입

### 8-1. Rule P-05 — 문서-데이터 시점 불일치 관리

1. 실제 `claim_id`와 필드값을 문서에 인용할 때는 해당 예시가 현재 상태, 특정 릴리스 스냅샷, 역사적 변경 기록 중 무엇인지 표시한다.
2. 가능한 경우 추상 예시를 우선 사용한다. 실제 Claim 예시를 사용한다면 릴리스 버전 또는 기준일을 함께 기록한다.
3. 현재 상태를 설명하는 문서는 해당 릴리스의 CSV와 대조한다.
4. `change_history`는 과거 판단을 보존하는 누적 기록이므로 과거 내용을 현재 판단으로 덮어쓰지 않는다. 다만 각 기록의 시점과 버전을 가능한 한 식별할 수 있게 한다.
5. 릴리스 체크리스트에서 문서 예시와 데이터의 시점·값 일치 여부를 점검한다.
6. 불일치는 다음 유형으로 분류한다.
   - 데이터 오류
   - 정당한 역사적 차이
   - 문서 갱신 누락
   - 원인 미확정

---

## 9. 결론

| 항목 | 판정 |
|---|---|
| Claim 문장↔URI↔relation 의미 정합성 7건 수정 | 완료 |
| date_status 정밀화 — 실제 버그 1건 수정 | 완료 |
| exclusion disposition 명칭 충돌 해소 | 완료 |
| 자동검증 8개 | 전부 통과 |
| TTL 재생성 및 Claim 수 일치 | 확인 |
| 데이터 사전 작성 | 완료 |
| 실제 예시의 릴리스 시점 관리 원칙 | Rule P-05로 명문화 |

v9.1~v9.4의 검증 흐름은 "구조적으로 유효한가"(v9.1) → "신뢰도로 거를 수 있는가"(v9.2) → "거른 결과를 어떻게 세분화·명명할 것인가"(v9.3) → "문장과 구조가 실제로 같은 것을 말하는가"(v9.4)로 심화됐다.

이는 v8 검증보고서 ver5 §9의 Schema/Source/Evidence/Claim/Date/Relation/Existence/Provenance validation 구분과 대응한다. v9.4는 그중 Relation validation, 즉 subject/object 관계가 실제로 맞는지에 대한 검토를 본격적으로 수행한 단계로 볼 수 있다.

### 부록 A. v8 검증보고서(ver5) 조항과의 대응

| v8 보고서 조항 | v9.4에서의 적용 |
|---|---|
| §2-1 `claim_status` 부여 기준 | CLM-046/016/018/019에서 문장을 relation에 맞춰 강화할지 판단하는 기준 |
| §11 Rule P-04(출처 충돌 보존) | CLM-014의 subject 정정에서도 기존 `change_history`를 삭제하지 않고 변경을 기록 |
| §12 Rule G-01(event type을 슬래시로 묶지 않음) | CLM-022b에서 문장과 단일 object의 불일치를 해소 |
| §9 Source Mapping 데이터 구조 | 22개 컬럼 고정 및 decision을 `change_history`로 기록하는 구조 |

### 부록 B. v9.4 데이터 사전의 예시 적용 범위

데이터 사전의 실제 Claim 예시는 v9.4 릴리스 시점에 한정된 스냅샷이다. 후속 릴리스의 CSV와 필드값이 다를 경우, 릴리스 간 변경인지 문서 갱신 누락인지 구분해 기록한다. 이 원칙은 v9.5에서 Rule P-05로 구체화한다.