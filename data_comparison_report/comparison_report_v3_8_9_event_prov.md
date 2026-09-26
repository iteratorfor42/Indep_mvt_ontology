# v3 → v8 → v9.5 비교분석: 단일 Event 모델의 발전과 Provenance 모델로의 전환

> 이 글은 **3_semantic_archive_v3.ttl과 v8.ttl 그리고 v9.5(=v9_5).ttl을 비교분석**한다.
> `김바로 교수의 박사논문 적용에 충실한 v3`과 `그 개선본인 v8` 그리고 `검증 모델인 v9.5`를
> **Claim–Evidence–Source provenance 모델인 v9.5의 관점**에서 다시 살펴 보며,
> v3에서부터 고려했던 내역이 v8에서 각각 어떻게 됐는지
> ("해소" / "완화" / "그대로 남음")를 먼저 확인하고, v8이 왜 그럼에도 v9.5로의 전환이 필요했는지를
> 정리한다.

> **참고 사항**: 이 문서의 "Prof.김바로 모델(;Prof.김 모델)"이라는 서술은 박사논문 전체를 정독한 결과가 아니라, 
> 이 프로젝트가 실제로 구현에 반영한 설계 원칙(학술모델·추정모델·조직모델·사건모델· 리)에 근거한다.
> 구현한 것은 논문의 일부 설계 원칙이지,논문 전체가 아니다.
> 이 점 때문에 ontology_readme.md에서도 박사 논문과의 비교 섹션이 없으며,
> 관련 내용은 주로 이 보고서에서 다루게 되었다.


---

## 1. 핵심 결론

**`v8은 v3의 최종 개선본`이자 동시에 `단일 Event 모델의 한계를 스스로 증명한 버전`이다.**
v8은 여러 차례의 검토(3~5회차, P라운드: v8.1 추가 검증에서 확정한 원칙 겸 v8.1~v8.4 적용 라운드)를 거치며 
v3의 문제점 일부를 구조적으로 해소했지만, 나머지는 "왜 그런지 코멘트로 정당화"하는 선에서 멈췄다.
그렇기에 v9단계에서 Claim/Evidence/Source로 전면 재설계하게 되었다.

```
Prof. 김바로 원 논문 모델 
  (범용 인문학 온톨로지 설계 방법론 — 학술/추정/조직/사건모델 + 공리)
        │
        │ 채택·적용
        ▼
v3   단일 Event 스키마 확립 (원 논문 패턴 검증 단계)
  ↓  여러 차례 검토 라운드(1~5회차, P라운드)
v8   Event 스키마를 유지한 채 정교화의 한계까지 밀어붙임
  ↓  "코멘트로 정당화"만으로는 안 되는 지점이 누적
v9   Claim–Evidence–Source로 패러다임 전환  (v8의 "다음 버전"이 아니라, 검증용 병렬 설계)
```

---

## 2. v3의 다섯 가지 어색함과 v8에서의 개선

이 글에서의 '어색함'이라는 표현은 v8~v9 작업에서 실제 느꼈던 감정이며,
대체할 만한 좋은 단어가 생각나지 않아서 어색함으로 서술했다.

| # | v3의 어색함 | v8에서의 상태 | 판정 |
|---|---|---|---|
| ① | `Event` 하나에 설립·재직·소속·참여·영향·졸업·사사·경영 등 모든 역할이 몰림 | 오히려 `:체포`, `:공동설립` 등 유형이 **더 늘어남**. 유형 수는 늘었지만 여전히 `Event` 한 클래스로 수렴 | **그대로 남음 (심화)** |
| ② | `hasPostObject`의 의미가 "사건 이후 상태"에서 "관계 대상"으로 확장됨 | 아예 정의(comment)를 고쳐서 "사건 발생 이후의 상태·대상·결과(관련 사건 포함)"로 **의미를 공식적으로 넓힘**. `:이승훈영향안창호_01`, `:이승훈참여삼일운동_01` 패턴은 그대로 유지 | **정당화로 봉합(혹은 상태 누적)** |
| ③ | `hasFoundedYear`(조직 속성)와 Event의 `hasTimeValue`가 같은 사실을 이중 표현 | `hasFoundedYear`의 comment에 "이 값은 Event의 요약이다"라며 **역할분담임을 명시**. 구조 자체는 그대로, 설명만 보강 | **정당화로 봉합(혹은 상태 누적)** |
| ④ | `hasBibo`가 단순 문자열(`rdfs:Literal`) | v8에서도 `hasBibo`는 여전히 문자열. 대신 개별 Event마다 어느 항목(인물/조직) 출처인지 문자열을 촘촘히 나눠 담는 방식으로 **정교화는 됐으나 구조는 그대로** | **그대로 남음** |
| ⑤ | `:백오인사건`이 `:Group`과 `:Event`에 이중 선언됨 | v8에서는 `:안악사건`, `:백오인사건` 모두 **`:Event` 단일 타입**으로만 선언됨. 실제로 구조적으로 해소 | **해소** |

