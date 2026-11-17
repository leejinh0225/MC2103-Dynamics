"""Verify Lecture 12 source coverage and independently evaluate the three examples."""
from math import cos, degrees, acos, dist, isclose, pi, radians, sin, sqrt
from pathlib import Path
import re

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'site/lecture12.html').read_text(encoding='utf-8')
CAPTIONS = {
    'overview': ('nDkuMJIMnFk', 15, '0:46'),
    'contents1': ('wvbS3WXMjrI', 389, '20:10'),
    'contents2': ('1vt2PrhhhcI', 255, '13:06'),
    'problem_solving': ('T32lX7S_jXg', 570, '28:19'),
    'summary': ('VycsK6lBDKQ', 31, '1:31'),
}
for name, (video, count, end) in CAPTIONS.items():
    raw = (ROOT / f'transcripts/lecture12/{name}.txt').read_text(encoding='utf-8')
    assert f'Video ID: {video}\nLanguage: en\nCaptions: auto-generated' in raw
    assert not re.search('[가-힣]', raw)
    times = re.findall(r'^\[(\d+:\d\d)\]', raw, re.M)
    assert len(times) == count and times[-1] == end and video in HTML
    seconds = [int(t.split(':')[0]) * 60 + int(t.split(':')[1]) for t in times]
    assert seconds == sorted(seconds)
sections = dict(re.findall(r'<section class="source-section" id="slide-(\d+)"[^>]*>([\s\S]*?)</section>', HTML))
assert list(sections) == [f'{n:02}' for n in range(1, 62)]
for number, body in sections.items():
    assert body.count('<figure class="source-slide">') == 1
    assert f'slide-{number}.jpg' in body
    with Image.open(ROOT / f'site/assets/slides/lecture12/slide-{number}.jpg') as slide:
        assert slide.size == (1920, 1080)
for n in (21, 30, 34, 35, 43, 44, 47, 48, 52, 54, 60):
    body = sections[f'{n:02}']
    assert body.index('</figure>') < body.index('원본 교정 · 적용 조건') < body.index('핵심 해설')
hero = HTML.split('<section class="hero">', 1)[1].split('</section>', 1)[0]
assert re.findall(r'button button--primary" href="https://www.youtube.com/watch\?v=([^"]+)', hero) == [
    CAPTIONS[name][0] for name in ('contents1', 'contents2', 'problem_solving')]
assert HTML.count('class="exam-card"') == 10


def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])


def angular_momentum(positions, omega, particle_mass):
    result = [0., 0., 0.]
    for r in positions:
        velocity = cross(omega, r)
        for i, moment in enumerate(cross(r, velocity)):
            result[i] += particle_mass * moment
    return result


# Integrate angular momentum directly on the four segments about the shaft midpoint.
bins = 2000
arm_points = []
for side in (1, -1):
    for k in range(bins):
        s = 0.2 * (k + 0.5) / bins
        arm_points.extend([(-side*s, 0, side*0.1), (-side*0.2, side*s, side*0.1)])
arm_h = angular_momentum(arm_points, (0, 0, 12*pi), 2.5/bins)
assert dist(arm_h, (1.8*pi, -0.6*pi, 4*pi)) < 1e-6
angle = degrees(acos(arm_h[2] / dist(arm_h, (0, 0, 0))))
assert round(angle, 2) == 25.38 and '25.38°' in sections['45']
assert '5.6549 a₁ − 1.8850 a₂ + 12.5664 a₃' in sections['44']

# Integrate equal-area disk elements about O, independent of the center-shift solution.
for m, r, length, spin in [(2., .4, 1.3, 5.), (3., .7, 2., -2.)]:
    omega = (spin, -r*spin/length, 0.)
    assert dist(cross(omega, (length, -r, 0.)), (0., 0., 0.)) < 1e-12
    rings, sectors = 30, 72
    points = [(length, radius*cos(2*pi*j/sectors), radius*sin(2*pi*j/sectors))
              for k in range(rings) for radius in [r*sqrt((k+.5)/rings)] for j in range(sectors)]
    disk_h = angular_momentum(points, omega, m/len(points))
    assert dist(disk_h, (m*r*r*spin/2, -m*r*spin/length*(r*r/4+length**2), 0)) < 1e-10
assert 'r²/4+L²' in sections['52']

# Integrate r x dm*a about the pin. The external moment about A eliminates the pin reaction.
m, g, length, beta, omega = 20., 9.81, 2., radians(60), 15.
total_radial_force = 0.
moment_at_pin = 0.
for k in range(bins):
    s = length * (k+.5) / bins
    x, y = s*cos(beta), s*sin(beta)
    dforce = -m/bins * omega**2 * x
    total_radial_force += dforce
    moment_at_pin -= y*dforce
tension = (moment_at_pin + m*g*length/2*cos(beta)) / (length*sin(beta))
pin_radial = total_radial_force + tension
assert isclose(total_radial_force, -2250, abs_tol=1e-9)
assert isclose(tension, 1556.638, abs_tol=.001) and '1556.638 N' in sections['60']
assert isclose(pin_radial, -693.362, abs_tol=.001) and '−693.362 N' in sections['60']
print(f'PASS 61 slides, 1260 English cues, 10 exam answers; arm {angle:.2f} deg, rolling disk integral, rod {tension:.3f} N and {pin_radial:.3f} N.')
