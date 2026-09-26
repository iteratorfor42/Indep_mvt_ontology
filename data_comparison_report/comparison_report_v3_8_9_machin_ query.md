## 기계 질의(Machine Query) 관점에서 본 v3 vs v8 vs v9.5

### v3: 검증 상태를 표현할 속성 자체가 없음

```turtle
:19071201이승훈설립_01 rdf:type :Event ;
    :hasObject :이승훈 ; :hasPostObject :오산학교 ; :hasEventType :설립 ;
    :hasTimeValue "1907-12-01"^^xsd:dateTime ;
    :hasEestimation "1"^^xsd:boolean ; :hasTimeEestimationRangeValue 1 ;
    :hasTimeEestimationRangeType "Month"@ko ;
    :hasCompiler :iteratorfor42 ;
    :hascompiledTime "2026-08-19T00:00:00+09:00"^^xsd:dateTime ;
    :hasBibo "한국민족문화대백과사전, '오산학교' 항목"@ko ;
    :hasWebResource "https://encykorea.aks.ac.kr/" .
```

v3에는 아직 "이승훈-신민회 소속" 관계 자체가 없어 — 47개체 확장 이전, 핵심 패턴 4종만 존재 —
**동일한 Event 스키마를 쓰는 가장 가까운 실제 예시인 "이승훈-오산학교 설립" 사건으로 대신**한다.

> `hasEestimation`은 "이 시점이 확실한가, 추정인가"만 구조화되어 있을 뿐, 
> **"이 관계 자체가 맞는지"를 표현할 속성이 아예 없다.** 
> 즉, v3 단계에서는 "이 사실을 얼마나 믿을 수 있는가"라는 질문 자체를 물을 방법이 없었다.

### v8: 검증 축이 하나 생겼지만, 대부분은 여전히 자연어

```turtle
:김좌진소속신민회_01 rdf:type :Event ;
    ...
    rdfs:comment "[v7] 재검증 결과, ... 김좌진은 포함되어 있지 않음. ... 재검증이 강력히 필요함 ..." ;
    :hasValidationStatus "검증보류"@ko ;
    ...
```

v8은 v3에 없던 **`hasValidationStatus`라는 새 데이터 속성을 실제로 도입**했다. 이건 규모 확장이
아니라 종류가 다른 변화다 

> v3는 "이 관계가 맞는지 의심스럽다"는 판단을 표현할 방법이 전혀 없었다.
> v8은 최소한 하나의 관계에 대해서나마 그 판단을 `SELECT ?e WHERE { ?e :hasValidationStatus "검증보류" }` 같은 질의로 걸러낼 수 있는 수준까지 끌어올렸다.
> **이 점에서 v8은 v3보다 기계어에 더 가까워졌다고 할 수 있다.**

다만 이 개선은 어디까지나 일부 영역에서 가능할 뿐이다.
> v8 전체를 보면:
- `hasValidationStatus`가 부여된 관계는 47개체 중 1건(김좌진-신민회)뿐이고, 나머지 대다수
  관계의 신뢰도 판단은 여전히 `rdfs:comment` 자연어 문장 안에서만 이루어진다.
- 왜 특정 연도로 추정했는지, 왜 날짜를 안 넣었는지 같은 판단 근거는 v3와 마찬가지로 자연어
  서술로 남아 있다.
- 출처(`hasBibo`)도 v3와 동일하게 문자열이다.

> 즉 v8은 "검증 상태를 구조화된 속성으로 표현한다"는 아이디어가 구현되었지만,
> 그 아이디어를 전체 데이터셋에 일관되게 적용하진 못했다.

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

주체·대상·시간·출처가 한 `Event` 노드에 뭉쳐 있고, "왜 1907년으로 추정했는가"라는 판단 근거는
`rdfs:comment` 자연어 문장 속에 있다. 

> 이 문장을 사람은 읽고 이해할 수 있지만,
> SPARQL로 "근거는 확인됐는데 날짜는 미확정인 관계만 걸러줘" 같은 질의를 하려면 
> 문자열을 텍스트마이닝하거나 수작업으로 걸러야 한다.

