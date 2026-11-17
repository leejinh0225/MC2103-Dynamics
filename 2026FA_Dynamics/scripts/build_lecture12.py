"""Build the Lecture 12 study note from the shared Lecture 1 template."""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
VIDEOS = [
    ('Overview', 'nDkuMJIMnFk'), ('Contents 1', 'wvbS3WXMjrI'),
    ('Contents 2', '1vt2PrhhhcI'), ('Problem Solving', 'T32lX7S_jXg'),
    ('Summary', 'VycsK6lBDKQ'),
]
slides = []


def card(title, *paragraphs, kind='card'):
    return f'<div class="{kind}"><h3>{title}</h3>' + ''.join(f'<p>{s}</p>' for s in paragraphs) + '</div>'


def formula(text):
    return f'<span class="formula">{text}</span>'


def table(headers, rows):
    head = ''.join(f'<th scope="col">{s}</th>' for s in headers)
    body = ''.join('<tr>' + ''.join(f'<td>{s}</td>' for s in row) + '</tr>' for row in rows)
    return f'<table class="term-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def add(n, title, evidence, *prose, eq='', detail='', correction='', role='Concept'):
    assert n == len(slides) + 1
    blocks = card('원본 교정 · 적용 조건', correction, kind='callout') if correction else ''
    if role == 'Concept':
        blocks += card('핵심 해설', *prose)
    else:
        blocks += card('슬라이드 안내', *prose, kind='quiet-card')
    if eq:
        blocks += card('식과 기호', *(formula(line) for line in eq.split(' | ')))
    slides.append((title, evidence, blocks + detail, role))


add(1, '강체의 병진과 회전을 함께 기술하는 방법', '원본 표지',
    'Kinetics of Rigid Bodies(강체의 운동역학). 힘이 질량중심의 속도를 어떻게 바꾸는지, 힘의 모멘트가 물체의 회전을 어떻게 바꾸는지 다룹니다.', role='Title')
add(2, 'Overview(개요) · 몸의 균형과 볼링공의 회전', 'Overview 00:18–00:43',
    'Overview(개요) 영상은 몸의 균형을 잡을 때 필요한 force(힘)와 torque(토크)를 묻습니다. 볼링에서도 공의 질량중심이 나아갈 속도·방향과 공에 줄 회전을 함께 조절합니다. 이 두 효과를 각각 식으로 쓰는 것이 이번 강의의 출발점입니다.', role='Divider')
add(3, '도입 보조 영상', '원본 링크 슬라이드',
    '<a href="https://youtu.be/vAQr_UoMR-o" target="_blank" rel="noreferrer">슬라이드에 수록된 보조 영상 열기</a>', role='Video link')
add(4, 'Contents 1(본문 1) · 질량 분포에서 운동량까지', 'Contents 1 · 도입',
    'Linear momentum(선운동량), angular momentum(각운동량), inertia matrix(관성행렬)를 순서대로 유도합니다.', role='Divider')
add(5, '운동학에서 강체의 운동역학으로', 'Contents 1 00:18–00:30',
    'Kinematics(운동학)는 주어진 자세와 운동으로 각 점의 속도·가속도를 구합니다. Kinetics(운동역학)는 그 운동이 주어진 힘과 양립하는지, 또는 그 운동을 만들 지지반력이 얼마인지 묻습니다. 앞서 배운 rigid-body kinematics(강체 운동학)와 particle kinetics(입자 운동역학)가 여기서 만납니다.',
    '예를 들어 회전축의 속력을 정해 놓으면 질량중심의 가속도는 기하로 구할 수 있습니다. 베어링이나 핀이 그 가속도를 어떻게 만들어 내는지는 질량과 힘을 포함한 식으로 계산합니다.')
add(6, '입자 하나의 법칙을 강체 전체에 적용하기', 'Contents 1 00:33–00:56',
    '강체를 작은 입자들로 나누면 각 입자에 Newton’s second law(뉴턴의 제2법칙)가 성립합니다. 전체를 한 계로 묶으면 입자 사이의 내부 작용·반작용이 상쇄되어 external forces(외력들)를 남길 수 있습니다.',
    'Free-body diagram(자유물체도)에는 강체의 경계, 외력의 작용점, 힘의 방향, 외부에서 가해진 couple(우력)을 표시합니다. 공간에서는 같은 크기의 힘도 작용선이 달라지면 회전 효과가 달라집니다.')
add(7, '힘을 선운동량의 시간 변화로 읽기', 'Contents 1 00:58–01:19',
    '질량이 일정한 입자에서 F=ma와 F=d(mv)/dt는 같은 식입니다. 운동량 형태는 여러 질량 요소의 기여를 먼저 합한 뒤 그 합을 미분할 수 있어 공간 강체에도 편리합니다.',
    '이 강의에서 L은 linear momentum(선운동량), H는 angular momentum(각운동량)입니다. D<sub>N</sub>은 지면에 고정된 inertial frame(관성 기준계) N에서 본 벡터의 시간미분입니다.', eq='ΣF = D<sub>N</sub>L')
add(8, '관성 기준계 N, 물체 기준계 B와 질량중심 G', 'Contents 1 01:31–02:01',
    'N에는 지면에 고정된 단위축 n₁,n₂,n₃를 놓고, B에는 물체와 함께 돌고 움직이는 body-fixed axes(물체 고정축) b₁,b₂,b₃를 놓습니다. G는 center of mass(질량중심)입니다. ω는 N에서 관찰한 강체 B의 angular velocity(각속도)입니다.',
    '관찰자와 성분을 적는 축을 구별합니다. 지면에서 측정한 하나의 속도 벡터도 그 순간의 b축으로 분해해 쓸 수 있습니다.')
add(9, '작은 질량 요소의 속도', 'Contents 1 02:04–02:36',
    '물체 안의 한 점 P에 작은 mass element(질량 요소) dm을 둡니다. r은 G에서 P로 향하고, 지면 원점에서 보면 r<sub>P</sub>=r<sub>G</sub>+r입니다. G와 P는 같은 강체에 있으므로 두 점 사이 거리는 일정합니다.',
    '지면에서 미분하면 첫 항은 G의 병진속도, 둘째 항은 G 주위의 회전이 P에 만드는 속도입니다. 회전축 위에서는 둘째 항이 0이고, 축에서 멀수록 그 크기가 커집니다.', eq='v<sub>P</sub> = v<sub>G</sub> + ω × r')
add(10, '모든 질량 요소를 더하면 회전 항이 사라지는 이유', 'Contents 1 02:40–04:23',
    'Linear momentum(선운동량)의 미소 기여는 v<sub>P</sub> dm입니다. 같은 시각에 물체 전체를 적분하면 v<sub>G</sub>와 ω는 모든 질량 요소가 공유하므로 적분 밖으로 나옵니다. 시간이 흘러도 일정하다는 가정은 필요하지 않습니다.',
    '질량중심의 정의는 ∫r<sub>P</sub> dm = m r<sub>G</sub>입니다. 따라서 ∫(r<sub>P</sub>−r<sub>G</sub>) dm = 0이고, 회전에 따른 선운동량의 합도 0입니다.',
    eq='L = ∫v<sub>P</sub> dm = v<sub>G</sub> ∫dm + ω × ∫r dm = m v<sub>G</sub>',
    correction='03:30 부근 자막의 “angular momentum” 자리에 식에서 적분 밖으로 나오는 벡터는 angular velocity(각속도) ω입니다.')
add(11, '질량중심의 운동이 전체 선운동량을 결정합니다', 'Contents 1 04:26–04:37',
    '강체 전체의 linear momentum(선운동량)을 구할 때는 질량 m을 G에 모아 놓은 입자처럼 계산할 수 있습니다. 단위는 kg·m/s입니다.',
    '가령 축에 고정된 원판이 제자리에서 돌면 양쪽의 선운동량이 상쇄됩니다. G가 정지하므로 L=0이지만 물체는 회전 중이며 angular momentum(각운동량)은 남습니다.')
add(12, '회전을 기술할 때 기준점이 필요한 이유', 'Contents 1 04:41–05:23',
    'Angular momentum about G(G점에 대한 각운동량)는 각 요소의 선운동량에 G부터 그 요소까지의 moment arm(모멘트 팔)을 반영합니다. 같은 속도로 움직여도 G를 지나는 작용선 위의 운동과 옆으로 떨어진 운동은 서로 다른 기여를 냅니다.',
    '미소 기여는 r×(v<sub>P</sub> dm)입니다. 오른손 손가락을 r에서 v<sub>P</sub> 방향으로 감으면 엄지가 각운동량 방향을 가리킵니다.')
add(13, '질량중심에 대한 각운동량의 적분', 'Contents 1 05:25–06:49',
    '앞 장의 속도를 대입하면 병진에 의한 적분은 (∫r dm)×v<sub>G</sub>=0입니다. 남는 이중 외적에서는 질량이 회전축에서 얼마나 떨어졌는지와 각 질량 요소가 어느 방향에 놓였는지가 함께 작용합니다.',
    '각운동량의 단위는 kg·m²/s입니다. 선운동량에 길이를 한 번 더 곱한 차원이며, 식에서 두 번 나타나는 r 중 하나는 ω×r을 통해 접선속도를 만듭니다.',
    eq='H<sub>G</sub> = ∫r × v<sub>P</sub> dm = ∫r × (ω × r) dm')
add(14, '물체 좌표에서 위치와 각속도 나타내기', 'Contents 1 06:53–08:04',
    '모든 요소의 위치를 같은 body basis(물체 기저)로 나타내 r=r₁b₁+r₂b₂+r₃b₃로 둡니다. ω=ω₁b₁+ω₂b₂+ω₃b₃도 같은 축을 사용합니다. 점마다 r₁,r₂,r₃가 다르고, 한 시각의 ω는 물체 전체가 공유합니다.',
    '물체에 고정된 요소의 r 성분은 시간에 따라 일정합니다. 지면에서 보았을 때 r 벡터 자체는 물체와 함께 회전할 수 있습니다.')
