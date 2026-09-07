# v9.5 검증 보고서

## — date_status 완전 정합화(P1)와 규칙 자체의 자기교정

> 본 보고서는 v9.1~v9.4와 동일하게 "v8 추가검증보고서(ver5, 설계 승인본)"의 형식을 준용한다. v9.5는 v9.4에서 발견된 P1(date_status 빈 값 15건)을 해소하는 패치 버전이며, 해소 규칙 자체가 검증 과정에서 한 번 수정된 사례를 포함한다.

---

## 0. 이 보고서가 검증하는 대상

- **입력**: v9.4의 34 Core + 5 Hold(39건, date_status 빈 값 15건 포함) + 16 Exclusion
- **출력**: `v9.5_claim_core.csv`(34건), `v9.5_claim_hold.csv`(5건), `v9.5_exclusion_manifest.csv`(16건), `v9.5_gwanhak_claims.ttl`, `v9.5_설명서.md`
- **목적**: v9.4 검증에서 "P2-1 정도"로 낮게 평가됐던 date_status 빈 값 문제가 실제로는 **P1(이미 정한 규칙의 데이터 미적용)**임을 재확인하고, 15건 전체를 정합화

## 1. 문제의 재정의 — P2 → P1

v9.4까지는 15건의 빈 `date_status`가 "설계상 문제 없을 수도 있다"는 정도로 취급됐다. 그러나 v9.4 데이터 사전이 이미 `not_applicable`("날짜 assertion 자체가 없음")을 정의해 둔 상태에서, 그 정의에 정확히 해당하는 데이터가 빈 값으로 방치된 것은 **설계 누락이 아니라 적용 누락**이다. ver5 원칙("빈 값이 아니라 명시적 상태값으로 남긴다")과도 어긋나므로, 이번 보고서에서 P1로 재확정한다. 다만 사실관계·TTL 구조·49개 item coverage는 손상되지 않았으므로 P0까지 올리지는 않는다.

## 2. 해소 규칙의 자기교정 — 검증 과정에서 규칙이 한 번 바뀌었다

### 2-1. 1차 제안 규칙 (기각)

```text
date_value 없음 → date_status = not_applicable
```

이 규칙은 "date_value의 유무"만을 기준으로 삼았다. 이 규칙을 그대로 적용하면 CLM-002·CLM-011(대성학교 설립)처럼 **본질적으로 시간축을 갖는 사건**까지도 "날짜 개념 자체가 없다"는 뜻의 `not_applicable`로 잘못 분류하게 된다 — 설립 사실은 확인됐지만 그 날짜를 이 Claim에서 직접 검증하지 못했을 뿐인데, 마치 "날짜라는 것 자체가 이 Claim과 무관하다"고 기록하는 셈이 된다.

이 규칙을 처음 제안한 검토에서조차 "date_value가 없다고 전부 not_applicable로 일반화하면 안 된다"는 경고를 스스로 냈으면서도, 곧이어 그 경고를 어기고 15건 전부에 이 규칙을 일괄 적용하자고 결론 내는 **자기모순**이 있었다. 이 모순은 재검토에서 지적됐고, 아래 2-2로 교정됐다.

### 2-2. 최종 채택 규칙

```text
date_status는 date_value의 존재 여부가 아니라
Claim이 어떤 종류의 시간적 주장을 하는가로 결정한다.
```

| Claim의 시간적 의미 | date_status |
|---|---|
| Claim 자체가 날짜 assertion을 요구하지 않음 | `not_applicable` |
| 시간축을 갖는 사건·관계이나 그 날짜를 직접 검증하지 못함 | `not_directly_verified` |
| 날짜 assertion을 출처에서 직접 확인함 | `verified` |

## 3. 15건 재분류 — 최종 확정본과의 대조

| 분류 | 건수 | claim_id | 판단 근거 |
|---|---|---|---|
| `not_applicable` | 9 | CLM-006, CLM-022a, CLM-022b(정의·성격 서술) + CLM-027-04, CLM-017, CLM-020, CLM-021, CLM-024, CLM-025(참여, Rule G-02) | 애초에 날짜 assertion을 요구하지 않음 |
| `not_directly_verified` | 6 | CLM-002, CLM-011(설립), CLM-013(재직), CLM-016, CLM-018, CLM-019(소속) | 시간축을 갖는 사건이나 날짜 미확인 |

실제 v9.5 파일을 재검산한 결과 이 분류와 **정확히 일치**함을 확인했다(claim_id 15건 전수 대조).

### 3-1. 참여 Claim에 대한 신설 Date Rule

```text
사건 참여 Claim에서 사건 자체의 날짜만 확인되고 개인의 참여일이
별도로 확인되지 않은 경우, 사건 날짜를 개인 Claim의 date_value로
상속하지 않는다(Rule G-02). 해당 Claim이 개인의 독립적인 참여
날짜를 assertion으로 요구하지 않는 경우 date_status=not_applicable로
기록한다.
```

