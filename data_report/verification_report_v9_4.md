# v9.4 검증 보고서

## — Claim 문장·subject/object URI·relation 의미 정합성 검증

> 본 보고서는 "v8 추가검증보고서(ver5, 설계 승인본)"의 형식을 준용하여, v9.3에서 구조적으로는 완결됐으나 의미론적 정합성이 남아 있던 문제를 실제 파일 대조를 통해 잡아낸 v9.4의 작업 내용과 검증 결과를 정리한다.

---

## 0. 이 보고서가 검증하는 대상

- **입력**: v9.3의 34 Core + 5 Hold + 16 Exclusion(구조는 확정, 의미론적 정합성 미검토)
- **출력**: `v9.4_claim_core.csv`(34건), `v9.4_claim_hold.csv`(5건), `v9.4_exclusion_manifest.csv`(16건), `v9.4_gwanhak_claims.ttl`, `v9.4_data_dictionary.md`
- **목적**: v9.3까지의 검증이 "행 수·CURIE 형식·날짜 형식"처럼 기계적으로 확인 가능한 정합성에 머물러 있었던 것을, **Claim 문장이 실제로 subject_uri→relation→object_uri 방향과 일치하는가**라는 의미론적 정합성까지 확장

## 1. 문제의 성격 — "형식은 맞는데 의미가 어긋난다"

v9.3까지의 6개 자동검증은 전부 통과했지만, 이는 CURIE 형식이나 날짜 포맷 같은 **구문(syntax) 수준**의 검증이었다. 실제 파일을 행 단위로 다시 읽어보니, `claim`(자연어 문장) ↔ `subject_uri`/`object_uri`/`relation`(구조화된 필드) 사이에 **의미(semantics) 수준의 불일치**가 6곳 남아 있었다. 이는 스크립트로 자동 검출할 수 없고 사람이 문장을 직접 읽어야 발견되는 유형의 문제다.

## 2. 발견·수정한 문제 6건 (P0)

### 2-1. CLM-014 — subject가 인물인데 문장 주어는 사건

**문제**: `subject_uri=:안명근`(인물)인데 claim 문장은 "안명근 **사건**은 105인 사건의 계기가 된 사건으로 연결된다"— 문장의 실제 주어는 안명근이라는 사람이 아니라 그를 둘러싼 **사건**이었다.

**수정**: `subject_uri`를 `:안악사건`(사건 엔티티, CLM-007에서 이미 쓰던 URI 재사용)으로 정정, `object_uri`에 `:105인사건`(CLM-008에서 이미 쓰던 URI 재사용)을 추가해 relation(`related_to`)의 대상을 명시. `item_no`/`item_name`(26/안명근)은 원본 매핑 출처이므로 그대로 유지하되, subject 엔티티와 의도적으로 다르다는 점을 change_history에 남겼다.

### 2-2. CLM-003 — 수동태 문장이 subject 방향과 불일치

**문제**: `subject_uri=:이회영`, `relation=설립`, `object_uri=:신흥강습소`인데, claim 문장은 "신흥강습소**가** … 설립되었다"는 수동태로 신흥강습소를 주어로 삼고 있었다.

**수정**: "이회영 등이 신흥강습소를 설립하였다"로 능동태 정렬. 실제 공동설립자(이회영·이시영·이동녕·이상룡) 전원을 주어에 넣으면 다중 주체 문제가 생기므로 "등"으로 대표 표기했고, 개별 인물의 별도 공동설립 Claim화는 후속 확장 과제로 남겼다.

### 2-3. CLM-022b — 문장의 복수 주체와 object 단수의 불일치

**문제**: claim 문장은 "북로군정서는 **서일·김좌진** 등이 주도한…"인데 `object_uri`는 `:김좌진` 하나뿐이었다.

**두 가지 선택지 검토**: (A) 문장을 김좌진 중심으로 축소, (B) 서일/김좌진을 별도 Claim으로 분리. B안은 Claim 수가 55→56으로 늘어난다.

