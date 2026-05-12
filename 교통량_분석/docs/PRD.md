# PRD: 한국도로공사 교통량 모니터링 대시보드

**문서 버전**: 1.0  
**작성일**: 2026-05-11  
**소스 파일**: `dashboard.html` (단일 파일, ~309KB)  
**대상 독자**: 개발자, Claude Code  

> **Claude Code 참고**: 이 문서는 `dashboard.html` 파일 전체를 정확히 기술한다.  
> 코드 수정 시 이 문서를 먼저 읽고 기존 패턴을 파악한 뒤 작업할 것.

---

## 1. 기술 스택

| 항목 | 상세 |
|------|------|
| 구현 방식 | 단일 HTML 파일 (HTML + CSS + JavaScript 통합) |
| 차트 라이브러리 | Chart.js 4.4.0 (CDN) |
| 차트 플러그인 | chartjs-plugin-datalabels 2.2.0 (CDN) |
| 프레임워크 | 없음 (Vanilla JS) |
| 서버 | 없음 (정적 파일, 브라우저 단독 실행) |
| 언어 | 한국어 |

**CDN 주소**:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js"></script>
```

---

## 2. 파일 구조

```
dashboard.html
├── <head>
│   ├── CDN 스크립트 2개 (Chart.js, DataLabels)
│   └── <style> 인라인 CSS (~63줄)
└── <body>
    ├── <header>          헤더 (로고, 부제, 배지)
    └── <div class="main">
        ├── .filter-bar   필터 3개 + 초기화 버튼
        ├── .kpi-grid     KPI 카드 4개
        ├── .charts-row.two  차트 2개 (시간대별, 차종별)
        ├── .charts-row.half 차트 2개 (요일별, 노선별 속도)
        ├── .table-card   Top 5 정체 테이블
        └── .warn-section 경고 카드 그리드
    └── <script>          JavaScript (~190줄)
        ├── const RAW     원시 데이터 배열 (~4200레코드)
        ├── 상수 선언     ROUTES, TYPES, HOURS 등
        ├── charts 객체   차트 인스턴스 저장소
        ├── 함수 8개      (아래 섹션 참조)
        └── 이벤트 바인딩 + render() 초기 호출
```

---

## 3. CSS 디자인 시스템

### 3.1 CSS 변수 (`:root`)
```css
--bg:      #f0f7ff   /* 페이지 배경 */
--panel:   #ffffff   /* 카드/패널 배경 */
--border:  #cde4f5   /* 테두리 */
--accent:  #0ea5e9   /* 주 강조색 (Sky Blue) */
--accent2: #38bdf8   /* 보조 강조색 */
--text:    #1e3a5f   /* 본문 텍스트 */
--muted:   #64869e   /* 보조 텍스트 */
--warn:    #f59e0b   /* 경고색 (Amber) */
--danger:  #ef4444   /* 위험색 (Red) */
--blue:    #0ea5e9
--purple:  #8b5cf6
```

### 3.2 레이아웃 클래스
| 클래스 | 역할 |
|--------|------|
| `.main` | 최대 너비 1440px, 가운데 정렬, 패딩 20px 24px |
| `.kpi-grid` | 4열 그리드 (900px 이하: 2열) |
| `.charts-row.two` | 2fr + 1fr 비율의 2열 그리드 |
| `.charts-row.half` | 1:1 비율의 2열 그리드 |
| `.warn-grid` | auto-fill, minmax(260px, 1fr) 그리드 |

### 3.3 컴포넌트 클래스
```
.kpi-card        KPI 카드 (상단 3px 컬러 바 있음, --accent-color 변수로 색상 제어)
.chart-card      차트 카드
.table-card      테이블 카드
.warn-card       경고 카드 (.critical / .warning / .info 수정자 클래스)
.rank-badge      순위 배지 (.rank-1 ~ .rank-5)
.speed-bar       속도 프로그래스 바 컨테이너
.filter-group    필터 드롭다운 그룹
.btn-reset       필터 초기화 버튼
```

---

## 4. HTML 요소 ID 레퍼런스

> Claude Code는 DOM 조작 시 반드시 이 ID를 사용할 것.

### 필터 입력
| ID | 타입 | 역할 |
|----|------|------|
| `selRoute` | `<select>` | 노선 선택 (기본값: "ALL") |
| `selHour` | `<select>` | 시간대 선택 (기본값: "ALL", 옵션은 JS로 동적 생성) |
| `selType` | `<select>` | 차종 선택 (기본값: "ALL") |

### KPI 표시
| ID | 역할 | 값 형식 |
|----|------|---------|
| `kpiTotal` | 총 교통량 | `"1,234,567"` (toLocaleString) |
| `kpiSpeed` | 평균 속도 | `"87.3"` (소수점 1자리) |
| `kpiPeakHour` | 최다 교통 시간대 | `"18시"` |
| `kpiPeakVol` | 최다 시간대 교통량 | `"12,345대"` |
| `kpiSlowHour` | 최저 속도 시간대 | `"08시"` |
| `kpiSlowSpeed` | 최저 평균 속도 | `"42.1 km/h"` |

### 차트 캔버스
| ID | 차트 타입 | 역할 |
|----|-----------|------|
| `chartHour` | Bar | 24시간 교통량 분포 |
| `chartType` | Doughnut | 5개 차종 교통량 비율 |
| `chartDay` | Line | 7일간 노선별 교통량 추이 |
| `chartSpeed` | Bar (수평, indexAxis:'y') | 5개 노선 평균속도 비교 |

### 기타
| ID | 역할 |
|----|------|
| `top5Body` | Top 5 테이블의 `<tbody>` |
| `warnGrid` | 경고 카드를 삽입하는 컨테이너 `<div>` |

---

## 5. JavaScript 상수 레퍼런스

```javascript
// 노선 목록 (5개, 순서 고정 - RCOLORS와 인덱스 대응)
const ROUTES = ['경부고속도로', '남해고속도로', '서해안고속도로', '영동고속도로', '중부고속도로'];