**5개 중 1개(⑤)만 구조적으로 해소되고, 3개(①②③)는 "왜 이런지 설명하는 코멘트"로 덮었으며,
1개(④)는 손도 대지 않았다.** 
그렇기에 v8을 "정교해졌지만 패러다임은 그대로"인 버전이라고 생각한다.

---

## 3. v8에서 실제로 새로 생긴 것 — 방향은 옳았다고 생각한다.

v8은 Provenance 사고의 원형이라고 볼 수 있다.

### ① `hasValidationStatus` — "존재 여부 자체가 불확실한 관계"를 표시하는 속성
```turtle
:김좌진소속신민회_01
    :hasValidationStatus "검증보류"@ko ;
```
신민회 공식 명단에 김좌진이 없다는 걸 발견하고도 완전히 삭제하지 않고 "검증보류" 상태로 격리한 것.
이건 v9.5의 `hasClaimStatus`(confirmed/confirmed_indirect/validation_hold)가 정확히
하려는 일을, Event 모델 틀 안에서 미리 적용했다.

### ② 근거 없는 관계의 적극적 삭제 — `succeedByPersonTo` 제거
```
# [v6] ... 기존에 있던 :오산학교 :succeedByPersonTo :대성학교 . 트리플을 삭제함.
# 확인 가능한 자료로는 두 학교가 조직적으로 승계 관계에 있다는 근거가 없고,
# 오히려 병렬적으로 설립된 사례로 보는 것이 자연스럽다.
```
"그럴듯해서 넣어뒀던" 관계를 근거 부족을 이유로 **실제로 제거**한 사례다. 
v9.5에서 `claim_hold.csv`나
`exclusion_manifest.csv`로 분리 관리하는 것과 같은 방식이다.

### ③ 신흥강습소/신흥무관학교 분리와 "사건 존재 자체의 불확실성" 표현
```turtle
:신흥강습소_신흥무관학교_개칭 ...
    rdfs:comment "... 단순히 날짜 오차 추정이 아니라 사건의 존재 자체에 대한 불확실성까지 포함..."
```
`hasEestimation`(원래는 "날짜가 언제인지"의 불확실성 전용)을 "이 사건이 있었는지 자체가 불확실함"을
표현하는 데까지 억지로 끌어다 썼다는 자각[???]이 코멘트에 그대로 드러난다. **이 지점이 v8의 가장 정직한
자기 진단**이며, v9.5가 `dateValueStatus`(source_stated 등)와 `hasClaimStatus`를 분리한 이유를
가장 잘 설명해주는 사례다.

---

## 4. v8과 v9.5의 결정적 차이

| 문제 | v8의 해법 | v9.5의 해법 |
|---|---|---|
| "날짜가 없는 이유"가 제각각임 | Event마다 자연어 comment로 설명(“시간정보 미상”, “Rule G-02 적용” 등) | `hasDateStatus`에 `not_applicable`(애초에 날짜 개념 없음) vs `not_directly_verified`(있을 법한데 못 찾음)로 **통제된 어휘(vocab)** 로 구분. 39개 Claim 전수에 대해 빈 값 0건까지 정합화 |
| "관계가 정말 있는지"에 대한 의심 | `hasValidationStatus "검증보류"`으로 부여(속성 자체가 v8 막판에 신설) | `hasClaimStatus`(confirmed/confirmed_indirect/validation_hold) + `hasReviewFlag`(relationship_issue 등) + `claimDecision`(core/hold)이 **처음부터 체계로 설계됨**, 별도 CSV(core/hold/exclusion)로 분리 |
| 출처 표현 | `hasBibo`(문자열) 그대로 | `Source`(제목 + `sourceUrl`을 `xsd:anyURI`로 타입 지정) + `Evidence`(근거 요약) + `Claim`이 서로 다른 개체로 **분리**, 실제 encykorea.aks.ac.kr 개별 URL까지 보유 |
| 관계와 사건의 혼재 | `Event` 하나로 계속 수렴 (①번 항목이 v8에서 더 심해짐) | `Claim`이 `hasRelation`(문자열)로 관계 성격을 직접 서술하고, `Item`이 인물/조직/사건별로 Claim들을 묶어 관리 — Event처럼 모든 것을 하나의 클래스로 밀어넣지 않음 |
| 변경 이력 | 파일 헤더 주석에 버전 단위로 서술 | `changeHistory`가 **Claim 개체 단위**로 존재. 예: `CLM-OSAN-01`의 changeHistory에 "v9.3: review_flag=relationship_issue가 있으나 claim_status=confirmed는 유지 근거가 충분함을 의미하므로 Core에 유지"처럼, 판단의 근거 자체가 데이터로 남음 |
| 중복 사실 처리 | 주석으로만 "중복 가능성 있음, 병합은 보류"라고 서술(예: 대성학교 CLM-002/CLM-011 상당분) | v9.5에서도 동일하게 "병합하면 Evidence를 잃으므로 보류"라고 명시 — **이 지점은 v9.5도 아직 완전히 풀지 못한 채 이어받은 문제** |

