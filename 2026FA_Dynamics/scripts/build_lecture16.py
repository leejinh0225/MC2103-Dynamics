"""Build the Lecture 16 study note from the shared Lecture 1 template."""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
VIDEOS = [
    ('Overview', 'mGm-rw2zxtw'), ('Contents 1', 'fdOdeRuE_2w'),
    ('Contents 2', 'ZPez6kr049w'), ('Problem Solving', '2U882l3jfs8'),
    ('Summary', 'y2VTGr96P6Y'),
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

add(1, '자이로스코프 운동 · 여러 축으로 도는 강체', '원본 표지',
    'Gyroscopic Motions(자이로스코프 운동)는 12주차에 배치된 추가 강의입니다. 기울어진 회전축의 방향이 왜 변하는지 살펴보고, 같은 원리로 비행 시뮬레이터의 베어링에 걸리는 힘을 구합니다.', role='Title')
add(2, 'Overview(개요) · 빠르게 도는 팽이', 'Overview 00:18–00:48',
    '팽이를 세게 돌리면 왜 더 오래 서 있을까요? 영상은 이 질문으로 시작합니다. 중력은 회전 중에도 작용합니다. 기울어진 팽이를 이해하려면 각운동량의 크기와 방향 중 어느 쪽이 토크에 의해 변하는지 살펴봐야 합니다.', role='Divider')
add(3, '도입 보조 영상', '원본 링크 슬라이드',
    '<a href="https://youtu.be/tC9JcpJr2q4" target="_blank" rel="noreferrer">슬라이드에 수록된 보조 영상 열기</a>', role='Video link')
add(4, 'Contents 1(본문 1) · 회전체의 운동방정식', 'Contents 1 · 도입',
    '두 짐벌과 회전체에 축을 붙인 뒤 angular momentum(각운동량)을 두 기저에서 각각 계산합니다.', role='Divider')
add(5, '팽이와 방향 계기가 공유하는 원리', 'Contents 1 00:18–01:24',
    '강체 운동학으로는 회전체의 각속도를 구할 수 있습니다. 강체 운동역학을 결합하면 그 회전을 유지하거나 축의 방향을 바꾸는 데 필요한 moment(힘의 모멘트)를 구할 수 있습니다. 그림은 팽이와 항공기 계기의 회전체를 연결합니다.',
    '질량중심 G에 대한 ΣM<sub>G</sub>=D<sub>N</sub>H<sub>G</sub>를 떠올려 봅니다. 외부 모멘트가 작으면 angular momentum(각운동량) H의 방향은 공간에서 천천히 변합니다. H에 수직인 모멘트가 계속 작용하면 크기를 유지하면서 방향이 돌아갈 수 있습니다.')
add(6, '모형의 세 움직임을 계산 순서로 연결하기', 'Contents 1 01:25–02:56',
    '그림의 초록색 outer gimbal(바깥 짐벌), 붉은색 inner gimbal(안쪽 짐벌), 파란색 rotor(회전체)는 차례로 연결됩니다. 바깥 고리를 움직이면 안쪽 두 부품도 따라갑니다. 안쪽 회전체에는 그 위에 독립적인 자전이 더해집니다.',
    '먼저 각 부품에 기준계와 축을 지정합니다. 이웃 부품 사이의 각도로 축 방향을 연결한 뒤 각속도 ω, 각운동량 H<sub>G</sub>, 모멘트 ΣM<sub>G</sub> 순으로 계산합니다. 이 모델에서는 회전체 중심 O=G가 고정되어 있습니다.')
add(7, '회전을 관찰하는 네 기준계 N, A, B, C', 'Contents 1 02:56–04:56',
    'Newtonian reference frame(뉴턴 관성 기준계) N은 이 문제에서 지면입니다. A는 바깥 고리, B는 안쪽 고리, C는 원판에 각각 붙습니다. 어떤 물체의 운동을 어떤 관찰자가 보는지 이 두 글자로 지정할 수 있습니다.',
    '예를 들어 B에서 본 C의 운동은 축 하나 주위의 단순 자전입니다. N에서 본 C에는 세 회전이 모두 들어갑니다. 강사는 지구 자전의 영향을 보려는 다른 문제에서는 지면을 관성계로 놓는 근사를 다시 검토해야 한다고 설명합니다.')
add(8, '이웃한 두 기준계가 공유하는 축', 'Contents 1 04:57–08:50',
    '네 좌표계의 원점은 공통점 O입니다. 각 부품의 세 축은 right-handed basis(오른손 기저)를 이룹니다. 그림에 축 두 개만 보이더라도 첫 축과 둘째 축의 외적이 셋째 축이라는 규칙으로 나머지를 정합니다.',
    '힌지 자체의 회전축은 그 힌지로 연결된 두 부품에서 같은 방향입니다. N→A의 공통축은 n₃=a₃, A→B의 공통축은 a₂=b₂, B→C의 공통축은 b₃=c₃입니다. 예컨대 B와 C의 세 번째 축이 같아도 원판이 자전하면 두 기저의 첫째 축은 달라집니다.')
add(9, '세 각도는 서로 다른 회전을 나타냅니다', 'Contents 1 08:50–11:10',
    'Generalized coordinate(일반화좌표)는 계의 자세를 정하는 독립 변수입니다. 여기서는 각도 세 개로 지정합니다. q₁은 수직 n₃ 주위로 바깥 고리가 도는 precession angle(세차각), q₂는 a₂ 주위로 기울여 수직축과 원판축 사이에 생기는 nutation angle(장동각), q₃는 b₃ 주위의 spin angle(자전각)입니다.',
    'q₂ 자체는 현재 기울기이고 q̇₂는 그 기울기가 변하는 빠르기입니다. q₂≠0인 채 q̇₂=0이면 기울어진 상태를 유지할 수 있습니다. 각도 위의 점 한 개는 시간에 대한 1차 미분, 두 개는 2차 미분입니다.')
add(10, '방향코사인 표에서 Z–Y–Z 회전 읽기', 'Contents 1 11:11–13:05',
    '각 표의 행은 바깥 기저의 단위축, 열은 안쪽 기저의 단위축입니다. 행 i와 열 j가 만나는 수는 두 단위축의 내적입니다. 열을 따라 읽으면 새 축 하나를 이전 기저의 성분으로 나타낼 수 있고, 행을 따라 읽으면 이전 축 하나를 새 기저로 표현할 수 있습니다.',
    '둘째 표의 셋째 행을 읽으면 a₃=−sin(q₂)b₁+cos(q₂)b₃입니다. 같은 표의 둘째 행이 (0,1,0)이므로 a₂=b₂입니다. 이 두 관계만으로 17장의 각속도 성분을 구할 수 있습니다.',
    eq='[v]<sub>N</sub> = Rz(q₁) Ry(q₂) Rz(q₃) [v]<sub>C</sub>',
    correction='둘째 표 아래의 “rotation about z axis”는 y axis(y축 회전)입니다. 강사가 12분대에 직접 정정하며, 표에서도 둘째 축만 그대로 남습니다.')
add(11, '세 개의 상대 각속도를 벡터로 더하기', 'Contents 1 13:05–15:24',
    '한 축으로만 도는 관절의 relative angular velocity(상대 각속도)는 각도의 시간 변화율에 그 관절의 단위축을 곱한 벡터입니다. N→A→B→C 경로를 순서대로 더하면 지면에서 본 회전체의 angular velocity(각속도)가 됩니다.',
    '세 항은 서로 다른 축을 따라갑니다. 아래 식 자체는 유효한 벡터 등식이지만, 행렬에 곱할 세 숫자를 얻으려면 선택한 기저 하나로 모든 항을 옮겨야 합니다.',
    eq='ω<sub>C/N</sub> = q̇₁ n₃ + q̇₂ a₂ + q̇₃ b₃')
add(12, '얇고 균질한 원판의 주관성모멘트', 'Contents 1 15:25–16:53',
    '원판의 질량을 m, 반지름을 r로 둡니다. 중심 G를 지나고 원판 면에 수직인 자전축 c₃에 대한 관성모멘트는 J=mr²/2입니다. 면 안에 놓인 두 지름축 c₁,c₂는 질량 분포의 회전대칭 때문에 같은 관성값 I를 갖습니다.',
    '얇은 평판의 perpendicular-axis theorem(수직축 정리)에 따라 J=I₁+I₂입니다. I₁=I₂이므로 I=J/2=mr²/4입니다. 다른 형상의 회전체에서는 주어진 관성값을 사용해야 합니다.',
    eq='[I<sub>G</sub>]<sub>C</sub> = diag(I,I,J),　I=mr²/4,　J=mr²/2　[kg·m²]')
add(13, '회전체 C에 붙은 축으로 각속도 성분 구하기', 'Contents 1 16:53–19:25',
    '계산을 따라가기 위해 P=q̇₁(세차율), U=q̇₂(장동률), S=q̇₃(상대 자전율), θ=q₂, ψ=q₃로 줄여 씁니다. n₃=a₃=−sinθ b₁+cosθ b₃와 a₂=b₂를 대입합니다. 그다음 b₁=cosψ c₁−sinψ c₂, b₂=sinψ c₁+cosψ c₂, b₃=c₃를 대입합니다.',
    'c₁에 붙는 두 항을 모으면 −P sinθ cosψ+U sinψ입니다. 나머지도 같은 방식으로 모읍니다. 마지막 성분에는 자전율 S와 세차율의 원판축 투영 P cosθ가 함께 들어갑니다.',
    eq='ω₁ᶜ = −P sinθ cosψ + U sinψ | ω₂ᶜ = P sinθ sinψ + U cosψ | ω₃ᶜ = P cosθ + S')
add(14, '각속도를 각운동량으로 바꾸는 행렬곱', 'Contents 1 19:25–21:50',
    'C축에서 원판의 inertia matrix(관성행렬)는 대각행렬입니다. 13장에서 구한 세 성분에 차례로 I,I,J를 곱합니다. 이것은 G에 대한 angular momentum(각운동량)이며 단위는 kg·m²/s입니다.',
    '강사가 설명한 표기상의 생략은 성분열과 벡터의 차이입니다. (Iω₁ᶜ,Iω₂ᶜ,Jω₃ᶜ)ᵀ는 C축에 대한 숫자 세 개이고, 실제 벡터를 쓰려면 각 숫자에 c₁,c₂,c₃를 붙여 더합니다.',
    eq='H<sub>G</sub> = Iω₁ᶜ c₁ + Iω₂ᶜ c₂ + Jω₃ᶜ c₃')
add(15, '회전체 축에서 오일러 방정식 쓰기', 'Contents 1 21:51–23:55',
    'Moment(모멘트)는 관성계 N에서 본 각운동량의 시간미분입니다. C에서 성분을 미분하면 축이 공간에서 돌아가는 효과가 빠집니다. Transport theorem(수송 정리)에 따라 ω<sub>C/N</sub>×H<sub>G</sub>를 더합니다. 원본의 긴 세 줄은 이 외적을 성분별로 전개한 결과입니다.',
    '예를 들어 c₁ 성분에서 외적은 ω₂ᶜJω₃ᶜ−ω₃ᶜIω₂ᶜ입니다. 따라서 아래처럼 계산하면 원본의 전개를 긴 삼각식부터 외우지 않고 복원할 수 있습니다. 성분 위 점은 C에서 본 숫자의 미분입니다.',
    eq='ΣM<sub>G</sub> = D<sub>C</sub>H<sub>G</sub> + ω<sub>C/N</sub> × H<sub>G</sub> | M₁ᶜ = Iω̇₁ᶜ+(J−I)ω₂ᶜω₃ᶜ | M₂ᶜ = Iω̇₂ᶜ+(I−J)ω₃ᶜω₁ᶜ,　M₃ᶜ = Jω̇₃ᶜ')
add(16, '같은 원판을 안쪽 짐벌 B에서 계산할 수 있는 이유', 'Contents 1 23:55–25:23',
    'B와 C는 자전축을 공유하고 면 안의 두 축만 서로 회전합니다. Axisymmetric rotor(축대칭 회전체)는 그 평면 안의 어느 지름에 대해서도 관성모멘트가 같습니다. 그래서 같은 G에 대해 B축에 쓴 관성행렬도 diag(I,I,J)입니다.',
    '편집자 보강 · 기저 회전 Q에 대해 [I<sub>G</sub>]<sub>B</sub>=Q[I<sub>G</sub>]<sub>C</sub>Qᵀ입니다. Q가 같은 관성값 I를 가진 두 축만 섞으면 값이 보존됩니다. 뒤의 곤돌라는 두 횡방향 관성이 달라서 같은 단축 계산을 그대로 적용할 수 없습니다.')
add(17, 'B축 각속도에서는 자전각 ψ가 사라집니다', 'Contents 1 25:24–26:25',
    'n₃를 B축에 투영하면 −sinθ b₁+cosθ b₃이고, 두 번째와 세 번째 관절의 축은 이미 b₂,b₃입니다. B에서 본 지면 기준 회전체 각속도 성분은 아래의 세 항입니다. 벡터의 관찰자는 여전히 N이고 B는 성분을 적은 기저입니다.',
    '식을 보면 자전각 ψ의 현재 값은 필요 없고 자전율 S는 남습니다. 자전하는 원판을 따라 돌지 않는 B축을 선택한 덕분입니다.',
    eq='[ω<sub>C/N</sub>]<sub>B</sub> = (−P sinθ, U, P cosθ + S)ᵀ | [ω<sub>B/N</sub>]<sub>B</sub> = (−P sinθ, U, P cosθ)ᵀ')
add(18, 'B축에서 각운동량을 나타내기', 'Contents 1 26:25–26:47',
    '17장의 ω<sub>C/N</sub> 성분에 I,I,J를 곱해 각운동량을 얻습니다. 원판의 자전율 S는 b₃ 성분에만 더해집니다. 회전체 H를 B축으로 표현한다고 해서 안쪽 짐벌 자체의 각운동량을 계산하는 것은 아닙니다.',
    eq='H<sub>G</sub> = −IP sinθ b₁ + IU b₂ + J(P cosθ + S)b₃',
    correction='원본 마지막 세 줄에는 c₁,c₂,c₃가 인쇄되어 있습니다. 바로 위 열벡터와 17·19장은 B기저로 계산하므로 단위축은 b₁,b₂,b₃입니다.')
add(19, '안쪽 짐벌의 각속도로 축의 회전을 보정하기', 'Contents 1 26:48–27:40',
    'B축으로 쓴 H를 미분할 때 수송항에 필요한 것은 그 축의 각속도 ω<sub>B/N</sub>입니다. 17장의 두 각속도를 비교하면 ω<sub>B/N</sub>에는 원판만의 자전 S가 없습니다. H 자체는 회전체의 전체 각속도로 구한 18장의 값을 사용합니다.',
    '예를 들어 셋째 성분 H₃=J(P cosθ+S)를 미분하면 J(Ṗ cosθ−PU sinθ+Ṡ)입니다. 셋째 방향 외적은 (−P sinθ)(IU)−U(−IP sinθ)=0입니다. 다른 두 성분에도 같은 연산을 하고 얇은 원판의 J=2I를 쓰면 다음과 같습니다.',
    eq='ΣM<sub>G</sub> = D<sub>B</sub>H<sub>G</sub> + ω<sub>B/N</sub> × H<sub>G</sub> | M₁ᴮ = I(2US−Ṗ sinθ) | M₂ᴮ = I(P² sinθ cosθ + 2PS sinθ + U̇) | M₃ᴮ = J(Ṗ cosθ − PU sinθ + Ṡ)')

add(20, 'Contents 2(본문 2) · 정상 세차와 그 응용', 'Contents 2 · 도입',
    '이제 임의의 운동을 기술하는 세 성분식에 steady precession(정상 세차)의 조건을 대입합니다.', role='Divider')
add(21, '정상 세차에서 일정한 것과 변하는 것', 'Contents 2 00:18–04:04',
    'Steady precession(정상 세차)은 원판의 자전축이 수직축과 일정한 기울기 θ를 유지하면서 일정한 세차율 P로 원뿔 면을 쓸고, 상대 자전율 S도 일정한 상태입니다. q₁과 q₃의 값은 계속 바뀔 수 있습니다. θ가 일정하기 때문에 장동률 U와 그 미분 U̇는 모두 0입니다.',
    '강사는 ΣF=m a<sub>G</sub>도 여전히 성립한다고 설명합니다. 이 모형에서 중심 G는 움직이지 않아 합력은 0입니다. 지지가 중량을 받는 경우처럼 개별 힘이 존재할 수 있으며, 필요한 회전 효과는 중심에 대한 합모멘트로 판단합니다.',
    eq='P=q̇₁=일정,　U=q̇₂=0,　S=q̇₃=일정 | Ṗ=q̈₁=0,　U̇=q̈₂=0,　Ṡ=q̈₃=0')
add(22, '일정한 세차율을 일반 모멘트 식에 대입하기', 'Contents 2 04:04–05:14',
    '19장의 M₁ᴮ에는 U와 Ṗ만 곱해져 있어 모든 항이 사라집니다. M₃ᴮ의 Ṗ, U, Ṡ도 모두 0입니다. M₂ᴮ에서는 장동 각가속도 U̇만 사라지고 세차와 자전의 곱 및 세차율 제곱 항은 남습니다.',
    '편집자 보강 · 같은 결과를 기하학적으로 얻을 수 있습니다. B에서 H의 성분이 일정하고 B는 Pn₃로 돕니다. 따라서 ΣM=P n₃×H입니다. 두 벡터가 b₁–b₃ 평면에 있어 외적은 b₂ 방향의 성분 하나만 가집니다.',
    eq='ΣM<sub>G</sub> = I(P² sinθ cosθ + 2PS sinθ)b₂')
add(23, '정상 세차에 필요한 모멘트의 크기와 방향', 'Contents 2 05:14–07:03',
    '외부 모멘트는 자전축 b₃와 수직 세차축 n₃가 만드는 평면에 수직입니다. M₂ᴮ는 방향을 포함한 성분입니다. 계산값이 음수면 실제 방향은 −b₂이고, 크기를 요구하면 절댓값을 씁니다.',
    '정상 세차에서도 모든 축의 모멘트가 0인 것은 아닙니다. 축이 원뿔을 따라 돌면서 H의 방향을 지속적으로 바꾸기 때문입니다. 반대로 θ=0이면 두 축이 나란해서 이 식의 세차 모멘트는 0입니다.',
    eq='M₁ᴮ=0,　M₂ᴮ=IP sinθ (P cosθ+2S),　M₃ᴮ=0')
add(24, '기울기를 유지할 모멘트를 작은 추로 만들기', 'Contents 2 07:03–08:14',
    'Spin rate(자전율) S와 nutation angle(장동각) θ를 준 상태에서 특정 precession rate(세차율) P를 원하면 23장의 식이 필요한 모멘트를 정합니다. 원본은 안쪽 고리 B의 D점에 작은 추를 달아 그 중력으로 모멘트를 만드는 방식을 제시합니다.',
    '추에 작용하는 힘은 수직 아래를 향합니다. 중심 O에서 D로 향하는 위치벡터 r<sub>OD</sub>와 무게 W를 외적해 모멘트 방향을 정합니다. 두 벡터가 n₃와 b₃의 평면에 있으면 외적은 그 평면에 수직입니다. 추의 질량과 지레팔이 주어졌을 때에만 구체적인 수치를 정할 수 있습니다.',
    eq='M<sub>O,weight</sub> = r<sub>OD</sub> × W,　|M| = (추의 무게) × (O에서 힘의 작용선까지 수직거리)')
add(25, '두 축이 직각이면 모멘트 식이 어떻게 줄어드나', 'Contents 2 08:15–12:11',
    'θ=90°에서는 sinθ=1, cosθ=0입니다. 따라서 외부 모멘트는 JPS b₂입니다. 회전체에 가하는 이 모멘트와 지지대가 받는 반작용 모멘트는 서로 반대입니다. 강의는 선박에서 회전체의 축 방향을 바꿔 동요를 억제하는 stabilizer(안정기)를 예로 듭니다.',
    '자전축과 세차축이 수직이면 두 각속도 벡터의 외적 크기는 주어진 두 속력에서 최대입니다. 일반 θ의 정확한 23장 식에는 P² sinθ cosθ 항도 있으므로, 그 전체 식의 최대라는 결론으로 확장할 수는 없습니다.',
    eq='θ=90°에서　ΣM<sub>G</sub> = JPS b₂ = J (P n₃) × (S b₃)',
    correction='자전거 사례에서 영상 11:40–12:11은 조향이 균형에 관여한다고 덧붙입니다. 바퀴의 자이로 효과 하나만으로 자전거의 균형을 설명하지 않습니다.')
add(26, '방향 계기는 회전체를 기준으로 기체의 회전을 읽습니다', 'Contents 2 12:11–13:50',
    'Directional gyroscope(방향 자이로)는 외부 모멘트가 작은 회전체의 각운동량 방향을 기준으로 사용합니다. 기체가 돌면 기체와 회전체 사이의 상대각이 바뀌므로 처음 맞춘 방향에서 얼마나 돌았는지 알 수 있습니다. 지자기를 이용하는 magnetic compass(자기 나침반)와 측정 원리가 다릅니다.',
    '기계 마찰이 작은 외부 모멘트를 계속 가하면 방향 오차가 누적됩니다. 이를 drift(표류 오차)라 부릅니다. 강의의 기계식 계기 예시는 기준 방향과 다시 맞춰 이 오차를 줄입니다. 원본의 10–15분은 해당 슬라이드가 든 예시 간격입니다.')
add(27, 'Problem Solving(문제풀이) · 비행 시뮬레이터', 'Problem Solving · 도입',
    '이제 원판 대신 서로 다른 세 주관성모멘트를 가진 gondola(탑승 곤돌라)의 회전과 베어링 반력을 계산합니다.', role='Divider')
add(28, '비행 시뮬레이터의 네 자유도와 관성 자료', 'Problem Solving 00:18–02:03',
    'Motion-based flight simulator(운동형 비행 시뮬레이터)는 탑승자가 공간 방향을 혼동하는 상황을 지상에서 재현합니다. 원본은 네 회전 자유도와 각 축의 400° 회전 범위를 설명합니다. 바닥의 planetary axis(공전축), 곤돌라 주변의 yaw(요), roll(롤), pitch(피치)를 그림에서 구별합니다.',
    '원문에서 주어진 주관성값은 Iₓ=400, Iᵧ=450, I<sub>z</sub>=900 kg·m²입니다. 37장 풀이에서는 곤돌라 고정축 (d₁,d₂,d₃) 순서에 (900,400,450)을 배정합니다. 아래의 수치 풀이는 그 배정을 따릅니다.',
    correction='28장의 문제문, 37장의 물체축 순서, 39장의 자유물체도에서 축 이름을 사용하는 방식이 다릅니다. 관성값은 37장의 d축 행렬, 지지력의 Aₓ·A<sub>z</sub> 등 첨자는 39–40장의 힘 표기로 읽어야 원본 풀이를 재현할 수 있습니다.')
add(29, '주어진 순간의 롤·피치 운동을 SI 단위로 바꾸기', 'Problem Solving 02:03–03:06',
    '롤 회전속력은 일정한 30 rpm입니다. 피치는 해당 순간 20 rpm이고, 피치 속력이 90°/s²의 비율로 증가합니다. “At the instant shown(그림에 보인 순간)”은 순간의 값이고, “increasing at a rate of(…의 비율로 증가하는)”는 그 순간 속력의 시간미분입니다.',
    '구할 것은 롤 짐벌 양쪽 지지점의 dynamic loads(동적 하중)입니다. 1회전은 2π rad, 1분은 60 s이며 각가속도를 바꿀 때는 각도 단위만 도에서 라디안으로 바꿉니다.',
    eq='q̇₃=30 × 2π/60=π rad/s,　q̈₃=0 | q̇₄=20 × 2π/60=2π/3 rad/s,　q̈₄=90 × π/180=π/2 rad/s²')
add(30, '풀이 순서 · 회전 상태에서 지지력까지', 'Problem Solving 03:05–03:30',
    '어느 부품이 어느 축을 따라 도는지 표시하고, 회전을 나타낼 좌표를 고릅니다. 회전율로부터 ω를 합성한 뒤 관성행렬과 같은 기저에서 H<sub>G</sub>를 구합니다. 그 관성계 미분이 곤돌라에 필요한 합모멘트입니다.',
    '합모멘트만으로는 양쪽 지지력 각각을 결정할 수 없습니다. 두 지지점의 간격을 넣은 모멘트 식과 질량중심에 대한 힘 식을 함께 사용합니다.')
add(31, '시뮬레이터의 기준계 N→A→B→C→D', 'Problem Solving 03:29–03:40',
    '지면은 N, 바닥 공전축을 따라 움직이는 큐브는 A, 요 운동부는 B, 롤 운동부는 C, 피치 운동을 하는 가장 안쪽 곤돌라는 D입니다. 앞 예제에서 C가 원판이었던 것과 달리 여기서는 D가 최종 계산 대상입니다.',
    '기준계는 한 부품에 타고 있는 관찰자라고 생각하면 편리합니다. C에 탄 관찰자는 곤돌라의 상대 피치만 보지만, 지면의 N에서는 C의 롤도 곤돌라 각속도에 들어갑니다.')
add(32, '그림에 물체축을 붙이는 방법', 'Problem Solving 03:39–04:11',
    'N,A,B,C,D에 각각 n,a,b,c,d로 시작하는 오른손 단위축을 붙입니다. 그림에서 기울어진 축이 겹쳐 보이면 부품 사이의 힌지 축을 먼저 찾습니다. 회전에 쓰는 축은 양쪽 기준계에 공통입니다.',
    '이 예제에서는 롤의 공통축이 b₂=c₂이고 피치의 공통축이 c₁=d₁입니다. 양의 회전 방향은 각 축의 화살표를 엄지 방향으로 한 오른손 규칙을 따릅니다.')
add(33, '네 일반화좌표와 물리적인 회전축 대응', 'Problem Solving 04:11–04:53',
    'q₁은 N→A 공전, q₂는 A→B 요, q₃는 B→C 롤, q₄는 C→D 피치입니다. 순서대로 국소 3축, 3축, 2축, 1축을 중심으로 돕니다. 기체 관례의 축 이름을 기억해 대입하기보다 이 그림이 정한 좌표 대응을 사용합니다.',
    'q₁과 q₂의 회전축 방향은 나란하지만 축선의 위치는 다릅니다. 따라서 각속도 기여는 더할 수 있어도, 중심의 병진가속도까지 항상 같다고 볼 수는 없습니다.')
add(34, '네 방향코사인 표의 곱', 'Problem Solving 04:53–05:09',
    '왼쪽 기저가 행, 오른쪽 기저가 열인 direction cosine matrix(방향코사인행렬)를 차례대로 만듭니다. D에서 쓴 벡터의 좌표를 N으로 보낼 때는 오른쪽에 D성분을 곱합니다. 반대 변환은 전체 곱의 전치입니다.',
    '실제로 한 공통축을 확인하면 부호를 점검할 수 있습니다. 마지막 Rx(q₄)는 첫째 축을 유지하고 c₂를 D축으로 쓰면 cos(q₄)d₂−sin(q₄)d₃입니다. 이 마이너스가 40장의 모멘트 계산에도 들어갑니다.',
    eq='[v]<sub>N</sub> = Rz(q₁) Rz(q₂) Ry(q₃) Rx(q₄) [v]<sub>D</sub>')
add(35, '곤돌라 전체의 각속도', 'Problem Solving 05:09–06:31',
    '서로 이어진 네 상대 각속도를 벡터로 합합니다. 공전과 요 성분은 n₃=a₃ 방향, 롤 성분은 b₂, 피치 성분은 c₁입니다. 순간적으로 앞의 두 회전율이 0이면 마지막 두 벡터만 남습니다.',
    '이 시점에서 q₄=0이라고 먼저 넣은 식을 시간 전체에 적용하면 안 됩니다. 피치 각속도가 0이 아니어서, 그 순간 양쪽 축이 겹쳐 있어도 다음 순간에는 축의 방향이 달라집니다.',
    eq='ω<sub>D/N</sub> = q̇₁n₃ + q̇₂a₃ + q̇₃b₂ + q̇₄c₁')
add(36, 'C축에서 짧은 식을 D축으로 옮기는 이유', 'Problem Solving 06:20–07:08',
    'K=q̇₁+q̇₂로 놓으면 C축 표현은 아래 첫 줄입니다. 이를 D축에 옮길 때 첫 성분은 그대로이고 나머지 두 성분은 q₄에 따라 섞입니다. 같은 물리 벡터를 다른 좌표축에 투영한 결과입니다.',
    '문제 조건 K=0이 계속 성립하는 구간에서는 [ω]<sub>D</sub>=(q̇₄, q̇₃ cos q₄, −q̇₃ sin q₄)ᵀ입니다. 마지막 성분은 q₄=0에서 0이지만 기울기, 즉 성분 시간미분은 일반적으로 0이 아닙니다.',
    eq='[ω]<sub>C</sub> = (q̇₄−K sin q₃, q̇₃, K cos q₃)ᵀ | ω₁ᴰ=q̇₄−K sin q₃ | ω₂ᴰ=q̇₃ cos q₄+K cos q₃ sin q₄ | ω₃ᴰ=−q̇₃ sin q₄+K cos q₃ cos q₄')
add(37, '곤돌라에서는 기저를 바꾸면 관성행렬도 바뀝니다', 'Problem Solving 07:08–08:27',
    '원본 풀이가 택한 곤돌라의 principal axes(관성주축) d₁,d₂,d₃에서는 관성행렬이 대각형입니다. 피치축 d₁과 수직한 두 방향의 관성값이 400과 450으로 다릅니다. 따라서 D가 C에 대해 피치 회전하면 일반적으로 C축 관성행렬에 비대각성분이 생깁니다.',
    '편집자 보강 · C축 표현으로 풀 때는 Q=Rx(q₄)로 [I]<sub>C</sub>=Q[I]<sub>D</sub>Qᵀ를 계산하고 그 시간 변화까지 반영합니다. 그림의 순간 q₄=0이라 두 행렬 값이 같더라도, 시간미분까지 같다는 뜻은 아닙니다.',
    eq='[I<sub>G</sub>]<sub>D</sub> = diag(900,400,450)　[kg·m²]')
add(38, '곤돌라의 각운동량과 그 시간 변화', 'Problem Solving 08:27–09:38',
    'D축 각운동량은 H₁=900ω₁, H₂=400ω₂, H₃=450ω₃입니다. 공전·요가 멈추고 롤·피치만 있는 경우 Pᵣ=q̇₃, Sₚ=q̇₄라 두겠습니다. 이때 H₃=−450Pᵣ sin q₄입니다.',
    'q₄=0인 순간 H₃=0이지만 그 미분은 −450PᵣSₚ입니다. 여기에는 cos(0)=1이 들어갑니다. 회전체 운동에서 한 순간 0이라는 정보와 시간에 걸쳐 항상 0이라는 조건을 구별해야 하는 예입니다.',
    eq='[H<sub>G</sub>]<sub>D</sub> = (900Sₚ, 400Pᵣ cos q₄, −450Pᵣ sin q₄)ᵀ　[kg·m²/s]')
add(39, '자유물체도 · 양쪽 베어링과 모터', 'Problem Solving 09:39–10:17',
    '그림의 roll gimbal(롤 짐벌) 양 끝에 왼쪽 지지점 A, 오른쪽 지지점 B가 있고 간격은 2.5 m입니다. 질량중심 G는 롤·피치 축의 교점이자 두 지지점의 가운데에 있습니다. G에서 A, B까지의 위치벡터는 각각 −1.25d₂, +1.25d₂ m입니다.',
    '원본 자유물체도는 양의 미지력 Aₓ,Bₓ를 d₁ 방향, A<sub>z</sub>,B<sub>z</sub>를 d₃ 방향으로 잡고, 구동 모멘트 Mᵧ를 d₂ 방향으로 둡니다. 계산값이 음수이면 실제 힘은 화살표 반대 방향입니다. 이 그림과 41장에서 구하는 것은 운동으로 추가되는 동적 하중입니다.')
add(40, '필요한 모멘트의 두 성분을 직접 계산하기', 'Problem Solving 10:17–12:42',
    '그림의 순간 q₄=0, Pᵣ=π, Sₚ=2π/3입니다. 따라서 [ω]<sub>D</sub>=(Sₚ,Pᵣ,0), [H]<sub>D</sub>=(900Sₚ,400Pᵣ,0)입니다. 먼저 38장의 시간에 따른 식을 미분합니다. 그 순간 D축 성분미분은 (900·π/2,0,−450PᵣSₚ)입니다.',
    '다음으로 ω×H를 구합니다. 셋째 성분은 Sₚ(400Pᵣ)−Pᵣ(900Sₚ)=−500PᵣSₚ입니다. 두 기여를 더하면 M₃=−950PᵣSₚ=−6250.75 N·m입니다. 첫째 성분은 피치 각가속도 때문에 450π=1413.72 N·m이고 둘째 성분은 0입니다.',
    '외력 쪽에서는 r<sub>GA</sub>×F<sub>A</sub>+r<sub>GB</sub>×F<sub>B</sub>에 모터의 우력을 더합니다. d₂×d₃=d₁, d₂×d₁=−d₃를 쓰면 아래와 같이 힘의 차이가 나타납니다.',
    eq='ΣM<sub>G</sub> = 1413.72d₁ − 6250.75d₃　[N·m] | ΣM<sub>G</sub> = 1.25(B<sub>z</sub>−A<sub>z</sub>)d₁ + Mᵧd₂ + 1.25(Aₓ−Bₓ)d₃')
add(41, '힘의 합은 0인데 베어링 하중이 남는 이유', 'Problem Solving 12:42–13:05',
    '공전과 요 운동이 없고 G가 롤·피치 축 교점에 있으므로 이 예제에서 a<sub>G</sub>=0입니다. Newton’s second law(뉴턴의 제2법칙)를 두 방향에 적용하면 각 베어링의 동적 하중이 서로 상쇄됩니다.',
    '작용점 A와 B가 떨어져 있기 때문에 크기가 같고 반대 방향인 두 힘은 couple(우력)을 만들 수 있습니다. 무게까지 포함한 실제 총 지지반력이 필요하면 정적 지지하중을 별도로 더해야 합니다. 질량 자료 없이 그 값을 정할 수 없습니다.',
    eq='Aₓ+Bₓ=0,　A<sub>z</sub>+B<sub>z</sub>=0')
add(42, '다섯 식으로 네 반력 성분과 구동 모멘트 구하기', 'Problem Solving 13:05–13:31',
    '힘 식에서 Aₓ=−Bₓ, A<sub>z</sub>=−B<sub>z</sub>입니다. 첫째 축 모멘트 1.25(B<sub>z</sub>−A<sub>z</sub>)=1413.72에 대입하면 2.5B<sub>z</sub>=1413.72입니다. 셋째 축에서는 1.25(Aₓ−Bₓ)=−6250.75이므로 2.5Aₓ=−6250.75입니다. 둘째 축 모멘트 식에서 Mᵧ=0입니다.',
    '따라서 A가 곤돌라에 가하는 동적 힘은 −d₁, −d₃ 방향이고 B는 정반대입니다. 장치가 각 베어링에 가하는 힘을 묻는 경우 작용·반작용으로 이 방향들을 뒤집습니다. 모터의 롤축 모멘트가 0이어도 베어링은 큰 우력을 전달합니다.',
    eq='Aₓ=−2500.30 N,　Bₓ=+2500.30 N | A<sub>z</sub>=−565.49 N,　B<sub>z</sub>=+565.49 N,　Mᵧ=0 N·m')
add(43, '여러 축이 도는 장치에서 베어링이 받는 동적 하중', 'Problem Solving 13:31–14:34',
    'Dynamic load(동적 하중)는 운동을 만들거나 유지하는 과정에서 지지부에 생기는 하중입니다. 이 예제는 곤돌라 중심이 정지해 있어도 여러 축의 회전이 결합해 두 지지점에 반대 방향의 힘이 생김을 보여줍니다.',
    'Products of inertia(관성곱)가 있는 축에서 한 방향으로 회전하면 각운동량에 다른 방향 성분도 나타날 수 있습니다. 주축에서 계산해 행렬을 대각화해도 ω×H는 남을 수 있으므로, 모터 토크를 평가할 때 회전 결합을 함께 확인합니다.')
add(44, '공전축까지 움직이면 다시 계산할 값', 'Problem Solving 14:34–15:28',
    '그림에서 곤돌라의 중심 G는 바닥 공전축에서 떨어져 있습니다. 여기에 공전을 추가하면 G가 원호를 따라 이동하고 a<sub>G</sub>가 생길 수 있습니다. 이때 41장의 반력끼리 상쇄시키는 식을 ΣF=m a<sub>G</sub>로 다시 세우고, 새 ω와 H의 변화율로 모멘트 식도 다시 계산합니다.',
    'Machine balancing(기계 밸런싱)은 질량중심을 적절한 회전축에 맞추고 질량 분포의 비대칭을 줄여 불필요한 베어링 하중을 줄이는 과정입니다. 영상의 바퀴 밸런싱 예시는 질량 배치가 달라지면 같은 회전속력에서 지지점의 하중이 달라진다는 뜻입니다.')
add(45, '원본 참고문헌', '원본 참고문헌 슬라이드',
    'Beer, Johnston, Cornwell, Self, Sanghi, <i>Vector Mechanics for Engineers: Dynamics</i>, 제12판, 18장.', role='References')

summary = ''.join([
    card('1. 팽이는 중력이 작용하는 동안에도 축을 기울인 채 돌 수 있습니다.',
         'Spin(자전)은 회전체가 자기 축을 도는 운동입니다. Precession(세차)은 그 축의 방향 자체가 수직축 주위를 도는 운동이고, nutation(장동)은 두 축 사이 기울기가 변하는 운동입니다. 기울어진 팽이의 중심을 지나는 무게는 바닥 접점에 대한 모멘트를 만듭니다. 중심이 고정된 강의의 짐벌 모형에서는 중심에 대한 외부 모멘트가 같은 역할을 합니다.',
         '회전 운동의 법칙은 ΣM=D<sub>N</sub>H입니다. 모멘트가 H에 수직이면 짧은 시간 동안 각운동량의 끝이 옆으로 움직입니다. 그 결과 H의 크기가 같아도 방향은 달라집니다. 편집자 보강 · 빠른 자전이 지배적이면 H는 원판축과 거의 나란하고 크기는 대략 J|S|입니다. 같은 수직 모멘트에서 |ΔH|≈|M|Δt이므로, H가 클수록 같은 시간 동안 방향이 변하는 각도는 작습니다.', kind='callout'),
    card('2. 각속도는 어느 축을 따라 도는지 표시한 뒤 더합니다.',
         '지면 N, 바깥 짐벌 A, 안쪽 짐벌 B, 원판 C를 순서대로 놓습니다. 회전축은 n₃=a₃, a₂=b₂, b₃=c₃입니다. P=q̇₁은 세차율, U=q̇₂는 기울기 변화율, S=q̇₃는 상대 자전율이고 θ=q₂입니다. 원판의 전체 각속도는 Pn₃+Ua₂+Sb₃입니다.',
         '안쪽 짐벌 B의 축으로 옮기면 n₃=−sinθ b₁+cosθ b₃입니다. 그래서 원판축을 따른 전체 각속도에는 자전에 세차의 투영도 더해집니다. 얇고 균질한 원판에서는 I=mr²/4가 지름축 관성이고 J=mr²/2가 원판축 관성입니다.',
         formula('[ω]<sub>B</sub>=(−P sinθ, U, P cosθ+S)ᵀ　　 [H<sub>G</sub>]<sub>B</sub>=(−IP sinθ, IU, J(P cosθ+S))ᵀ')),
    card('3. 모멘트를 구할 때는 성분을 적은 축이 도는 효과까지 더합니다.',
         'H<sub>G</sub>에는 원판의 전체 각속도를 씁니다. 그 H를 B축에서 미분할 때는 B축의 회전속도 ω<sub>B/N</sub>=Pn₃+Ub₂를 사용합니다. ΣM=D<sub>B</sub>H+ω<sub>B/N</sub>×H에서 첫 항은 B에서 본 세 숫자의 변화, 둘째 항은 기저가 회전해 생긴 변화입니다.',
         '정상 세차에서는 P,S,θ가 일정하고 U=0입니다. H의 B성분이 일정하므로 첫 항은 0이고 둘째 항이 남습니다. 필요한 외부 모멘트는 n₃와 b₃가 이루는 평면에 수직인 b₂ 방향이며 아래 식이 크기와 부호를 정합니다.',
         formula('M₁ᴮ=M₃ᴮ=0,　M₂ᴮ=I P² sinθ cosθ + J P S sinθ　　 (얇은 원판 J=2I)'),
         '두 축이 직각이면 M₂ᴮ=JPS입니다. 선박의 안정기는 회전체에 가하는 모멘트의 반작용을 활용합니다. 방향 자이로는 공간에서 천천히 변하는 축을 기준으로 기체의 상대 방향을 읽으며, 마찰로 인한 drift(표류 오차)는 기준을 다시 맞춰 줄입니다.'),
    card('4. 원판에서 되던 기저 선택이 곤돌라에서 그대로 통하지 않는 이유',
         '원판은 자전축에 수직한 두 관성값이 같으므로 B와 C축에서 같은 대각 관성행렬을 쓸 수 있습니다. 비행 시뮬레이터의 곤돌라는 물체축 D에서 diag(900,400,450) kg·m²입니다. 피치 회전이 서로 다른 400과 450의 축을 섞으므로, D축에서 ω와 H를 모두 계산하는 편이 간단합니다.',
         '주어진 순간 롤은 π rad/s로 일정하고 피치는 2π/3 rad/s에서 π/2 rad/s²로 빨라집니다. 피치각이 0이라 d₃ 속도 성분은 0이지만, 그 미분에는 롤축과 피치축의 결합이 남습니다. 각운동량 성분의 미분과 ω×H를 합하면 필요한 모멘트는 1413.72d₁−6250.75d₃ N·m입니다.'),
    card('5. 중심이 정지해도 베어링의 힘은 클 수 있습니다.',
         'G는 두 지지점 중앙에서 움직이지 않아 양쪽 동적 반력의 합은 0입니다. 반면 두 지지점 사이에는 2.5 m의 간격이 있으므로 반대 방향의 두 힘이 우력을 만듭니다. 각 모멘트를 두 지지점 사이 거리로 나누면 성분별 힘의 크기를 구할 수 있습니다.',
         '원본 자유물체도 기준 왼쪽 A의 동적 힘은 d₁ 방향 −2500.30 N, d₃ 방향 −565.49 N이고 오른쪽 B는 각각 반대입니다. 롤축의 구동 모멘트는 이 순간 0 N·m입니다. <a href="#slide-39">자유물체도</a>와 <a href="#slide-40">모멘트 계산</a>에서 축과 부호를 따라갈 수 있습니다.'),
])

exams = [
    ('Distinguish spin, precession, and nutation.',
     'Spin is the relative rotation of the rotor about its symmetry axis. Precession is the sweep of that axis about the vertical axis. Nutation changes the inclination between the two axes.',
     'Spin(자전), precession(세차), nutation(장동)을 설명할 때 어느 축이 회전하는지와 inclination(기울기)이 변하는지를 명시합니다.'),
    ('Why can the disk inertia matrix be used in the inner-gimbal frame?',
     'The disk is axisymmetric. Its two transverse principal moments are equal, and the two frames share the spin axis. A rotation of the transverse axes therefore leaves the inertia matrix unchanged.',
     'Axisymmetric(축대칭인)이라는 조건과 transverse principal moments(횡방향 주관성모멘트) 두 개가 같다는 사실을 연결합니다.'),
    ('Which angular velocity appears in the transport term if the momentum is expressed in frame B?',
     'Use the angular velocity of frame B relative to the inertial frame. The momentum being differentiated is still the angular momentum of the rotor.',
     'Transport term(수송항)에는 미분에 사용한 기저 B의 각속도, H에는 회전체 C의 전체 각속도를 씁니다.'),
    ('State the conditions for steady precession and identify the required moment direction.',
     'The precession rate and the relative spin rate are constant, and the nutation angle is fixed. For the disk in the lecture the required moment has only a component along the second inner-gimbal axis.',
     'Fixed inclination(고정된 기울기)은 기울기 값이 0이라는 뜻이 아닙니다. 이 조건에서 M₂ᴮ 한 성분이 남습니다.'),
    ('Determine the applied moment when the spin and precession axes are perpendicular.',
     'For the uniform disk undergoing steady precession, the applied moment is the axial moment of inertia times the cross product of the precession and relative spin angular velocities.',
     'Perpendicular(수직인) 조건에서 cosθ=0, sinθ=1입니다. 외적은 세차 각속도부터 자전 각속도 순서로 취합니다.'),
    ('Why is periodic realignment discussed for a mechanical directional gyroscope?',
     'Small frictional torques cause the reference direction to drift over time. Realignment restores the heading reference.',
     'Frictional torque(마찰 토크)가 누적된 drift(표류 오차)를 일으킨다는 인과관계를 씁니다.'),
    ('Why can the bearings carry dynamic loads when the center of mass has zero acceleration?',
     'The resultant dynamic force is zero. Equal and opposite bearing forces separated by a distance can still provide the couple required to change the angular momentum.',
     'Resultant force(합력)와 couple(우력)을 구분합니다. 두 힘이 어디에 작용하는지를 쓰면 모멘트가 남는 이유를 설명할 수 있습니다.'),
    ('Determine the bearing reactions and the roll motor moment at the instant shown.',
     'In the coordinates of the free-body diagram, the x and z components at A are approximately minus 2500.30 N and minus 565.49 N. The corresponding components at B have the opposite signs. The roll motor moment is zero.',
     'At the instant shown(그림에 보인 순간)과 dynamic reactions(동적 반력)이라는 조건을 유지합니다. 베어링이 물체에 가하는 힘의 방향을 기준으로 적었습니다.'),
]

glossary = [
    ('gyroscope(자이로스코프) / rotor(회전체)', '빠르게 회전하는 물체의 각운동량을 이용하는 장치 / 내부에서 자전하는 물체'),
    ('outer gimbal(바깥 짐벌) / inner gimbal(안쪽 짐벌)', '회전체가 여러 축으로 회전하도록 차례로 지지하는 회전 고리'),
    ('spin rate(자전율) / precession rate(세차율)', '내부 원판의 상대 자전 각속도 / 원판축이 수직축 주위를 도는 각속도'),
    ('nutation angle(장동각) / fixed inclination(고정된 기울기)', '세차축과 원판축이 이루는 각도 / 그 각도가 시간에 따라 일정한 상태'),
    ('steady precession(정상 세차)', '강의 모형에서 세차율과 자전율이 일정하고 장동각이 유지되는 운동'),
    ('generalized coordinate(일반화좌표) / degree of freedom(자유도)', '계의 자세를 정하는 변수 / 독립적으로 움직일 수 있는 운동의 수'),
    ('inertial frame(관성 기준계) / body-fixed frame(물체 고정 기준계)', '뉴턴–오일러 식의 관찰 기준계 / 물체와 함께 움직이는 관찰 기준계'),
    ('direction cosine(방향코사인) / aligned(정렬된)', '두 단위축 사이 각도의 코사인 / 기준으로 삼은 축 방향이 일치하는 상태'),
    ('axisymmetric(축대칭인) / transverse(횡방향의)', '어떤 축 주위로 질량 분포가 회전대칭인 / 그 축에 수직한 방향의'),
    ('principal moment of inertia(주관성모멘트) / product of inertia(관성곱)', '관성주축 주위의 질량관성모멘트 / 좌표 두 개의 곱을 질량에 대해 적분한 값'),
    ('angular momentum(각운동량) / torque(토크)', '회전 운동의 상태량 H / 지정한 점에 대한 H의 관성계 변화율과 연결되는 힘의 회전 효과'),
    ('drift(표류 오차) / realignment(재정렬)', '기준 방향의 누적 편차 / 외부 기준과 계기 방향을 다시 맞추는 일'),
    ('gondola(탑승 곤돌라) / bearing reaction(베어링 반력)', '시뮬레이터의 탑승부 / 베어링이 물체에 가하는 지지력'),
    ('roll(롤) / pitch(피치) / yaw(요)', '시뮬레이터의 세 회전 자유도. 실제 대입할 축은 각 장치의 그림과 표로 정합니다.'),
    ('dynamic load(동적 하중) / couple(우력)', '운동 때문에 추가되는 하중 / 떨어진 두 점에 작용하는 크기가 같고 반대 방향인 힘의 쌍'),
    ('at the instant shown(그림에 보인 순간) / increasing at a rate of(…의 비율로 증가하는)', '현재 값의 평가 시점 / 해당 값의 시간 변화율을 지정하는 문제 표현'),
    ('determine(구하라) / perpendicular to(…에 수직인)', '요구된 미지량을 계산하라는 지시 / 두 축이 90°를 이룬다는 조건'),
]

audit = [
    ('Contents 1 01:43–02:01 · 6장', 'router', '그림 안에서 자전하는 rotor(회전체)입니다.'),
    ('Contents 1 05:13 · 8장', 'right hand row', '서로 수직인 세 축의 방향을 정하는 right-hand rule(오른손 규칙)입니다.'),
    ('Contents 1 12:02–12:27 · 10장', '둘째 표의 z axis', '표의 불변축과 강사의 직접 정정에 따라 q₂는 y회전입니다.'),
    ('Contents 1 19:45–20:07 · 14장', 'moment of inertia → angular momentum', '행렬 I에 ω를 곱한 결과 H를 지칭하며 영상도 이 용어로 정정합니다.'),
    ('Contents 1 26:25–27:10 · 18장', 'B축 성분에 c단위벡터', '17장의 성분을 대입하고 19장에서 B기준 미분을 하므로 b단위벡터를 붙입니다.'),
    ('Contents 2 03:41–04:04 · 21장', '중앙의 q̇₂=0 반복', '기울기가 일정하게 유지되는 구간에서는 q̈₂=0도 성립해 22장에서 사용할 수 있습니다.'),
    ('Contents 2 07:15 · 24장', 'new mutation angle', '두 축이 이루는 nutation angle(장동각) q₂입니다.'),
    ('Contents 2 09:25–10:03 · 25장', '직각에서 최대', '두 벡터의 크기를 고정했을 때 외적의 크기가 최대라는 의미로 적용합니다.'),
    ('Contents 2 11:40–12:11 · 25장', '자전거 균형', '강사의 조향 설명까지 반영해 바퀴의 자이로 효과와 구별합니다.'),
    ('Problem Solving 01:08–02:12 · 28–29장', 'your / raw / role', '그림의 yaw(요), roll(롤) 및 roll gimbals(롤 짐벌)로 읽습니다.'),
    ('28·37·39–40장', '축 이름과 관성값 순서', '수치 계산에는 원본의 D축 대각행렬과 자유물체도에서 명시한 반력 방향을 사용합니다.'),
    ('Problem Solving 09:40–10:00 · 39장', 'Free by diagram', '힘과 우력의 작용점을 표시하는 free-body diagram(자유물체도)입니다.'),
    ('Problem Solving 13:56–14:22 · 43장', 'octagonal terms / Product of the energy', '관성행렬의 off-diagonal terms(비대각성분) 및 products of inertia(관성곱)를 뜻합니다.'),
]
roadmap = '''<section class="editorial-section section-divider" id="course-roadmap" aria-labelledby="roadmap-title">
<p class="section-kicker">Summary video · Course closing</p>
<h2 class="section-title" id="roadmap-title">Summary 영상 후반 · 녹화 강좌의 맺음말</h2>
<p class="section-lead">00:17–00:43의 세차·안정기·방향 계기 복습은 핵심 개념 요약에 반영했습니다. 00:47부터는 녹화 강좌를 마치는 인사입니다.</p></section>
<section class="editorial-section" id="roadmap-detail" aria-labelledby="roadmap-detail-title">
<p class="section-kicker">Course closing</p><h2 class="section-title" id="roadmap-detail-title">입자와 강체의 역학을 공학 문제에 적용하기</h2>
<div class="card"><p>강사는 입자와 강체의 운동학·운동역학이 여러 공학 분야의 기초가 된다고 설명하며 녹화 과정을 마무리합니다. 이번 학기 강의 인덱스에서는 이 영상을 포함한 렉쳐 16을 12주차 추가 강의로 분류하며 별도 날짜는 미기재입니다.</p></div></section>'''

def fill(template, values):
    return re.sub(r'\{\{([^{}]+)\}\}', lambda match: values[match[1]], template)


def build():
    template = (SITE / 'templates/lecture-page.template.html').read_text(encoding='utf-8')
    template = re.sub(r'\s*<!--[\s\S]*?-->', '', template)
    slide = re.search(r'<section class="source-section"[\s\S]*?</section>', template).group()
    assert len(slides) == 45
    sections = []
    for number, (title, evidence, blocks, role) in enumerate(slides, 1):
        sections.append(fill(slide, dict(
            NN=f'{number:02d}', SLIDE_ROLE=role, SLIDE_HEADING=title,
            LECTURE_SLUG='lecture16', DESCRIPTIVE_ALT_TEXT=escape(f'Lecture 16 원본 {number}장 · {title}'),
            CURRENT_PAGE=str(number), PAGE_COUNT='45', TRANSCRIPT_TIME_OR_SLIDE_ROLE=evidence,
            SLIDE_EXPLANATION_BLOCKS=blocks,
        )))
    template = template.replace(slide, '\n\n'.join(sections))
    exam = re.search(r'<div class="exam-card">[\s\S]*?</p>\s*</div>', template).group()
    template = template.replace(exam, '\n'.join(fill(exam, dict(
        EXAM_QUESTION=q, MODEL_ANSWER=escape(a), KOREAN_ANSWER_EXPLANATION=ko,
    )) for q, a, ko in exams))
    toc = [('overview', '전체 개요'), ('concept-map', '개념 지도'), ('concept-summary', '핵심 개념 요약')]
    toc += [(f'slide-{i:02d}', f'{i:02d} · {row[0]}') for i, row in enumerate(slides, 1)]
    toc += [('course-roadmap', 'Summary · 종강 인사'), ('exam-english', '시험 영어'),
            ('glossary', '용어집'), ('asr-log', '원본·자막 교정'), ('sources', '출처 및 강의 영상')]
    pdf = 'https://github.com/leejinh0225/MC2103-Dynamics/raw/refs/heads/main/2026FA_Dynamics/lecture_notes/lecture16_note.pdf'
    sources = '<ul class="plain-list"><li><a href="' + pdf + '">Lecture 16 원본 PDF</a> · 12주차 추가 강의 · 날짜 미기재 · 45장</li>'
    for label, vid in VIDEOS:
        sources += f'<li><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상</a> · 영어 자동생성 자막 원문</li>'
    sources += '</ul><p>강의 인덱스에 등록된 5편의 영어 자동생성 자막 원문을 2026-11-21에 확보해 45장과 대조했습니다. 슬라이드 아래의 시간은 관련 설명 구간입니다. 3장의 보조 영상은 원본 링크를 실었으며, 45장의 교재는 강의가 제시한 참고문헌입니다.</p>'
    sources += '<p>성분 변환의 중간식, 모멘트 외적 전개와 수치 검산은 강의의 계산을 따라가기 위한 시험용 보강입니다. 이 강의에 쓰인 운동량·관성행렬의 기초는 <a href="lecture12.html#concept-summary">렉쳐 12 핵심 개념 요약</a>에 정리되어 있습니다.</p>'
    template = template.replace('날짜 {{DATE_OR_날짜_미기재}}', '{{DATE_OR_날짜_미기재}}')
    template = fill(template, dict(
        LECTURE_NUMBER='Lecture 16', LECTURE_TITLE='Gyroscopic Motions',
        ONE_SENTENCE_DESCRIPTION='자이로스코프의 자전·세차·장동, 회전 기저의 각운동량과 비행 시뮬레이터 베어링 하중을 다루는 12주차 추가 강의',
        WEEK='Week 12 추가 강의', DATE_OR_날짜_미기재='날짜 미기재', PAGE_COUNT='45',
        LECTURE_PROMISE='팽이의 기울어진 축이 도는 이유를 각운동량의 변화로 설명합니다. 원판과 짐벌에 붙인 두 좌표계에서 같은 모멘트를 구하고, 비행 시뮬레이터의 롤·피치 운동으로부터 양쪽 베어링에 걸리는 하중을 계산합니다.',
        VIDEO_SET='Overview · Contents 1·2 · Problem Solving · Summary',
        ALL_CONTENTS_AND_PROBLEM_SOLVING_BUTTONS='\n'.join(
            f'<a class="button button--primary" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{name} 영상 열기</a>'
            for name, vid in VIDEOS[1:4]),
        ORIGINAL_PDF_URL=pdf, LECTURE_NOTE_FILENAME='lecture16_note.pdf',
        CORE_RELATIONSHIP_HEADLINE='기울어진 팽이의 축은 왜 옆으로 돌까요?',
        CORE_RELATIONSHIP_EXPLANATION='팽이의 접점에 대해 중력이 만드는 모멘트는 각운동량의 방향을 바꿉니다. 회전체를 고리에 지지한 자이로스코프에서도, 일정한 속력으로 도는 회전체의 축을 다른 방향으로 돌리려면 모멘트가 필요합니다. 이 모멘트가 어떤 방향을 향하는지부터 살펴봅니다.',
        CONCEPT_MAP_HEADLINE='회전축 정하기 → 각운동량 미분하기 → 지지력 구하기',
        CONCEPT_MAP_BLOCKS='<div class="grid-3">' +
            card('세 회전 · Spin, precession, nutation','자전은 원판 자체의 회전, 세차는 축이 수직 방향 주위를 도는 운동, 장동은 축의 기울기가 변하는 운동입니다.') +
            card('회전 기준계 · Rotating frame','회전체의 H를 짐벌축 또는 물체축의 성분으로 적습니다. 그 성분의 변화와 기저의 회전을 함께 계산하면 실제 모멘트를 얻습니다.') +
            card('베어링 하중 · Bearing loads','각운동량의 방향이 바뀌는 데 필요한 모멘트는 서로 떨어진 두 베어링의 힘으로도 만들어집니다.') + '</div>',
        STANDALONE_CONCEPT_SUMMARY=summary, DISTINCT_SUMMARY_VIDEO_SECTION_IF_NEEDED=roadmap,
        EXAM_SECTION_TITLE='세차의 조건과 베어링 하중을 설명하는 영어 답안',
        BILINGUAL_GLOSSARY_TABLE=table(['영어(한국어)', '뜻과 쓰임'], glossary),
        AUDIT_SECTION_TITLE='원본 슬라이드와 영어 자막의 축·용어 교정',
        ASR_CORRECTION_TABLE=table(['위치', '원문 또는 쟁점', '채택한 해석과 근거'], audit),
        SOURCE_LIST_AND_PROVENANCE_NOTE=sources,
        TABLE_OF_CONTENTS_LINKS=''.join(f'<li><a href="#{key}">{label}</a></li>' for key, label in toc),
    ))
    template = template.replace('이 부분만 읽어도 렉처의 핵심 정의, 개념 관계, 가정과 풀이 흐름을 이해할 수 있도록 작성합니다.',
                                '팽이의 축이 도는 이유부터 비행 시뮬레이터의 양쪽 지지력까지, 같은 각운동량 법칙으로 연결합니다.')
    (SITE / 'lecture16.html').write_text(template, encoding='utf-8')


if __name__ == '__main__':
    build()