add(15, '이중 외적에서 관성행렬의 계수 꺼내기', 'Contents 1 08:09–09:34',
    '벡터 삼중곱 r×(ω×r)=(r·r)ω−(r·ω)r를 씁니다. 예를 들어 b₁ 성분의 ω₁ 계수는 (r₁²+r₂²+r₃²)−r₁²=r₂²+r₃²이고, ω₂의 계수는 −r₁r₂입니다. 같은 전개를 다른 두 축에 반복합니다.',
    '아래에서 ∫는 강체 전체에 대한 질량 적분입니다. 서로 다른 축의 좌표곱이 남을 수 있으므로 ω가 한 성분뿐이어도 H에는 여러 성분이 생길 수 있습니다.',
    eq='H₁ = ∫[(r₂²+r₃²)ω₁ − r₁r₂ω₂ − r₁r₃ω₃] dm | H₂ = ∫[−r₂r₁ω₁ + (r₁²+r₃²)ω₂ − r₂r₃ω₃] dm | H₃ = ∫[−r₃r₁ω₁ − r₃r₂ω₂ + (r₁²+r₂²)ω₃] dm')
add(16, '각운동량 벡터를 행렬곱으로 계산하기', 'Contents 1 09:37–13:57',
    '세 성분식에서 ω₁,ω₂,ω₃의 계수를 열별로 묶으면 3×3 inertia matrix(관성행렬) I<sub>G</sub>가 됩니다. 열벡터 [ω]<sub>B</sub>를 오른쪽에서 곱한 결과는 같은 기저에서의 각운동량 성분 [H<sub>G</sub>]<sub>B</sub>입니다.',
    '원본은 물리 벡터와 그 성분 열을 같은 기호로 간략히 씁니다. 실제 계산에서는 G라는 기준점과 B라는 성분축을 먼저 확인해야 합니다. ω₃만 있으면 I<sub>G</sub>의 세 번째 열 전체에 ω₃를 곱합니다.',
    eq='[H<sub>G</sub>]<sub>B</sub> = [I<sub>G</sub>]<sub>B</sub> [ω]<sub>B</sub>')
add(17, '대각성분과 비대각성분의 물리적 의미', 'Contents 1 13:59–14:39',
    'I₁₁은 b₁축에서 각 질량 요소까지의 수직거리 제곱을 적분한 moment of inertia(관성모멘트)입니다. 대각성분은 항상 0 이상입니다. 어느 한 방향으로 거리가 두 배가 되면 그 거리에 따른 기여는 네 배가 됩니다.',
    '비대각성분은 서로 다른 두 좌표의 곱을 적분합니다. 이 강의의 행렬에는 음수 부호가 포함됩니다. 교재가 product of inertia(관성곱)를 양의 적분 기호로 정의한다면, 행렬에 넣을 때 그 부호를 확인합니다. 모든 성분의 단위는 kg·m²입니다.',
    eq='I₁₁=∫(r₂²+r₃²)dm, I₂₂=∫(r₃²+r₁²)dm, I₃₃=∫(r₁²+r₂²)dm | I₁₂=I₂₁=−∫r₁r₂ dm, I₂₃=I₃₂=−∫r₂r₃ dm, I₃₁=I₁₃=−∫r₃r₁ dm')
add(18, '회전 관성이 크다는 말의 의미', 'Contents 1 14:44–15:15',
    '같은 원판에 추를 달더라도 가장자리로 옮기면 회전축에 대한 moment of inertia(관성모멘트)가 커집니다. 한 고정 주축 주위에서 같은 angular acceleration(각가속도)을 만들려면 더 큰 축 방향 토크가 필요합니다.',
    '관성은 운동 상태의 변화와 관련된 성질입니다. 마찰이 없는 고정 주축에서 이미 일정하게 회전 중이라면, 그 회전속력을 유지하는 데 축 방향 토크는 필요하지 않습니다.')
add(19, '강체에 붙인 축을 쓰면 관성행렬이 일정합니다', 'Contents 1 15:19–16:09',
    'Inertia matrix(관성행렬)는 기준점, 질량 분포, 축 방향에 따라 정해집니다. 변형하지 않는 강체에서 G와 축을 물체에 고정하면 각 dm의 좌표가 고정되므로 행렬 성분이 시간에 따라 일정합니다. 지면축으로 나타내면 자세 변화에 따라 성분이 달라질 수 있습니다.',
    '좌표곱 rᵢrⱼ=rⱼrᵢ이므로 행렬은 symmetric(대칭)입니다. B성분을 N성분으로 보내는 회전행렬을 Q라 두면 [I]<sub>N</sub>=Q[I]<sub>B</sub>Qᵀ입니다.',
    correction='16:09의 “symmetric and positive”에서 정확한 일반 성질은 uᵀIu=∫|u×r|²dm ≥ 0입니다. 비대각성분은 음수가 될 수 있고, 57장의 이상적인 가는 봉은 길이축 관성이 0입니다.')
add(20, '주축을 선택하면 관성행렬이 대각화됩니다', 'Contents 1 16:15–18:37',
    '실대칭행렬의 서로 직교하는 고유축을 principal axes of inertia(관성주축)라 부릅니다. 그 축을 쓰면 H의 각 성분은 같은 축의 principal moment of inertia(주관성모멘트)와 ω 성분의 곱입니다. 질량 분포가 대칭이면 좌표곱들이 상쇄되어 기하학적으로 주축을 찾기도 쉽습니다.',
    'H와 ω가 평행하려면 ω가 한 고유값의 고유공간에 있어야 합니다. 예를 들어 주관성모멘트가 다른 두 주축을 동시에 회전 성분으로 쓰면, 두 성분의 비가 달라져 H의 방향이 ω와 달라집니다.',
    eq='[I<sub>G</sub>]<sub>principal</sub> = diag(I₁,I₂,I₃),　[H<sub>G</sub>] = (I₁ω₁, I₂ω₂, I₃ω₃)ᵀ')
add(21, '기준점을 질량중심 G에서 다른 점 C로 옮길 때', 'Contents 1 18:41–19:25',
    '베어링이나 핀을 지나는 축을 쓰면 힘의 모멘트 계산이 간단해질 수 있습니다. C와 G를 지나는 서로 평행한 축의 관성모멘트는 parallel-axis theorem(평행축 정리)으로 연결합니다. 두 기저의 축 방향은 똑같이 유지합니다.',
    '각 질량 요소의 위치를 두 구간으로 나눕니다. 그러면 각 질량 요소 P에 대해 CP=ρ+GP입니다. 이 방향은 뒤에서 H와 M의 기준점을 옮길 때도 그대로 씁니다.',
    correction='영상 19:18–19:25는 G에서 C로 읽힙니다. 30–35장의 기준점 이동식에 맞춰 ρ=CG, 즉 C에서 G로 정의합니다. 평행축 정리의 이차식은 방향을 뒤집어도 같지만, 각운동량과 모멘트의 기준점 이동항은 부호가 바뀝니다.')
add(22, '평행축 정리의 행렬형과 스칼라형', 'Contents 1 19:27–20:06',
    '각 요소의 위치 r에 ρ를 더해 관성행렬을 다시 적분합니다. r과 ρ의 혼합항은 ∫r dm=0으로 없어집니다. 남는 추가항은 질량 m 전체가 C에서 ρ만큼 떨어진 G 한 점에 놓일 때의 관성입니다. 𝟙은 3×3 단위행렬이고 ρρᵀ는 두 벡터의 다이애딕 곱(outer product)입니다.',
    '예를 들어 ΔI₁₁=m(ρ₂²+ρ₃²), ΔI₁₂=−mρ₁ρ₂입니다. 단위축 u 주위의 스칼라식에서는 두 평행축 사이의 수직거리 d=|ρ×u|를 사용합니다. 기준점 간 거리 |ρ|와 d가 언제나 같지는 않습니다.',
    eq='I<sub>C</sub> = I<sub>G</sub> + m[(ρ·ρ)𝟙 − ρρᵀ] | I<sub>C,u</sub> = I<sub>G,u</sub> + md²')

add(23, 'Contents 2(본문 2) · 힘과 모멘트의 운동방정식', 'Contents 2 · 도입',
    '앞에서 구한 운동량을 지면 기준으로 미분해 Newton–Euler equations(뉴턴–오일러 방정식)를 만듭니다. G에서 성립하는 식을 다른 점 C에 쓸 때의 조건도 살펴봅니다.', role='Divider')
add(24, '외력의 합은 질량중심의 가속도를 결정합니다', 'Contents 2 00:17–00:51',
    '강체 전체에 작용하는 resultant external force(합외력)는 전체 선운동량의 관성계 시간미분입니다. 질량이 일정하면 바로 m a<sub>G</sub>가 됩니다. 회전하는 물체에도 이 병진식이 그대로 성립합니다.',
    '힘은 작용점과 관계없이 벡터로 합합니다. 합외력이 0이면 질량중심의 속도 벡터가 일정합니다. 서로 떨어진 두 힘이 만드는 couple(우력)은 여전히 회전을 바꿀 수 있습니다.',
    eq='ΣF<sub>ext</sub> = D<sub>N</sub>L = m a<sub>G</sub>')
add(25, '회전 운동에는 힘의 모멘트가 필요합니다', 'Contents 2 00:57–01:18',
    '같은 크기의 힘도 G를 지나는 힘은 G에 대한 moment(모멘트)가 0이고, 옆으로 떨어진 작용선의 힘은 모멘트를 만듭니다. Euler’s law(오일러의 법칙)는 이 회전 효과와 angular momentum(각운동량)의 변화를 연결합니다.',
    '질량중심 G는 움직이거나 가속할 수 있습니다. 그래도 G에 대한 식에는 기준점 이동 보정항이 생기지 않습니다.')
