import { existsSync, readFileSync, readdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "../site");
const lectures = [
  { page: "lecture01.html", slug: "lecture01", expectedSlides: 18 },
  { page: "lecture02.html", slug: "lecture02", expectedSlides: 63 },
];
const pages = ["index.html", ...lectures.map(({ page }) => page)];
const errors = [];

const attrValues = (html, attr) =>
  [...html.matchAll(new RegExp(`${attr}=["']([^"']+)["']`, "g"))].map((match) => match[1]);

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
}

const index = readFileSync(join(root, "index.html"), "utf8");
for (const { page } of lectures) {
  if (!index.includes(`href="${page}"`)) errors.push(`index.html: missing link to ${page}`);
}

let totalSourceSections = 0;
let totalSlideFiles = 0;

for (const { page, slug, expectedSlides } of lectures) {
  const lecture = readFileSync(join(root, page), "utf8");
  if (!lecture.includes('id="concept-summary"')) errors.push(`${page}: missing standalone concept summary`);

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

const lecture01 = readFileSync(join(root, "lecture01.html"), "utf8");
if (!lecture01.includes("Summary 영상: 앞으로 배울 내용")) {
  errors.push("lecture01.html: Summary video is not clearly labeled as future-course content");
}
if (lecture01.includes("개념 순서와 실제 일정의 차이")) {
  errors.push("lecture01.html: ambiguous roadmap heading remains");
}

const lecture02 = readFileSync(join(root, "lecture02.html"), "utf8");
const lecture02Hero = lecture02.match(/<section class="hero">([\s\S]*?)<\/section>/)?.[1] ?? "";
const requiredLecture02HeroLinks = [
  ["https://www.youtube.com/watch?v=Lh8tQnI6A9o", "Contents 1 영상 열기"],
  ["https://www.youtube.com/watch?v=i6XabI4ffzc", "Contents 2 영상 열기"],
  ["https://www.youtube.com/watch?v=Pocl0GKnmSA", "Problem Solving 영상 열기"],
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
if (attrValues(lecture02Hero, "href").length !== 4) {
  errors.push("lecture02.html: hero must contain exactly three main-video actions and the lecture index action");
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

if (errors.length) {
  console.error(`SITE_VALIDATION_FAILED (${errors.length})`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`SITE_VALIDATION_OK pages=${pages.length} source_sections=${totalSourceSections} slides=${totalSlideFiles}`);
