"""Check source coverage and compare the lecture formulas to inertial-frame derivatives."""
from math import cos, sin, pi
from pathlib import Path
import re

import numpy as np
from PIL import Image
from pypdf import PdfReader

root = Path(__file__).resolve().parents[1]
html = (root/'site/lecture16.html').read_text(encoding='utf-8')
courses = [('overview','mGm-rw2zxtw',14,'0:51'), ('contents1','fdOdeRuE_2w',552,'27:44'),
           ('contents2','ZPez6kr049w',270,'13:56'), ('problem_solving','2U882l3jfs8',307,'15:42'),
           ('summary','y2VTGr96P6Y',23,'1:07')]
for name, video, count, last in courses:
    raw = (root/f'transcripts/lecture16/{name}.txt').read_text(encoding='utf-8')
    assert f'Video ID: {video}\nLanguage: en\nCaptions: auto-generated' in raw
    times = re.findall(r'^\[(\d+:\d\d)\]', raw, re.M)
    assert len(times) == count and times[-1] == last and video in html
    seconds = [60*int(t.split(':')[0]) + int(t.split(':')[1]) for t in times]
    assert seconds == sorted(seconds)
sections = dict(re.findall(r'<section class="source-section" id="slide-(\d+)"[^>]*>([\s\S]*?)</section>', html))
assert len(PdfReader(root/'lecture_notes/lecture16_note.pdf').pages) == 45
assert list(sections) == [f'{i:02}' for i in range(1,46)]
for n, body in sections.items():
    assert f'slide-{n}.jpg' in body and body.count('<figure class="source-slide">') == 1
    with Image.open(root/f'site/assets/slides/lecture16/slide-{n}.jpg') as slide:
        assert slide.size == (1920,1080)
for n in ['10','18','28']:
    b = sections[n]
    assert b.index('</figure>') < b.index('원본 교정 · 적용 조건') < b.index('핵심 해설')
cards = re.findall(r'<article class="lecture-card">[\s\S]*?</article>',
                   (root/'site/index.html').read_text(encoding='utf-8'))
previous = next(i for i, card in enumerate(cards) if 'href="lecture12.html"' in card)
assert 'href="lecture16.html"' in cards[previous+1] and 'Week 12 추가 강의 · 날짜 미기재' in cards[previous+1]
hero = html.split('<section class="hero">')[1].split('</section>')[0]
assert 'Week 12 추가 강의' in hero and '날짜 미기재' in hero and '날짜 날짜' not in hero
assert re.findall(r'button button--primary" href="https://www.youtube.com/watch\?v=([^"]+)', hero) == [row[1] for row in courses[1:4]]

def rx(t):
    return np.array([[1,0,0],[0,cos(t),-sin(t)],[0,sin(t),cos(t)]])

def ry(t):
    return np.array([[cos(t),0,sin(t)],[0,1,0],[-sin(t),0,cos(t)]])

def rz(t):
    return np.array([[cos(t),-sin(t),0],[sin(t),cos(t),0],[0,0,1]])

def derivative(f, t, step):
    return (f(t+step)-f(t-step))/(2*step)

def momentum(orientation, inertia, t):
    # Obtain spatial angular velocity from the rate of change of the physical orientation.
    q = orientation(t)
    skew = derivative(orientation, t, 2e-5) @ q.T
    omega = np.array([skew[2,1],skew[0,2],skew[1,0]])
    return q @ inertia @ q.T @ omega

# Check unrestricted and steady disk motions without differentiating B-axis coordinate formulas.
I, J = 2., 4.
disk = np.diag([I,I,J])
for theta, P, U, S, Pd, Ud, Sd in [
        (.6,1.2,-.3,2.4,-.7,.4,.5), (1.1,-.9,.8,-1.1,.4,-.2,.3),
        (.7,.8,0,3.,0,0,0), (pi/2,1.1,0,-2.0,0,0,0)]:
    def frame_b(t):
        return rz(.3+P*t+Pd*t*t/2) @ ry(theta+U*t+Ud*t*t/2)
    def frame_c(t):
        return frame_b(t) @ rz(.4+S*t+Sd*t*t/2)
    def h_disk(t):
        return momentum(frame_c, disk, t)
    calculated = frame_b(0).T @ derivative(h_disk, 0, 1e-4)
    expected = [I*(2*U*S-Pd*sin(theta)),
                I*(P**2*sin(theta)*cos(theta)+2*P*S*sin(theta)+Ud),
                J*(Pd*cos(theta)-P*U*sin(theta)+Sd)]
    np.testing.assert_allclose(calculated, expected, atol=1e-6)

# Differentiate gondola angular momentum in space, then solve the bearing equations.
def gondola(t):
    return ry(pi*t) @ rx((2*pi/3)*t + pi*t*t/4)

def h_gondola(t):
    return momentum(gondola, np.diag([900,400,450]), t)

moment = derivative(h_gondola, 0, .00005)
np.testing.assert_allclose(moment, [450*pi,0,-950*2*pi**2/3], atol=.0004)
az, ax = -moment[0]/2.5, moment[2]/2.5
np.testing.assert_allclose([ax,-ax,az,-az], [-2500.30,2500.30,-565.49,565.49], atol=.005)
assert '1413.72' in sections['40'] and '6250.75' in sections['40']
assert '−2500.30 N' in sections['42'] and '−565.49 N' in sections['42']
print(f'PASS 45 slides, 5 original-English transcripts, {sum(r[2] for r in courses)} cues, menu order and hero links.')
print(f'PASS 4 disk cases, simulator moments and reactions: Ax {ax:.2f} N, Az {az:.2f} N.')