---

## 5. 구체적 사례로 보는 3단계 변화 — "신민회 소속" 관계

같은 사실("○○가 신민회에 소속되었다")이 세 버전에서 어떻게 표현되는지 비교하면 
전환의 의미가 가장 잘 드러난다.

**v3[Prof.김 모델]**: 관계 자체가 아직 없음 (47개체 확장 이전 핵심 패턴 4종에만 국한).

**v8**:
```turtle
:이승훈소속신민회_01 rdf:type :Event ;
    :hasObject :이승훈 ; :hasPostObject :신민회 ; :hasEventType :소속 ;
    :hasTimeValue "1907-01-01T00:00:00"^^xsd:dateTime ;
    :hasEestimation "1"^^xsd:boolean ; :hasTimeEestimationRangeValue 1 ;
    :hasTimeEestimationRangeType "Year"@ko ;
    rdfs:comment "[v7] 한국민족문화대백과사전(신민회 항목) 및 Encyves Wiki 교차확인: ..." ;
    :hasBibo "한국민족문화대백과사전, '이승훈' 항목"@ko ;
    :hasBibo "한국민족문화대백과사전, '신민회' 항목"@ko .
```
관계·시간·출처가 **한 Event 노드 안에 전부 뭉쳐** 있다. 
출처가 문자열이고, 검증 판단(왜 1907년인지)이
자연어 comment 안에 서술돼 있어 기계적으로 질의하기 어렵다.
(자연어와 기계어 설명은 comparison_report_v3_8_9_machin_ query.md에 있으니 생략)

**v9.5**:
```turtle
claim:CLM-018 a prov:Claim ;
    prov:hasSubject ent:이회영 ; prov:hasObject ent:신민회 ; prov:hasRelation "소속" ;
    prov:claimText "이회영은 신민회에 소속되어 중심 인물로 활동하였다."@ko ;
    prov:hasClaimStatus vocab:confirmed ;
    prov:hasDateStatus vocab:not_directly_verified ;
    prov:hasVerificationStatus vocab:directly_verified ;
    prov:hasSource src:SRC-018 ; prov:hasEvidence evd:EVD-018 ;
    prov:changeHistory "... v9.5: date_status 공란→not_directly_verified 정합화 ..." .

src:SRC-018 a prov:Source ;
    prov:sourceTitle "이회영" ;
    prov:sourceUrl "https://encykorea.aks.ac.kr/Article/E0046635"^^xsd:anyURI .
```
`Claim`(주장) · `Evidence`(근거 요약) · `Source`(제목+타입 있는 URL)가 **분리된 개체**로 존재하고,
"날짜가 왜 없는가"는 `not_directly_verified`라는 통제 어휘로, "얼마나 믿을 만한가"는
`hasClaimStatus`/`hasVerificationStatus`로 각각 기계가 질의 가능한 형태로 분리되어 있다.


---
 
## 6. 개념 대응표 (Prof.김 모델 ↔ v8 ↔ v9.5)

