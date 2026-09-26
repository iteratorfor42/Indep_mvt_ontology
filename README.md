# 일제강점기 독립운동-근대학교 온톨로지

[📖 온톨로지 프로젝트에 대한 자세한 소개 보기](./ontology_readme.md)

> 이 README에서는 전체 저장소에 대한 개괄적 설명을 다루며,
> 참고문헌과의 비교 분석 등 세부 내용이 궁금하시다면 위의 [📖 자세한 소개 보기]를 눌러 확인해 주시길 바랍니다.


일제강점기 독립운동가·근대학교·단체·사건 간의 관계를 온톨로지(RDF/OWL)로
구조화한 프로젝트. 
모든 사실관계는 우리역사넷, 한국민족문화대백과사전, 위키백과 등을 교차 확인해 반영했다.

이 저장소는 **데이터(온톨로지 본체 + 검증 기록)**에 집중한다. 
이 데이터를 브라우저에서 눈으로 확인하는 시각화 페이지(버전별 뷰어, 시행착오 기록,
공훈전자사료관 연동 등)는 별도 저장소 `dh-webpage`의 `site/ontology/`에서 관리한다.
혹은 다른 저장소 `makeGraph2026_refined_GUI_TTL_ver`에서 실행파일로 ttl을 확인할 수 있다.
(참고> ttl 사용 예시는 `makeGraph2026_refined_GUI_TTL_ver` 저장소에서 찾을 수 있다.)
또한 이 저장소에는 HTML/JS 뷰어를 두지 않는다.

> **진행 상황 요약(2026-09-10 기준)**: 이 온톨로지는 크게 두 갈래로 개선되어 왔다. 
> (A) **본체 설계**(`data/1_*` ~ `data/8_*`) — 이항관계(v1)
> → 사건 중심 재설계(v2~v3) → 5차례의 사실 검증·불확실성 모델링(v4~v8).
> (B) **Provenance 검증 트랙**(`data/9_*`, `data/v9_5_*`)
> — 본체(v8)를 감사(audit[혹은 검증])하기 위해 별도로 시작한, 스키마 자체가 다른(Claim 중심)
> 병렬 데이터셋(ver2~ver5 방법론 설계 → v9.1~v9.5 구현). **v9는 v8의
> "다음 버전"이 아니다.** 모든 단계의 검증 과정은 `data_report/`에
> 개별 보고서로 남겨뒀다.

## 데이터 변화 (`data/`)

버전마다 **독립된 스냅샷 파일**로 남겼다 — 하나의 파일을 계속 덮어써
이전 상태를 잃는 대신, 파일명 앞에 순번을 붙이고 각 파일 상단에 이전
버전까지의 누적 changelog 주석을 담는 방식을 택했다. 그래서 임의의
과거 버전을 그 파일 하나만 열어서 그대로 재현할 수 있다.