add(26, 'G에 대한 오일러 방정식', 'Contents 2 01:21–02:02',
    'G에 대한 모든 외력 모멘트와 외부 우력을 합하면 지면에서 본 H<sub>G</sub>의 시간 변화입니다. 각운동량의 크기가 일정해도 방향이 바뀌면 우변은 0이 아닐 수 있습니다. 양변의 단위는 N·m입니다.',
    'I<sub>G</sub>ω를 먼저 계산할 때는 물체축이 편리합니다. 그러나 D<sub>N</sub>은 inertial derivative(관성계 미분)이므로, 물체축의 성분만 시간에 따라 미분하면 회전하는 축의 효과가 빠집니다.',
    eq='ΣM<sub>G</sub> = D<sub>N</sub>H<sub>G</sub>,　H<sub>G</sub> = I<sub>G</sub>ω')
add(27, '각운동량을 관성계에서 미분하는 방법', 'Contents 2 02:12–02:55',
    'H<sub>G</sub>=H₁b₁+H₂b₂+H₃b₃를 직접 미분하면 각 성분의 변화와 각 단위축의 변화가 나옵니다. 회전축의 미분 D<sub>N</sub>bᵢ=ω×bᵢ를 쓰면 뒤의 세 항이 ω×H<sub>G</sub>로 묶입니다.',
    'D<sub>B</sub>는 물체 기준계 B에서 보는 변화입니다. 물체축에서 H₁,H₂,H₃가 모두 일정하면 첫 항은 0입니다. 회전축과 H가 나란하지 않으면 두 번째 항은 남습니다.',
    eq='D<sub>N</sub>H<sub>G</sub> = D<sub>B</sub>H<sub>G</sub> + ω × H<sub>G</sub>')
add(28, '오일러 방정식을 물체축 성분으로 풀기', 'Contents 2 03:01–04:46',
    '물체축에서는 I<sub>G</sub>가 일정하므로 성분미분이 I<sub>G</sub>ω̇가 됩니다. ω̇는 물체축 각속도 성분의 시간미분입니다. D<sub>N</sub>ω와 D<sub>B</sub>ω의 차이는 ω×ω=0이므로 이 성분들은 각가속도 성분과 같습니다.',
    '원본의 ω̃는 왼쪽에서 벡터에 곱하면 ω와의 외적이 되는 skew-symmetric matrix(반대칭행렬)입니다. 각 행은 (0,−ω₃,ω₂), (ω₃,0,−ω₁), (−ω₂,ω₁,0)입니다. 주축을 쓰더라도 외적 항은 일반적으로 남습니다.',
    eq='ΣM<sub>G</sub> = I<sub>G</sub>ω̇ + ω × (I<sub>G</sub>ω) | 주축 성분 M₁=I₁ω̇₁+(I₃−I₂)ω₂ω₃,　M₂=I₂ω̇₂+(I₁−I₃)ω₃ω₁,　M₃=I₃ω̇₃+(I₂−I₁)ω₁ω₂')
add(29, '직접 가한 우력과 외력이 만드는 모멘트', 'Contents 2 04:53–05:23',
    'Couple moment(우력 모멘트)는 서로 반대인 두 힘이 순수한 회전 효과를 만드는 경우로, 기준점과 관계없이 그대로 더합니다. 점 Pᵢ에 가해진 외력 Fᵢ는 G에서 Pᵢ로 향하는 rᵢ를 써서 rᵢ×Fᵢ를 더합니다.',
    '예를 들어 무게가 G에 작용하면 G에 대한 중력 모멘트는 0입니다. 같은 중력도 핀 A에 대한 모멘트 식에서는 AG×mg로 들어갈 수 있습니다.',
    eq='ΣM<sub>G</sub> = ΣM<sub>couple</sub> + Σ(rᵢ × Fᵢ)')
add(30, '다른 점 C에서 본 각 힘의 모멘트 팔', 'Contents 2 05:30–06:06',
    'C에서 각 작용점 Pᵢ까지 가려면 먼저 C에서 G로 ρ만큼 이동하고 G에서 Pᵢ로 rᵢ만큼 이동합니다. 따라서 moment arm(모멘트 팔)이 ρ+rᵢ가 됩니다. 외부 우력은 같은 벡터로 남습니다.',
    'C와 G는 모든 힘에 공통인 한 쌍의 점이므로 ρ는 합 밖으로 꺼낼 수 있습니다. 각 힘의 작용점 위치가 달라지는 것은 rᵢ에 담겨 있습니다.',
    eq='ΣM<sub>C</sub> = ΣM<sub>couple</sub> + Σ[(ρ+rᵢ) × Fᵢ]',
    correction='원본 괄호 안 ρᵢ의 두 끝점 C와 G는 공통입니다. 31장의 전개처럼 ρ에 개별 힘의 첨자를 붙이지 않습니다.')
add(31, '모멘트의 기준점 이동은 합력으로 계산합니다', 'Contents 2 06:11–07:10',
    '앞 식을 나누면 ΣM<sub>G</sub>와 ρ×ΣF가 됩니다. 그래서 G에 대한 식을 이미 알고 있으면 힘마다 새 모멘트 팔을 재계산할 필요가 없습니다. C가 움직이더라도 같은 순간의 두 모멘트를 연결하는 이 기하 관계는 성립합니다.',
    '합력이 0이면 두 점에 대한 전체 모멘트는 같습니다. 합력이 0이 아니어도 C와 G를 잇는 선이 합력 방향과 평행하면 기준점 이동에 따른 차이는 0입니다.',
    eq='ΣM<sub>C</sub> = ΣM<sub>G</sub> + ρ × ΣF = ΣM<sub>G</sub> + ρ × m a<sub>G</sub>')
add(32, '질량중심에서 알고 있는 각운동량', 'Contents 2 07:19–07:25',
    '기준점 이동의 출발값은 H<sub>G</sub>=I<sub>G</sub>ω입니다. 이 식은 강체가 병진과 회전을 동시에 하는 경우에도 G에서 성립합니다. 각운동량을 구하는 시각의 I<sub>G</sub>와 ω를 한 좌표계로 표현합니다.',
    '단순히 식의 첨자 G를 C로 바꾸기 전에, C에서 볼 때 질량중심의 병진이 만드는 기여를 다음 장처럼 더해야 합니다.')
add(33, '임의의 점 C에 대한 각운동량', 'Contents 2 07:28–08:11',
    '지면에서 본 각 요소의 운동량 v<sub>P</sub>dm은 그대로 두고 모멘트 팔만 CP=ρ+r로 바꿉니다. ρ는 요소마다 같으므로 ∫ρ×v<sub>P</sub>dm=ρ×L입니다. 나머지 적분은 정의상 H<sub>G</sub>입니다.',
    '첫 항은 G 주위 회전의 각운동량, 둘째 항은 G에 전체 질량이 모였다고 볼 때의 각운동량입니다. 회전 없는 병진 중에도 질량중심의 속도 작용선에서 떨어진 C에는 각운동량이 생길 수 있습니다.',
    eq='H<sub>C</sub> = H<sub>G</sub> + ρ × L = I<sub>G</sub>ω + ρ × m v<sub>G</sub>')
add(34, '어떤 기준점에서 H = Iω를 쓸 수 있나', 'Contents 2 08:15–10:01',
    'C가 강체에 고정된 점이라면 v<sub>G</sub>=v<sub>C</sub>+ω×ρ입니다. 이를 33장에 대입합니다. ρ×m(ω×ρ)는 평행축 정리의 추가 행렬에 ω를 곱한 값이므로 I<sub>G</sub>ω와 합쳐 I<sub>C</sub>ω가 됩니다.',
    'Pinned point(고정 핀점)처럼 C가 지면에서 정지하면 보정항이 0입니다. 물체와 무관하게 선택한 자유로운 C에는 먼저 33장의 일반식을 사용합니다.',
    eq='물체에 고정된 C에서　H<sub>C</sub> = I<sub>C</sub>ω + ρ × m v<sub>C</sub>',
    correction='원본의 “Only when C is a fixed point”는 충분조건입니다. 영상 09:42–09:58처럼 ρ와 v<sub>C</sub>가 평행해도 외적이 0입니다. 여기서 고정점 약식에 필요한 것은 지면 기준 속도이고, 유도에 쓰인 두 점 속도식에는 물체에 고정된 C가 필요합니다.')
add(35, '움직이는 점 C에서 모멘트와 각운동량 변화율', 'Contents 2 10:06–11:34',
    '33장의 식을 관성계에서 미분합니다. D<sub>N</sub>ρ=v<sub>G</sub>−v<sub>C</sub>이므로 (v<sub>G</sub>−v<sub>C</sub>)×m v<sub>G</sub>=−v<sub>C</sub>×m v<sub>G</sub>입니다. 나머지 D<sub>N</sub>H<sub>G</sub>+ρ×m a<sub>G</sub>는 31장에 따라 ΣM<sub>C</sub>입니다.',
    '이 식은 C가 임의로 움직여도 성립합니다. 속도 보정항이 0인지 판단한 뒤 회전 방정식을 단순화합니다.',
    eq='D<sub>N</sub>H<sub>C</sub> = ΣM<sub>C</sub> + m v<sub>G</sub> × v<sub>C</sub> | ΣM<sub>C</sub> = D<sub>N</sub>H<sub>C</sub> + v<sub>C</sub> × m v<sub>G</sub>',
    correction='영상의 고정점과 순수 병진은 보정항이 사라지는 대표 사례입니다. 정확한 조건은 v<sub>C</sub>×m v<sub>G</sub>=0입니다. G가 순간적으로 정지하거나 두 속도가 평행한 경우도 포함합니다.')