| Prof.김 모델 | v8의 대응 | v9.5의 대응 |
|---|---|---|
| 사건모델: `:Event`(`hasObject`/`hasPreObject`/`hasPostObject`/`hasEventType`) | TTL에 그대로 구현 | `subject_uri`/`relation`/`object_uri`로 구조화(단, "사건"이 아니라 "주장" 단위, §7 참조) |
| 학술모델: `hasBibo`(전통 서지)/`hasWebResource`(URL) | `hasBibo`는 문자열, `hasWebResource`는 대체로 미기입 | `source_id`+`source_title`+`source_url`(개체 분리) + `evidence_id`+`evidence_note`(근거 문장까지 별도 개체) |
| 추정모델: `hasEestimation`(0/1) + `hasTimeEestimationRangeValue/Type` | 그대로 사용, 다만 "사건 존재 자체의 불확실성"까지 억지로 떠맡음(§3-③) | `date_value`+`date_precision`+`date_value_status`+`has_estimation`(4개 필드로 세분) |
| (원 논문에 없음, v8에서 즉석 추가) `hasValidationStatus` | 3지 판정(완료/권장/보류) — 실제 분포는 권장 29 > 완료 19 > 보류 1로, "대부분 재검증이 남아 있다"는 쪽에 치우침 | `claim_status`+`date_status`+`verification_status`+`review_flag`(4개 독립 축) + `part`(core/hold/exclusion, 3분할) |
| 조직모델: `hasGroupPart`/`isGroupPartOf`/`succeedTo`류 | 코멘트로 자유서술(예: "승계관계 삭제") | 별도 조직 URI 분리(`:조선물산장려회_평양` vs `:조선물산장려회_서울`)로 구조화 |
| 공리설계(재직기간=해임-임명 등) | 날짜가 구조화 안 돼 계산 불가 | 이론상 `date_value`가 채워진 Claim끼리는 계산 가능하나, 실제 파생값 계산은 아직 미구현 |
 
**가장 중요한 줄은 `hasValidationStatus` 행이다.**  
> Prof.김 모델은 "관계 자체가 불확실할 수 있다"는 축을 원래 갖고 있지 않았다. 
> v8은 그 빈칸을 속성 하나로 메웠고, v9.5는 그걸 아예 4개의 독립 축으로 재설계했다.
 
---
 
## 7. 같은 사실, 세 스키마의 실제 기록 — 3중 대조
 
 
### 7-1. 오산학교 설립 — ①(실증됨)
 
**근거 상태**: v6~v8 TTL에 실제로 `:19071224이승훈설립_01`(hasObject=:이승훈,
hasPostObject=:오산학교, hasEventType=:설립, hasTimeValue=1907-12-24T00:00:00,
hasEestimation=0) 트리플이 그대로 존재한다.
 
**v8 실제 기록**: "1907년 12월 24일 이승훈이 … 설립", **재검증 필요 여부: 완료**.
`출처(1차 확인)`란에는 "한국민족문화대백과사전 / 우리역사넷 / 독립운동인명사전" 세 매체가
나열돼 있을 뿐, 어느 매체가 정확히 "12월 24일"을 말하는지는 구분되지 않는다.
 
**v9.5 실제 기록**:
```text
CLM-OSAN-01  이승훈 --설립--> 오산학교   1907-12(Month)      part=core
CLM-OSAN-02  이승훈 --개교--> 오산학교   1907-11-24(Day)      part=hold
```
> Prof.김 모델의 `:Event` 한 개, v8의 "완료" 한 줄은
> 학교 연혁 계열 출처(12월)와 인물 항목 계열 출처(11월 24일)가 서로 다른 값을 말하고 있었다는 사실을 밝히기 어렵다.
> 관련 내역은 Evidence 단위로 분리하고 나서야 드러났다.
 
### 7-2. 김좌진 — 신민회 — ①(실증됨)
 
**근거 상태**: v7~v8 TTL에 실제로 `:hasValidationStatus "검증보류"`가
`:김좌진소속신민회_01`에 부여된 것이 확인된다. 이 속성이 원 논문에 없다는 것도 v8 changelog
자체가 명시하는 사실이다 — 가정이 아니다.
 
**v8 실제 기록**: **재검증 필요 여부: 보류(v8)**. 비고에 "`hasValidationStatus` '검증보류'
속성을 신설해 이 관계를 활성 그래프에서 격리 처리함"이라고 명시.
 
**v9.5 실제 기록**:
```text
CLM-KIM-01  김좌진 --가입--> 신민회       claim_status=confirmed   part=core
CLM-KIM-02  김좌진 --활동--> 청년학우회   claim_status=confirmed   part=core
```
v8의 "보류"가 완전히 뒤집혔다. 원인은 모델의 우열이 아니라 **어떤 Evidence를 확인했는가의
차이**다 — 이전 검증은 "신민회 공식 명단"이라는 Source 하나만 확인했고, v9.5는 "김좌진 본인의
인물 항목"이라는 두 번째 Source를 추가로 확인해 그 안에서 직접 서술을 찾아냈다.
 