**결정**: A안 채택. 문장에서 "서일·"을 제거해 "북로군정서는 김좌진이 주도한 독립군 조직이다"로 정리했다 — 서일과 북로군정서의 관계는 이미 별도 Claim `CLM-022a`(item 43)가 담당하고 있어 정보 손실이 없기 때문이다. 55개 Claim 수를 유지하는 쪽을 우선했다.

### 2-4~2-6. CLM-046 / CLM-016 / CLM-018 / CLM-019 — relation="소속"과 문장의 "활동" 사이 의미 간극

**문제**: 양기탁(CLM-046)·이종호(CLM-016)·이회영(CLM-018)·이시영(CLM-019) 4건 모두 `relation=소속`(비교적 강한 membership assertion)인데, claim 문장은 "…의 핵심/중심 인물로 활동하였다"(더 넓은 의미)였다. `소속`이 실제로 지지되는지 relation 자체를 낮출지, 문장을 relation에 맞춰 강화할지의 선택에서, Evidence가 membership 자체를 뒷받침하는 경우이므로 후자를 택했다.

**수정**: "~에 소속되어 ~로 활동하였다" 형태로 통일.

```text
CLM-046: "양기탁은 신민회에 소속되어 핵심 인물로 활동하였다."
CLM-016: "이종호는 신민회에 소속되어 중심 인물로 활동하였다."
CLM-018: "이회영은 신민회에 소속되어 중심 인물로 활동하였다."
CLM-019: "이시영은 신민회에 소속되어 중심 인물로 활동하였다."
```

수정 과정에서 조사 오류("이회영는"→"이회영은", "이시영는"→"이시영은")도 함께 발견해 정정했다.

## 3. date_status 정밀화 (P1) — 6건 중 진짜 버그는 1건뿐

v9.3에서 `date_value`가 비어 있는데 `date_status`가 채워진 행 6건을 전수 재검토했다.

| Claim | date_status | 판정 |
|---|---|---|
| CLM-010 | `verified` | **버그** — 날짜가 없는데 "검증됨"이라 한 논리 오류 |
| CLM-046, CLM-035, CLM-KIM-01, CLM-KIM-02, CLM-047 | `not_directly_verified` | 정상 — "날짜가 있을 법한데 못 찾음"이라는 의미로 타당 |

`not_directly_verified`("날짜가 있을 법한데 아직 못 찾음")와 그동안 없었던 `not_applicable`("이 Claim에는 애초에 날짜 assertion 자체가 없음")을 구분해야 한다는 것이 이번에 확정한 원칙이다. `date_status` vocab에 `not_applicable`을 신설하고 CLM-010에만 적용했다 — 나머지 5건은 손대지 않았다.

## 4. exclusion manifest 용어 충돌 해소

`exclusion_manifest.csv`의 `disposition` 컬럼 값이 v9.3까지 `보류`였는데, 이는 `claim_hold.csv`가 이미 쓰고 있는 "보류"와 이름이 겹쳐 "hold와 exclusion의 차이가 뭔가"라는 혼동을 일으켰다. 16건 전체를 `excluded_from_ttl`로 통일했다.

```text
claim_core.csv       → TTL 반영, 판정=core
claim_hold.csv        → TTL 반영(상태 명시), 판정=hold
exclusion_manifest.csv → TTL 미반영, disposition=excluded_from_ttl (삭제 아님)
```

## 5. 자동검증 8개 (v9.3 대비 2개 신설)

```text
[1] claim_id unique                     : OK (39건)
[2] source_id ↔ title/url 정합성        : OK
[3] source_url 형식                     : OK
[4] CURIE 형식                          : OK
[5] date_value ↔ date_precision 일치     : OK
[6] controlled vocabulary(not_applicable 포함) : OK
[7] (신규) date_value 없이 verified인 잔존 오류  : OK — 0건
[8] (신규) exclusion disposition 통일    : OK — 16건 전부 excluded_from_ttl
[coverage] 49개 item_no 전체 커버        : OK
[coverage] core 34 + hold 5 + exclusion 16 = 55 : OK
```

