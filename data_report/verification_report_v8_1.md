# v8 추가 검증 보고서

## — 49개 항목 출처 URL 팩트체크 및 Provenance Layer 설계

### 1. 검증 목적

나는 v8 RDF와 CSV에 담긴 각 사실을 다시 출처까지 역추적하여 다음 구조를 확립하고자 했다.

> **개체/사건 → 주장(Claim) → 관계(Relation) → 날짜(Date) → 실제 출처(Source URL)**

기존 CSV의 `출처(1차 확인)` 컬럼은 "어떤 자료를 참고했는가" 수준에 머물러 있었다.

이번 v8 추가 검증에서는 이것을 다음 단계로 강화하기로 했다.

> **이 RDF 트리플을 왜 넣었는가?
> 그 관계와 날짜를 실제로 증명하는 출처는 무엇인가?
> 그 출처의 어느 내용이 해당 값을 지지하는가?**

이를 위해 각 RDF 주장마다 provenance 정보를 1:1로 연결하는 작업을 진행했다.

---

# 2. 1차 핵심 발견 — 기존 CSV의 "확정"을 그대로 유지하면 안 되는 항목

## 2-1. 이승훈 → 오산학교 → 1907-12-24

### 기존 CSV

> 1907년 12월 24일 이승훈이 오산학교 설립 — 확정

### 내가 재검증한 결과

한국민족문화대백과사전의 「오산고등학교」 항목을 확인해 보니:

> 1907년 12월 이승훈이 오산학교를 설립

이라고만 되어 있었다.

우리역사넷 역시:

> 1907년 12월 이승훈이 정주에 오산학교를 설립

이라고 기록하고 있었다.

그런데 한국민족문화대백과사전의 **이승훈 개인 항목**을 따로 확인해보니:

> 1907년 11월 24일 오산학교를 개교

라고 기록되어 있었다.

### 내 판정

**기존 `1907-12-24 확정`을 그대로 유지할 근거를 나는 찾지 못했다.**

그래서 이번 v8 추가검증에서는 다음과 같이 낮추기로 했다.

```text
date_value = 1907-12
date_precision = Month
hasEestimation = false
verification_status = 공식자료간 날짜 충돌
```

`1907-12-24`를 다시 살리려면 **그 날짜를 직접 명시하는 별도의 공식/1차 자료 URL을 내가 추가로 확보해야 한다.**

### 내가 이 사례를 중요하게 보는 이유

이 사례는 내가 왜 v8에서 Source Mapping을 도입해야 한다고 판단했는지를 그대로 보여준다.

기존 CSV에는:

> 오산학교 / 1907-12-24 / 확정

이라고 적혀 있었지만,

내가 실제 provenance를 추적해보니:

* 공식 학교 항목 → 1907년 12월
* 공식 인물 항목 → 1907년 11월 24일
* 우리역사넷 → 1907년 12월

이라는 충돌을 발견했다.

즉 **CSV의 확정값이 실제 출처보다 더 강하게 서술되어 있었던 것**이다.

---

# 3. 49개 항목 URL 팩트체크 결과

아래 표에서 상태는 내가 다음과 같이 구분했다.

* **확인** = 현재 실제 URL과 해당 사실의 직접적인 근거를 내가 확인함
* **부분확인** = URL은 확인했지만 CSV의 모든 세부 주장까지 직접 뒷받침하지는 못함
* **재확인** = 기존 CSV에는 출처가 있으나 이번 검증에서 해당 URL의 직접 근거까지는 확정하지 못함
* **보류** = 관계 또는 날짜 자체가 논쟁적이어서 URL을 붙이는 것만으로 내가 확정하지 않기로 함

---

## A. 학교·단체

