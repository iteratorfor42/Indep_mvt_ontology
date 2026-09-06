# v9.1 검증 보고서

## — Pre-TTL Clean CSV 및 1차 TTL 구조 검증

> 본 보고서는 "v8 추가검증보고서(ver5, 설계 승인본)"의 형식(§0 핵심 설계 원칙 → §2 상태값 체계 → §4 핵심 사례 → 결론 → 부록 순)을 준용하여, v9 완성본(55 Claim)을 TTL로 변환하기 직전 단계인 v9.1의 작업 내용과 검증 결과를 정리한다.

---

## 0. 이 보고서가 검증하는 대상

- **입력**: v9 완성본 CSV (49개 원본 항목 전체 매핑, 55개 Claim — ver5 §4에서 설계된 6개 표준 Claim 패턴을 실제 적용한 결과)
- **출력**: `v9.1_claim_pre_ttl_clean.csv`(55행), `v9.1_gwanhak_claims.ttl`
- **목적**: "TTL 생성 자체는 시작해도 되지만, 먼저 CSV에 대한 pre-TTL cleanup을 한 번 거쳐야 한다"는 외부 피드백에 따라, TTL 변환 전 데이터 정합성을 확보하는 것

## 1. 핵심 설계 원칙 (v8 보고서 §0 계승)

v9.1은 v8 추가검증보고서 ver5에서 확정된 다음 원칙을 그대로 따른다.

```text
Claim status  ≠  Date status
Claim         ≠  Event date
Source        ≠  Evidence
Evidence      ≠  Claim
Negative evidence  ≠  Contradiction
Old value     ≠  Deleted value
```

여기에 TTL 변환에 특화된 원칙 하나를 추가한다.

```text
구조적으로 유효한 것  ≠  신뢰도가 검증된 것
```

v9.1의 TTL은 55개 Claim **전체**를 담는다 — 이는 신뢰도로 거른 결과가 아니라, "TTL로 파싱 가능한 형태로 구조를 맞췄다"는 뜻이다. 신뢰도별 분리는 이후 v9.2의 몫으로 이미 예정되어 있었다(ver5 Rule G-01~G-08, v9 로드맵 §11).

## 2. Pre-TTL Cleanup에서 발견·수정한 문제 2건

TTL 변환 전 자동검증을 돌리기 전에, 수작업으로 먼저 짚어야 했던 문제가 두 가지 있었다.

### 2-1. CLM-023(이승만) — source/evidence 오배정

**문제**: `source_id=SRC-004`, `evidence_id=EVD-004`를 갖고 있었는데, 이 ID는 원래 대한민국임시정부(§10, E0015017)에 배정된 것이었다. 그런데 CLM-023의 `source_title`/`source_url`은 실제로는 대한민국임시정부헌법(E0015021)을 가리키고 있었다 — **같은 ID 아래 서로 다른 두 문서가 뒤섞여 있던 것**이다.

**수정**: 전용 `SRC-113`/`EVD-113`으로 분리하고, 대한민국임시정부(SRC-004)와의 관계는 `evidence_note`에 별도로 명시했다.

```text
change_history: "v9.1: source_id/evidence_id를 SRC-004→SRC-113으로 재정렬(URL 불일치 수정)"
```

### 2-2. CLM-010(물산장려운동) — 비표준 date_precision

**문제**: `date_precision="Decade"`가 xsd 표준 타입이 아니었다. 게다가 "1920년대 초부터 전개된"이라는 서술은 애초에 단일 시점을 가리키는 Claim이 아니었다.

**수정**: `date_value`/`date_precision`/`date_value_status` 3개 필드를 모두 비우고, 서술은 `evidence_note`로만 유지했다.

```text
change_history: "v9.1: 비표준 precision(Decade) 제거, 단일시점 아님을 명시"
```

## 3. 6개 자동검증 (v8 보고서 §7 v9 데이터 생성 규칙과 연동)

TTL 생성 직전, 다음 6개 항목을 스크립트로 검증했다.