### v9.5: 검증 상태의 핵심 축만 통제 어휘로 분리됨

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

`hasClaimStatus`/`hasDateStatus`/`hasVerificationStatus`의 값이 따옴표 없는 URI
(`vocab:confirmed`, `vocab:not_directly_verified` 등)로 일관되게 부여되고, `vocab:not_applicable`
같은 값은 `vocab:DateStatus`의 인스턴스로 명시 선언되어 있다.

> 그 결과 다음과 같은 SPARQL 질의가 실제로 가능해진다.

```sparql
# "사실관계는 확인됐지만 날짜는 아직 직접 검증 안 된 모든 Claim 찾기"
SELECT ?claim WHERE {
  ?claim a prov:Claim ;
         prov:hasVerificationStatus vocab:directly_verified ;
         prov:hasDateStatus vocab:not_directly_verified .
}
```
출처 역시 `hasBibo`처럼 이름만 있는 문자열이 아니라, `src:SRC-018`이라는 독립된 개체로 분리되고
`sourceUrl`이 `xsd:anyURI`로 타입까지 지정되어 실제 웹 자원(즉, 실제 링크 등)과 연결된다.

### 위 비교에서 유의해야 할 사항

**`prov:` 접두어는 "W3C 표준 PROV-O 채택"이 아니다.**
W3C PROV-O의 공식 네임스페이스(`http://www.w3.org/ns/prov#`)와 핵심 클래스는 `prov:Entity`,
`prov:Activity`, `prov:Agent` 세 가지이며, `wasGeneratedBy`/`wasAttributedTo`/`wasAssociatedWith`
같은 속성으로 이들을 연결한다. v9.5의 `prov:Claim`, `prov:Source`, `prov:Evidence`,
`prov:hasSubject`, `prov:hasRelation`, `prov:claimText` 등은 이 표준 어휘에 존재하지 않는
이름들이다.

> `prov:`라는 접두어는 표준 네임스페이스를 그대로 가져온 것이 아니라, 
> 본 연구가 독자적으로 설계한 로컬 온톨로지에 붙인 이름이다. 

> 즉, v9.5는 W3C PROV-O의 Claim–Evidence–Source 분리 정신에서 착안하였으나,
> 실제 클래스와 속성은 본 연구에서 독자적으로 설계하였다.
> `prov:` 접두어는 관례적 명명일 뿐, W3C 표준 네임스페이스(`http://www.w3.org/ns/prov#`)를 그대로 재사용한 것은 아니다.


### 요약

| 항목 | v3 | v8 | v9.5 |
|---|---|---|---|
| 검증 근거 | 자연어 `rdfs:comment` (또는 아예 없음) | 자연어 `rdfs:comment` | `hasClaimStatus`/`hasDateStatus`/`hasVerificationStatus` (통제 어휘, URI 값) |
| 출처 표현 | 문자열(`hasBibo`) — **이 한계가 v3에서부터 시작** | 문자열(`hasBibo`) | 독립 개체(`Source`) + 타입 있는 URL(`xsd:anyURI`) |
| 관계유형 다양성 | 4종(설립/임명/전향/확대)뿐 — 문제가 아직 규모 있게 드러나지 않음 | 여러 종류(소속/참여/영향/재직/경영 등)로 확장. 다만, 동일한 한계가 전체 데이터셋에 반복됨 | `hasRelation`으로 관계 성격을 Claim 자체에 문자열 기술 |
| SPARQL로 상태 필터링 | 사실상 불가 | 사실상 불가 (텍스트마이닝 필요) | 가능 (위 예시 질의 참고) |
| 서술적 내용(주장 문장, 근거 설명, 변경이력) | 자연어 | 자연어 | **v9.5에서도 여전히 자연어** — 완전 기계화는 아님 |
| 표준 근거 | 없음 | 없음 | W3C PROV-O에서 착안한 로컬 설계 — **PROV-O 자체를 재사용한 것은 아님** |
