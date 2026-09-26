# 온톨로지 시각화 버전 비교: v1 vs v6(~v8)
## 이 글은 본래 VisualHumanities 저장소의 post에 있었고, html로 시행착오 글을 구현하기 전 작성한 원본이다.


## 0. v1과 v6_with_gonghun & v8_with_gonghun 시각화 정리.
> v1 이항관계 경우 시각화했을 때 가시성이 좋았는데, 
> v3 이후 스키마(Prof.김바로 방식 단일 모두 적용한 Event 모델)가 v1식 하드코딩 그래프로 그리기엔 너무 복잡해져서, 처음부터 그래프가 아니라 .ttl 원문을 구문강조해서 보여주는 텍스트 뷰어(ttl-highlight.js)로 설계했다.

> v2~v5까지는 포트폴리오용으로 원문 ttl을 볼 수 있게끔 놔두되, 지난 8월 당시 기준 최종 버전이었던 v5를 기반으로 다시 시각화를 시도했다. 이게 v6이며, v6에 공훈api를 추가한 게 v6_with_gonghun이다.



> 관련하여 차이점 비교 표는 다음과 같다.

---

## 1. v1 vs v6_with_gonghun & v8_with_gonghun 핵심 차이 비교

| 구분 | v1 | v6_with_gonghun & v8_with_gonghun |
| :--- | :--- | :--- |
| **데이터 출처** | JS 파일 안에 `nodesData`/`linksData`로 직접 하드코딩 | `.ttl` 파일을 브라우저에서 `fetch`로 읽어와 실시간 파싱 |
| **시각화 라이브러리** | D3.js (Force-directed graph 직접 구현) | vis-network (관계망) + Leaflet (GIS 지도) |
| **온톨로지 구조** | `School`/`Organization`/`Event`/`Person`/`Place` 5개 타입이 직접 관계로 연결<br>*(예: 이승훈 —설립→ 오산학교)* | **김바로 교수님 박사논문 방식의 "단일 사건 스키마"**<br>모든 관계가 `Event` 노드를 매개로 `hasObject`/`hasPreObject`/`hasPostObject`로 표현됨 |
| **화면 구성** | 그래프 1개 + 필터 버튼 + 검색창 + 상세 패널 | 탭 3개 구조 (GIS 지도 / 관계망 / 공훈전자사료관 연동) |
| **좌표(장소) 정보** | 없음 (`Place`는 그래프 노드로만 존재) | Leaflet 지도에 실제 좌표로 표시 (온톨로지 명시값 1건 + 별도 조사값) |
| **외부 연동** | 없음 | 국가보훈부 공훈전자사료관 오픈API 대조 |
| **유지보수 방식** | 데이터가 바뀌면 JS 코드 자체를 수정해야 함 | `.ttl` 파일만 새로 만들면 뷰어 코드는 그대로 재사용 (v2~v8 전부 같은 패턴) |

> 아마 이 표를 보시면 왜 제가 굳이 ttl을 썼는지 아실 듯하여 관련 설명은 생략합니다.

---

## 2. "v1처럼 구현" 가능성 여부

> v1의 D3 force-graph 자체가 훨씬 더 자유로운 시각화 방식이며, 
> v6/v8의 event-centric 데이터를 v1 스타일로 그리는 것도 기술적으로는 가능하다.
> 실제 v8_d3style.html 경우 v1의 D3 스타일로 v8 데이터를 재현했다.

다만 구조적 차이에 따라 아래 내용의 구현이 어려울 수 있다.

* **v1의 방식 (이항관계):** `["이승훈", "오산학교", "설립"]` 형태 경우
    두 개체 간의 **이항관계(binary relation)**를 전제로 만들어졌다.

* **v6~v8의 방식 (사건 중심 스키마):** `.ttl` 파일의 관계는 전부 `Event`를 매개로 한다.
  :* `"최린 임명"` 이벤트가 `hasPreObject=천도교`, `hasObject=최린`, `hasPostObject=독립선언서초안작성자`를 가진다.
 (3개 이상의 개체가 하나의 사건으로 묶이며, 이렇게 사건이 복잡해지니 시각화도 복잡해지는 것)

### 해결 방안 (현재 구현 상태)
v6에서는 이러한 차이를 극복하기 위해 **"Event를 두 개의 간선으로 접어서(pre → object, object → post) v1과 비슷한 이항관계 그래프처럼 보이게"** 변환하는 로직(`ttl-parser.js` + `buildNetwork()`)을 구축.

> 현재 v6/v8의 관계망 탭은 사실상 "v1 스타일로 재현한 v8 데이터"이며,
> 단지 그래픽 라이브러리만 D3에서 `vis-network`로 변경된 형태이다.