add(36, '뉴턴–오일러 방정식 · 질량중심을 기준으로', 'Contents 2 11:39–12:08',
    '공간 강체에는 합외력에 대한 세 성분식과 G에 대한 합외력 모멘트의 세 성분식이 있습니다. 자유물체도에서 찾은 같은 외력을 두 식에 쓰되, 첫 식에는 힘 벡터, 둘째 식에는 그 힘의 모멘트를 넣습니다.',
    '문제에서 가속도가 알려져 있으면 미지의 reaction(반력)과 tension(장력)을 풀 수 있습니다. G에 작용하는 무게는 병진식에는 들어가고 G를 기준으로 한 회전식에는 기여하지 않습니다.',
    eq='ΣF = m a<sub>G</sub>　[N] | ΣM<sub>G</sub> = D<sub>N</sub>H<sub>G</sub>　[N·m]')
add(37, '기준점을 고를 때 서로 다른 두 조건', 'Contents 2 12:10–13:03',
    '“각운동량 자체를 I<sub>C</sub>ω로 쓸 수 있는가?”와 “각운동량의 변화율을 바로 ΣM<sub>C</sub>로 쓸 수 있는가?”는 별개의 질문입니다. 전자는 위치벡터 ρ와 점 C의 속도, 후자는 C와 G의 두 속도에 달려 있습니다.',
    '두 질문을 한꺼번에 단순화하기 좋은 선택은 지면에 고정되어 있고 동시에 강체의 한 점으로 취급할 수 있는 핀입니다. 일반 이동점에서는 G에서 먼저 풀어 기준점을 옮겨도 됩니다.',
    detail=table(['판단할 식','일반식에서 사라져야 할 항'],[
        ('물체 고정점 C에서 H<sub>C</sub>=I<sub>C</sub>ω','ρ×m v<sub>C</sub>'),
        ('임의점 C에서 ΣM<sub>C</sub>=D<sub>N</sub>H<sub>C</sub>','v<sub>C</sub>×m v<sub>G</sub>')]))

add(38, 'Problem Solving(문제풀이) · 세 강체에 적용하기', 'Problem Solving 00:17–00:40',
    '첫 예제는 회전축과 각운동량 사이의 각도, 둘째는 구르는 원판의 각운동량, 셋째는 경사진 봉을 일정하게 회전시키는 장력과 지지반력을 구합니다.', role='Divider')
add(39, '예제 1 · 두 L자 암이 달린 회전축', 'Problem Solving 00:41–01:42',
    '각각 질량 5 kg인 L-shaped arm(L자 암) 두 개가 길이 600 mm인 축 AB의 두 삼등분점에 용접되어 있습니다. 각 암의 두 직선부 길이는 각각 200 mm입니다. 축은 360 rpm의 constant rate(일정한 회전속력)로 회전합니다. A에 대한 각운동량과 그 벡터가 AB와 이루는 각을 구합니다.',
    '그림에서 두 암은 축 중앙을 기준으로 서로 반대쪽으로 뻗습니다. 같은 밀도의 가는 봉으로 모델링하면 전체 질량중심 G는 축의 중앙입니다. 원본 풀이처럼 주어진 두 암의 질량을 사용합니다. 축 자체의 질량·단면 정보는 주어지지 않았습니다.')
add(40, '예제 1 · 어느 관성성분부터 계산할 것인가', 'Problem Solving 01:44–02:17',
    '물체축 하나를 AB에 맞추면 각속도 성분 두 개가 0이 됩니다. 먼저 G에 대한 관성행렬에서 실제로 필요한 열을 찾아 H<sub>G</sub>를 구하고, G에서 A로 기준점을 옮긴 뒤 AB와의 각을 구합니다.',
    correction='원본 전략의 마지막 줄과 영상의 “disk”는 이 예제의 두 L-shaped arms(L자 암) 조립체를 가리킵니다. 원판은 46장부터 등장합니다.')
add(41, '예제 1 · 축 방향과 기저 정하기', 'Problem Solving 02:20–02:35',
    'N은 지면에 고정된 기준계이고 A는 암 조립체에 붙은 기준계입니다. 점 A와 frame A(기준계 A)가 같은 글자를 쓴다는 점에 주의합니다. a₃를 A에서 B로 향하는 축 방향에 놓고, a₁,a₂를 그림처럼 수직인 두 횡방향으로 놓습니다.',
    '질량 적분에서는 원점을 G에 옮겨 같은 축 방향을 사용합니다. 두 암의 부착점은 이 좌표에서 z=±0.100 m입니다. 길이 0.600 m의 중앙과 삼등분점의 간격이 0.100 m이기 때문입니다.')
add(42, '예제 1 · 회전속력을 rad/s로 변환', 'Problem Solving 02:38–03:20',
    '360 revolutions per minute(분당 360회전)는 1초에 6회전입니다. 한 바퀴는 2π rad이므로 크기는 12π rad/s입니다. 그림의 양의 a₃축을 따르므로 다른 성분은 모두 0입니다.',
    eq='ω = (360 × 2π / 60) a₃ = 12π a₃ rad/s')
add(43, '예제 1 · 네 직선부에서 관성행렬의 세 번째 열 구하기', 'Problem Solving 03:23–06:29',
    '각 직선부의 길이를 ℓ=0.2 m, 질량을 μ=2.5 kg, 부착점의 축 방향 거리를 c=0.1 m라 둡니다. x,y,z는 각각 a₁,a₂,a₃ 성분입니다. z=+c 쪽 암은 x가 음수인 쪽으로 뻗고 그 끝에서 y가 증가합니다. 반대편은 좌표 부호가 모두 뒤집히므로 xz, yz와 거리 제곱의 적분값은 같습니다.',
    '한쪽의 가로부는 x의 평균이 −ℓ/2이고 세로부는 x=−ℓ입니다. 그래서 −∫xz dm은 두 암을 합해 2μc(ℓ/2+ℓ)입니다. −∫yz dm은 y=0인 가로부에서 0이고, 세로부 두 개에서 −2μcℓ/2가 됩니다.',
    'I₃₃에는 x²+y²를 적분합니다. 가로부의 평균 x²는 ℓ²/3입니다. 세로부의 평균 x²+y²는 ℓ²+ℓ²/3입니다. 두 암의 기여를 합하면 1/3 kg·m²입니다.',
    eq='I₁₃ = +0.150,　I₂₃ = −0.050,　I₃₃ = 2μ(ℓ²/3 + ℓ² + ℓ²/3) = 1/3　[kg·m²]',
    correction='원본의 I₂₃ 적분 전개는 I₁₃ 줄과 같은 항을 반복합니다. 그림에서 y가 변하는 구간으로 다시 적분하면 원본의 최종 성분 −0.050 kg·m²가 나옵니다. 행렬의 X는 이번 곱에 쓰이지 않는 성분입니다.')
add(44, '예제 1 · A점의 각운동량과 성분 부호', 'Problem Solving 06:32–08:20',
    'H<sub>G</sub>는 43장의 세 번째 열에 12π를 곱한 벡터입니다. G는 지면에 고정된 회전축 위에 있으므로 v<sub>G</sub>=0이고, A점으로 옮겨 더하는 AG×m v<sub>G</sub>도 0입니다. H<sub>A</sub>와 H<sub>G</sub>의 값이 같습니다.',
    '첫째·둘째 성분이 남습니다. AB를 중심으로 돌고 있어도 AB가 이 조립체의 principal axis(관성주축)는 아니므로 각운동량이 AB와 기울어집니다.',
    eq='[H<sub>A</sub>]<sub>A</sub> = 12π(0.15, −0.05, 1/3)ᵀ | H<sub>A</sub> = 5.6549 a₁ − 1.8850 a₂ + 12.5664 a₃　[kg·m²/s]',
    correction='원본 결과 열의 둘째 성분은 양수로 인쇄되었고 아래 벡터식은 a₃를 세 번 씁니다. 바로 위 행렬의 세 번째 열과 그림의 기저 순서로 각 성분의 축과 부호를 복원했습니다.')
add(45, '예제 1 · 축과 각운동량 사이의 각', 'Problem Solving 08:22–09:15',
    'AB 방향의 unit vector(단위벡터)가 a₃이므로 H<sub>A</sub>·a₃=H₃입니다. 분모의 벡터 크기에는 세 성분을 모두 넣습니다. 곱셈 중간값은 반올림하기 전에 사용합니다.',
    eq='|H<sub>A</sub>| = 12π√(0.15²+0.05²+(1/3)²) ≈ 13.9084 kg·m²/s | θ = cos⁻¹[(4π)/13.9084] ≈ 25.38°',
    detail=card('결과 읽기','만약 shaft axis(회전축)가 관성주축이었다면 H₁과 H₂는 0이고 이 각도도 0°였을 것입니다. 이 예제의 기울기는 회전속력의 크기보다 질량의 배치로 결정됩니다.'))
add(46, '예제 2 · 수평축에 달려 구르는 원판', 'Problem Solving 09:19–09:54',
    'Homogeneous disk(균질 원판)의 질량은 m, 반지름은 r입니다. 질량을 무시하는 수평축 OG의 길이는 L이고, O는 지면에 고정되어 있습니다. 원판이 OG에 대해 그림 방향으로 상대 각속력 ω₁로 회전하며 바닥에서 미끄러지지 않습니다.',
    '구할 것은 지면 기준 원판의 전체 angular velocity(각속도)와 O에 대한 angular momentum(각운동량)입니다. 상대 자전만 고려하면 원판 중심 G가 O 주위를 도는 운동이 빠집니다.')