| 파일 | 버전 | 핵심 내용 |
|---|---|---|
| `1_independence_school_ontology.ttl` | v1 | 이항관계 중심 1차 설계. 신민회 계열 오산학교·대성학교에서 시작해 숭실학교·보성학교·신흥무관학교·청산리전투·대한민국임시정부·조선물산장려회/신간회·3·1운동 이후 친일 전향 인물(최린·정춘수·박희도)까지 확장. **53개체, 78관계** |
| `2_prof.kimbaro_style_ontology.ttl` | v2 | 사건 중심 재설계 초안. 한국학중앙연구원 인문정보학 전공(김현 교수 정립, 김바로 교수 계승) 방법론 적용 — "설립"·"임명"·"역할" 같은 사건 자체를 노드로 승격, 시간·장소·원문 근거를 사건에 직접 결합. `RoleEvent`로 "최린이 1919년엔 독립운동가, 1934년 이후엔 친일 협력자"같은 시간에 따른 지위 변화를 표현. 초안 시점엔 핵심 패턴 4종(임명/설립/역할변화/사건 인과)만 예시 변환 |
| `3_semantic_archive_v3_full_sourced.ttl` | v3 | v2의 예시 패턴을 전체로 확장, 단일 `:Event` 스키마 정착. **47개체, 627 트리플**, Protégé 정상 파싱 확인 |
| `4_semantic_archive_v4.ttl` | v4 | `hasCompiler`/`hascompiledTime` 미기입 65건 보강, `:백오인사건` Group/Event 이중 타입 충돌 해소, 중복 개체(`:이승훈설립오산학교_01`) 제거 |
| `5_semantic_archive_v5.ttl` | v5 | 편찬자 placeholder를 실제 개체(`:iteratorfor42`)로 전체 치환, 도메인을 "구한말 관공립학교"에서 "독립운동-근대학교 네트워크"로 확장 |
| `6_semantic_archive_v6.ttl` | v6 | 외부 검토안을 처음 도입해 필수수정 4건(안명근체포 시간·유형, 오산학교 개교일, 오산-대성 승계관계 삭제, 안악사건→백오인사건 2단계 확대구조) 반영 |
| `7_semantic_archive_v7.ttl` | v7 | "사건 날짜를 참여자 개인에게 자동 상속하지 않는다" 원칙을 데이터에 처음 대규모 적용(신민회/임시정부 소속 12건, 3·1운동 참여 9건), 설립→공동설립 구분 |
| `8_semantic_archive_v8.ttl` | v8 | `hasValidationStatus` 속성 신설 — "관계 자체의 존재 여부가 불확실한 경우"를 정상 fact와 구분해 격리(김좌진-신민회). 신흥강습소/신흥무관학교 실체 분리. **47개체**, `hasEestimation`/`hasTimeEestimationRange*` 추정모델 전면 적용 |
| `9_semantic_archive_v9_5.ttl` + `v9_5_claim_core.csv` / `v9_5_claim_hold.csv` / `v9_5_exclusion_manifest.csv` | v9.5 (Provenance 트랙 최종본) | v8까지의 인스턴스가 실제 근거를 갖추고 있는지 49개 항목 단위로 재검증한 결과물. Event 중심이 아니라 **Claim 중심** 스키마(subject/relation/object + source/evidence + claim_status/date_status/verification_status/review_flag 4필드 상태체계). **Core 34건 + Hold 5건**(TTL 반영, 987 트리플) **+ Exclusion 16건**(CSV만 보관, 삭제 아님) = 원본 49개 항목 전체 coverage |

## 사실관계 확인 자료 (`data/`)

- `independence_ontology_factcheck_v5.xlsx` / `independence_ontology_factcheck_v5csv` — v5 시점 47개체 사실관계 1차 확인표
- `independence_ontology_factcheck_v8.csv` / `independence_ontology_factcheck_v8.xlsx` — v8 시점 재확인표. 매체·확인방식·재검증 필요 여부를 기록

이 표들은 v9 계열 Provenance 트랙(Claim/Evidence/Source 분리 모델)의 전신에 해당.
— v9은 이 표가 항목 단위로만 근거를 표시하던 것을, Claim 단위로 쪼개고 출처·근거 문장까지 구조화한 것이다.

## 검증 보고서 아카이브 (`data_report/`)

버전마다 "무엇을 검증했고, 무엇을 발견했고, 무엇을 고쳤는가"를 개별 마크다운 보고서로 남겼다.
전체 흐름을 한 번에 보려면 `verification_report_v1-v10.md `(통합본)을 보고,
특정 버전의 세부 내용을 보려면 버전별 개별 보고서를 참고할 것.
(보고서를 일일이 또 재확인하고 수정하는 과정에서 꼭 필요한 검증 보고서만 일부 남겼다.
만약 이전 보고서가 필요하다면 깃 커밋 이력을 통해 확인 가능하다.)