// 차종 목록 (5개, 순서 고정 - TCOLORS와 인덱스 대응)
const TYPES = ['승용차', '소형화물', '중형화물', '대형화물', '버스'];

// 시간대 목록 (24개, '00시' ~ '23시')
const HOURS = Array.from({length:24}, (_, i) => String(i).padStart(2,'0') + '시');

// 날짜 목록 (7개)
const DATE_LIST = ['2026-04-01','2026-04-02','2026-04-03','2026-04-04','2026-04-05','2026-04-06','2026-04-07'];

// 요일 목록 (DATE_LIST와 1:1 대응)
const DAYS = ['수','목','금','토','일','월','화'];

// 노선별 색상 (ROUTES와 인덱스 대응)
const RCOLORS = ['#0ea5e9','#6366f1','#f59e0b','#10b981','#f43f5e'];

// 차종별 색상 (TYPES와 인덱스 대응)
const TCOLORS = ['#0ea5e9','#6366f1','#f59e0b','#10b981','#f43f5e'];

// 차트 인스턴스 저장소 (render 시 destroy & 재생성)
const charts = { hour: null, type: null, day: null, speed: null };
```

---

## 6. JavaScript 함수 명세

### 6.1 `getFiltered() → Array`
```
역할: 3개 필터 값을 읽어 RAW 데이터를 필터링하여 반환
입력: DOM에서 selRoute, selHour, selType 값을 직접 읽음
출력: 필터 조건을 모두 만족하는 RAW 레코드 배열
조건: 'ALL'은 해당 필드를 무시 (전체 통과)
```

### 6.2 `updateKPI(data)`
```
역할: KPI 카드 6개의 텍스트 업데이트
계산:
  - kpiTotal    = data의 r[4] 합계
  - kpiSpeed    = data의 r[5] 평균 (소수점 1자리)
  - kpiPeakHour = 시간대별 교통량 합산 후 최댓값 시간대
  - kpiPeakVol  = 해당 시간대의 교통량 합계
  - kpiSlowHour = 시간대별 평균속도 계산 후 최솟값 시간대
  - kpiSlowSpeed= 해당 시간대의 평균속도