```text
[1] claim_id unique                          : OK (55건)
[2] source_id ↔ evidence_id ↔ source_url 정합성 : OK (고유 source_id 29개)
[3] source_url 형식(http/https)                : OK
[4] subject_uri/object_uri CURIE 형식          : OK
[5] date_value ↔ date_precision 일치            : OK
[6] controlled vocabulary(claim_status 등) 일치  : OK
```

6개 전부 통과한 뒤에만 TTL을 생성했다 — "구조 검증 없이 CSV를 바로 TTL로 옮기지 않는다"는 원칙의 실행이다.

## 4. TTL 설계에서 내린 두 가지 핵심 판단

### 4-1. `source_url`을 IRI가 아니라 리터럴로 저장

`source_url`을 `<...>` 형태의 IRI 노드가 아니라 `xsd:anyURI` **문자열 리터럴**로 저장했다. 이유: 신흥무관학교 용어해설 URL처럼 쿼리스트링에 비ASCII 문자(`ganada=전체`)가 섞인 경우, IRI로 해석하면 파싱 오류가 날 수 있다. 리터럴로 두면 이런 문제 자체가 발생하지 않는다.

### 4-2. `item_no` 중복을 삭제하지 않고 별도 grouping 개체로 분리

조선물산장려회처럼 하나의 `item_no`가 여러 Claim(평양 월단위/일단위, 서울)을 가질 때, Claim을 합치는 대신 `prov:Item` 개체를 신설해 `prov:groupsClaim`으로 묶었다. "원본 항목"(item_no)과 "실제 Claim"을 서로 다른 층위로 유지하기 위함이다(v8 보고서 §7의 "49개 항목 상태표는 보조 지표, Claim이 권위값" 원칙과 동일한 결).

## 5. 검증 결과 수치

```text
CSV 총 Claim 행       : 55
고유 item_no          : 49  (원본 49개 항목 전체 커버 확인)
고유 source_id        : 29
고유 evidence_id      : 30
TTL 트리플 수(rdflib)  : 1155
```

rdflib으로 파싱해 문법 오류 없음을 확인했다. 55개 Claim이 신뢰도 구분 없이 전부 TTL에 반영된 상태다.

## 6. 이 단계에서 의도적으로 하지 않은 것

- **신뢰도 필터링**: 하지 않았다. v9.1의 목적은 "구조적으로 유효한가"이지 "신뢰할 만한가"가 아니다.
- **Core/Hold/Exclusion 분리**: 아직 개념 자체가 도입되지 않았다(v9.3에서 도입).
- **relation vocabulary 정규화**: `related_to`, `해당` 같은 넓은 관계어를 그대로 두었다 — 이 시점에는 아직 문제로 식별되지도 않았다.

## 7. 결론

| 항목 | 판정 |
|---|---|
| Pre-TTL 버그 2건(CLM-023, CLM-010) 수정 | 완료 |
| 6개 자동검증 | 전부 통과 |
| TTL 구조적 유효성(rdflib 파싱) | 통과 |
| 신뢰도 기반 선별 | 미착수 — v9.2 과제로 이관 |

v9.1은 "55개 Claim 전체가 구조적으로 TTL화 가능하다"는 것만 보장한다. 이 TTL을 최종본으로 볼 수 없는 이유는, 그 안에 `validation_hold`이거나 근거 없는 날짜 추정이 섞여 있는 채로 아무 구분 없이 담겨 있기 때문이다 — 이 문제를 다루는 것이 다음 v9.2 검증보고서의 주제다.

---

## 부록. 참고 — 이번 보고서에서 참조한 v8 검증보고서(ver5) 조항

| v8 보고서 조항 | v9.1에서의 적용 |
|---|---|
| §0 핵심 설계 원칙(6줄) | 그대로 계승, TTL 특화 원칙 1줄 추가 |
| §2 상태값 체계(4필드 독립성) | pre-TTL cleanup에서 필드 오염(CLM-023) 발견에 사용 |
| §7 "49개 상태표는 보조지표, Claim이 권위값" | item_no vs Claim 분리 설계(§4-2)에 직접 적용 |
| §9 Source Mapping 데이터 구조 | CSV 22개 컬럼 스키마의 근거 |
| §12 v9 데이터 생성 규칙(Rule G-01~G-08) | 6개 자동검증 항목 설계의 근거 |
