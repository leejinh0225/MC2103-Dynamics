"""Verify the Lecture 13 sources, slide layout and the seven worked examples."""
from math import cos, sin, radians, sqrt, isclose
from pathlib import Path
import re

from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / 'site/lecture13.html').read_text(encoding='utf-8')
videos = [('overview', 'Joko6GH1eyo', 12, '0:41'),
          ('contents1', 'GEn0WjgNc4g', 457, '24:38'),
          ('contents2', 'Q509zKDUG1Y', 329, '17:51'),
          ('problem_solving', 'YIU6x1269f4', 622, '30:42'),
          ('summary', 'Q0Qn_pXVbjA', 27, '1:14')]
for name, vid, count, endpoint in videos:
    transcript = (ROOT / f'transcripts/lecture13/{name}.txt').read_text(encoding='utf-8')
    assert f'Video ID: {vid}\nLanguage: en\nCaptions: auto-generated' in transcript
    cues = re.findall(r'^\[(\d+:\d\d)\]', transcript, re.M)
    assert len(cues) == count and cues[-1] == endpoint and vid in html
    seconds = [60 * int(t.split(':')[0]) + int(t.split(':')[1]) for t in cues]
    assert seconds == sorted(seconds)

sections = dict(re.findall(r'<section class="source-section" id="slide-(\d+)"[^>]*>([\s\S]*?)</section>', html))
assert len(PdfReader(ROOT / 'lecture_notes/lecture13_note.pdf').pages) == 135
assert list(sections) == [f'{i:02}' for i in range(1, 136)]
for n, body in sections.items():
    assert f'slide-{n}.jpg' in body and body.count('<figure class="source-slide">') == 1
    assert ('원본 PDF · 영상에 없는 예제' in body) == (76 <= int(n) <= 122)
    with Image.open(ROOT / f'site/assets/slides/lecture13/slide-{n}.jpg') as image:
        assert image.size == (1920, 1080)
for n in ('31', '43', '45', '70', '82', '83', '89', '110', '118', '120', '126', '133'):
    body = sections[n]
    assert body.index('</figure>') < body.index('원본 교정 · 적용 조건') < body.index('핵심 해설')

hero = html.split('<section class="hero">')[1].split('</section>')[0]
assert 'Week 13' in hero and '2026-11-25' in hero
assert re.findall(r'button button--primary" href="https://www.youtube.com/watch\?v=([^"]+)', hero) == [v[1] for v in videos[1:4]]
index = (ROOT / 'site/index.html').read_text(encoding='utf-8')
assert index.index('href="lecture12.html"') < index.index('href="lecture16.html"') < index.index('href="lecture13.html"')

def check_output(page, computed, display, tolerance):
    assert abs(computed - float(display)) <= tolerance, (page, computed, display)
    assert display in sections[str(page)], (page, display)

g = 9.81
# 1. Front/rear reactions from moments about G; loads below are per wheel, in units of W.
mu = 10**2 / (2 * 7 * g)
front = (1.5 + 1.2 * mu) / (3.6 * 2)
rear = .5 - front
check_output(58, mu, '0.728', .001)
check_output(60, rear, '0.1705', .0003)
check_output(61, front, '0.3295', .0003)
check_output(60, mu * rear, '0.1241', .0003)
check_output(61, mu * front, '0.240', .0005)

# 2. Moments use the cross products of the two link directions about G.
theta = radians(30)
upper_arm = -.250 * sin(theta) + .100 * cos(theta)
lower_arm = -.250 * sin(theta) - .100 * cos(theta)
upper = 8*g*sin(theta) / (1 - upper_arm/lower_arm)
lower = -upper*upper_arm/lower_arm
check_output(69, g*cos(theta), '8.50', .006)
check_output(72, upper, '47.9', .06)
check_output(72, -lower, '8.70', .02)

# 3. Use individual block equations to check the torque exerted by the tensions.
inertia = 6*.2**2
alpha = (5*g*.15 - 2.5*g*.25) / (inertia + 5*.15**2 + 2.5*.25**2)
ta, tb = 2.5*(g+.25*alpha), 5*(g-.15*alpha)
assert isclose(.15*tb - .25*ta, inertia*alpha)
check_output(83, alpha, '2.410', .001)
check_output(84, .25*alpha, '0.603', .0006)
check_output(84, .15*alpha, '0.362', .0006)

# 4. Check center force balance, angular momentum and the tangent at the cord.
ay = 180/15 - g
alpha_cw = 180*.5 / (.5*15*.5**2)
check_output(90, ay, '2.19', .001)
check_output(91, alpha_cw, '48.0', .01)
check_output(92, ay+.5*alpha_cw, '26.19', .001)

# 5. Verify the closed-form transition against slip speed and angular impulse.
for v0, radius, friction in ((5, .12, .2), (9, .35, .5)):
    transition = 2*v0/(7*friction*g)
    speed = v0-friction*g*transition
    spin = (5/2)*friction*g/radius*transition
    assert isclose(speed-radius*spin, 0., abs_tol=1e-10)
    assert isclose(speed, 5*v0/7) and isclose(spin, 5*v0/(7*radius))
assert '5v₀/7' in sections['104'] and '2v₀/(7' in sections['103']

# 6. Energy gives the two speeds independently of the force-based derivation.
distance = 10*.3048
drop = distance*sin(theta)
check_output(117, (2/7)*sin(theta)/cos(theta), '0.165', .001)
check_output(118, sqrt(2*g*drop/(1+2/5)), '4.62', .005)
check_output(120, sqrt(2*g*drop), '5.47', .005)

# 7. Solve the trial by moment balance at C and actual motion at G.
mass, pull, outer, inner = 50., 200., .100, .060
inertia = mass*.070**2
trial = pull*(outer-inner)/(inertia+mass*outer**2)
needed = mass*outer*trial-pull
available = .2*mass*g
assert abs(needed) > available
check_output(128, abs(needed), '146.3', .05)
check_output(130, available, '98.1', .01)
friction = .15*mass*g
check_output(132, (pull-friction)/mass, '2.53', .005)
check_output(133, (pull*inner-friction*outer)/inertia, '18.95', .01)
print('LECTURE13_OK slides=135 english_cues=1447 videos=5 examples=7')
