from pathlib import Path
import subprocess
from PIL import Image, ImageDraw
from pypdf import PdfReader

root = Path(__file__).resolve().parents[1]
out = root / 'site/assets/slides/lecture04'
qa = root / 'tmp/lecture04'
out.mkdir(parents=True, exist_ok=True)
qa.mkdir(parents=True, exist_ok=True)
pdf = root / 'lecture_notes/lecture04_note.pdf'
reader = PdfReader(pdf)
(qa / 'slides.txt').write_text('\n\n'.join(f'=== PAGE {i+1:02d} ===\n{p.extract_text()}' for i,p in enumerate(reader.pages)), encoding='utf-8')
subprocess.run(['pdftoppm','-jpeg','-scale-to-x','1920','-scale-to-y','1080','-jpegopt','quality=90',str(pdf),str(out/'slide')], check=True)
files = sorted(out.glob('slide-*.jpg'))
for start in range(0,len(files),6):
    sheet = Image.new('RGB',(1920,1710),'white')
    draw = ImageDraw.Draw(sheet)
    for offset,file in enumerate(files[start:start+6]):
        x,y=(offset%2)*960,(offset//2)*570
        sheet.paste(Image.open(file).resize((960,540)),(x,y+30))
        draw.text((x+12,y+8),file.stem,fill='black')
    sheet.save(qa/f'contact-{start+1:02d}.jpg',quality=92)
print(f'RENDERED {len(files)} slides')
