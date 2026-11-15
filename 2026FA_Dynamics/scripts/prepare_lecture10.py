"""Render all Lecture 10 pages and extract source text for review."""
from pathlib import Path
from pypdf import PdfReader
from PIL import Image, ImageDraw
import subprocess
import logging

logging.getLogger('pypdf').setLevel(logging.ERROR)
root = Path(__file__).resolve().parents[1]
pdf = root/'lecture_notes/lecture10_note.pdf'
out = root/'site/assets/slides/lecture10'
qa = root/'tmp/lecture10'
out.mkdir(parents=True,exist_ok=True)
qa.mkdir(parents=True,exist_ok=True)
reader = PdfReader(pdf)
(qa/'slides.txt').write_text('\n\n'.join(f'=== PAGE {i+1:02d} ===\n{p.extract_text().replace(chr(0)," ")}' for i,p in enumerate(reader.pages)),encoding='utf-8')
subprocess.run(['pdftoppm','-jpeg','-scale-to-x','1920','-scale-to-y','1080','-jpegopt','quality=90',str(pdf),str(out/'slide')],check=True)
files = sorted(out.glob('slide-*.jpg'))
assert len(files) == len(reader.pages)
for start in range(0,len(files),6):
    sheet = Image.new('RGB',(1920,1710),'white')
    draw = ImageDraw.Draw(sheet)
    for k,file in enumerate(files[start:start+6]):
        x,y=(k%2)*960,(k//2)*570
        with Image.open(file) as im:
            assert im.size==(1920,1080)
            sheet.paste(im.resize((960,540)),(x,y+30))
        draw.text((x+12,y+8),file.stem,fill='black')
    sheet.save(qa/f'contact-{start+1:02d}.jpg',quality=93)
print(f'RENDERED {len(files)} slides')
