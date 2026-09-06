# v9.3 검증 보고서

## — 3분할 구조(Core/Hold/Exclusion) 확립과 4단계 판정

> 본 보고서는 "v8 추가검증보고서(ver5, 설계 승인본)"의 형식을 준용하여, v9.2의 이분법(포함/제외)을 3분할(Core/Hold/Exclusion)로 세분화한 v9.3의 작업 내용과 검증 결과를 정리한다.

---

## 0. 이 보고서가 검증하는 대상

- **입력**: v9.2의 39개 포함 Claim(당시 "High-confidence"로 잘못 불렸던 것) + 16개 exclusion
- **출력**: `v9.3_claim_core.csv`(34건), `v9.3_claim_hold.csv`(5건), `v9.3_exclusion_manifest.csv`(16건), `v9.3_gwanhak_claims.ttl`
- **목적**: v9.2를 그대로 TTL 최종본으로 고정하지 않고, "삭제"와 "TTL 제외"를 구분하는 3분할 구조로 정제

## 1. 용어 정정 — "39 High-confidence"는 부정확했다

v9.2 검증보고서 §6에서 예고한 대로, "39 High-confidence"라는 표현을 폐기한다. 그 39개 안에는 `review_flag=relationship_issue`가 붙은 Claim이 이미 섞여 있었고, 이는 "고신뢰"라는 표현과 맞지 않는다. v9.3에서 이를 숫자로 정확히 재정의한다.

```text
39개 포함(included) Claim
   = 34 Core(유지+수정, review_flag가 있어도 근거가 충분하면 Core)
   + 5 Hold(보류, 근거는 있으나 관계·해석 추가 검증 필요)
```

## 2. 3분할 구조와 4단계 판정의 매핑 (v8 보고서 §2 상태값 체계와 동일한 결)

"분할(저장 구조)"과 "판정(작업 결정)"은 서로 다른 축이며, 다음처럼 대응한다.

| 판정 | 의미 | 귀속 파일 |
|---|---|---|
| 유지 | 근거·표현 모두 문제 없음 | `claim_core.csv` |
| 수정 | 근거는 있으나 provenance/relation/날짜 표현을 정규화 | `claim_core.csv` |
| 보류 | 근거는 있으나 관계·해석에 추가 검증 필요 | `claim_hold.csv` |
| 제외 | 현재 증거 수준으로는 Claim으로 확정 불가(원본 항목 삭제 아님) | `exclusion_manifest.csv` |

`claim_core`는 "고신뢰"가 아니라 **"직접적인 근거가 확보되어 본류 데이터에 포함할 수 있는 Claim"**으로 정의해야 정확하다 — 수정이 필요한 Claim도 정규화를 거쳐 Core에 남기 때문이다. 판정 컬럼은 CSV 스키마(22개 컬럼 고정)에 신설하지 않고 `change_history`에 텍스트로 기록했다.

## 3. Hold 5건과 review_flag의 독립성 (v8 보고서 Rule G-05의 실제 사례)

```text
CLM-047       신흥강습소→신흥무관학교 개칭, 시점 불확실
CLM-JOSEON-03 서울 조선물산장려회, 평양과 동일 조직 여부 미확인
CLM-OSAN-02   이승훈 개교, 설립 Claim과 동일 사건 여부 미확인
CLM-LEE-A     이동휘 취임(1919-08)
CLM-LEE-B     이동휘 합동 취임식(1919-11-03) — LEE-A와 동일 단계 사건인지 미확인
```

이 5건 모두 `review_flag=relationship_issue`를 갖지만, **같은 flag를 가진 CLM-OSAN-01(오산학교 설립)은 Hold가 아니라 Core로 분류**됐다. review_flag(문제 신호)와 claim_status/판정(처리 결과)이 독립축이라는 v8 보고서 Rule G-05("verification_status와 claim_status는 독립적으로 조합될 수 있다")를 Core/Hold 분류에 실제로 적용한 사례다.

## 4. 검증 과정에서 발견한 문제: CLM-023 재누락 — 파이프라인 재현성 문제로 격상

전달된 v9.3 초안을 검증한 결과 39행이 아니라 **38행**이었다. v9.2의 39개 claim_id와 대조한 결과 `CLM-023`(이승만)이 유지/수정/보류/제외 어느 판정도 없이 누락되어 있었다.

이 Claim의 이력을 추적하면 우연이 아니다.

```text
v9.1: SRC-004 재사용 문제 발견 → SRC-113으로 수정
v9.2: cleaned본에서 같은 문제 재발 → 재수정
v9.3: 행 자체가 통째로 사라짐
```