---
 
## 8. 세 스키마의 "확신"이 의미하는 바가 다르다
 
| | 김바로 모델(`hasEestimation`) | v8(`재검증 필요 여부`) | v9.5(`claim_status`+`date_status`) |
|---|---|---|---|
| "확실"의 단위 | 사건 하나(날짜만) | 항목 하나(모든 측면 종합) | 주장 하나(사실 여부)와 날짜 하나(정밀도)를 분리 |
| 표현 가능한 값 | 0 또는 1 (이진) | 완료/권장/보류(v8) 3지 | confirmed/confirmed_indirect/validation_hold/contradicted × verified/inferred/estimated/conflicting_sources/not_directly_verified/not_applicable (조합 다수) |
| "관계 자체가 불확실함"을 표현 가능한가 | 불가능(추정모델은 날짜 전용) | 가능하지만 속성을 즉석에서 신설해야 함(`hasValidationStatus`) | 애초에 설계에 포함(`claim_status=validation_hold`, `review_flag`) |
| 중복 서술(같은 사실, 다른 Evidence)을 표현 가능한가 | 불가능(사건 하나=행 하나) | 불가능(항목 하나=행 하나) | 가능(Claim을 항목당 여러 개 둘 수 있음) — 실제로 CLM-002/CLM-011, CLM-OSAN-01/02 사례로 노출됨 |
 
---
 
## 9. v9.5의 장점
 
1. **Prof.김 모델은 "사건을 어떻게 표현할까"에 최적화된 범용 스키마다.** `hasEestimation`
   하나로 날짜의 확신도는 깔끔하게 표현하지만, "이 관계가 애초에 존재하는가"라는 질문은 설계
   범위 밖이었다.
2. **v8(정확하게는 v2~v8)은 그 모델을 그대로 쓰면서, 빈칸이 드러날 때마다 속성을 하나씩 추가해 메웠다**
   (`hasValidationStatus`가 대표 사례). 이 방식은 "지금 당장 급한 문제"는 해결하지만, 어떤
   축이 새로 필요했는지의 논리적 근거는 코멘트로만 남고 스키마 자체에는 체계적으로 반영되지
   않는다.
3. **v9.5는 4개의 독립된 축 + 3분할 + Source/Evidence 분리로 설계했다.**
   그 결과 항목 단위였던 것이 Claim 단위로 늘어났다 —
   "항목 하나 = 확신도 하나"이던 것이 "항목 하나 = 여러 개의 독립 평가 대상"으로 바뀐 것의
   직접적 결과다.
---
 
## 10. v9.5의 단점 — 사건 인과연쇄의 표현력
 
 
Prof.김 모델의 `hasPreObject`/`hasPostObject`는 "사건이 사건을 참조"할 수 있게 설계되어
있고, 이 프로젝트는 실제로 이를 활용해 **사건 인과연쇄**를 표현했다. 다만 그 연결 방식은
"A가 B를 가리키고 B가 C를 가리키는" 순차 체인이 아니라, **"확대"라는 별도의 Event 자신이
이전 상태(hasPreObject)와 이후 상태(hasPostObject)를 양쪽에 붙들고 있는 허브 구조**다.
실제 트리플 방향은 다음과 같다.
 
```text
:19101201안명근체포_01 (Event, 체포)
        ▲
        │ hasPreObject
:안악사건확대_01 (Event, 확대) ──hasPostObject──▶ :안악사건 (Event)
                                                        ▲
                                                        │ hasPreObject
                                :19110101백오인사건확대_01 (Event, 확대)
                                                        │
                                                   hasPostObject
                                                        ▼
                                                    :백오인사건 (Event)
```
 
즉 `:안악사건확대_01`이 "이전 상태=안명근체포, 이후 상태=안악사건"을 자기 자신의 두
속성으로 갖고, `:19110101백오인사건확대_01`이 "이전 상태=안악사건, 이후 상태=백오인사건"을
또 자기 자신의 두 속성으로 갖는 식이다 — 각 "확대" Event가 앞뒤 상태를 양쪽에서 참조하는
방식으로 2단계 확대 과정을 표현했다(v6에서 확립). 이는 김바로 사건모델의
`hasPreObject`/`hasPostObject`가 "관련 사건"까지 참조할 수 있도록 확장(v6, 검토안 6·24번
반영)된 덕분에 가능했다.