```text
verification_report_v1-v10.md        본체(v1~v8) 전체 흐름 요약
verification_report_v8_1.md 
verification_report_v8_5.md
                                     v8 세부 검증(단계별 처리 과정)
verification_report_v9_1.md ~
verification_report_v9_5.md,
verification_report_v9_5_guide.md
                                     v9 계열(Provenance 트랙) 버전별 검증
                                     + v9.5 date_status 규칙 설명서
visualization_revision_report_v1_vs_v6.md
visualization_revision_report_v9_5_vs_v9_5re.md
                                     시각화 레이어 변경분 diff 기반 검증
                                     (실제 뷰어는 dh-webpage 저장소에 있음)
```

## 도구 — 변환·시각화 파이프라인 (v1 전용, 구형)

6. **`scripts/ttl_to_lst.py`** — MAKEGRAPH2022 변환기
   `data/*.ttl`을 파싱해 `makeGraph2026_refined`가 읽는 `.lst` 포맷으로 변환한다. 
   TTL의 세분화된 서브클래스(IndependenceActivist, Educator 등)를
   `.lst`가 허용하는 6개 클래스(School/Organization/Event/Place/Person/
   ColonialCollaborator)로 압축하고, `ledTo` 관계는 `.lst`의 `sequence`
   화살표(사건의 시간적 인과 표현)에 매핑했다.

> 간략히 말해서 원래 시각화를  `.lst`로 하고자 이거 만들었는데, 진행 과정에서 'ttl'과 'html'을 병행했다.
> (여담인데, lst로는 시각화 표현할 만한 게 많지 않기에 ttl을 썼다.)
> 마찬가지의 이유에서 초반에는 표를 xlsx과 csv로 함께 놔뒀지만, csv만 놔뒀다.
> (엑셀이 필요하다면 커밋 이력에서 사용 가능하지만, 필자는 csv 위주로 분석했기에 csv & 코랩 혹은 본인 IDE로 확인하는 걸 추천한다.)

   ```bash
   pip install rdflib
   python scripts/ttl_to_lst.py data/1_independence_school_ontology.ttl \
       -o makegraph-output/independence_school_ontology.lst
   ```

7. **`makegraph-output/`** — 변환 검증 결과
   위 스크립트로 생성한 `.lst`와, 이를 `makeGraph2026_refined`의
   `phase1-compatible/makegraph.py`에 실제로 넣어 생성한 HTML.
   오류 0건, 53개 노드·78개 링크·6개 클래스·15개 관계 정상 파싱 확인

> 앞서 적은 것처럼 이 저장소의 output은 별 의미가 없다. makegraph를 클린룸으로 구현한 ver이 궁금하다면, 관련 저장소를 확인하시길 바란다.

   ```bash
   # makeGraph2026_refined 저장소를 클론한 뒤
   python phase1-compatible/makegraph.py \
       independence-movement-ontology/makegraph-output/independence_school_ontology.lst
   ```

8. **`viz/independence_school_ontology.html`** — 독립 D3.js 뷰어(v1 전용)
   MAKEGRAPH와 별개로, 브라우저에서 바로 여는 것만으로 동작하는
   자체 인터랙티브 그래프. 노드 클릭 시 사료 설명(`.lst`에는 담기지 않는 상세 정보)까지 패널에 표시된다.

   > v3 이후(47개체, 단일 Event 스키마)와 v9 계열(Claim 스키마)을 보려면
   > 이 뷰어가 아니라 `dh-webpage` 저장소 `site/ontology/versions/`의
   > 페이지(v6, v8, v9_5, v9_5re, v10 등)를 참고할 것
   >— 스키마가 달라 이 D3 뷰어/MAKEGRAPH 파이프라인으로는 그대로 표시할 수 없다.

## 한계

- `.lst` 포맷은 노드별 자유 서술(사료 원문, 설명)을 저장할 필드가 없어,
  MAKEGRAPH 결과물에는 이름·클래스·관계만 남는다.
  (이런 점 때문에 그냥 .ttl을 이용한 것이다.)