add(47, '예제 2 · 자전축 OG와 순간 회전축 OC', 'Problem Solving 10:01–10:47',
    'Axle(차축)는 O를 지나는 수직축 주위로 돌 수 있습니다. 원판은 그 차축 OG에 대해서도 자전합니다. Rolling without slipping(미끄럼 없는 구름)이므로 지면과 접하는 원판의 물질점 C는 그 순간 속도가 0입니다.',
    'O는 원판에 고정된 기하학적 연장점으로 취급할 수 있습니다. OG가 원판의 자전축이므로 자전은 O의 속도에 기여하지 않으며 공전의 중심 O도 움직이지 않습니다. 따라서 속도가 0인 O와 C를 잇는 선이 원판 전체의 instantaneous axis(순간 회전축)입니다.',
    correction='47장 반복 문제문의 “about OC”는 주어진 상대 자전축을 설명하는 자리에서는 OG로 읽습니다. OC는 두 회전을 합한 결과의 순간축입니다. 접촉한 물질점 C는 시간이 지나면 바뀝니다.')
add(48, '예제 2 · 지면, 차축, 원판의 세 기준계', 'Problem Solving 10:52–11:08',
    '관성 기준계 N, 차축에 붙은 A, 원판에 붙은 B를 둡니다. a₁은 OG를 따라 수평, n₂는 수직 위쪽입니다. 계산 순간에는 b₁=a₁, b₂=n₂로 정렬하고 b₃=b₁×b₂로 둡니다. 이 순간의 성분 일치는 이후 모든 시각의 축 일치를 뜻하지 않습니다.',
    correction='원본 표에서 A와 B가 모두 arm(암)으로 적혔습니다. 그림의 축과 영상 설명에 따라 A는 axle(차축), B는 disk(원판)입니다.')
add(49, '예제 2 · 상대 자전과 수직축 회전을 더하기', 'Problem Solving 11:11–12:43',
    'N에서 본 A의 각속도를 ω₂n₂, A에서 본 B의 각속도를 ω₁a₁이라 둡니다. 각속도 합성에 따라 두 벡터를 더하면 지면에 대한 원판의 각속도입니다. 미지수는 축의 수직 회전 성분 ω₂ 하나입니다.',
    'ω₂의 방향을 미리 맞힐 필요는 없습니다. n₂를 양의 방향으로 가정하고 다음 장의 no-slip condition(비미끄럼 조건)으로 부호를 결정합니다.',
    eq='ω = ω₁a₁ + ω₂n₂')
add(50, '예제 2 · 접촉점 속도 0에서 공전 각속도 구하기', 'Problem Solving 12:46–13:51',
    'O에서 G까지는 Lb₁이고 G에서 접촉점 C까지는 −rb₂입니다. O의 속도가 0이므로 C의 속도는 ω×OC입니다. b₁×b₂=b₃, b₂×b₁=−b₃를 쓰면 두 항이 모두 b₃ 방향에 놓입니다.',
    '지면과의 상대속도가 0이려면 rω₁+Lω₂=0이어야 합니다. 음수는 차축의 회전 방향이 처음 가정한 +n₂와 반대라는 뜻입니다. 얻은 ω는 (ω₁/L)OC이므로 순간축 결과도 확인됩니다.',
    eq='v<sub>C</sub> = (ω₁b₁+ω₂b₂) × (Lb₁−rb₂) = −(rω₁+Lω₂)b₃ = 0 | ω₂ = −rω₁/L,　ω = ω₁b₁ − (rω₁/L)b₂')
add(51, '예제 2 · 균질한 얇은 원판의 중심 각운동량', 'Problem Solving 13:54–16:48',
    'b₁은 원판 면에 수직이므로 normal-axis inertia(면 법선축 관성모멘트)는 mr²/2입니다. 면 안의 두 직경 b₂,b₃에 대한 관성은 대칭으로 같고 얇은 평판의 수직축 정리에 따라 각각 mr²/4입니다.',
    '세 축이 principal axes(관성주축)이므로 50장의 각속도 성분마다 해당 주관성모멘트를 곱합니다. 원판의 자전과 공전에 서로 다른 계수가 붙습니다.',
    eq='[I<sub>G</sub>]<sub>B</sub> = diag(mr²/2, mr²/4, mr²/4) | H<sub>G</sub> = (mr²ω₁/2)b₁ − (mr³ω₁/4L)b₂')
add(52, '예제 2 · 중심에서 고정점 O로 각운동량 옮기기', 'Problem Solving 16:51–17:58',
    'v<sub>G</sub>=ω×OG에서 OG와 나란한 자전 성분은 없어지고, 수직 회전 성분이 원판 중심을 +b₃ 방향으로 움직입니다. 그래서 v<sub>G</sub>=rω₁b₃입니다. OG×m v<sub>G</sub>=−mLrω₁b₂를 중심 각운동량에 더합니다.',
    '고정점 O에서 직접 검산할 수도 있습니다. 평행축 정리로 I₁₁은 그대로, I₂₂는 mr²/4+mL²가 됩니다. 여기에 각각 ω₁과 −rω₁/L을 곱하면 같은 두 성분이 나옵니다.',
    eq='H<sub>O</sub> = H<sub>G</sub> + OG × m v<sub>G</sub> | H<sub>O</sub> = (mr²ω₁/2)b₁ − (mrω₁/L)(r²/4+L²)b₂',
    correction='영상 17:31–17:47에서 강사가 C를 G로 정정합니다. 이 기준점 이동에 들어가는 속도는 center velocity(중심 속도) v<sub>G</sub>입니다. 접촉점 속도 v<sub>C</sub>=0은 50장에서 사용했습니다.')
add(53, '예제 3 · 수평 와이어가 지탱하는 회전 봉', 'Problem Solving 18:02–19:19',
    'Uniform slender rod(균일한 가는 봉) AB의 질량 m=20 kg, 길이 L=2 m입니다. 봉은 A에서 수직축에 핀으로 연결되고 B에서 C로 향하는 horizontal wire(수평 와이어)가 봉을 수평선과 β=60°로 유지합니다. 축은 ω=15 rad/s로 일정하게 회전합니다.',
    '구할 것은 wire tension(와이어 장력)의 크기 T와 A에서 봉이 받는 pin reaction(핀 반력) 벡터 R입니다. +n₁은 축에서 바깥쪽, +n₂는 위쪽입니다. B에 작용하는 장력은 축 안쪽이므로 −Tn₁입니다.')
add(54, '예제 3 · 자유물체도와 두 운동방정식', 'Problem Solving 19:21–20:04',
    '봉을 분리하면 외력은 A의 반력 R, B의 장력 −Tn₁, G의 무게 −mgn₂입니다. 먼저 회전 운동학으로 a<sub>G</sub>와 D<sub>N</sub>H<sub>G</sub>를 정하고, 외력과 모멘트의 합을 각각 여기에 연결합니다.',
    '전략 슬라이드는 A에 대한 모멘트를 제안합니다. 실제 마지막 장은 G를 택해 무게의 모멘트를 없앱니다. A를 택하면 반력의 모멘트가 사라지므로 두 경로로 답을 검산할 수 있습니다.',
    correction='원본 전략의 “couple H<sub>G</sub>”에 필요한 양은 D<sub>N</sub>H<sub>G</sub>입니다. 우력의 단위 N·m와 일치하며, 58장과 60장도 시간미분을 사용합니다.')
add(55, '예제 3 · 봉 축과 수평·수직축 연결하기', 'Problem Solving 20:04–20:51',
    'N은 관성계, A는 회전축, B는 봉의 기준계입니다. 그림의 순간에 b₁은 A에서 B로 향합니다. n₁은 수평 바깥쪽, n₂는 위쪽이며 b₁=cosβ n₁+sinβ n₂입니다. b₂를 그 평면에서 b₁보다 90° 회전시켜 b₂=−sinβ n₁+cosβ n₂로 둡니다.',
    '수직 회전벡터를 봉 축으로 분해하려면 역관계 n₂=sinβ b₁+cosβ b₂를 사용합니다. n₁×n₂=b₁×b₂=b₃이고, 각 모멘트의 부호는 이 방향을 기준으로 정합니다.')
add(56, '예제 3 · 봉의 기울기와 각속도', 'Problem Solving 20:53–22:06',
    '수직축 자체의 각속도는 ωn₂이고 봉이 핀에서 기울기를 바꾸는 상대 각속도는 β̇a₃입니다. 수평 와이어가 봉의 기울기를 유지하므로 β̇=0입니다. 따라서 이 운동에서 봉 전체의 각속도는 지면에 고정된 수직 방향입니다.',
    '축의 회전속력까지 일정하므로 지면 기준 angular acceleration(각가속도)은 0입니다. 그래도 질량중심은 원운동하고 봉 축은 공간에서 방향을 바꿉니다.',
    eq='ω<sub>rod</sub> = ωn₂ + β̇a₃ = ωn₂')
add(57, '예제 3 · 가는 봉 중심의 각운동량', 'Problem Solving 22:09–23:45',
    '이상적인 slender rod(가는 봉)의 질량은 모두 길이축 b₁ 위에 있어 I₁₁=0입니다. 중심을 지나는 횡축에서는 ∫x²(m/L)dx를 −L/2에서 L/2까지 적분해 I₂₂=I₃₃=mL²/12를 얻습니다.',
    'ω를 b축으로 분해하면 길이 방향 성분은 ωsinβ, 횡방향 성분은 ωcosβ입니다. 첫 성분의 관성이 0이므로 H<sub>G</sub>에는 b₂ 성분만 남습니다. 따라서 H<sub>G</sub>의 방향은 수직 회전축과 다릅니다.',
    eq='[I<sub>G</sub>]<sub>B</sub> = diag(0, mL²/12, mL²/12) | H<sub>G</sub> = (mL²/12)ω cosβ b₂')