```

### 6.3 `updateChartHour(data)`
```
역할: chartHour 캔버스에 Bar 차트 렌더링
X축: HOURS (24개)
Y축: 각 시간대별 교통량(r[4]) 합계
강조: 최댓값 막대는 #f43f5e (빨강), 나머지는 #0ea5e9 (파랑)
플러그인: ChartDataLabels (막대 위에 숫자 표시, 1만 이상은 '1.2만' 형식)
```

### 6.4 `updateChartType(data)`
```
역할: chartType 캔버스에 Doughnut 차트 렌더링
레이블: TYPES (5개)
데이터: 각 차종별 교통량(r[4]) 합계
색상: TCOLORS
cutout: '65%'
```

### 6.5 `updateChartDay(data)`
```
역할: chartDay 캔버스에 Line 차트 렌더링
X축: DAYS + DATE_LIST (예: '수(04-01)')
Y축: 날짜별 교통량 합계
데이터셋: selRoute가 'ALL'이면 ROUTES 5개 전체, 특정 노선이면 해당 노선만
색상: RCOLORS (ROUTES 인덱스 기준)
tension: 0.4, fill: false
주의: 차트에 표시할 노선 목록은 getFiltered() 데이터가 아닌 selRoute 값으로 결정
```

### 6.6 `updateChartSpeed(data)`
```
역할: chartSpeed 캔버스에 수평 Bar 차트 렌더링
Y축 (indexAxis:'y'): ROUTES 노선명 (고속도로 제거 후 표시, 예: '경부')
X축: 평균속도 (0~120 고정)
데이터: 각 노선별 r[5] 평균 (소수점 1자리)
색상: RCOLORS (알파 88 처리)
```

### 6.7 `updateTop5()`
```
역할: top5Body 테이블에 최저 속도 Top 5 구간 렌더링
데이터 소스: 필터 무시, 항상 전체 RAW 데이터 사용
그룹 키: r[1]+'|'+r[0]+'|'+r[2] (노선|날짜|시간대)
정렬 기준: 그룹별 평균속도 오름차순
표시 컬럼: 순위, 노선, 날짜, 시간대, 속도 프로그래스바, 교통량
속도 색상: < 50 → #f85149(빨강), 50~70 → #d29922(주황), > 70 → #2ea043(초록)
```

### 6.8 `updateWarnings()`
```
역할: warnGrid에 경고 카드 렌더링
데이터 소스: 필터 무시, 항상 전체 RAW 데이터 사용
알고리즘:
  ROUTES × DATE_LIST × HOURS 순으로 순회
  1. 전 시간 대비 교통량 비율 계산
     ratio = (현재_vol - prev_vol) / prev_vol * 100
     ratio >= 60 → level: 'critical'
     ratio >= 35 → level: 'warning'
  2. 시간대 평균속도 < 45 km/h → level: 'critical', slow: true
정렬: critical(0) → warning(1) 순
표시: 최대 12개 카드
카드 형식:
  🔴/🟡 노선명
  날짜 시간대 | 메시지
  교통량 (대)
```

### 6.9 `render()`
```
역할: 메인 렌더링 함수, 필터 변경 시마다 전체 갱신
실행 순서: getFiltered → updateKPI → updateChartHour → updateChartType
          → updateChartDay → updateChartSpeed → updateTop5 → updateWarnings
```

### 6.10 `resetFilters()`
```
역할: 3개 필터를 모두 'ALL'로 초기화 후 render() 호출
트리거: "필터 초기화" 버튼 onclick
```

---

## 7. 이벤트 바인딩

```javascript
// 3개 필터 드롭다운에 change 이벤트 등록
['selRoute','selHour','selType'].forEach(id =>
  document.getElementById(id).addEventListener('change', render));

// 초기 렌더링
render();
```

```html
<!-- 초기화 버튼 -->
<button class="btn-reset" onclick="resetFilters()">필터 초기화</button>
```

---

## 8. 데이터 흐름 다이어그램

```
[RAW 배열 (4200레코드)]
       │
       ▼
[getFiltered()]  ←──── selRoute, selHour, selType 값
       │
       ├──▶ [updateKPI()]         → kpiTotal, kpiSpeed, kpiPeakHour/Vol, kpiSlowHour/Speed
       ├──▶ [updateChartHour()]   → chartHour (Bar)
       ├──▶ [updateChartType()]   → chartType (Doughnut)
       ├──▶ [updateChartDay()]    → chartDay (Line)  * selRoute도 직접 참조
       └──▶ [updateChartSpeed()]  → chartSpeed (Horizontal Bar)

[RAW 배열 전체]  (필터 무관)
       ├──▶ [updateTop5()]        → top5Body (Table)
       └──▶ [updateWarnings()]    → warnGrid (Cards)
