# 일제강점기 독립운동-근대학교 온톨로지

일제강점기 독립운동가·근대학교·단체·사건 간의 관계를 온톨로지(RDF/OWL)로
구조화한 프로젝트. 모든 사실관계는 우리역사넷, 한국민족문화대백과사전,
위키백과 등을 교차 확인해 반영했다.

시각화 도구는 별도 저장소
[makeGraph2026_refined](https://github.com/iteratorfor42/makeGraph2026_refined)에서
관리한다. 
이 저장소는 데이터(온톨로지)에 집중한다.

## 구축 순서

1. **`data/independence_school_ontology.ttl`** — 1차 설계 (이항관계 중심)
   Protégé로 편집 가능한 표준 OWL/Turtle. 신민회 계열 오산학교·대성학교에서
   시작해 숭실학교·보성학교·신흥무관학교(계몽운동↔무장투쟁을 잇는 다리)·
   청산리전투·대한민국임시정부·조선물산장려회/신간회(국내 계열)·
   3.1운동 이후 친일로 전향한 인물(최린·정춘수·박희도)까지 단계적으로 확장했다.
   총 53개 개체, 78개 관계.

2. **`data/kimbaro_style_ontology.ttl`** — 2차 설계 (사건 중심 재설계)
   한국학중앙연구원 인문정보학 전공(김현 교수 정립, 김바로 교수 계승)의
   방법론을 적용한 버전. "설립", "임명", "역할" 같은 사건 자체를 노드로
   승격시켜, 시간·장소·원문 근거를 사건에 직접 묶었다. 1차 설계의 한계였던
   "시간에 따른 지위 변화"(예: 최린이 1919년엔 독립운동가, 1934년 이후엔
   친일 협력자였다는 사실)를 `RoleEvent`로 표현해 해결했다. 현재는 핵심
   패턴 4종(임명 사건, 설립 사건, 역할 변화, 사건 인과 연쇄)만 예시로
   변환되어 있으며, 전체 확장은 진행 중.

3. **`scripts/ttl_to_lst.py`** — MAKEGRAPH2022 변환기
   `data/*.ttl`을 파싱해 `makeGraph2026_refined`가 읽는 `.lst` 포맷으로
   변환한다. TTL의 세분화된 서브클래스(IndependenceActivist, Educator 등)를
   `.lst`가 허용하는 6개 클래스(School/Organization/Event/Place/Person/
   ColonialCollaborator)로 압축하고, `ledTo` 관계는 `.lst`의 `sequence`
   화살표(사건의 시간적 인과 표현)에 매핑했다.

   ```bash
   pip install rdflib
   python scripts/ttl_to_lst.py data/independence_school_ontology.ttl \
       -o makegraph-output/independence_school_ontology.lst
   ```

4. **`makegraph-output/`** — 변환 검증 결과
   위 스크립트로 생성한 `.lst`와, 이를 `makeGraph2026_refined`의
   `phase1-compatible/makegraph.py`에 실제로 넣어 생성한 HTML.
   오류 0건, 53개 노드·78개 링크·6개 클래스·15개 관계 정상 파싱 확인.

   ```bash
   # makeGraph2026_refined 저장소를 클론한 뒤
   python phase1-compatible/makegraph.py \
       independence-movement-ontology/makegraph-output/independence_school_ontology.lst
   ```

5. **`viz/independence_school_ontology.html`** — 독립 D3.js 뷰어
   MAKEGRAPH와 별개로, 브라우저에서 바로 여는 것만으로 동작하는
   자체 인터랙티브 그래프. 노드 클릭 시 사료 설명(`.lst`에는 담기지
   않는 상세 정보)까지 패널에 표시된다. GitHub Pages로 배포하면
   `https://사용자명.github.io/independence-movement-ontology/viz/`로
   바로 접근 가능.

## 알려진 한계

- `.lst` 포맷은 노드별 자유 서술(사료 원문, 설명)을 저장할 필드가 없어,
  MAKEGRAPH 결과물에는 이름·클래스·관계만 남는다. 상세 설명이 필요하면
  TTL 원본이나 `viz/` HTML을 참고할 것.
- `kimbaro_style_ontology.ttl`은 아직 4개 예시 패턴만 구현되어 있고,
  전체 53개 개체로 확장되지 않았다.

## 참고 방법론

- 김현, 『인문정보학의 모색』, 북코리아, 2012.
- AKS 디지털인문학연구소, ["온톨로지 설계 방법"](https://dh.aks.ac.kr/Edu/wiki/index.php/온톨로지_설계_방법)
