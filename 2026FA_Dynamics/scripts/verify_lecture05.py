"""Reproduce Lecture 5 numerical checks and validate original English capture."""
from pathlib import Path
from math import sqrt, pi, isclose
import re
from PIL import Image

root = Path(__file__).resolve().parents[1]
expected = {
    'overview': ('e6CYZ3fRRn8', 9, '0:59'),
    'contents1': ('LO3tJFnPtGc', 66, '9:04'),
    'contents2': ('XNCbWvN9bg4', 120, '16:14'),
    'problem_solving': ('r786FbIQots', 52, '6:55'),
    'summary': ('2Mi9L9DWCDE', 10, '1:04'),
}
for name, (video, count, last) in expected.items():
    text = (root / f'transcripts/lecture05/{name}.txt').read_text(encoding='utf-8')
    assert f'Video ID: {video}' in text and 'Language: en' in text
    assert not re.search('[가-힣]', text), f'{name}: translated text'
    stamps = re.findall(r'^\[(\d+:\d{2})\]', text, re.M)
    assert len(stamps) == count and stamps[-1] == last, name
    seconds = [int(s.split(':')[0])*60 + int(s.split(':')[1]) for s in stamps]
    assert seconds == sorted(seconds), name

for page in range(1, 51):
    with Image.open(root / f'site/assets/slides/lecture05/slide-{page:02}.jpg') as image:
        assert image.size == (1920, 1080)

R = 6.37e6
mu = 9.81 * R**2
r0, v0 = 6.87e6, 36900 / 3.6
h = r0*v0
C = 1/r0 - mu/h**2
epsilon = C*h**2/mu
ra = 1/(mu/h**2-C)
a, b = (r0+ra)/2, sqrt(r0*ra)
period = 2*pi*a*b/h
assert 0 < epsilon < 1
assert sqrt(mu/r0) < v0 < sqrt(2*mu/r0)
assert isclose(period, 2*pi*sqrt(a**3/mu), rel_tol=1e-12)
assert round((ra-R)/1000, -2) == 60300
assert round(period, -2) == 70300
assert round(30000 * 6770/10370, -1) == 19590

# Independent gravity-only consistency check of the first problem's input.
rA, vA = 6.77e6, 30000/3.6
hA = rA*vA
CA = 1/rA-mu/hA**2
predicted_ra = 1/(mu/hA**2-CA)
assert isclose((predicted_ra-R)/1000, 3393.916069966206, abs_tol=1e-6)

print('LECTURE05_SOURCE_AND_MATH_OK transcripts=5 segments=257 images=50')
print(f'Example 2: h={h:.6g}, C={C:.9g}, eccentricity={epsilon:.9f}')
print(f'Example 2: maximum altitude={(ra-R)/1000:.6f} km, period={period:.6f} s')
print(f'Example 1: given-apsides answer={30000*6770/10370:.6f} km/h')
print(f'Example 1: gravity-only predicted altitude={(predicted_ra-R)/1000:.6f} km')
