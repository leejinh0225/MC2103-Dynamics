import { existsSync, readFileSync, readdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "../site");
const pages = ["index.html", "lecture01.html"];
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

const lecture = readFileSync(join(root, "lecture01.html"), "utf8");
if (!lecture.includes('id="concept-summary"')) errors.push("lecture01.html: missing standalone concept summary");
if (!lecture.includes("Summary 영상: 앞으로 배울 내용")) errors.push("lecture01.html: Summary video is not clearly labeled as future-course content");
if (lecture.includes("개념 순서와 실제 일정의 차이")) errors.push("lecture01.html: ambiguous roadmap heading remains");
const sourceSections = [...lecture.matchAll(/class=["'][^"']*source-section[^"']*["']/g)].length;
if (sourceSections !== 18) errors.push(`lecture01.html: expected 18 source sections, found ${sourceSections}`);

const slideDir = join(root, "assets/slides/lecture01");
const slideFiles = readdirSync(slideDir).filter((name) => /^slide-\d{2}\.jpg$/.test(name)).sort();
if (slideFiles.length !== 18) errors.push(`lecture01 slides: expected 18 images, found ${slideFiles.length}`);
for (let i = 1; i <= 18; i += 1) {
  const expected = `slide-${String(i).padStart(2, "0")}.jpg`;
  if (!slideFiles.includes(expected)) errors.push(`lecture01 slides: missing ${expected}`);
  if (!lecture.includes(`id="slide-${String(i).padStart(2, "0")}"`)) errors.push(`lecture01.html: missing slide section ${i}`);
}

if (errors.length) {
  console.error(`SITE_VALIDATION_FAILED (${errors.length})`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`SITE_VALIDATION_OK pages=${pages.length} source_sections=${sourceSections} slides=${slideFiles.length}`);
