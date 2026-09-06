# v9.2 검증 보고서

## — High-Confidence Claim 선별 및 exclusion manifest 분리

> 본 보고서는 "v8 추가검증보고서(ver5, 설계 승인본)"의 형식을 준용하여, v9.1에서 구조적으로만 검증됐던 55개 Claim을 신뢰도 기준으로 선별한 v9.2 작업 내용과 검증 결과를 정리한다.

---

## 0. 이 보고서가 검증하는 대상

- **입력**: v9.1의 55개 Claim(구조 검증만 완료, 신뢰도 미필터링)
- **출력**: `v9.2_claim_high_confidence.csv`(39건), `v9.2_exclusion_manifest.csv`(16건), `v9.2_gwanhak_claims_high_confidence.ttl`
- **목적**: v8 보고서 ver5 Rule G-01~G-08과 v9 로드맵에서부터 예정되어 있던 "검증 가능한 것 위주로 두고 확장한다"는 원칙을, 처음으로 실제 산출물 단위로 구현

## 1. 핵심 전제 — 이것은 방향 전환이 아니다

v9.1까지 55개 Claim이 전부 TTL에 담겨 있었던 것은 "신뢰도가 확인됐다"는 뜻이 아니라, "49개 항목을 빠짐없이 매핑했다"는 커버리지 확보 단계였다. v8 보고서 ver5 §7의 "49개 항목 상태표는 보조 지표일 뿐, Claim 단위가 권위값"이라는 선언과, §12 Rule G-01~G-08은 애초에 이 선별 작업을 예정하고 있었다. v9.2는 그 계획을 처음 실행에 옮긴 것이다.

## 2. 제외 기준 (v8 보고서 §11 Negative Evidence 원칙과 연동)

다음에 해당하는 Claim을 제외 후보로 식별했다.

```text
- verification_status = url_recheck_required (근거 URL 자체를 확보하지 못함)
- 사건 날짜를 개인 참여일로 그대로 추론한 Claim (Rule G-02 위반 소지)
- provenance_gap이 있고 근거를 역추적하지 못한 값
```

**중요**: "제외"는 "삭제"가 아니다. `exclusion_manifest.csv`에 항목명·claim_id·제외 사유를 남겨, 근거를 확보하면 재투입할 수 있게 했다.

## 3. 재검증에서 발견한 버그 4건

업로드된 cleaned/exclusion 파일을 검증 없이 그대로 쓰지 않고 6개 자동검증을 다시 돌린 결과, 이미 고쳤다고 생각했던 문제의 재발과 완전히 새로운 문제를 함께 발견했다.

| 문제 | 내용 | 조치 |
|---|---|---|
| CLM-006 컬럼 밀림 | `date_value_status`부터 오른쪽 전체가 한 칸씩 밀려 `verification_date`가 통째로 소실 | 행 전체를 CLM-006-DATE와 동일 구조로 재정렬 |
| CLM-023 source 충돌 재발 | v9.1에서 SRC-113으로 고쳤던 문제가 이번 cleaned본에서 SRC-004로 다시 나타남 | SRC-113으로 재차 분리 |
| CLM-010 비표준 precision 재발 | `Decade`가 다시 등장 | 재제거 |
| item_no 15(안악사건) 완전 누락 | high-confidence 39건에도 exclusion 16건에도 어디에도 없었음 | 원본 근거(E0034866, 1910-11)로 복원 |

이 4건 중 3건이 "이미 고쳤던 문제의 재발"이라는 점은, 이 단계에서는 아직 "실수가 반복된다" 정도로만 기록했고 — 이 패턴이 파이프라인 구조 자체의 문제라는 인식은 v9.3 검증보고서에서 격상된다.

## 4. 6개 자동검증 재실행

```text
[1] claim_id unique                          : OK (39건)
[2] source_id ↔ title/url 정합성              : OK (고유 source_id 30개)
[3] source_url 형식                           : OK
[4] CURIE 형식                                : OK
[5] date_value ↔ date_precision 일치           : OK
[6] controlled vocabulary 일치                 : OK
[coverage] core 39 + exclusion 16 = 55, 49개 item_no 전체 커버 : OK
```

## 5. TTL 재생성 결과

```text
Claim  : 39
Source : 30
Evidence: 31
Item   : 35
트리플 수(rdflib) : 928
```

`validation_hold`, `review_flag=relationship_issue`(오산학교·이동휘·서울 조선물산장려회) 같은 불확실성 정보는 삭제하지 않고 그대로 보존했다 — v8 보고서 §11 Rule P-04("출처 간 충돌은 삭제하지 않고 provenance에 보존한다")의 적용이다.

## 6. 용어상 남긴 문제 (v9.3에서 정정됨)

이 단계의 산출물을 "39 High-confidence Claim"이라고 불렀는데, 이는 부정확한 표현이었다. 39개 안에는 `review_flag=relationship_issue`가 붙은 Claim이 여럿 섞여 있어 "고신뢰"라는 표현과는 어긋난다. 더 정확한 표현은 "제외되지 않고 본류에 남은(included) Claim"이며, 이 39개를 다시 Core/Hold로 세분화하는 것이 v9.3의 작업이다.

## 7. 결론

| 항목 | 판정 |
|---|---|
| 신뢰도 기반 39/16 분리 최초 구현 | 완료 |
| 재발 버그 4건 수정 | 완료 |
| 6개 자동검증 + coverage 검증 | 전부 통과 |
| TTL 재생성(928 트리플) | 완료 |
| "39 High-confidence" 표현의 정확성 | 부정확 — v9.3에서 "39 included = 34 Core + 5 Hold"로 재정정 필요 |

---

## 부록. 참고 — 이번 보고서에서 참조한 v8 검증보고서(ver5) 조항

| v8 보고서 조항 | v9.2에서의 적용 |
|---|---|
| §7 "Claim이 권위값" | 항목(item_no) 단위가 아니라 Claim 단위로 포함/제외를 판정하는 근거 |
| §8 v9 작업 큐 | url_recheck_required 항목을 제외 후보로 식별하는 기준 |
| §11 Rule P-04(출처 충돌 보존) | validation_hold/relationship_issue Claim을 삭제하지 않고 유지한 근거 |
| §12 Rule G-02(사건 날짜 자동상속 금지) | 개인 참여일 추론 Claim을 제외 기준에 포함한 근거 |
