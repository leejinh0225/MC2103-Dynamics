"""Extract and render every Lecture 9 page; preserve the original PDF."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw
from pypdf import PdfReader

root = Path(__file__).resolve().parents[1]
out = root/'site/assets/slides/lecture09'
qa = root/'tmp/lecture09'
out.mkdir(parents=True,exist_ok=True)
qa.mkdir(parents=True,exist_ok=True)
pdf = root/'lecture_notes/lecture09_note.pdf'
reader = PdfReader(pdf)
count = len(reader.pages)
(qa/'slides.txt').write_text('\n\n'.join(f'=== PAGE {i+1:02d} ===\n{p.extract_text().replace(chr(0)," ")}' for i,p in enumerate(reader.pages)),encoding='utf-8')
subprocess.run(['pdftoppm','-jpeg','-scale-to-x','1920','-scale-to-y','1080','-jpegopt','quality=90',str(pdf),str(out/'slide')],check=True)
files = sorted(out.glob('slide-*.jpg'))
assert len(files)==count
for start in range(0,count,6):
    sheet = Image.new('RGB',(1920,1710),'white')
    draw = ImageDraw.Draw(sheet)
    for offset,file in enumerate(files[start:start+6]):
        x,y=(offset%2)*960,(offset//2)*570
        with Image.open(file) as im:
            assert im.size==(1920,1080)
            sheet.paste(im.resize((960,540)),(x,y+30))
        draw.text((x+12,y+8),file.stem,fill='black')
    sheet.save(qa/f'contact-{start+1:02d}.jpg',quality=92)
print(f'RENDERED {len(files)} slides')
