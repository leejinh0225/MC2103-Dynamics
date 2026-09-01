# MC2103 Dynamics static site

GitHub Pages에 그대로 배포할 수 있는 무의존성 정적 사이트입니다.

## 페이지

- `index.html`: 강의 목록
- `lecture01.html`: Lecture 1 완성 샘플
- `templates/lecture-page.template.html`: 이후 렉처용 구조 템플릿

## 공통 자산

- `assets/css/styles.css`: Crimson 디자인 시스템을 HTML 장문 읽기에 맞게 변환한 공통 스타일
- `assets/js/site.js`: 스크롤 진행률과 현재 목차 표시
- `assets/slides/lectureXX/`: 1920×1080 원본 슬라이드 렌더링 이미지

## 로컬 확인

정적 서버의 문서 루트를 이 디렉터리로 지정하고 `index.html`을 엽니다. 파일을 직접 열어도 핵심 내용은 읽히지만, 배포 환경과 동일한 상대경로 검증에는 정적 서버가 권장됩니다.

## 새 렉처 추가

상위의 `NOTE_AUTHORING_GUIDE.md`를 먼저 읽고 `lecture01.html`의 실제 완성본과 템플릿을 함께 참고합니다. 템플릿의 placeholder(자리표시자)를 실제 근거 기반 내용으로 교체하고, 원본 PDF 페이지 수와 `.source-section` 수가 같은지 검증합니다.