```

---

## 9. UI 컴포넌트 상세

### 9.1 헤더
```html
<header>
  로고: "🛣 한국도로공사 교통량 모니터링 대시보드"
  부제: "노선별 · 시간대별 교통량 분석 | 데이터 기간: 2026.04.01 ~ 2026.04.07"
  배지: "DASHBOARD v1.0"
</header>
```

### 9.2 KPI 카드 4개 (--accent-color로 상단 바 색상 제어)
| 카드 | accent-color | kpi-label | kpi-value ID | kpi-sub ID |
|------|-------------|-----------|--------------|-----------|
| 총 교통량 | `#10b981` (초록) | 총 교통량 | `kpiTotal` | - |
| 평균 속도 | `#0ea5e9` (파랑) | 평균 속도 | `kpiSpeed` | "km/h" 고정 텍스트 |
| 최다 교통 시간대 | `#f59e0b` (주황) | 최다 교통 시간대 | `kpiPeakHour` | `kpiPeakVol` |
| 최저 속도 시간대 | `#ef4444` (빨강) | 최저 속도 시간대 | `kpiSlowHour` | `kpiSlowSpeed` |

### 9.3 차트 배치
```
[charts-row two]
  ├── chart-card (2fr): 시간대별 총 교통량 (chartHour)
  └── chart-card (1fr): 차종별 교통량 비율 (chartType)

[charts-row half]
  ├── chart-card (1fr): 요일별 교통량 추이 (chartDay)
  └── chart-card (1fr): 노선별 평균 속도 (chartSpeed)
```

### 9.4 Top 5 테이블 컬럼
```
순위 | 노선 | 날짜 | 시간대 | 평균속도(프로그래스바) | 교통량
```

### 9.5 경고 카드 구조
```html
<div class="warn-card critical|warning">
  <div class="warn-route">🔴|🟡 {노선}</div>
  <div class="warn-msg">{날짜} {시간대} | {메시지}</div>
  <div class="warn-val" style="color:{색상}">{교통량} 대</div>
</div>
```

---

## 10. 반응형 브레이크포인트

| 조건 | 변화 |
|------|------|
| 기본 (>900px) | KPI 4열, 차트 2열 |
| ≤ 900px | KPI 2열, 차트 1열 (스택) |

---

## 11. 수정 가이드 (Claude Code용)

### 새 노선 추가
1. `ROUTES` 배열에 노선명 추가
2. `RCOLORS`에 색상 추가
3. `<select id="selRoute">`에 `<option>` 추가
4. RAW 데이터에 해당 노선의 레코드 추가

### 새 차종 추가
1. `TYPES` 배열에 차종명 추가
2. `TCOLORS`에 색상 추가
3. `<select id="selType">`에 `<option>` 추가
4. RAW 데이터에 해당 차종의 레코드 추가

### 경고 임계값 변경
- CRITICAL 급증: `updateWarnings()` 내 `ratio >= 60` 수정
- WARNING 급증: `ratio >= 35` 수정
- 정체 속도: `speed < 45` 수정

### 차트 색상 변경
- 노선별: `RCOLORS` 배열
- 차종별: `TCOLORS` 배열
- 피크 시간대 강조: `updateChartHour()` 내 `'#f43f5e'` 수정

### 데이터 기간 변경
1. `DATE_LIST` 배열 수정
2. `DAYS` 배열 수정 (DATE_LIST와 동일 길이 유지)
3. `<div class="subtitle">` 텍스트 수정
4. RAW 데이터 교체

### 차트 재생성 패턴
모든 차트 함수는 동일한 패턴을 따른다:
```javascript
if(charts.XXX) charts.XXX.destroy();  // 기존 차트 제거
charts.XXX = new Chart(ctx, { ... }); // 새 차트 생성
```
이 패턴을 반드시 유지할 것 (안 하면 메모리 누수 + 차트 중첩 오류).

---

## 12. 알려진 제한사항

| 항목 | 내용 |
|------|------|
| 실시간성 | 데이터가 하드코딩되어 있어 자동 갱신 없음 |
| 오프라인 | Chart.js CDN 필요, 인터넷 없으면 차트 미표시 |
| 모바일 | 900px 이하 1열 지원, 그 이하는 미최적화 |
| 경고 범위 | 최대 12개만 표시 (전체 경고 목록 보기 불가) |
| Top 5 필터 | Top 5 테이블과 경고 섹션은 필터 상태 무관 (항상 전체 기준) |
