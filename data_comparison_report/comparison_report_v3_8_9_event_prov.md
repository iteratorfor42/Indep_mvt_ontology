# v3 → v8 → v9.5 비교분석: 단일 Event 모델의 발전과 Provenance 모델로의 전환

> 이 글은 **3_semantic_archive_v3.ttl과 v8.ttl 그리고 v9.5(=v9_5).ttl을 비교분석**한다.
> `김바로 교수의 박사논문 적용에 충실한 v3`과 `그 개선본인 v8` 그리고 `검증 모델인 v9.5`를
> **Claim–Evidence–Source provenance 모델인 v9.5의 관점**에서 다시 살펴 보며,
> v3에서부터 고려했던 내역이 v8에서 각각 어떻게 됐는지
> ("해소" / "완화" / "그대로 남음")를 먼저 확인하고, v8이 왜 그럼에도 v9.5로의 전환이 필요했는지를
> 정리한다.

> readme (연구계획서에서는 김바로 교수의 박사논문에 대해 제대로 다루지 않는다.)
> 논문 한 편 정독한 것도 아닌 상황에서 구현 내역 일부만 ... 이거 넣기.


---

## 1. 핵심 결론

**`v8은 v3의 최종 개선본`이자 동시에 `단일 Event 모델의 한계를 스스로 증명한 버전`이다.**
v8은 여러 차례의 검토(3~5회차, P라운드: v8.1 추가 검증에서 확정한 원칙 겸 v8.1~v8.4 적용 라운드)를 거치며 
v3의 문제점 일부를 구조적으로 해소했지만, 나머지는 "왜 그런지 코멘트로 정당화"하는 선에서 멈췄다.
그렇기에 v9단계에서 Claim/Evidence/Source로 전면 재설계하게 되었다.

```
v3   단일 Event 스키마 확립 (원 논문 패턴 검증 단계)
  ↓  여러 차례 검토 라운드(1~5회차, P라운드)
v8   Event 스키마를 유지한 채 정교화의 한계까지 밀어붙임
  ↓  "코멘트로 정당화"만으로는 안 되는 지점이 누적
v9   Claim–Evidence–Source로 패러다임 전환
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

## 3. v8에서 실제로 새로 생긴 것 — 방향은 옳았다고 생각한다.???

v8은 헛돌기만 한 게 아니다. 특히 두 가지는 Provenance 사고의 맹아(씨앗???)라고 볼 만하다.

### ① `hasValidationStatus` — "존재 여부 자체가 불확실한 관계"를 표시하는 속성
```turtle
:김좌진소속신민회_01
    :hasValidationStatus "검증보류"@ko ;
```
신민회 공식 명단에 김좌진이 없다는 걸 발견하고도 완전히 삭제하지 않고 "검증보류" 상태로 격리한 것.
이건 v9.5의 `hasClaimStatus`(confirmed/confirmed_indirect/validation_hold)가 정확히
하려는 일을, Event 모델 틀 안에서 미리 적용했다....?????

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

## 4. v9.5는 무엇을 다르게 하는가 — v8과의 결정적 차이

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

**v3**: 관계 자체가 아직 없음 (47개체 확장 이전 핵심 패턴 4종에만 국한).

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

## 6. 종합 판단

1. **v3의 다섯 어색함 중 4개는 v8 단계까지도 구조적으로 해소되지 않았다.**
   : 하나(백오인사건 이중타입)만 실제로 고쳐졌고, 나머지는 "왜 이런지" 설명을 붙이는 방식으로 봉합했다.(?)
2. **그럼에도 v8은 헛수고가 아니다.**
   : `hasValidationStatus`, 근거 없는 관계의 실제 삭제 (succeedByPersonTo),
    "사건 존재 자체의 불확실성"을 어떻게든 표현하려던 시도는 
    모두 v9에서의 Claim/Evidence/Source로 공식화로 이어졌다.
3. **v9.5의 진짜 기여**
   : 새로운 사실을 더 찾아낸 게 아니라, **"이 사실을 어떻게 믿을 수 있는가"라는
   질문에 답하는 전용 어휘 체계(Claim/Evidence/Source, 통제된 dateStatus/claimStatus vocab)를
   만든 것**. v8이 자연어 comment로 하던 일을, v9.5는 기계가 질의할 수 있는 속성으로
   끌어올렸다고도 할 수 있다. 이 내용은 comparison_report_v3_8_9_machin_ query.md와 이어진다.
4. **다만 v9.5도 모든 걸 풀지는 못했다.** 
   : 대성학교 설립 관련 중복 Claim(CLM-002/CLM-011) 병합 문제처럼,
    v8에서 보류됐던 것 중 일부는 v9.5에서도 여전히 "후속 provenance 정리 과제"로 남아있다
    — 이건 v9.5의 결함이 아니라, 온톨로지 구축이 원래 계속 갱신되는 작업이라는 걸
   보여주는 흔적으로 봐야 한다.