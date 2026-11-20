"""Verify the Lecture 14 sources, slide layout and the six worked problems."""
from math import cos, sin, radians, sqrt, isclose, pi, hypot
import logging
from pathlib import Path
import re

from PIL import Image
from pypdf import PdfReader

logging.getLogger('pypdf').setLevel(logging.ERROR)
ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / 'site/lecture14.html').read_text(encoding='utf-8')
videos = [('overview', '5FvYg8_g4Kc', 14, '0:44'),
          ('contents1', 'DAAh-kmraMk', 345, '17:27'),
          ('contents2', '70zC0inID7U', 144, '7:05'),
          ('problem_solving', 'ueXnVFAv_DQ', 374, '18:26'),
          ('summary', 'HDMwsgNuYWo', 33, '1:33')]
for name, vid, count, endpoint in videos:
    transcript = (ROOT / f'transcripts/lecture14/{name}.txt').read_text(encoding='utf-8')
    assert f'Video ID: {vid}\nLanguage: en\nCaptions: auto-generated' in transcript
    cues = re.findall(r'^\[(\d+:\d\d)\]', transcript, re.M)
    assert len(cues) == count and cues[-1] == endpoint and vid in html
    seconds = [60 * int(t.split(':')[0]) + int(t.split(':')[1]) for t in cues]
    assert seconds == sorted(seconds)

sections = dict(re.findall(r'<section class="source-section" id="slide-(\d+)"[^>]*>([\s\S]*?)</section>', html))
assert len(PdfReader(ROOT / 'lecture_notes/lecture14_note.pdf').pages) == 93
assert list(sections) == [f'{i:02}' for i in range(1, 94)]
for n, body in sections.items():
    assert f'slide-{n}.jpg' in body and body.count('<figure class="source-slide">') == 1
    assert ('원본 PDF · 영상 풀이 없음' in body) == (44 <= int(n) <= 51 or 69 <= int(n) <= 78 or 80 <= int(n) <= 92)
    with Image.open(ROOT / f'site/assets/slides/lecture14/slide-{n}.jpg') as image:
        assert image.size == (1920, 1080)
for n in ('12', '20', '21', '29', '37', '48', '50', '68', '75', '76', '86'):
    body = sections[n]
    assert body.index('</figure>') < body.index('원본 교정 · 적용 조건') < body.index('핵심 해설')

hero = html.split('<section class="hero">')[1].split('</section>')[0]
assert 'Week 14' in hero and '2026-12-02' in hero
assert re.findall(r'button button--primary" href="https://www.youtube.com/watch\?v=([^"]+)', hero) == [v[1] for v in videos[1:4]]
index = (ROOT / 'site/index.html').read_text(encoding='utf-8')
assert index.index('href="lecture12.html"') < index.index('href="lecture16.html"') < index.index('href="lecture13.html"') < index.index('href="lecture14.html"')

def check_output(page, computed, display, tolerance):
    assert abs(computed - float(display)) <= tolerance, (page, computed, display)
    assert display in sections[str(page)], (page, display)


g = 9.81

# 1. Independent force/torque balance of a falling mass coupled to a fixed drum.
radius = 0.4
accel = (120*g - 90/radius) / (120 + 16/radius**2)
check_output(41, 120*g*1.25-90*1.25/radius, '1190.25', 1e-8)
check_output(42, sqrt(2**2+2*accel*1.25), '3.85', .005)

# 2. Reflect gear A's inertia to B and apply the constant torque at B.
ratio = .100/.250
ia, ib = 10*.200**2, 3*.080**2
omega_b = 600*2*pi/60
eq_inertia = ib+ia*ratio**2
alpha_b = 6/eq_inertia
angle_b = omega_b**2/(2*alpha_b)
check_output(48, .5*eq_inertia*omega_b**2, '164.23', .005)
check_output(49, angle_b/(2*pi), '4.356', .0005)
check_output(50, ia*ratio*alpha_b/.250, '46.2', .05)

# 3. Integrate the constant downhill acceleration along an arbitrarily chosen incline.
angle, drop = radians(10), .8
distance = drop/sin(angle)
for inertia_ratio, multiplier in [(2/5, '0.845'), (.5, '0.816'), (1., '0.707')]:
    accel = g*sin(angle)/(1+inertia_ratio)
    check_output(56, sqrt(2*accel*distance)/sqrt(2*g*drop), multiplier, .0005)

# 4. Evaluate kinetic energy using only the fixed-pivot inertia and then the pin force.
mass, offset, length = 15, .45, 1.5
pivot_inertia = mass*(length**2/12+offset**2)
available = .5*300000*.025**2-mass*g*offset
speed_sq = 2*available/pivot_inertia
check_output(65, sqrt(speed_sq), '3.068', .0005)
check_output(67, mass*(g-offset*speed_sq), '83.6', .05)
small_speed_sq = 2*(.5*30000*.025**2-mass*g*offset)/pivot_inertia
assert small_speed_sq < 0 and '−19.43' in sections['68']
assert abs(small_speed_sq + 19.43) < .01

# 5. Differentiate the center positions using beta as the single generalized angle.
m, ell = 6., .75
beta = radians(20)
# G_AB=(L cos(beta)/2, L sin(beta)/2), G_BD=(3L cos(beta)/2, L sin(beta)/2).
left = ell/2
right = hypot(1.5*ell*sin(beta), .5*ell*cos(beta))
coefficient = .5*m*(left**2 + right**2) + m*ell**2/12
delta_v = m*g*ell*(sin(radians(60))-sin(beta))
omega = sqrt(delta_v/coefficient)
check_output(74, right, '0.522', .0005)
check_output(76, coefficient, '1.520', .0005)
check_output(77, omega, '3.90', .005)
check_output(78, 2*ell*sin(beta)*omega, '2.00', .005)

# Group. Obtain the stretches and the center offset directly from the dimensions.
m, ell, top, gap = 4., .6, .12, .35
offset = ell/2 - top
x1 = hypot(gap, top)-.15
x2 = gap-top-.15
released = .5*400*(x1**2-x2**2)
kinetic = released-m*g*offset
inertia_b = m*(ell**2/12+offset**2)
check_output(85, .5*400*x1**2, '9.68', 1e-8)
check_output(86, m*g*offset, '7.0632', 1e-8)
check_output(87, .5*400*x2**2, '1.28', 1e-8)
check_output(91, sqrt(2*kinetic/inertia_b), '3.27', .005)
print('LECTURE14_OK slides=93 english_cues=910 videos=5 problems=6')
