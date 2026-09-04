import { existsSync, readFileSync, readdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "../site");
const lectures = [
  { page: "lecture01.html", slug: "lecture01", expectedSlides: 18 },
  { page: "lecture02.html", slug: "lecture02", expectedSlides: 63 },
];
const noteFiles = Array.from({ length: 16 }, (_, index) =>
  `lecture${String(index + 1).padStart(2, "0")}_note.pdf`,
);
const noteDownloadBase =
  "https://github.com/leejinh0225/MC2103-Dynamics/raw/refs/heads/main/2026FA_Dynamics/lecture_notes/";
const pages = ["index.html", "downloads.html", ...lectures.map(({ page }) => page)];
const errors = [];

const attrValues = (html, attr) =>
  [...html.matchAll(new RegExp(`${attr}=["']([^"']+)["']`, "g"))].map((match) => match[1]);

const sectionTagById = (html, id) =>
  [...html.matchAll(/<section\b[^>]*>/g)]
    .map((match) => match[0])
    .find((tag) => attrValues(tag, "id")[0] === id) ?? "";

const sectionBodyById = (html, id) => {
  const escapedId = id.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return html.match(new RegExp(`<section\\b[^>]*id=["']${escapedId}["'][^>]*>([\\s\\S]*?)<\\/section>`))?.[1] ?? "";
};

const classesOf = (tag) => new Set((attrValues(tag, "class")[0] ?? "").split(/\s+/).filter(Boolean));

const layoutClasses = new Map([
  ["overview", ["editorial-section", "section-divider"]],
  ["concept-map", ["editorial-section"]],
  ["concept-summary", ["editorial-section"]],
  ["exam-english", ["editorial-section"]],
  ["glossary", ["editorial-section"]],
  ["asr-log", ["editorial-section"]],
  ["sources", ["editorial-section"]],
]);

const layoutKickers = new Map([
  ["overview", "Lecture overview"],
  ["concept-map", "Concept map"],
  ["concept-summary", "Content summary"],
  ["exam-english", "Exam English"],
  ["glossary", "Core glossary"],
  ["asr-log", "Transcript audit"],
  ["sources", "Sources"],
]);

const hasExactClasses = (tag, expected) => {
  const actual = classesOf(tag);
  return expected.every((name) => actual.has(name)) && actual.size === expected.length;
};