add(58, '예제 3 · 일정한 회전에도 모멘트가 필요한 이유', 'Problem Solving 23:47–24:27',
    'H<sub>G</sub>의 물체축 성분은 일정하므로 D<sub>B</sub>H<sub>G</sub>=0입니다. 그러나 b₂가 회전하므로 지면에서 본 변화율은 ω×H<sub>G</sub>입니다. ω의 b₂ 성분은 외적이 0이고, b₁ 성분과 H의 b₂ 성분만 +b₃를 만듭니다.',
    '수치를 넣으면 필요한 중심 모멘트는 (20×2²/12)×15²×sin60°×cos60°≈649.52 N·m입니다. 이것이 장력과 핀 반력의 모멘트가 합쳐서 만들어야 할 값입니다.',
    eq='D<sub>N</sub>H<sub>G</sub> = (mL²/12)ω² sinβ cosβ b₃')
add(59, '예제 3 · 질량중심의 원운동 가속도', 'Problem Solving 24:29–25:10',
    'G는 봉의 중점에 있으므로 수직축에서의 거리 R<sub>G</sub>=(L/2)cosβ=0.500 m입니다. 일정한 속력의 원운동에서는 radial acceleration(반지름 방향 가속도)이 축 안쪽을 향합니다.',
    '같은 결과가 두 점 가속도 관계 a<sub>G</sub>=a<sub>A</sub>+α×AG+ω×(ω×AG)에서도 나옵니다. A는 정지하고 α=0입니다. AG의 수직 성분은 사라지고 수평 성분에 −ω²가 곱해집니다.',
    eq='a<sub>G</sub> = −(L/2)ω² cosβ n₁ = −112.5 n₁ m/s² | m a<sub>G</sub> = −2250 n₁ N')
add(60, '예제 3 · 장력과 핀 반력을 성분별로 풀기', 'Problem Solving 25:13–28:18',
    '병진식에서 R₁−T=−2250 N, R₂−mg=0, R₃=0입니다. G에 대한 모멘트 팔은 GA=−(L/2)b₁, GB=(L/2)b₁입니다. 외적에서 남는 b₃ 성분은 (L/2)[sinβ(R₁+T)−cosβ R₂]입니다. 무게는 G를 지나므로 모멘트가 0입니다.',
    '이 성분을 58장의 (mL²/12)ω²sinβcosβ와 같게 놓습니다. R₁=T−(mL/2)ω²cosβ, R₂=mg를 대입해 정리하면 2T=mg cotβ+(2mL/3)ω²cosβ입니다. 장력의 크기는 양수이고 힘 벡터는 안쪽입니다.',
    eq='T = (mg/2)cotβ + (mL/3)ω²cosβ = 56.638 + 1500 = 1556.638 N | R₁ = 1556.638 − 2250 = −693.362 N,　R₂ = 196.2 N,　R₃ = 0 | T⃗ ≈ −1557 n₁ N,　R⃗ ≈ (−693.4 n₁ + 196.2 n₂) N',
    detail=card('고정 핀 A에서 독립 검산','A에 대한 외력 모멘트는 [LT sinβ−(L/2)mg cosβ]b₃입니다. 균일 봉의 끝점 횡축에 대한 관성은 mL²/3이므로 필요한 모멘트는 (mL²/3)ω²sinβcosβ b₃입니다. 두 값을 같게 두고 T를 풀면 G에 대한 풀이와 같습니다.'),
    correction='원본 마지막 줄의 수평 반력은 −697 N입니다. 그림의 L=2 m, β=60°, ω=15 rad/s와 m=20 kg를 사용하면 수평 합력은 정확히 −2250 N입니다. 원본 장력의 반올림값 1557 N과도 일치하는 반력은 약 −693 N입니다.')
add(61, '원본 참고문헌', '원본 참고문헌 슬라이드',
    'Beer 외, <i>Vector Mechanics for Engineers: Dynamics</i>, 12판, 18장. 유홍희, 『동역학』, 1판, 문운당, 8장.', role='References')

summary = ''.join([
    card('1. 강체의 운동은 질량중심의 이동과 질량중심 주위의 회전으로 나눕니다.',
        '볼링공은 앞으로 나아가면서 동시에 회전합니다. 공 전체의 이동은 center of mass(질량중심) G의 속도 v<sub>G</sub>로 대표할 수 있습니다. 공 위의 한 점 P는 여기에 회전 속도 ω×GP가 더해집니다. 한쪽 점이 얻는 회전 속도와 반대쪽 점이 얻는 회전 속도가 질량 가중합에서 상쇄되므로 전체 linear momentum(선운동량)은 L=m v<sub>G</sub>입니다.',
        '각 점의 운동량에 G부터의 지레팔을 적용해 r×v<sub>P</sub> dm을 더하면 회전의 기여가 남습니다. 이것이 angular momentum about G(G에 대한 각운동량)입니다. 제자리에서 도는 원판처럼 L=0이면서 H<sub>G</sub>가 0이 아닐 수 있습니다.',
        formula('L = m v<sub>G</sub>　[kg·m/s]　　 H<sub>G</sub> = I<sub>G</sub>ω　[kg·m²/s]'), kind='callout'),
    card('2. 관성행렬은 회전축과 질량이 놓인 위치를 함께 반영합니다.',
        'Inertia matrix(관성행렬)의 대각성분은 그 축까지의 수직거리 제곱을 질량에 대해 더한 값입니다. 비대각성분은 −∫xy dm처럼 좌표가 함께 변하는 정도를 나타냅니다. 따라서 한 축으로만 돌더라도 각운동량에는 다른 축 성분이 생길 수 있습니다. 예제 1에서 실제 회전축과 각운동량 사이의 각은 25.38°입니다.',
        'Principal axes(관성주축)를 쓰면 I는 대각행렬이 되고 Hᵢ=Iᵢωᵢ입니다. ω와 H는 동일한 좌표계에서 성분을 써야 합니다. 강체에 고정한 축에서는 질량 분포가 변하지 않아 행렬 성분도 일정합니다. 기준점을 C로 평행 이동할 때는 ρ=CG로 두어 I<sub>C</sub>=I<sub>G</sub>+m[(ρ·ρ)𝟙−ρρᵀ]를 씁니다. 한 축만 필요하면 I<sub>C,u</sub>=I<sub>G,u</sub>+md²이고 d는 두 평행축 사이 거리입니다.'),
    card('3. 힘은 선운동량을, 모멘트는 각운동량을 바꿉니다.',
        'Free-body diagram(자유물체도)에 외력의 작용점과 방향을 표시합니다. 힘을 그대로 합한 값은 m a<sub>G</sub>입니다. G에서 각 힘까지의 위치벡터와 힘을 외적하고, 별도로 가한 couple(우력)을 더하면 ΣM<sub>G</sub>입니다. 이 값은 지면에서 본 H<sub>G</sub>의 시간미분입니다.',
        '물체가 돌면 H<sub>G</sub>의 물체축 성분이 일정해도 공간에서 그 방향은 바뀔 수 있습니다. 그래서 물체축 성분을 미분한 I<sub>G</sub>ω̇에 ω×H<sub>G</sub>를 더합니다. 예제 3의 경사진 봉은 일정한 속력으로 돌면서도 이 둘째 항 때문에 모멘트가 필요합니다.',
        formula('ΣF = m a<sub>G</sub>　　 ΣM<sub>G</sub> = D<sub>N</sub>H<sub>G</sub> = I<sub>G</sub>ω̇ + ω×(I<sub>G</sub>ω)')),
    card('4. 모멘트의 기준점을 옮길 때는 먼저 무엇을 옮기는지 정합니다.',
        'C에서 G를 향하는 ρ를 그립니다. 힘의 모멘트를 옮기면 ρ×ΣF가 추가되고, 각운동량을 옮기면 ρ×m v<sub>G</sub>가 추가됩니다. 뒤 식은 C가 움직일 때도 한 순간의 H<sub>C</sub>를 구할 수 있는 일반식입니다.',
        formula('ΣM<sub>C</sub> = ΣM<sub>G</sub> + ρ×ΣF　　 H<sub>C</sub> = H<sub>G</sub> + ρ×m v<sub>G</sub>'),
        '시간미분까지 하면 C의 속도가 새로 들어갑니다. 일반식은 ΣM<sub>C</sub>=D<sub>N</sub>H<sub>C</sub>+v<sub>C</sub>×m v<sub>G</sub>입니다. 한편 C가 강체에 붙은 점이면 H<sub>C</sub>=I<sub>C</sub>ω+ρ×m v<sub>C</sub>입니다. 지면에 고정된 핀에서는 v<sub>C</sub>=0이므로 두 식 모두 단순해집니다. 일반 이동점에서는 두 보정항을 각각 판단합니다.'),
    card('5. 예제의 첫 식은 문제에서 주어진 구속조건이 정합니다.',
        '<a href="#slide-39">두 L자 암</a>은 축 AB를 따라 ω=12πa₃이므로 I<sub>G</sub>의 세 번째 열만 곱합니다. G가 회전축 위에 정지해 H<sub>A</sub>=H<sub>G</sub>=(5.6549,−1.8850,12.5664) kg·m²/s입니다. H₃을 전체 크기로 나누고 역코사인을 취해 축과 이루는 각을 구합니다.',
        '<a href="#slide-46">구르는 원판</a>은 rolling without slipping(미끄럼 없는 구름)이므로 접점 속도 v<sub>C</sub>=0입니다. (ω₁b₁+ω₂b₂)×(Lb₁−rb₂)=0에서 ω₂=−rω₁/L입니다. 중심 G는 rω₁b₃로 움직이므로 O의 각운동량에는 OG×m v<sub>G</sub>를 더합니다. 결과는 H<sub>O</sub>=(mr²ω₁/2)b₁−(mrω₁/L)(r²/4+L²)b₂입니다.',
        '<a href="#slide-53">경사진 봉</a>은 와이어가 기울기 β를 유지합니다. G의 원운동 반지름은 (L/2)cosβ=0.5 m이므로 안쪽 힘이 2250 N 필요합니다. 수평 힘 식 R₁−T=−2250과 G의 모멘트 식을 함께 풀면 장력 1556.6 N, 핀 반력은 안쪽 693.4 N·위쪽 196.2 N입니다.'),
])