| No | 항목       | 내가 확인한 실제 출처                                                                                                                                                                                                                                                                                          | 판정                 |
| -: | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
|  1 | 오산학교     | [한국민족문화대백과사전 — 오산고등학교](https://encykorea.aks.ac.kr/Article/E0038302?utm_source=chatgpt.com) / [우리역사넷 — 오산 학교](https://contents.history.go.kr/mobile/tg/view.do?levelId=tg_004_2280&utm_source=chatgpt.com) / [한국민족문화대백과사전 — 이승훈](https://encykorea.aks.ac.kr/Article/E0044964?utm_source=chatgpt.com) | **날짜 충돌**          |
|  2 | 대성학교     | [한국민족문화대백과사전 — 대성학교](https://encykorea.aks.ac.kr/Article/E0014519?utm_source=chatgpt.com)                                                                                                                                                                                                             | 확인                 |
|  3 | 숭실학교     | 기존 CSV의 한국민족문화대백과사전 URL은 내가 별도로 재확인해야 함                                                                                                                                                                                                                                                             | 재확인                |
|  4 | 보성학교     | 기존 CSV의 한국민족문화대백과사전 URL은 내가 별도로 재확인해야 함                                                                                                                                                                                                                                                             | 재확인                |
|  5 | 신흥무관학교   | [한국민족문화대백과사전 — 신민회](https://encykorea.aks.ac.kr/Article/E0032974?utm_source=chatgpt.com) / [우리역사넷 — 신흥무관학교 용어해설](https://contents.history.go.kr/front/tg/list.do?ganada=%EC%A0%84%EC%B2%B4&pageIndex=3&pageUnit=20&treeId=0202&utm_source=chatgpt.com)                                                | **명칭 주의**          |
|  6 | 신흥강습소    | [우리역사넷 — 독립군 아내들의 헌신](https://contents.history.go.kr/front/hm/view.do?levelId=hm_126_0050&utm_source=chatgpt.com) / [한국민족문화대백과사전 — 이시영](https://encykorea.aks.ac.kr/Article/E0044990?utm_source=chatgpt.com)                                                                                          | 확인                 |
|  7 | 신민회      | [한국민족문화대백과사전 — 신민회](https://encykorea.aks.ac.kr/Article/E0032974?utm_source=chatgpt.com)                                                                                                                                                                                                              | 확인                 |
|  8 | 대한독립군    | [한국민족문화대백과사전 — 홍범도](https://encykorea.aks.ac.kr/Article/E0064093?utm_source=chatgpt.com)                                                                                                                                                                                                              | 부분확인               |
|  9 | 북로군정서    | [한국민족문화대백과사전 — 북로군정서](https://encykorea.aks.ac.kr/Article/E0024657?utm_source=chatgpt.com)                                                                                                                                                                                                            | 확인 / 역할관계는 내가 재검증  |
| 10 | 대한민국임시정부 | [한국민족문화대백과사전 — 대한민국 임시정부](https://encykorea.aks.ac.kr/Article/E0015017?utm_source=chatgpt.com) / [우리역사넷 — 대한민국 임시 헌장](https://contents.history.go.kr/front/hm/view.do?levelId=hm_123_0060&utm_source=chatgpt.com)                                                                                     | 확인                 |
| 11 | 조선물산장려회  | [한국민족문화대백과사전 — 조선물산장려회](https://encykorea.aks.ac.kr/Article/E0052021?utm_source=chatgpt.com)                                                                                                                                                                                                          | **기존 8/23 확정, 내가 재검토** |
| 12 | 신간회      | 기존 CSV의 한국민족문화대백과사전 URL을 내가 직접 재확인해야 함                                                                                                                                                                                                                                                             | 재확인                |
| 13 | 보성사      | [한국민족문화대백과사전 — 보성사](https://encykorea.aks.ac.kr/Article/E0023417?utm_source=chatgpt.com)                                                                                                                                                                                                              | 확인                 |

### 11번 조선물산장려회도 내가 수정이 필요하다고 판단했다

기존 CSV는:

> 1920년 8월 23일 조만식 등이 평양에서 창립

으로 되어 있었다.

그러나 내가 현재 한국민족문화대백과사전을 다시 확인해보니, 평양 조선물산장려회가 **1920년 8월 조만식·오윤선·김동원·김보애 등 70인이 발기·조직**했다고 서술되어 있었다. 정확한 `8월 23일`은 내가 확인한 해당 공식 URL에서는 직접 확인되지 않았다.

따라서 나는 `1920-08-23 확정` 역시 **별도 날짜 근거가 확보될 때까지 Month 수준으로 낮추는 것이 안전하다**고 판단했다.

---

# 4. 사건 6개

| No | 사건     | 내가 확인한 실제 출처                                                                                | 판정                    |
| -: | ------ | ----------------------------------------------------------------------------------------- | --------------------- |
| 14 | 3·1운동  | [한국민족문화대백과사전 — 3·1운동](https://encykorea.aks.ac.kr/Article/E0026772?utm_source=chatgpt.com)    | 확인                    |
| 15 | 안악사건   | [한국민족문화대백과사전 — 안악사건](https://encykorea.aks.ac.kr/Article/E0034866?utm_source=chatgpt.com)     | 확인                    |
| 16 | 105인사건 | [한국민족문화대백과사전 — 105인 사건](https://encykorea.aks.ac.kr/Article/E0022233?utm_source=chatgpt.com)  | 확인                    |
| 17 | 봉오동전투  | [한국민족문화대백과사전 — 봉오동전투](https://encykorea.aks.ac.kr/Article/E0023974?utm_source=chatgpt.com)    | 사건 자체는 내가 확인          |
| 18 | 청산리전투  | 기존 CSV의 한국민족문화대백과사전 URL을 내가 직접 재확인해야 함                                                       | 사건 자체는 확인, URL은 재확인 필요 |
| 19 | 물산장려운동 | [한국민족문화대백과사전 — 조선물산장려운동](https://encykorea.aks.ac.kr/Article/E0052020?utm_source=chatgpt.com) | 확인                    |

### 15번 안악사건

내가 확인한 현재 공식 자료는 매우 명확했다.

안악사건 자체는 **1910년 11월**, 안명근이 서간도 무관학교 설립자금을 모집하다가 관련자들과 검거된 사건이다. 그리고 안명근의 실제 체포는 **1910년 12월 평양역**이라고 별도로 기록되어 있었다.

따라서 기존 RDF의:

```text
안명근체포 = 1910-12
안악사건 = 1910-11
```

분리는 **내가 보기에도 정확했다.**

이 부분은 v6 이후 작업에서 이미 잘 정리되어 있던 사례라고 판단했다.

---

# 5. 인물 30명

| No | 인물  | 내가 확인 가능했던 실제 출처                                                                                                                                                                                                                                                                       | 판정                       |
| -: | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| 20 | 이승훈 | [한국민족문화대백과사전 — 이승훈](https://encykorea.aks.ac.kr/Article/E0044964?utm_source=chatgpt.com) / [오산고등학교](https://encykorea.aks.ac.kr/Article/E0038302?utm_source=chatgpt.com)                                                                                                            | **날짜 충돌**                |
| 21 | 안창호 | [한국민족문화대백과사전 — 안창호](https://encykorea.aks.ac.kr/Article/E0035050?utm_source=chatgpt.com)                                                                                                                                                                                            | 확인                       |
| 22 | 조만식 | [한국민족문화대백과사전 — 조만식](https://encykorea.aks.ac.kr/Article/E0051729?utm_source=chatgpt.com)                                                                                                                                                                                            | 확인                       |
| 23 | 유영모 | [한국민족문화대백과사전 — 유영모](https://encykorea.aks.ac.kr/Article/E0041674?utm_source=chatgpt.com)                                                                                                                                                                                            | **사사관계는 내가 추가 검증**       |
| 24 | 함석헌 | 기존 CSV의 위키백과 URL을 내가 직접 재확인해야 함                                                                                                                                                                                                                                                        | 재확인                      |
| 25 | 양기탁 | 신민회 공식 명단으로 내가 확인: [한국민족문화대백과사전 — 신민회](https://encykorea.aks.ac.kr/Article/E0032974?utm_source=chatgpt.com)                                                                                                                                                                          | 확인                       |
| 26 | 안명근 | [한국민족문화대백과사전 — 안명근](https://encykorea.aks.ac.kr/Article/E0034719?utm_source=chatgpt.com)                                                                                                                                                                                            | 확인                       |
| 27 | 홍범도 | [한국민족문화대백과사전 — 홍범도](https://encykorea.aks.ac.kr/Article/E0064093?utm_source=chatgpt.com)                                                                                                                                                                                            | 확인                       |
| 28 | 배위량 | 기존 위키백과 URL을 내가 직접 재확인해야 함                                                                                                                                                                                                                                                            | 재확인                      |
| 29 | 최광옥 | 신민회 공식 명단: [한국민족문화대백과사전 — 신민회](https://encykorea.aks.ac.kr/Article/E0032974?utm_source=chatgpt.com)                                                                                                                                                                                 | 소속 확인                    |
| 30 | 차이석 | 기존 한국민족문화대백과사전 URL을 내가 직접 재확인해야 함                                                                                                                                                                                                                                                     | 재확인                      |
| 31 | 이용익 | 기존 한국민족문화대백과사전 URL을 내가 직접 재확인해야 함                                                                                                                                                                                                                                                     | 재확인                      |
| 32 | 이종호 | [한국민족문화대백과사전 — 이종호](https://encykorea.aks.ac.kr/Article/E0045955?utm_source=chatgpt.com)                                                                                                                                                                                            | 확인                       |
| 33 | 손병희 | [한국민족문화대백과사전 — 손병희](https://encykorea.aks.ac.kr/Article/E0030507?utm_source=chatgpt.com) / [한국민족문화대백과사전 — 3·1운동](https://encykorea.aks.ac.kr/Article/E0026772?utm_source=chatgpt.com)                                                                                               | 확인                       |
| 34 | 이회영 | [한국민족문화대백과사전 — 이회영](https://encykorea.aks.ac.kr/Article/E0046635?utm_source=chatgpt.com) / [우리역사넷 — 신흥강습소 자료](https://contents.history.go.kr/front/hm/view.do?levelId=hm_126_0050&utm_source=chatgpt.com)                                                                           | 확인                       |
| 35 | 이시영 | [한국민족문화대백과사전 — 이시영](https://encykorea.aks.ac.kr/Article/E0044990?utm_source=chatgpt.com)                                                                                                                                                                                            | 신흥강습소 확인 / 임정 날짜는 내가 추가검증 |
| 36 | 이동녕 | 기존 한국민족문화대백과사전 URL을 내가 직접 재확인해야 함                                                                                                                                                                                                                                                     | 재확인                      |
| 37 | 이상룡 | 기존 한국민족문화대백과사전 URL을 내가 직접 재확인해야 함                                                                                                                                                                                                                                                     | 재확인                      |
| 38 | 지청천 | 기존 위키백과 URL을 내가 직접 재확인해야 함                                                                                                                                                                                                                                                            | 재확인                      |
| 39 | 이종일 | [한국민족문화대백과사전 — 이종일](https://encykorea.aks.ac.kr/Article/E0045940?utm_source=chatgpt.com) / [한국민족문화대백과사전 — 보성사](https://encykorea.aks.ac.kr/Article/E0023417?utm_source=chatgpt.com)                                                                                                 | 확인                       |
| 40 | 한용운 | [한국민족문화대백과사전 — 3·1운동](https://encykorea.aks.ac.kr/Article/E0026772?utm_source=chatgpt.com)                                                                                                                                                                                          | 참여 확인                    |
| 41 | 오세창 | [한국민족문화대백과사전 — 3·1운동](https://encykorea.aks.ac.kr/Article/E0026772?utm_source=chatgpt.com) / [3·1독립선언서](https://encykorea.aks.ac.kr/Article/E0026764?utm_source=chatgpt.com)                                                                                                        | 확인                       |
| 42 | 김좌진 | [한국민족문화대백과사전 — 북로군정서](https://encykorea.aks.ac.kr/Article/E0024657?utm_source=chatgpt.com)                                                                                                                                                                                          | **신민회 관계는 내가 보류로 판단**    |
| 43 | 서일  | [한국민족문화대백과사전 — 북로군정서](https://encykorea.aks.ac.kr/Article/E0024657?utm_source=chatgpt.com)                                                                                                                                                                                          | 조직관계 확인 / 공동설립은 내가 재검증   |
| 44 | 이범석 | 기존 위키백과 URL을 내가 직접 재확인해야 함                                                                                                                                                                                                                                                            | 재확인                      |
| 45 | 이승만 | [한국민족문화대백과사전 — 대한민국 임시정부](https://encykorea.aks.ac.kr/Article/E0015017?utm_source=chatgpt.com) / [대한민국임시정부헌법](https://encykorea.aks.ac.kr/Article/E0015021?utm_source=chatgpt.com)                                                                                                  | 1919-09-11 맥락 확인         |
| 46 | 이동휘 | [한국민족문화대백과사전 — 이동휘](https://encykorea.aks.ac.kr/Article/E0044080?utm_source=chatgpt.com) / [한국민족문화대백과사전 — 고려공산당](https://encykorea.aks.ac.kr/Article/E0003430?utm_source=chatgpt.com) / [한국민족문화대백과사전 — 공산주의운동](https://encykorea.aks.ac.kr/Article/E0004340?utm_source=chatgpt.com) | **출처 간 날짜 차이**           |
| 47 | 최린  | [한국민족문화대백과사전 — 최린](https://encykorea.aks.ac.kr/Article/E0057276?utm_source=chatgpt.com) / [3·1운동](https://encykorea.aks.ac.kr/Article/E0026772?utm_source=chatgpt.com)                                                                                                              | 확인                       |
| 48 | 정춘수 | [한국민족문화대백과사전 — 3·1운동](https://encykorea.aks.ac.kr/Article/E0026772?utm_source=chatgpt.com)                                                                                                                                                                                          | 33인 서명 확인 / 참여시점은 보류가 타당 |
| 49 | 박희도 | 기존 친일인명사전/위키백과 URL을 내가 직접 재확인해야 함                                                                                                                                                                                                                                                     | 재확인                      |

---

# 6. 내가 확인한 주요 팩트 수정사항

## 수정사항 1 — 오산학교

기존:

```text
1907-12-24 / 확정
```

내가 권장하는 값:

```text
1907-12 / Month / 확정
```

단, `11월 24일`을 주장하는 이승훈 개인 항목과의 충돌은 별도 provenance로 남겨두었다.

**v9에서 12월 24일을 되살리려면 해당 날짜를 직접 명시하는 1차 또는 정부·공식 DB를 내가 추가로 확보해야 한다.**

---

## 수정사항 2 — 조선물산장려회

기존:

```text
1920-08-23 / 확정
```

내가 확인한 공식 자료:

```text
1920년 8월 / 조직
```

따라서 나는 다음으로 조정했다:

```text
1920-08 / Month
```

---

## 수정사항 3 — 신흥강습소

내가 v8에서 잡은 방향은 **옳았다고 본다.**

우리역사넷 자료를 보면 1911년 4월 이회영·이시영 형제와 이동녕·이상룡 등이 삼원보에 독립운동 기지를 마련하고 신흥강습소를 설립했다고 기록되어 있다.

또 이시영 항목은 1911년 신흥강습소 설립을 주도하고, 1912년 합니하에서 신흥무관학교로 확대 발전했다고 명시하고 있다.

그래서 나는 v8에서:

```text
이회영 → 공동설립 → 신흥강습소
이시영 → 공동설립 → 신흥강습소
이동녕 → 공동설립 → 신흥강습소
이상룡 → 공동설립 → 신흥강습소
```

로 바꾼 것이 근거가 있다고 판단했다.

다만 **"1912년에 신흥무관학교로 공식 개칭"이라는 표현은 내가 확정하지 않기로 했다.**

한국민족문화대백과사전 신민회 항목은 처음에는 신흥강습소로 불렀다가 뒤에 신흥무관학교로 이름을 바꾸었다고 설명하는 반면, 이시영 항목은 "신흥무관학교로 확대 발전"이라고 표현하고 있어서 서로 뉘앙스가 달랐다.

그래서 나는 v9에서 **명칭관계의 존재 여부와 시점 불확실성을 분리해서 기록**하기로 했다.

---

## 수정사항 4 — 이동휘

내가 확인한 공식 자료끼리도 표현 차이가 있었다.

한국민족문화대백과사전의 이동휘 항목은 1919년 8월 말 상하이에 도착하여 국무총리에 취임하기 위해 왔다고 기록하고 있었다.

「고려공산당」 항목은 1919년 8월 말 상해 도착 및 초대 국무총리 취임을 명시하고 있었다.

반면 「공산주의운동」 항목은 임시정부 국무총리로 추대되었고 **11월 취임**이라고 기록하고 있었다.

그래서 나는 v8의:

```text
1919-09 ±2개월
```

을 **출처 간 충돌을 보수적으로 표현한 값으로 그대로 유지하기로 했다.**

---

# 7. Provenance Layer

## 7-1. 핵심 개념

나는 v8부터 RDF의 모든 중요한 사실을 다음 구조로 추적하기로 했다.

```text
Entity
  ↓
Claim
  ↓
Relation
  ↓
Object
  ↓
Date
  ↓
Source
  ↓
Evidence
```

예를 들어:

```text
이종일
  ↓
"보성사를 경영했다"
  ↓
:경영
  ↓
보성사
  ↓
1919년 2월
  ↓
한국민족문화대백과사전 「보성사」
  ↓
"사장 이종일 ... 독립선언서를 인쇄"
```

이렇게 만들어야 나중에 누군가

> "왜 이종일의 hasPostObject가 보성학교가 아니라 보성사인가?"

라고 물었을 때,

**RDF → Claim → Source → Evidence**

순으로 내가 즉시 추적할 수 있다.

실제로 한국민족문화대백과사전의 보성사 항목은 1919년 2월 27일 사장 이종일이 독립선언서를 인쇄했다고 명시하고 있었다.

---

# 8. Source Mapping의 최소 데이터 구조

나는 v9부터 CSV에 다음 컬럼을 추가하기로 했다.

```text
source_id
claim_id
subject_uri
claim
relation
object_uri
date_value
date_precision
has_estimation
source_title
source_url
evidence_note
verification_status
verification_date
```

예:

```text
SM-001,
CLM-001,
:이종일,
이종일이 보성사에서 독립선언서 인쇄를 총괄,
:경영,
:보성사,
1919-02,
Month,
false,
한국민족문화대백과사전 보성사,
[실제 URL],
"1919년 2월 27일 사장 이종일이 독립선언서 21,000매를 인쇄",
확인
```

---

# 9. Claim과 Source를 분리해야 하는 이유

예를 들어 홍범도와 봉오동전투를 생각해보면 다음은 서로 다른 주장이다.

### Claim A

```text
봉오동전투가 1920년 6월에 발생했다.
```

### Claim B

```text
홍범도가 봉오동전투를 지휘했다.
```

### Claim C

```text
홍범도의 봉오동전투 참여일을 1920-06으로 입력한다.
```

A와 B가 모두 확인됐다고 해서 C가 자동으로 확정되는 것은 아니라고 나는 판단한다.

한국민족문화대백과사전은 봉오동전투가 1920년 만주 봉오동에서 발생했고 홍범도와 최진동이 이끄는 독립군이 일본군과 싸웠다고 설명하고 있다.

따라서 A와 B는 강하게 확인되지만,

```text
홍범도 개인 Event의 date = 1920-06
```

는 **별도의 provenance 판단으로 내가 따로 기록해야 한다고 결론지었다.**

이것이 내가 v7에서 확립한 **"사건 날짜 자동상속 금지"** 원칙을 Source Mapping까지 확장한 것이다.

---

# 10. Provenance 상태값

나는 각 Claim에 다음 상태를 부여하기로 했다.

```text
confirmed
confirmed_indirect
estimated
conflicting_sources
not_directly_verified
validation_hold
contradicted
```

예:

### 이승훈-오산학교

```text
claim_status = conflicting_sources
```

### 이동휘-임시정부

```text
claim_status = conflicting_sources
date_status = estimated
```

### 김좌진-신민회

```text
claim_status = validation_hold
```

### 홍범도-봉오동전투 날짜

```text
claim_status = confirmed
date_status = inferred
```

---

# 11. 내가 v8 추가 검증에서 확정한 원칙

### Rule P-01

**출처 URL이 존재한다고 해당 RDF 값이 자동으로 검증되는 것은 아니다.**

### Rule P-02

**Claim과 Date는 별도로 검증한다.**

### Rule P-03

**사건 날짜와 개인 참여 날짜를 별도로 검증한다.**

### Rule P-04

**출처 간 충돌은 삭제하지 않고 provenance에 보존한다.**

### Rule P-05

**공식 출처가 Month까지만 지지하면 Day를 확정하지 않는다.**

### Rule P-06

**관계가 확인됐더라도 관계 시작일을 자동으로 부여하지 않는다.**

### Rule P-07

**Negative evidence도 provenance로 기록한다.**

김좌진 → 신민회가 대표적인 사례다.

"김좌진이 신민회에 있었다는 자료를 찾지 못했다" 역시 내 검증 과정에서 중요한 정보라고 판단했다.

---

# 12. 내가 내린 v8 최종 Source Mapping 판정

이번 재검색을 통해 나는 **49개 전체를 단순히 "URL 있음 = 완료"로 처리하는 것은 부적절하다는 결론에 도달했다.**

현재 상태를 정리하면:

### A. 내가 직접 근거까지 확인한 핵심 항목

* 신민회
* 대성학교
* 신흥강습소
* 신흥무관학교 관련 관계
* 대한민국임시정부
* 조선물산장려회
* 보성사
* 3·1운동
* 안악사건
* 105인사건
* 봉오동전투
* 물산장려운동
* 안창호
* 조만식
* 유영모의 오산학교 재직
* 안명근
* 홍범도
* 이종호
* 손병희
* 이회영
* 이시영
* 이종일
* 한용운
* 오세창
* 서일/북로군정서
* 이승만
* 이동휘
* 최린
* 정춘수

### B. URL은 존재하지만 내가 CSV의 세부 주장까지 직접 검증하지 못한 항목

* 숭실학교
* 보성학교
* 신간회
* 함석헌
* 배위량
* 차이석
* 이용익
* 이동녕
* 이상룡
* 지청천
* 이범석
* 박희도
* 청산리전투

이 항목들은 **가짜 URL을 만들어 채우지 않고 `재확인`으로 남겨두는 것이 정직한 상태라고 나는 판단했다.**

---

# 13. 내가 내린 v8 추가보고서 최종 결론

v8의 RDF 자체는 앞서 내가 진행한 rdflib 검증에서 구조적 무결성을 확인했다.

이번 Source Mapping 검증에서 내가 확인한 다음 단계의 문제는 **문법 문제가 아니라 provenance 문제였다.**

즉 앞으로 내가 던져야 할 핵심 질문은:

> "이 트리플이 RDF 문법상 유효한가?"

가 아니라,

> **"이 트리플을 왜 넣었으며, 어떤 출처의 어떤 근거가 이 트리플을 지지하는가?"**

이다.

특히 이번 검증에서 나는:

**이승훈 → 오산학교 → 1907-12-24**

와

**조선물산장려회 → 1920-08-23**

이 기존 CSV의 "확정"보다 현재 공식 자료가 더 보수적인 값을 제시하고 있음을 확인했다. 오산학교는 공식 자료 간에 1907년 12월과 11월 24일이 서로 충돌하며, 조선물산장려회는 현재 공식 백과사전에서 1920년 8월까지만 직접 확인된다.

따라서 나는 **v8을 완성본이라고 선언하기 전에 이 두 날짜를 포함한 provenance 충돌 항목을 CSV에 반영하는 것이 바람직하다**고 결론지었다.

최종적으로 나는 v9 이후의 RDF/CSV가 다음 수준을 목표로 해야 한다고 본다.

```text
RDF Triple
    ↓
Claim ID
    ↓
Relation + Object
    ↓
Date + Precision + Estimation
    ↓
Source ID
    ↓
실제 URL
    ↓
Evidence Note
    ↓
Verification Status
```

이 구조가 만들어지면 향후 누군가 특정 RDF 트리플을 클릭했을 때,

> **"이 데이터는 어디서 왔는가?" → "그 출처는 무엇을 말하는가?" → "그 날짜는 확정인가 추정인가?" → "다른 출처와 충돌하는가?"**

까지 내가 역추적할 수 있다.

이것이 내가 v8에서 구축하고자 한 **provenance layer의 최종 형태**다.
