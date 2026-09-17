1. v1~v8 (온톨로지 본체)
김바로 논문 스키마 기반 단일 Event 모델로 8단계 진화. 이항관계(v1)→사건유형별 클래스(v2)→단일 Event 스키마(v3)→편찬메타데이터 정합(v4~v5)→3회차 검토안 반영(v6, 오산학교 개교일·안명근체포 등)→날짜자동상속금지 원칙 최초 적용(v7)→불확실성 자체의 모델링(v8, hasValidationStatus 신설·신흥강습소 실체분리). v9 계열은 이 v8을 검증하기 위해 병렬로 시작된 별도 Provenance 트랙이지 v8의 다음 버전이 아님.

2. v9.1 — Pre-TTL Clean, 구조 검증
55개 Claim(신뢰도 필터링 이전) 전체를 구조적으로만 검증. CLM-023(SRC-004/EVD-004 오배정→SRC-113 분리), CLM-010(비표준 Decade precision 제거) 2건 수정. 6개 자동검증 통과 후 TTL 생성(1155 트리플). source_url을 IRI 대신 리터럴로 저장, item_no와 Claim을 분리하는 설계 결정.

3. v9.2 — High-Confidence 선별 (39+16)
39개 포함 Claim + 16개 exclusion으로 최초 분리. 재검증 중 재발 버그 4건 발견: CLM-006 컬럼 밀림, CLM-023 SRC 재충돌, CLM-010 Decade 재발, item 15(안악사건) 완전 누락. TTL 928 트리플. "39 High-confidence"라는 표현이 부정확했음을 스스로 예고(review_flag 섞여 있음).

4. v9.3 — 3분할 구조 확립 (34 Core + 5 Hold + 16 Exclusion)
"39 High-confidence" 정정 → 34 Core + 5 Hold. 유지/수정/보류/제외 4단계 판정 확정. CLM-OSAN-01(유지)과 CLM-OSAN-02(보류)의 비대칭 사례로 review_flag≠판정 원칙 실증. CLM-023이 또 재누락된 것을 발견해 "개별 버그가 아니라 파이프라인 재현성 문제"로 격상. TTL 969 트리플. "완성본 아닌 초안"으로 명시.

5. v9.4 — Claim 문장·URI·relation 의미 정합성
자동검증으로는 못 잡는 의미론적 불일치 6건 수정: CLM-014(subject 오류), CLM-003(수동태 방향불일치), CLM-022b(복수주체-단수object), CLM-046/016/018/019(소속-활동 간극). not_applicable vocab 신설, exclusion disposition을 excluded_from_ttl로 통일. 8개 자동검증. TTL 972 트리플. 데이터 사전 신설.

6. v9.5 — date_status 완전 정합화, 규칙의 자기교정
남은 15건의 빈 date_status 해소. 1차 제안 규칙("date_value 없음→전부 not_applicable")이 스스로의 경고를 어기는 자기모순임이 재검토에서 발견돼 폐기, "Claim의 시간적 의미" 기준 규칙으로 재수립. 결과: not_applicable 9건 + not_directly_verified 6건, 빈값 0건. TTL 987 트리플. 9개 자동검증 전부 통과.

7. v9.5 설명서 — Date Rule 명문화
정의·성격 서술(CLM-006/022a/022b)과 참여 Claim(Rule G-02, 사건일과 개인 참여일 분리)은 not_applicable, 설립·재직·소속처럼 실제 시간축이 있는데 미확인인 것(CLM-002/011/013/016/018/019)은 not_directly_verified로 구분하는 근거를 상세 기술. "규칙을 한 번 잘못 세웠다가 고친 경위를 숨기지 않는다"는 태도 명시.

8. v9.5 vs v9.5re — 시각화 레이어 비교 (diff 기반)
v9.5re는 새 데이터 버전이 아니라 같은 v9.5 데이터에 SEMANTIC_REVIEW(CLM-024, CLM-027-04 2건) 표시축만 얹은 오버레이. diff 49줄 전부가 문구·정적 참조표·조건부 렌더링에 국한되고 데이터 fetch/파싱 로직은 0줄 변경. dashes(core/hold 구분)는 review와 무관하게 유지됨을 코드 레벨에서 확인.

9. v10 + 공훈전자사료관 API 연동 시행착오 (보고서 미작성, 진행 중)
v9.5re 위에 공훈전자사료관 탭만 순증(diff 193줄 추가/2줄 삭제, GIS·관계망 코드 무변경). 그러나 실사용 단계에서 연쇄 실패: ① 필드명 오류(성명→NAME_KO, 수정완료) ② HTTP-only API vs HTTPS 배포로 인한 mixed content 차단(구조적, 코드로 미해결) ③ 공식 문서의 nameKo 파라미터가 실제로는 서버에서 무시됨(직접 호출로 실측 확인) → 전체 순회 방식(약 382페이지)으로 회귀 ④ 순회 중 서버가 내려주는 XML 자체가 명세를 위반하는 문자 참조를 포함해 파싱 오류로 재중단(139/382 페이지 지점) — 재시도 로직이 결정론적 오류와 일시적 오류를 구분 못하는 설계 허점 발견. 현재 이 문제의 해결책(파싱 오류 시 페이지 skip-and-continue)까지는 확정, 실제 완주는 아직 미완료 상태로 남아 있음.