const validateLectureLayout = (lecture, page, expectedSlides) => {
  const requiredSections = ["overview", "concept-map", "concept-summary", "exam-english", "glossary", "asr-log", "sources"];
  const sectionPositions = new Map();
  for (const id of requiredSections) {
    const position = lecture.indexOf(`id="${id}"`);
    sectionPositions.set(id, position);
    if (position < 0) errors.push(`${page}: missing fixed layout section #${id}`);
  }

  const fixedOrder = requiredSections.map((id) => sectionPositions.get(id));
  if (fixedOrder.every((position) => position >= 0) &&
      fixedOrder.some((position, index) => index > 0 && position <= fixedOrder[index - 1])) {
    errors.push(`${page}: fixed layout sections are out of Lecture 1 order`);
  }

  const firstSlidePosition = lecture.indexOf('id="slide-01"');
  const lastSlidePosition = lecture.indexOf(`id="slide-${String(expectedSlides).padStart(2, "0")}"`);
  if (!(sectionPositions.get("concept-summary") < firstSlidePosition &&
        firstSlidePosition <= lastSlidePosition &&
        lastSlidePosition < sectionPositions.get("exam-english"))) {
    errors.push(`${page}: source-slide sequence is outside the fixed summary-to-exam slot`);
  }

  for (const [id, expected] of layoutClasses) {
    const tag = sectionTagById(lecture, id);
    if (!hasExactClasses(tag, expected)) {
      errors.push(`${page}: #${id} must use exactly class="${expected.join(" ")}"`);
    }
    if (tag && attrValues(tag, "aria-labelledby").length !== 1) {
      errors.push(`${page}: #${id} must use aria-labelledby like Lecture 1`);
    }
    const expectedKicker = layoutKickers.get(id);
    if (expectedKicker && !sectionBodyById(lecture, id).includes(`<p class="section-kicker">${expectedKicker}</p>`)) {
      errors.push(`${page}: #${id} must keep Lecture 1 kicker "${expectedKicker}"`);
    }
  }

  const overviewBody = sectionBodyById(lecture, "overview");
  if (/class=["'][^"']*\bevidence\b/.test(overviewBody)) {
    errors.push(`${page}: overview must not contain timestamp or evidence chips`);
  }

  const examBody = sectionBodyById(lecture, "exam-english");
  const examCards = [...examBody.matchAll(/class=["'][^"']*\bexam-card\b[^"']*["']/g)].length;
  const answers = [...examBody.matchAll(/class=["'][^"']*\banswer\b[^"']*["']/g)].length;
  const answerLabels = [...examBody.matchAll(/class=["'][^"']*\banswer__label\b[^"']*["']/g)].length;
  if (!/class=["'][^"']*\bnote-stack\b/.test(examBody) || examCards === 0 || answers !== examCards || answerLabels !== examCards) {
    errors.push(`${page}: exam section must keep note-stack > exam-card > answer + answer__label structure`);
  }

  for (const tag of lecture.match(/<section\b[^>]*>/g) ?? []) {
    const classes = classesOf(tag);
    if (!classes.has("section-divider")) continue;
    const id = attrValues(tag, "id")[0] ?? "(missing id)";
    if (id !== "overview" && id !== "course-roadmap") {
      errors.push(`${page}: #${id} uses section-divider outside the Lecture 1 contract`);
    }
  }

  if (lecture.includes('id="audit-log"') || lecture.includes('href="#audit-log"')) {
    errors.push(`${page}: noncanonical audit-log id found; use asr-log`);
  }
};

for (const page of pages) {
  const pagePath = join(root, page);
  if (!existsSync(pagePath)) {
    errors.push(`${page}: missing page`);
    continue;
  }

  const html = readFileSync(pagePath, "utf8");
  const ids = attrValues(html, "id");
  const duplicateIds = ids.filter((id, index) => ids.indexOf(id) !== index);
  if (duplicateIds.length) errors.push(`${page}: duplicate ids ${[...new Set(duplicateIds)].join(", ")}`);

  for (const href of attrValues(html, "href")) {
    if (href.startsWith("#")) {
      if (!ids.includes(href.slice(1))) errors.push(`${page}: missing anchor target ${href}`);
      continue;
    }
    if (/^(https?:|mailto:|tel:)/.test(href)) continue;
    const localPath = href.split(/[?#]/, 1)[0];
    if (localPath && !existsSync(resolve(dirname(pagePath), localPath))) {
      errors.push(`${page}: missing local href ${href}`);
    }
  }

  for (const src of attrValues(html, "src")) {
    if (/^(https?:|data:)/.test(src)) continue;
    if (!existsSync(resolve(dirname(pagePath), src))) errors.push(`${page}: missing src ${src}`);
  }

  if (/<img\b(?![^>]*\balt=)[^>]*>/i.test(html)) errors.push(`${page}: image without alt`);
  if (/\{\{[A-Z0-9_가-힣]+\}\}/.test(html)) errors.push(`${page}: unresolved placeholder`);
  if (/(에델|노이슈반트|마스터|메이드|츠ン데레)/i.test(html)) errors.push(`${page}: private persona text found`);
  if (/(학습 목표|자가\s*점검|Learning goals?|Self check)/i.test(html)) errors.push(`${page}: excluded study-planning section found`);
  if (/private-materials/i.test(html)) errors.push(`${page}: private material path found`);
}

const index = readFileSync(join(root, "index.html"), "utf8");
if (!index.includes('href="downloads.html"')) errors.push("index.html: missing downloads page link");
for (const { page } of lectures) {
  if (!index.includes(`href="${page}"`)) errors.push(`index.html: missing link to ${page}`);
}

const downloads = readFileSync(join(root, "downloads.html"), "utf8");
const downloadNoteHrefs = attrValues(downloads, "href").filter((href) =>
  href.startsWith(noteDownloadBase) && /lecture\d{2}_note\.pdf$/.test(href),
);
if (downloadNoteHrefs.length !== noteFiles.length) {
  errors.push(`downloads.html: expected ${noteFiles.length} PDF links, found ${downloadNoteHrefs.length}`);
}
for (const noteFile of noteFiles) {
  const sourceNotePath = resolve(root, "../lecture_notes", noteFile);
  if (!existsSync(sourceNotePath)) errors.push(`downloads.html: missing source PDF file ${noteFile}`);
  const noteUrl = `${noteDownloadBase}${noteFile}`;
  const escapedUrl = noteUrl.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const escapedFile = noteFile.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const downloadAnchor = new RegExp(
    `<a\\b(?=[^>]*href=["']${escapedUrl}["'])(?=[^>]*download=["']${escapedFile}["'])[^>]*>`,
  );
  if (!downloadAnchor.test(downloads)) {
    errors.push(`downloads.html: missing downloadable link for ${noteFile}`);
  }
}
const lecture12Position = downloads.indexOf("lecture12_note.pdf");
const lecture16Position = downloads.indexOf("lecture16_note.pdf");
const lecture13Position = downloads.indexOf("lecture13_note.pdf");
if (!(lecture12Position < lecture16Position && lecture16Position < lecture13Position)) {
  errors.push("downloads.html: Lecture 16 must appear below Lecture 12 and before Lecture 13");
}
if (!downloads.includes("Week 12 추가 강의 · 날짜 미기재")) {
  errors.push("downloads.html: Lecture 16 must be labeled as an undated Week 12 extra lecture");
}
if (!downloads.includes("Week 08 · 날짜 미기재") || !downloads.includes("Midterm — No class")) {
  errors.push("downloads.html: undated Week 8 midterm notice is missing");
}

let totalSourceSections = 0;
let totalSlideFiles = 0;

for (const { page, slug, expectedSlides } of lectures) {
  const lecture = readFileSync(join(root, page), "utf8");
  validateLectureLayout(lecture, page, expectedSlides);

  const sourceSections = [...lecture.matchAll(/class=["'][^"']*source-section[^"']*["']/g)].length;
  totalSourceSections += sourceSections;
  if (sourceSections !== expectedSlides) {
    errors.push(`${page}: expected ${expectedSlides} source sections, found ${sourceSections}`);
  }

  const slideDir = join(root, `assets/slides/${slug}`);
  if (!existsSync(slideDir)) {
    errors.push(`${slug} slides: missing directory`);
    continue;
  }
  const slideFiles = readdirSync(slideDir).filter((name) => /^slide-\d{2}\.jpg$/.test(name)).sort();
  totalSlideFiles += slideFiles.length;
  if (slideFiles.length !== expectedSlides) {
    errors.push(`${slug} slides: expected ${expectedSlides} images, found ${slideFiles.length}`);
  }
  for (let i = 1; i <= expectedSlides; i += 1) {
    const number = String(i).padStart(2, "0");
    const expected = `slide-${number}.jpg`;
    if (!slideFiles.includes(expected)) errors.push(`${slug} slides: missing ${expected}`);
    if (!lecture.includes(`id="slide-${number}"`)) errors.push(`${page}: missing slide section ${i}`);
  }
}

const lectureTemplate = readFileSync(join(root, "templates/lecture-page.template.html"), "utf8");
let previousTemplatePosition = -1;
for (const [id, expected] of layoutClasses) {
  const tag = sectionTagById(lectureTemplate, id);
  if (!tag) errors.push(`lecture template: missing fixed section #${id}`);
  if (tag && !hasExactClasses(tag, expected)) {
    errors.push(`lecture template: #${id} must use exactly class="${expected.join(" ")}"`);
  }
  const position = lectureTemplate.indexOf(`id="${id}"`);
  if (position >= 0 && position <= previousTemplatePosition) {
    errors.push(`lecture template: #${id} is out of Lecture 1 order`);
  }
  if (position >= 0) previousTemplatePosition = position;
}
if (!sectionBodyById(lectureTemplate, "exam-english").includes("answer__label")) {
  errors.push("lecture template: missing canonical exam answer card structure");
}

const lecture01 = readFileSync(join(root, "lecture01.html"), "utf8");
if (!lecture01.includes("Summary 영상: 앞으로 배울 내용")) {
  errors.push("lecture01.html: Summary video is not clearly labeled as future-course content");
}
if (lecture01.includes("개념 순서와 실제 일정의 차이")) {
  errors.push("lecture01.html: ambiguous roadmap heading remains");
}
const lecture01Hero = lecture01.match(/<section class="hero">([\s\S]*?)<\/section>/)?.[1] ?? "";
if (!lecture01Hero.includes(`href="${noteDownloadBase}lecture01_note.pdf"`) ||
    !lecture01Hero.includes('download="lecture01_note.pdf"')) {
  errors.push("lecture01.html: original PDF download action is missing");
}

const lecture02 = readFileSync(join(root, "lecture02.html"), "utf8");
const lecture02Hero = lecture02.match(/<section class="hero">([\s\S]*?)<\/section>/)?.[1] ?? "";
const requiredLecture02HeroLinks = [
  ["https://www.youtube.com/watch?v=Lh8tQnI6A9o", "Contents 1 영상 열기"],
  ["https://www.youtube.com/watch?v=i6XabI4ffzc", "Contents 2 영상 열기"],
  ["https://www.youtube.com/watch?v=Pocl0GKnmSA", "Problem Solving 영상 열기"],
  [`${noteDownloadBase}lecture02_note.pdf`, "원본 PDF 다운로드"],
  ["index.html", "강의 목록"],
];
for (const [href, label] of requiredLecture02HeroLinks) {
  if (!lecture02Hero.includes(`href="${href}"`) || !lecture02Hero.includes(label)) {
    errors.push(`lecture02.html: missing hero action ${label}`);
  }
}
if (lecture02Hero.includes("OHqvWeXi_JY") || lecture02Hero.includes("NIFDAI5sgA0")) {
  errors.push("lecture02.html: Overview or Summary video must not appear in hero actions");
}
if (attrValues(lecture02Hero, "href").length !== 5) {
  errors.push("lecture02.html: hero must contain three main-video actions, one PDF action, and the lecture index action");
}
const lecture02HeroAnchors = [...lecture02Hero.matchAll(/<a\b([^>]*)>([\s\S]*?)<\/a\s*>/g)].map((match) => ({
  classes: attrValues(match[1], "class")[0]?.split(/\s+/) ?? [],
  href: attrValues(match[1], "href")[0] ?? "",
  label: match[2].replace(/<[^>]+>/g, "").trim(),
}));
for (const action of lecture02HeroAnchors.filter(({ href }) => href.startsWith("https://www.youtube.com/"))) {
  if (!action.classes.includes("button--primary")) {
    errors.push(`lecture02.html: main-video action must use crimson primary styling: ${action.label}`);
  }
}
const lectureIndexAction = lecture02HeroAnchors.find(({ href }) => href === "index.html");
if (!lectureIndexAction || lectureIndexAction.classes.includes("button--primary")) {
  errors.push("lecture02.html: lecture index action must keep neutral button styling");
}
const lecturePdfAction = lecture02HeroAnchors.find(({ href }) => href === `${noteDownloadBase}lecture02_note.pdf`);
if (!lecturePdfAction || lecturePdfAction.classes.includes("button--primary")) {
  errors.push("lecture02.html: original PDF action must keep neutral button styling");
}

if (errors.length) {
  console.error(`SITE_VALIDATION_FAILED (${errors.length})`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`SITE_VALIDATION_OK pages=${pages.length} source_sections=${totalSourceSections} slides=${totalSlideFiles}`);