v9.5 통합본 역시 위 내역을 다음의 두 Claim을 통해 구현했으나,
구현 과정에서 손실된 부분이 존재한다.
 
```text
CLM-007  :안악사건 --related_to--> (object 없음)   claim="안악사건은 일제가 민족운동 세력을 탄압한 사건이다."
CLM-014  :안악사건 --related_to--> :105인사건        claim="안악사건은 이후 105인 사건으로 이어지는 계기 가운데 하나로 언급된다."
```

이와 관련하여 **"안악사건 → 105인사건(=백오인사건)"이라는 2단계 중 뒷부분은 `CLM-014`가 이미 표현하고 있다.**
이 Claim은 v9.4 단계에서 subject를 `:안명근`(인물)에서 `:안악사건`(사건)으로 정정하며 만들어진 것인데,
생성 과정에서 다음의 두 문제점이 발생했다.
 
1. **관계의 의미가 뭉개진다.** `CLM-014`의 `relation` 값은 `related_to`인데, 이 값은
   `CLM-022a`(서일–북로군정서, 인과관계 아님)처럼 인과와 무관한 다른 관계에도 똑같이 쓰인다.
   김바로 모델의 `:확대`(hasBT로 상위어까지 연결 가능한 전용 사건유형)에 해당하는 **전용
   relation 어휘가 v9.5에는 아직 없다** — "관련이 있다"와 "확대되어 이어졌다"를 구분할 방법이 없다.
2. **1단계(안명근체포→안악사건)는 아예 빠졌다.** v9.4에서 `CLM-014`의 subject를 `:안명근`에서 `:안악사건`으로 옮기면서, 
    **"안명근" 자신을 subject나 object로 갖는 Claim이 현재 core+hold 39건 중 단 하나도 남지 않게 됐다.** 
    원래 2단계 구조(안명근체포→안악사건→백오인사건) 중 뒷단만 살아남고 앞단은 v9.4 수정 과정에서 조용히 사라진 것이다.

> 정리하자면, "모델로 표현은 가능하다." 그러나 "① 전용 관계 어휘가 없어 인과와 단순 연관을 구분 못 하고", 
> ② 실제 데이터에서 한쪽 단계가 유실됐다"는, 스키마 설계와 데이터 정합성이 뒤섞인 문제가 발생했다.
>** 전자는 `relation` 통제어휘에 `확대`류 값을 추가하면 되고,
>> 후자는 안명근(인물) 자신을 subject로 갖는 Claim을 다시 만들어 넣으면 될 것 같은데, 일단 후속 과제로 남긴다.
 
---
 
## 11. 종합 판단
 
1. **v3의 다섯 어색함 중 4개는 v8 단계까지도 구조적으로 해소되지 않았다.** 하나(백오인사건
   이중타입)만 실제로 고쳐졌고, 나머지는 "왜 이런지" 설명을 붙이는 방식으로 봉합했다.
2. **그럼에도 v8은 헛수고가 아니다.** `hasValidationStatus`, 근거 없는 관계의 실제 삭제
   (succeedByPersonTo), "사건 존재 자체의 불확실성"을 어떻게든 표현하려던 시도는 모두 v9에서
   Claim/Evidence/Source로 공식화되는 데로 이어졌다.
3. **v9.5의 진짜 기여는 새로운 사실을 더 찾아낸 게 아니라, "이 사실을 어떻게 믿을 수 있는가"
   라는 질문에 답하는 전용 어휘 체계(Claim/Evidence/Source, 통제된 dateStatus/claimStatus
   vocab)를 만든 것이다.** v8이 자연어 comment로 하던 일을, v9.5는 기계가 질의할 수 있는
   속성으로 끌어올렸다.
4. **다만 v9.5도 모든 걸 풀지는 못했다.** 대성학교 설립 관련 중복 Claim(CLM-002/CLM-011)
   병합 문제, 그리고 안악사건 인과연쇄의 1단계 유실과 전용 relation 어휘 부재처럼, 세분화
   과정에서 오히려 새로 생긴 손실도 있다 — 이건 v9.5의 결함이라기보다, **목적이 다르면
   필요한 스키마의 세밀함도 달라지고, 그 세분화 과정에서 개별 데이터가 유실될 위험도 함께
   커진다**는 걸 보여주는 흔적으로 봐야 한다.