같은 Claim의 수정 이력이 버전마다 CSV를 사람이 손으로 옮겨 적는 과정에서 안정적으로 계승되지 못했다는 뜻이다. 이는 개별 데이터 오류가 아니라 **데이터 파이프라인의 재현성(reproducibility) 문제**로 격상해 기록한다. 향후에는 버전마다 CSV를 손으로 재작성하는 방식 대신, 단일 master Claim registry에서 core/hold/exclusion을 자동 파생시키는 방식으로 전환할 필요가 있다. v9.3에서는 즉시 CLM-023을 Core로 복원해 34건을 확보했다.

## 5. 자동검증 재실행 (Core+Hold 39건 대상)

```text
[1] claim_id unique(core+hold)          : OK (39건)
[2] source_id ↔ title/url 정합성        : OK (고유 source_id 30개)
[3] source_url 형식                     : OK
[4] CURIE 형식                          : OK
[5] date_value ↔ date_precision 일치     : OK
[6] controlled vocabulary 일치          : OK
[coverage] 49개 item_no 전체 커버        : OK
[coverage] core 34 + hold 5 + exclusion 16 = 55 : OK
```

## 6. TTL 설계 — Core/Hold를 단일 그래프에 유지하되 명시적으로 구분

Named graph 분리 대신, `prov:claimDecision "core"|"hold"` 속성을 신설해 같은 그래프 안에서 SPARQL로 필터링 가능하게 했다. Exclusion 16건은 TTL에 반영하지 않았다(삭제 아님, CSV 보관).

```text
Claim(core+hold) : 39  (core=34, hold=5)
Source : 30
Evidence: 31
Item   : 35
트리플 수(rdflib) : 969
TTL claim count = CSV claim count : 39 = 39 (일치)
```

## 7. v9.3 Final 완료 조건 체크리스트

```text
[x] 55개 원본 Claim 전체 coverage(39 포함 + 16 exclusion)
[x] CLM-023 복원(34 Core에 포함되어 39=34+5 성립)
[x] 39 = Core 34 + Hold 5 수치 확인
[ ] 4개 수정 Claim(CLM-006/010/012/035)의 수정 결과 확정  ← 텍스트 정규화는
    v9.3에서 판정만 기록, 실제 문장/값 수정은 v9.4로 이관(§8 참조)
[x] 16개 exclusion 각각에 exclusion reason 존재
[x] claim_id 중복 없음 / item_no 49개 전체 coverage
[x] source_id ↔ source_title/url 일치
[x] date_value ↔ date_precision 일치
[x] subject/object URI 형식(CURIE) 검증
[x] controlled vocabulary 검증
[x] TTL claim count = CSV claim count
```

## 8. 결론

| 항목 | 판정 |
|---|---|
| 3분할(Core/Hold/Exclusion) 구조 확립 | 완료 |
| 4단계 판정(유지/수정/보류/제외) 매핑 확정 | 완료 |
| CLM-023 복원 | 완료 |
| 34 Core + 5 Hold 수치 확정 | 완료 |
| 4개 수정 대상(CLM-006/010/012/035)의 실제 데이터 수정 | **미완료** — 판정만 기록됨, 다음 v9.4의 과제 |
| CONDITIONAL PASS 상태 | v9.3은 구조적으로 완결됐으나, 의미론적 정합성(Claim 문장↔subject/object URI↔relation 방향 일치) 재검토가 필요한 상태로 다음 단계에 인계됨 |

**현재 상태는 "초안/검증 중간본"이며, 완성본이 아니다.** 특히 이 단계에서는 아직 발견하지 못했던 문제 — Claim 문장과 subject/object URI·relation의 방향이 어긋나는 행들(CLM-014, CLM-003, CLM-022b 등) — 이 별도의 실제 파일 대조 검토에서 추가로 드러났으며, 이는 v9.4 검증보고서에서 다룬다.

---

## 부록. 참고 — 이번 보고서에서 참조한 v8 검증보고서(ver5) 조항

| v8 보고서 조항 | v9.3에서의 적용 |
|---|---|
| §2 상태값 체계(4필드 독립성) | review_flag와 판정의 독립성을 Core/Hold 분류에 실제 적용(§3) |
| §12 Rule G-05 | CLM-OSAN-01(유지) vs CLM-OSAN-02(보류)의 비대칭 판정 근거 |
| §11 Rule P-04(출처 충돌 보존) | Hold 5건을 삭제하지 않고 별도 파일에 보존한 근거 |
| §9 Source Mapping 데이터 구조(22개 컬럼 고정) | 판정을 change_history에 기록하고 별도 decision 컬럼을 신설하지 않은 근거 |