exams = [
    ('Why does the linear momentum of a rotating body equal m v<sub>G</sub>?',
     'The velocity of each element is the center-of-mass velocity plus a rotational contribution. The rotational contributions sum to zero because the first mass moment about G vanishes.',
     'First mass moment(질량 일차 모멘트) ∫r dm=0을 근거로 듭니다. Linear momentum(선운동량)의 회전 기여가 상쇄되는 이유입니다.'),
    ('Is the angular momentum of a rigid body always parallel to its angular velocity?',
     'Angular momentum is the inertia tensor applied to angular velocity. For nonzero angular velocity, the two are parallel when the angular velocity lies along a principal axis with nonzero principal moment.',
     'Parallel(평행한) 조건을 principal axis(관성주축)와 묶어 설명합니다. 예제 1에서 두 방향은 약 25.38° 차이 납니다.'),
    ('State the parallel-axis theorem for two parallel axes.',
     'The moment of inertia about the displaced axis is the centroidal moment of inertia plus the mass times the square of the perpendicular distance between the axes.',
     'Centroidal(질량중심을 지나는), displaced axis(이동한 축), perpendicular distance(수직거리)가 핵심 표현입니다.'),
    ('Why is a transport term needed in Euler’s equation?',
     'The body axes rotate relative to the inertial frame. The inertial derivative of angular momentum therefore includes the cross product of angular velocity and angular momentum.',
     'Transport term(기준계 회전에 따른 항)은 ω×H입니다. Inertial derivative(관성계 미분)가 필요한 이유부터 밝힙니다.'),
    ('How do you find the angular momentum about an arbitrary moving point C?',
     'First compute the angular momentum about the center of mass. Then add the cross product of the position vector from C to G and the total linear momentum measured in the inertial frame.',
     'Arbitrary moving point(임의의 이동점)에는 H<sub>C</sub>=H<sub>G</sub>+CG×m v<sub>G</sub>를 쓸 수 있습니다. From C to G(C에서 G로)의 순서를 지킵니다.'),
    ('Under what condition can the external moment about C be equated to the inertial derivative of H<sub>C</sub>?',
     'The cross product of the velocity of C and the total linear momentum must vanish. A point fixed in the inertial frame satisfies this condition.',
     'Must vanish(0이 되어야 한다)는 보정항에 대한 조건입니다. Point fixed in the inertial frame(관성계에 고정된 점)은 이를 만족하는 한 예입니다.'),
    ('Determine the angle between the shaft and the angular momentum of the arms.',
     'I multiply the third column of the inertia matrix by the shaft speed. Projecting the resulting angular momentum onto the shaft and dividing by its magnitude gives the cosine of the angle. The angle is 25.38 degrees.',
     'Project onto the shaft(축에 투영하다)는 H·a₃를 뜻합니다. Magnitude(크기)는 세 성분을 모두 이용합니다.'),
    ('What constraint determines the vertical angular velocity of the rolling disk?',
     'Rolling without slipping requires zero instantaneous velocity at the contact point. Setting the cross product of the total angular velocity and OC to zero gives the vertical component as minus r times the spin rate divided by L.',
     'Contact point(접촉점)의 instantaneous velocity(순간속도)를 0으로 둡니다. 마이너스 부호는 처음 둔 양의 수직축에 상대적인 방향입니다.'),
    ('Why does the inclined rod require a moment even at constant angular velocity?',
     'The angular momentum of the rod is not aligned with its angular velocity. Its components are constant in the body frame, but its direction changes in the inertial frame.',
     'Inclined rod(경사진 봉)의 각속도는 일정합니다. Angular momentum(각운동량)의 방향이 변한다는 사실을 답에 포함합니다.'),
    ('Determine the wire tension and the pin reaction for the rod.',
     'Applying the force balance and the moment equation about G gives a wire tension of approximately 1557 N. The pin exerts approximately 693.4 N radially inward and 196.2 N upward on the rod.',
     'Tension(장력)은 크기를, pin reaction(핀 반력)은 radially inward(반지름 방향 안쪽)와 upward(위쪽) 성분을 제시합니다.'),
]

glossary = [
    ('kinematics(운동학) / kinetics(운동역학)', '운동의 기하를 기술하는 분야 / 그 운동을 힘과 모멘트에 연결하는 분야'),
    ('rigid body(강체) / body-fixed(물체에 고정된)', '점 사이 거리가 일정한 물체 / 그 물체와 함께 움직이는 점이나 축'),
    ('center of mass(질량중심) / mass element(질량 요소)', '질량 가중 평균 위치 G / 적분하는 미소 질량 dm'),
    ('linear momentum(선운동량) / angular momentum(각운동량)', 'm v<sub>G</sub> / 기준점부터의 위치와 각 요소의 선운동량을 외적한 합'),
    ('moment of a force(힘의 모멘트) / couple(우력)', '기준점에서 작용점으로 향하는 r과 F의 외적 / 합력이 0이면서 모멘트를 만드는 힘쌍'),
    ('moment of inertia(관성모멘트) / product of inertia(관성곱)', '질량과 축까지 거리 제곱의 적분 / 서로 다른 두 좌표곱의 질량 적분'),
    ('principal axes(관성주축) / diagonal(대각의)', '관성행렬이 대각형이 되는 축 / 행과 열의 번호가 같은 성분'),
    ('parallel-axis theorem(평행축 정리)', '질량중심을 지나는 축의 관성에서 평행한 다른 축의 관성을 구하는 관계'),
    ('arbitrary point(임의점) / fixed point(고정점)', '자유롭게 선택한 기준점 / 지정한 기준계에서 움직이지 않는 점'),
    ('inertial derivative(관성계 미분) / body components(물체축 성분)', '관성 관찰자가 본 벡터의 변화 / 물체에 붙은 축으로 쓴 숫자 성분'),
    ('aligned with(나란한) / perpendicular to(수직인)', '같은 직선 방향에 놓인 / 두 방향이 직각을 이루는'),
    ('homogeneous(균질한) / slender(가늘고 긴) / negligible(무시할 수 있는)', '밀도가 균일한 / 길이에 비해 단면이 작은 / 계산에서 무시할 정도로 작은'),
    ('axle(차축) / welded(용접된) / pinned(핀으로 연결된)', '물체의 회전을 지지하는 축 / 상대 운동이 없도록 결합된 / 핀 연결을 갖는'),
    ('rolling without slipping(미끄럼 없는 구름) / contact point(접촉점)', '접하는 두 물질점의 순간속도가 같은 조건 / 현재 접촉하고 있는 점'),
    ('spin rate(자전 각속력) / instantaneous axis(순간 회전축)', '물체가 자체 축 주위로 도는 빠르기 / 그 순간 속도가 0인 점들을 잇는 회전축'),
    ('constant rate(일정한 속력) / counterclockwise(반시계 방향의)', '회전 빠르기가 일정함 / 제시된 관찰 방향에서 시계 반대 방향으로 도는'),
    ('tension(장력) / pin reaction(핀 반력)', '팽팽한 줄이 줄을 따라 당기는 힘 / 핀이 연결된 물체에 가하는 힘'),
    ('radially inward(반지름 방향 안쪽으로) / upward(위쪽으로)', '회전축 쪽으로 향하는 수평 성분 / 중력의 반대 방향 성분'),
    ('determine(구하라) / express about G(G를 기준으로 나타내라)', '요구한 크기·방향을 계산 / 모멘트나 각운동량의 기준점을 G로 택해 표현'),
]

audit = [
    ('Contents 1 03:30 · 10장', 'angular momentum', '적분 밖으로 꺼내는 공통 벡터는 angular velocity(각속도) ω입니다.'),
    ('Contents 1 16:09 · 19장', 'symmetric and positive', '단위축에 대한 관성은 0 이상입니다. 개별 비대각성분에는 음수가 가능합니다.'),
    ('Contents 1 19:18–19:25 · 21–22장', 'from G to C', '뒤의 CP=CG+GP와 일치하도록 ρ=CG를 사용합니다. 평행축 정리의 이차항은 부호에 무관합니다.'),
    ('Contents 1 19:42–20:01 · 22장', 'momentum inertia / minority Matrix', '질량 분포를 담는 moment of inertia matrix(관성행렬)입니다.'),
    ('30–31장', 'ρᵢ 표기', '여러 외력에 대해 같은 ρ를 합 밖으로 꺼냅니다.'),
    ('Contents 2 09:42–09:58 · 34장', 'only when C is a fixed point', '물체 고정점에서 ρ×v<sub>C</sub>=0인 경우 전체가 포함됩니다.'),
    ('Contents 2 10:40–11:25 · 35장', 'only in these two cases', '정확한 소거 조건은 v<sub>C</sub>×m v<sub>G</sub>=0입니다.'),
    ('Problem Solving 02:14 · 40장', 'disk', '조립체의 그림과 질량 자료는 L-shaped arms(L자 암)를 가리킵니다.'),
    ('Problem Solving 06:15–06:29 · 43장', 'I₂₃ 중간식 / 자막 0.01 0.05', '각 직선부에 대해 −∫yz dm을 계산하면 −0.050 kg·m²입니다.'),
    ('44장', '결과 열의 양의 둘째 성분 / 반복된 a₃', 'I<sub>G</sub>의 세 번째 열로 세 성분과 단위축을 복원했습니다.'),
    ('47–48장', 'OC를 자전축으로 표기 / A, B 모두 arm', '46·49장과 영상이 지칭하는 OG, axle(차축) A, disk(원판) B를 적용했습니다.'),
    ('Problem Solving 17:31–17:47 · 52장', 'velocity of point C', '영상에서 G로 직접 정정합니다. 원판 중심의 속도가 기준점 이동식에 필요합니다.'),
    ('Problem Solving 18:44 · 53장', 'horizontal wire PC', '원본 그림에서 와이어는 봉 끝 B와 축 위 C를 잇습니다.'),
    ('54·58장', 'couple H<sub>G</sub>', '힘의 모멘트는 D<sub>N</sub>H<sub>G</sub>와 단위 및 물리적 의미가 일치합니다.'),
    ('53·59–60장', '수평 반력 −697 N', '그림의 회전 반지름 0.500 m와 수평 힘 식에서 −693.362 N입니다.'),
    ('Summary 00:19–01:26', 'mess Center / translational emotion', '질량중심과 병진 운동을 가리킵니다. 01:08부터 시작되는 평면운동 예고는 별도 구간으로 옮겼습니다.'),
]