- 6~8절의 MAKEGRAPH/D3 파이프라인은 **v1 스키마 전용**이다.
  이후 스키마가 단일 Event 중심으로 바뀌고 v9부터는 다시 Claim 중심으로 바뀌면서,
  두 파이프라인 모두 이후 버전으로 재적용·재검증되지 않았다. 
  v2 이후는 `dh-webpage` 저장소의 vis-network 기반 뷰어가 대신한다.
- v9 계열(Provenance 트랙)은 v8 본체와 **다른 스키마**를 쓴다 
 — 두 트랙을 하나의 통합 TTL로 병합하는 작업은 아직 이뤄지지 않았다.
  (이건 노력 대비 완성도 높은 결과가 나오기 힘들기에 안 하는 게 좋다고 생각하며, 그냥 병렬로 접근 & 비교 분석하는 걸 추천한다.)


## 프로젝트 참고 사항 및 AI 활용 내역
- 데이터 보안 및 프라이버시 준수: Claude(무료 기본 버전: Sonnet 5) 및 ChatGPT(무료 기본 버전:GPT-5.5 Instant~GPT-5.6 Luna) 활용 시, 입력 데이터의 비식별화 전처리 및 AI 학습 방지(Opt-out) 설정을 적용하여 보안을 중시했습니다.

- 역할 분담: 핵심 로직 구현은 직접 수행하였으며, 앱과 웹 개발 및 시각화 처리, 기본 데이터 분석 코드 작성 및 문서 검증 과정에서 AI를 보조 도구로 병행 활용했습니다.   

- 한계점 및 대응: 온톨로지 비식별화 방식에 대한 이해 부족으로 인해, Opt-out 상태에서 공개된 인터넷 문서를 원 데이터로 삼았습니다. 또한 이번 포트폴리오에 포함된 DS 계열 또한 김소월 시처럼 공개된 인터넷 문서에 적용했습니다.
  
## 참고 문헌

- 김현 (2012). 인문정보학의 모색. 북코리아.
- 김바로. (2017). *제도와 인사의 관계성 데이터 아카이브 구축과 활용: 근대 학교 자료(1895~1910)를 중심으로* [박사학위논문, 한국학중앙연구원 한국학대학원].
- 김바로 (2018). 『시맨틱 데이터 아카이브의 구축과 활용. 디지털인문학연구총서 6. 보고사.   
- AKS 디지털인문학연구소. ["온톨로지 설계 방법"](https://dh.aks.ac.kr/Edu/wiki/index.php/온톨로지_설계_방법)
- 류인태, 곽지은, 권기성, 김바로, 김병준, 김지선, 박진호, 양승목, 이민철, 이재연, 장문석, 지영원, 한희연 (2023). 디지털로 읽고 데이터로 쓰다: 디지털 한국어문학의 모색. 성균한국어문학총서 2. 휴머니스트.
- Tuominen, J., Hyvönen, E., & Leskinen, P. (2018). Bio CRM: A data model for representing biographical data for prosopographical research. In A. Fokkens, S. ter Braake, R. Sluijter, P. Arthur, & E. Wandl-Vogt (Eds.), *Proceedings of the Second Conference on Biographical Data in a Digital World 2017 (BD2017)* (pp. 59–66). RWTH Aachen University. http://ceur-ws.org/Vol-2119/paper10.pdf
(Baro. (2025, May 21). BioCRM: 인물 생애 정보 기술을 위한 데이터 모델. 한국디지털인문학협의회 (KADH). https://www.kadh.org/biocrm-%EC%9D%B8%EB%AC%BC-%EC%83%9D%EC%95%A0-%EC%A0%95%EB%B3%B4-%EA%B8%B0%EC%88%A0%EC%9D%84-%EC%9C%84%ED%95%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EB%AA%A8%EB%8D%B8/)
- 김바로. (2026년 5월 11일). *지식 그래프 기반 근대 인물 LOD 구축 및 LLM 연계를 위한 지식 보충 생성(KAG) 모델 연구*. 한국디지털인문학협의회(KADH). KADH 연구과제 소개 페이지.

