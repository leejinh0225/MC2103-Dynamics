# MC2103 Dynamics static site

GitHub Pages에 그대로 배포할 수 있는 무의존성 정적 사이트입니다.

## 페이지

- `index.html`: 강의 목록
- `downloads.html`: Lecture 01–16 원본 강의노트 PDF 다운로드
- `lecture01.html`: Lecture 1 학습 노트
- `lecture02.html`: Lecture 2 학습 노트
- `lecture03.html`: Week 02 · Lecture 3 곡선운동 학습 노트 (65장, 영어 영상 5개 대조)
- `lecture04.html`: Week 03 · Lecture 4 입자의 운동역학 학습 노트 (72장, 영어 영상 5개 대조)
- `lecture05.html`: Week 04 · Lecture 5 중심력 운동 학습 노트 (50장, 영어 영상 5개 대조)
- `lecture06.html`: Week 05 · Lecture 6 일과 에너지 원리 학습 노트 (111장, 영어 영상 5개 대조)
- `lecture07.html`: Week 06 · Lecture 7 충격량과 운동량 원리 학습 노트 (74장, 영어 영상 5개 대조)
- `lecture08.html`: Week 07 · Lecture 8 입자계 학습 노트 (70장, 영어 영상 5개 대조)
- `lecture09.html`: Week 09 · Lecture 9 강체 운동학 I 학습 노트 (44장, 영어 영상 5개 대조)
- `lecture10.html`: Week 10 · Lecture 10 강체 운동학 II 학습 노트 (58장, 영어 영상 5개 대조)
- `lecture11.html`: Week 11 · Lecture 11 강체 운동학 III 학습 노트 (53장, 영어 영상 5개 대조)
- `lecture12.html`: Week 12 · Lecture 12 강체 운동역학 학습 노트 (61장, 영어 영상 5개 대조)
- `lecture16.html`: Week 12 추가 강의 · 날짜 미기재 · Lecture 16 자이로스코프 운동 학습 노트 (45장, 영어 영상 5개 대조)
- `lecture13.html`: Week 13 · Lecture 13 강체의 평면운동과 힘·가속도 학습 노트 (135장, 예제 7개, 영어 영상 5개 대조)
- `lecture14.html`: Week 14 · Lecture 14 평면운동의 일과 에너지 학습 노트 (93장, 예제 5개와 그룹 문제, 영어 영상 5개 대조)
- `templates/lecture-page.template.html`: 이후 렉처용 구조 템플릿

## 공통 자산

- `assets/css/styles.css`: Crimson 디자인 시스템을 HTML 장문 읽기에 맞게 변환한 공통 스타일
- `assets/js/site.js`: 스크롤 진행률과 현재 목차 표시
- `assets/slides/lectureXX/`: 1920×1080 원본 슬라이드 렌더링 이미지
- `../lecture_notes/lectureXX_note.pdf`: 공개 저장소에 보존된 원본 강의노트 PDF이며, 사이트에서는 GitHub raw URL로 직접 연결

## 로컬 확인

정적 서버의 문서 루트를 이 디렉터리로 지정하고 `index.html`을 엽니다. 파일을 직접 열어도 핵심 내용은 읽히지만, 배포 환경과 동일한 상대경로 검증에는 정적 서버가 권장됩니다.

## 새 렉처 추가

상위의 `NOTE_AUTHORING_GUIDE.md`를 먼저 읽고 `lecture01.html`을 유일한 형식 기준으로 사용합니다. 반드시 `templates/lecture-page.template.html`을 복제한 뒤 placeholder(자리표시자)와 반복 블록만 실제 근거 기반 내용으로 교체합니다. `lecture02.html`은 긴 유도·문제풀이의 내용 깊이만 참고하며 별도 형식으로 취급하지 않습니다. 원본 PDF 페이지 수와 `.source-section` 수, Lecture 1 기반 고정 섹션 계약을 검사기로 확인합니다. 새 렉처를 완성할 때는 공개 저장소의 해당 원본 PDF raw URL을 `downloads.html`의 렉처 카드와 렉처 페이지에 연결하고, 파일명과 직접 다운로드 링크도 함께 확인합니다.