## 6. TTL 재생성 결과

```text
Claim(core+hold) : 39  (core=34, hold=5, claimDecision으로 구분)
트리플 수(rdflib) : 972
TTL claim count = CSV claim count : 39 = 39 (일치)
```

## 7. 데이터 사전 신설

`v9.4_data_dictionary.md`를 별도로 작성해 `claim_status`/`verification_status`/`date_status` 세 필드가 각각 "Claim이 얼마나 강하게 지지되는가" / "이번에 원출처를 직접 확인했는가" / "날짜값(또는 날짜 없음 자체)의 검증 상태"라는 서로 다른 질문에 답한다는 것, `not_directly_verified`와 `not_applicable`의 차이, `review_flag`와 판정(decision)의 관계, v1~v8 TTL 본체의 `hasEestimation`과 v9 계열의 `has_estimation`이 이름은 비슷하지만 독립적으로 설계된 별개 속성이라는 점을 명문화했다. 22개 CSV 컬럼 자체는 v9.1부터 고정되어 있으므로 컬럼을 늘리지 않고, 의미 정의만 별도 문서로 보강하는 방식을 택했다.

## 8. 의도적으로 손대지 않은 것 (P2, 후속 과제)

- `related_to`, `해당`, `조직`, `조직관계` 등 relation vocabulary의 전면 정규화 — 지금 새 관계어를 발명하지 않는다는 v9 원칙에 따라 유보
- `decision`을 별도 machine-readable 컬럼으로 분리할지 여부
- CLM-002/CLM-011(대성학교 설립, 서로 다른 Evidence로 중복 기술) — "동일 Claim + 복수 Evidence" 통합 여부 결정
- SHACL 셰이프를 통한 수동 검사의 자동화
- master Claim registry 기반 파이프라인 전환(CLM-023의 3연속 재발이 드러낸 재현성 문제의 근본 해법)

## 9. 결론

| 항목 | 판정 |
|---|---|
| Claim 문장↔URI↔relation 의미 정합성 6건 수정 | 완료 |
| date_status 정밀화(진짜 버그 1건만 수정) | 완료 |
| exclusion disposition 명칭 충돌 해소 | 완료 |
| 8개 자동검증 | 전부 통과 |
| TTL 재생성 및 claim count 일치 | 확인 |
| 데이터 사전 작성 | 완료 |

v9.1~v9.4에 걸쳐 "구조적으로 유효한가"(v9.1) → "신뢰도로 거를 수 있는가"(v9.2) → "그 거른 결과를 어떻게 세분화·명명할 것인가"(v9.3) → "문장과 구조가 실제로 같은 것을 말하고 있는가"(v9.4) 순으로 검증의 층위가 점점 깊어졌다. 이는 v8 검증보고서 ver5 §9에서 제시된 검증 층위 구분(Schema/Source/Evidence/Claim/Date/Relation/Existence/Provenance validation)과 대응하며, v9.4는 그중 **Relation validation**(subject/object 관계가 실제로 맞는가)에 처음으로 본격 도달한 단계로 볼 수 있다.

---

## 부록. 참고 — 이번 보고서에서 참조한 v8 검증보고서(ver5) 조항

| v8 보고서 조항 | v9.4에서의 적용 |
|---|---|
| §2-1 claim_status 부여 기준("Claim 문장 자체의 근거 강도") | CLM-046/016/018/019에서 문장을 relation에 맞춰 강화할지 relation을 낮출지 판단하는 기준 |
| §11 Rule P-04(출처 충돌 보존) | CLM-014의 subject 정정 시에도 기존 change_history를 삭제하지 않고 누적 기록 |
| §12 Rule G-01(event type을 슬래시로 묶지 않는다) | CLM-022b에서 서일/김좌진을 한 문장에 억지로 묶지 않고 object 단수에 맞춰 정리한 것과 같은 결 |
| §9 Source Mapping 데이터 구조 | 22개 컬럼 고정, decision을 change_history로만 기록하는 근거 |