이 규칙을 `v9.5_설명서.md`와 TTL의 `vocab:not_applicable` 주석에 명문화했다 — 이 규칙이 없으면 "참여에는 당연히 날짜가 있을 텐데 왜 not_applicable인가?"라는 의문이 반복 제기될 수 있기 때문이다.

## 4. 9개 자동검증 (v9.4 대비 1개 신설)

```text
[1] claim_id unique                     : OK (39건)
[2] source_id ↔ title/url 정합성        : OK
[3] source_url 형식                     : OK
[4] CURIE 형식                          : OK
[5] date_value ↔ date_precision 일치     : OK
[6] controlled vocabulary               : OK
[7] date_value 없이 verified인 잔존오류  : OK — 0건
[8] exclusion disposition 통일          : OK — 16건 전부 excluded_from_ttl
[9] (신규) date_status 빈 값 0건(완전정합) : OK
[coverage] 49개 item_no 전체 커버       : OK
[coverage] core 34 + hold 5 + exclusion 16 = 55 : OK
```

## 5. date_status 최종 분포

```text
              v9.4    v9.5
verified        18      18
not_directly_verified  5      11  (+6)
not_applicable    1      10  (+9)
빈 값            15       0  (완전 해소)
합계             39      39
```

## 6. TTL 재생성 결과

```text
Claim(core+hold) : 39  (core=34, hold=5, claimDecision으로 구분)
Source : 30 | Evidence : 31 | Item : 35
트리플 수(rdflib) : 987
TTL claim count = CSV claim count : 39 = 39 (일치)
```

`vocab:not_applicable`의 TTL 주석을 이번에 갱신해, "정의·성격 서술"과 "Rule G-02에 따른 참여일 의도적 분리" 두 가지 의미를 모두 포괄하도록 명시했다.

## 7. 남은 후속 과제 (P2, 의도적 유보)

- 참여 Claim 6건(CLM-027-04, CLM-017/020/021/024/025)에 대한 장기 세분화 여지 — "개인 참여일 개념 자체가 적용 불가"라기보다 "참여는 확인했으나 사건일을 참여일로 대체할 수 없어 assertion을 만들지 않았다"는 의미에 더 가까워, 향후 상태 어휘가 더 세분화되면 별도 상태값이 필요할 수 있음. 지금은 근거 없이 새 어휘를 만들지 않는다는 원칙에 따라 `not_applicable`로 보수적으로 유지
- CLM-002/CLM-011 Evidence 중복 통합 여부
- `related_to`/`해당`/`조직관계` 등 relation vocabulary 정규화
- SHACL 셰이프 작성

## 8. 결론

| 항목 | 판정 |
|---|---|
| P1 재확정(date_status 빈 값 15건) | 타당함, 유지 |
| 1차 제안 규칙("date_value 없음→not_applicable 일괄") | 기각 — 자기모순 발견 후 폐기 |
| 최종 규칙(Claim semantics 기반 분류) | 채택, 실제 데이터에 반영 완료 |
| 9건/6건 재분류 | 완료, 실제 파일과 전수 대조 일치 확인 |
| 참여 Claim Date Rule 명문화 | 완료 |
| 9개 자동검증 | 전부 통과 |
| TTL 재생성 및 claim count 일치 | 확인 |
| freeze 가능 여부 | 이번 P1 해소로 baseline 요건 충족. 단, §7의 후속과제(특히 relation vocabulary)는 P2로 계속 이월 |

**v9.4 → v9.5는 새로운 기능을 추가한 버전이 아니라, v9.4가 이미 정의해 둔 규칙을 데이터 전체에 일관되게 적용하고, 그 적용 과정에서 규칙 자체의 결함(자기모순)을 발견해 교정한 버전이다.** 이는 v9.1~v9.4에 걸쳐 반복됐던 "결정은 했지만 실제 파일에 반영이 안 됨"(CLM-023의 3연속 재발 등) 패턴과 같은 계열의 문제이지만, 이번에는 규칙을 실제로 적용하기 전에 규칙 자체의 결함을 먼저 잡아냈다는 점에서 차이가 있다.

---

## 부록. 참고 — 이번 보고서에서 참조한 v8 추가검증보고서(ver5) 조항

| ver5 조항 | v9.5에서의 적용 |
|---|---|
| §2 date_status 정의(4필드 독립성) | `claim_status`와 `date_status`의 독립성이 CLM-002/011/013/016/018/019(관계는 확인, 날짜는 미확인)에서 실제로 필요했던 이유 |
| §12 Rule G-02(사건 날짜 자동상속 금지) | 참여 Claim 6건에 대한 신설 Date Rule의 직접적 근거 |
| §12 Rule G-03(정밀도 축소≠추정) | not_applicable/not_directly_verified 구분이 "값이 없다"와 "값을 추정하지 않는다"를 혼동하지 않도록 하는 것과 같은 결 |
| §0 "근거 없이 vocabulary를 발명하지 않는다" | 참여 Claim의 장기 세분화 여지를 지금 새 어휘로 만들지 않고 유보한 근거 |