## 3. 참고 사항
### 시각화 트랙과 관련하여 verification_report_v1-v10.md 전문은 다음과 같다.
### IV. 시각화 트랙 상세 (v6\~v10, dh-webpage)

### 1. v6.html

TTL을 fetch로 읽어 GIS+관계망 2탭으로 렌더링했다. 
`ttl-parser.js`로 Event를 두 개의 간선(`hasPreObject→hasObject`,
`hasObject→hasPostObject`)으로 "접어" 표시했다.

### 2. v6_with_gonghun.html

관계망 탭에 v1 스타일 필터·검색 UI를 이식하고, 
공훈전자사료관 연동을 최초 시도했다. 
당시 필드명 버그로 0명 매칭이 발생했다. 
이 버그는 이후 `v8_with_gonghun.html`에도 그대로 이어졌다가 v10에서야 발견 & 수정.

### 3. v8_d3style.html / v8_with_gonghun.html

v1의 D3 코드 자산을 v8 데이터로 재현했다. 
이 과정에서 버그 3건(숨은 탭 초기화, CSS grid 높이, `versions-data.js` 스키마 사고)을 발견·수정했다.

**\[해결\] v8 트리플 수 불일치(982 vs 985)**

`v8_with_gonghun.html`의 화면 표시 트리플 수(982개)가 
`v8.ttl` 원문을 rdflib로 직접 파싱한 결과(985개)와 3건 차이 나던 문제를 조사했다.
`ttl-parser.js`와 `v8.ttl`을 Node.js로 나란히 실행해 재현을 시도한 결과,
현재 코드·데이터 조합에서는 985개로 rdflib과 type별 구성까지 완전히 일치했다.

-   Ontology 1
-   Class 5
-   ObjectProperty 15
-   DatatypeProperty 14
-   Term 18
-   Group 14
-   Person 31
-   Event 74

총합만 우연히 같은 것이 아니라 구성 요소 단위로 검증했다. 
따라서 현재 파서에는 트리플을 누락시키는 버그가 없다. 

(아마 982 경우 필자가 5 대신 2를 잘못 누른 듯하다.)
>참고> 앞서 언급한 1/5/15/14/18/14/31/74(합 172) = 개체(instance) 수 관련 추가 설명.
>예를 들어 Event 인스턴스 74개는 각각 hasObject, hasEventType, hasTimeValue, hasCompiler 등 평균 5~6개 트리플을 갖고 있으니, 
>172개 개체가 985개 트리플을 만들어내는 건 인스턴스당 평균 5.7개 트리플이라는 뜻이다.
>본 프로젝트의 스키마(속성이 각 Event/Group/Person에 여러 개씩 붙는 구조)를 감안하면 자연스러운 비율이라 생각한다.

또한 위의 검증 과정에서 인물 수 30(UI 배열 `ONTOLOGY_PERSONS`)과 
31(rdflib의 `rdf:type :Person` 카운트)의 차이도 해소됐다.
편찬자 메타 개체 `:iteratorfor42`가 `rdf:type :Person`으로 선언되어
rdflib 카운트에는 포함되지만, 역사적 인물만 보여주는 UI 배열에는 의도적으로 제외되어
있었다. 따라서 이는 버그가 아니다.

### 4. v9_5.html

Provenance 트랙의 최초 뷰어다.
`claimDecision`(core 실선/hold 점선)으로 신뢰도 구분을 표시했다.

### 5. v9_5re.html

데이터는 `v9_5.html`과 완전히 동일하다. 
`SEMANTIC_REVIEW` 참조표(CLM-024·CLM-027-04 2건)로 
"의미론 재검토 권고" 표시축만 추가했다.
diff 기준으로도 데이터 fetch·파싱 로직은 0줄 변경으로 확인됐다.

### 6. v10.html + gonghun_match.py

공훈전자사료관 오픈API 연동 탭을 추가했다. 
필드명 오류(`성명`→`NAME_KO`)를 수정했으나, 
HTTP-only API와 HTTPS 배포 간 mixed content 차단이라는 구조적 문제가 남았다. 
공식 문서상 `nameKo` 파라미터가 실제로는 서버에서 무시됨을 직접 확인했고, 
브라우저 호출을 포기하고 `gonghun_match.py`(로컬 실행 스크립트)로 
전체 순회(약 382페이지) 방식으로 전환했다. 
그러나 순회 중 서버 XML 자체의 명세 위반으로 139/382페이지 지점에서 파싱이 재중단됐다. 
실패 원인이 바뀔 때마다 갱신 기록을 남겼으며, api는 **현재도 미해결**이다.
