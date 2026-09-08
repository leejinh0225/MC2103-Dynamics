from pathlib import Path
import subprocess
from PIL import Image, ImageOps, ImageDraw

root = Path(__file__).resolve().parents[1]
out = root / 'site/assets/slides/lecture03'
qa = root / 'tmp/lecture03'
out.mkdir(parents=True, exist_ok=True)
qa.mkdir(parents=True, exist_ok=True)
subprocess.run(['pdftoppm', '-jpeg', '-scale-to-x', '1920', '-scale-to-y', '1080', '-jpegopt', 'quality=90', str(root / 'lecture_notes/lecture03_note.pdf'), str(out / 'slide')], check=True)
files = sorted(out.glob('slide-*.jpg'))
for start in range(0, len(files), 6):
    sheet = Image.new('RGB', (1920, 3 * 570), 'white')
    draw = ImageDraw.Draw(sheet)
    for offset, file in enumerate(files[start:start + 6]):
        im = Image.open(file).resize((960, 540))
        x, y = (offset % 2) * 960, (offset // 2) * 570
        sheet.paste(im, (x, y + 30))
        draw.text((x + 12, y + 8), file.stem, fill='black')
    sheet.save(qa / f'contact-{start + 1:02d}.jpg', quality=92)
print(f'RENDERED {len(files)} slides')