roadmap = '''<section class="editorial-section section-divider" id="course-roadmap" aria-labelledby="roadmap-title">
<p class="section-kicker">Summary video · Course roadmap</p>
<h2 class="section-title" id="roadmap-title">Summary 영상 후반 · 다음 강의는 평면에서 움직이는 강체입니다.</h2>
<p class="section-lead">영상 00:19–01:05는 이번 강의의 뉴턴–오일러 방정식과 관성행렬을 복습합니다. 01:08부터는 공간 운동의 특수한 경우인 평면 운동을 예고합니다.</p></section>
<section class="editorial-section" id="roadmap-detail" aria-labelledby="roadmap-detail-title">
<p class="section-kicker">What comes next</p><h2 class="section-title" id="roadmap-detail-title">평면 운동에서는 어느 방향의 방정식이 남을까요?</h2>
<div class="card"><h3>Lecture 13 · Planar Motion of Rigid Bodies(강체의 평면 운동)</h3><p>다음 정규 강의에서는 한 평면 안에서 움직이는 강체에 병진의 뉴턴 방정식과 회전의 오일러 방정식을 적용합니다. 이번에 다룬 3차원 식을 출발점으로 삼습니다.</p></div>
<div class="evidence"><span>Summary 01:08–01:26</span><span>강의 인덱스 · Week 13</span></div></section>'''


def fill(template, values):
    return re.sub(r'\{\{([^{}]+)\}\}', lambda match: values[match[1]], template)


def build():
    template = (SITE / 'templates/lecture-page.template.html').read_text(encoding='utf-8')
    template = re.sub(r'\s*<!--[\s\S]*?-->', '', template)
    slide = re.search(r'<section class="source-section"[\s\S]*?</section>', template).group()
    assert len(slides) == 61
    sections = []
    for number, (title, evidence, blocks, role) in enumerate(slides, 1):
        sections.append(fill(slide, dict(
            NN=f'{number:02d}', SLIDE_ROLE=role, SLIDE_HEADING=title,
            LECTURE_SLUG='lecture12', DESCRIPTIVE_ALT_TEXT=escape(f'Lecture 12 원본 {number}장 · {title}'),
            CURRENT_PAGE=str(number), PAGE_COUNT='61', TRANSCRIPT_TIME_OR_SLIDE_ROLE=evidence,
            SLIDE_EXPLANATION_BLOCKS=blocks,
        )))
    template = template.replace(slide, '\n\n'.join(sections))
    exam = re.search(r'<div class="exam-card">[\s\S]*?</p>\s*</div>', template).group()
    template = template.replace(exam, '\n'.join(fill(exam, dict(
        EXAM_QUESTION=q, MODEL_ANSWER=escape(a), KOREAN_ANSWER_EXPLANATION=ko,
    )) for q, a, ko in exams))
    toc = [('overview', '전체 개요'), ('concept-map', '개념 지도'), ('concept-summary', '핵심 개념 요약')]
    toc += [(f'slide-{i:02d}', f'{i:02d} · {row[0]}') for i, row in enumerate(slides, 1)]
    toc += [('course-roadmap', 'Summary · 다음 단원'), ('exam-english', '시험 영어'),
            ('glossary', '용어집'), ('asr-log', '원본·자막 교정'), ('sources', '출처 및 강의 영상')]
    pdf = 'https://github.com/leejinh0225/MC2103-Dynamics/raw/refs/heads/main/2026FA_Dynamics/lecture_notes/lecture12_note.pdf'
    sources = '<ul class="plain-list"><li><a href="' + pdf + '">Lecture 12 원본 PDF</a> · 2026-11-18 · 61장</li>'
    for label, vid in VIDEOS:
        sources += f'<li><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상</a> · 영어 자동생성 자막 원문</li>'
    sources += '</ul><p>2026-11-18에 확보한 영상 5편의 영어 자동생성 자막 1,260구간과 원본 PDF를 대조했습니다. 그림과 식은 원본 순서대로 실었고, 캡션 시각은 각 설명에 대응하는 구간입니다. 3장의 보조 영상은 원본 링크를 수록했습니다. 61장의 교재 두 권은 원본 슬라이드의 참고문헌입니다.</p>'
    sources += '<p>좌표 적분의 중간 단계, 이동 기준점의 보정항 소거 조건, 세 예제의 검산은 강의 내용을 따라 계산할 수 있도록 보충했습니다.</p>'
    sources += '<p>같은 주차의 추가 강의는 별도로 등록된 Lecture 16 · Gyroscopic Motions(자이로스코프 운동)이며 날짜는 미기재입니다. <a href="https://github.com/leejinh0225/MC2103-Dynamics/blob/main/2026FA_Dynamics/강의_인덱스.md#week-12--2026-11-18">12주차 추가 강의 원본 PDF와 영상 목록</a></p>'
    template = fill(template, dict(
        LECTURE_NUMBER='Lecture 12', LECTURE_TITLE='Kinetics of Rigid Bodies',
        ONE_SENTENCE_DESCRIPTION='강체의 선운동량·각운동량, 관성행렬과 뉴턴–오일러 방정식을 세 가지 공간 운동 예제로 배우는 한국어 노트',
        WEEK='Week 12', DATE_OR_날짜_미기재='2026-11-18', PAGE_COUNT='61',
        LECTURE_PROMISE='질량중심의 이동은 힘으로, 강체의 회전은 모멘트로 설명합니다. 회전축의 L자 암, 구르는 원판, 와이어로 지지한 봉의 세 예제를 따라 각운동량·장력·핀 반력을 계산합니다.',
        VIDEO_SET='Overview · Contents 1·2 · Problem Solving · Summary',
        ALL_CONTENTS_AND_PROBLEM_SOLVING_BUTTONS='\n'.join(
            f'<a class="button button--primary" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{name} 영상 열기</a>'
            for name, vid in VIDEOS[1:4]),
        ORIGINAL_PDF_URL=pdf, LECTURE_NOTE_FILENAME='lecture12_note.pdf',
        CORE_RELATIONSHIP_HEADLINE='회전속력이 일정한데도 지지대가 힘을 내야 하는 이유는 무엇일까요?',
        CORE_RELATIONSHIP_EXPLANATION='경사진 봉이 수직축 주위를 일정한 속력으로 돌면 질량중심은 원을 그리고, 각운동량 벡터는 방향을 바꿉니다. 자유물체도에 표시한 외력과 모멘트를 이 두 변화에 연결하면 와이어가 당기는 힘과 핀이 봉을 미는 힘을 각각 구할 수 있습니다.',
        CONCEPT_MAP_HEADLINE='질량 분포에서 운동량을 구하고, 그 변화율로 외력을 찾습니다.',
        CONCEPT_MAP_BLOCKS='<div class="grid-3">' +
            card('질량 분포 · Inertia(회전 관성)', '질량중심과 축을 정하고 관성행렬을 구성합니다. 질량이 축에서 어느 방향으로 얼마나 떨어졌는지 반영합니다.') +
            card('운동 상태 · Momentum(운동량)', 'L=m v<sub>G</sub>와 H<sub>G</sub>=I<sub>G</sub>ω를 구합니다. 다른 기준점에서는 질량중심의 이동 기여를 더합니다.') +
            card('운동방정식 · Force and moment(힘과 모멘트)', '관성계에서 운동량을 미분하고 자유물체도의 외력·외력 모멘트와 연결합니다.') + '</div>',
        STANDALONE_CONCEPT_SUMMARY=summary, DISTINCT_SUMMARY_VIDEO_SECTION_IF_NEEDED=roadmap,
        EXAM_SECTION_TITLE='관성, 기준점, 구속조건을 설명하는 영어 답안',
        BILINGUAL_GLOSSARY_TABLE=table(['영어(한국어)', '뜻과 쓰임'], glossary),
        AUDIT_SECTION_TITLE='슬라이드·영어 자동자막의 표기와 계산 교정',
        ASR_CORRECTION_TABLE=table(['위치', '원문 또는 쟁점', '해설에 사용한 해석과 근거'], audit),
        SOURCE_LIST_AND_PROVENANCE_NOTE=sources,
        TABLE_OF_CONTENTS_LINKS=''.join(f'<li><a href="#{key}">{label}</a></li>' for key, label in toc),
    ))
    template = template.replace('이 부분만 읽어도 렉처의 핵심 정의, 개념 관계, 가정과 풀이 흐름을 이해할 수 있도록 작성합니다.',
                                '질량중심과 기준점을 정하는 방법부터 세 예제에서 사용할 식과 답까지 한 번에 읽을 수 있습니다.')
    (SITE / 'lecture12.html').write_text(template, encoding='utf-8')


if __name__ == '__main__':
    build()
