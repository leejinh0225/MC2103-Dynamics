"""Build Lecture 9 from the shared Lecture 1 HTML template and reviewed source material."""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
videos = [('Overview', '7eQKoc8KhL4'), ('Contents 1', 'c18PFwr6QPA'),
          ('Contents 2', 'JChKRZ1SMhk'), ('Problem Solving', 'FpJjwilEOMM'), ('Summary', 'f_lQxmcZCdc')]
records = []


def fmt(s):
    # D_N etc. are convenient source aliases; the page uses actual subscripts/superscripts.
    s = re.sub(r'D_([NABC])', r'D<sub>\1</sub>', s)
    s = re.sub(r'([NABC])\|([vaω])\|([PAB])', r'<sup>\1</sup>\2<sup>\3</sup>', s)
    return s


def p(s):
    return '<p>' + fmt(s) + '</p>'


def card(title, *body, kind='card'):
    return f'<div class="{kind}"><h3>{fmt(title)}</h3>' + ''.join(map(p, body)) + '</div>'


def table(headers, rows):
    def cells(values, tag):
        return ''.join(f'<{tag}>{fmt(v)}</{tag}>' for v in values)
    return '<table class="term-table"><thead><tr>' + cells(headers, 'th') + '</tr></thead><tbody>' + ''.join(
        '<tr>' + cells(row, 'td') + '</tr>' for row in rows) + '</tbody></table>'


def add(n, title, evidence, *body, eq='', correction='', extra='', role='Concept'):
    assert n == len(records) + 1
    blocks = card('원본 교정 · 적용 조건', correction, kind='callout') if correction else ''
    blocks += card('핵심 해설' if role == 'Concept' else '슬라이드 안내', *body,
                   kind='card' if role == 'Concept' else 'quiet-card')
    if eq:
        blocks += card('식과 기호', '<span class="formula">' + eq + '</span>')
    records.append((title, evidence, blocks + extra, role))


summary = ''.join([
    card('1. 누가 보고, 어느 축으로 쓰며, 어떤 수로 정하는가',
         '기차 안의 사람이 의자에 붙은 점을 보면 그 점은 정지해 있지만, 지상에서는 움직입니다. Reference frame(기준계)은 이렇게 무엇과 함께 운동하는 관찰자인지를 정합니다. Coordinate system(좌표계)은 원점과 성분을 재는 축을 정합니다. Coordinate(좌표)는 그 약속으로 읽은 수입니다. 한 기준계 안에서도 축을 여러 방식으로 정할 수 있습니다.',
         '예를 들어 같은 원점에서 오른쪽을 가리키는 1 m짜리 화살표는 어떤 축에서는 (1, 0), 90° 돌아간 축에서는 (0, −1)입니다. 축만 바꾸면 숫자만 달라집니다. 반면 지상에서 보던 점을 회전하는 물체에 탄 사람이 관찰하면 velocity(속도) 자체가 달라질 수 있습니다. 이 구분이 강의 전체의 출발점입니다.', kind='callout'),
    card('2. 관성 기준계는 그 안의 물체가 모두 정지한 곳이 아닙니다.',
         'Inertial frame(관성 기준계)에서는 외력 합이 0인 자유입자가 일정한 속도로 움직이며, 추가 보정 없이 ΣF=ma를 적용합니다. 다른 관성 기준계에 대해 회전하지 않고 일정한 속도로 병진하는 기준계도 관성 기준계입니다. Body frame(물체 기준계)은 물체와 함께 움직이므로 관성 기준계라는 보장이 없습니다.',
         'Overview의 Foucault pendulum(푸코 진자)은 지구와 함께 도는 관찰자에게 진동면의 방향이 변해 보이는 사례입니다. 지구를 관성 기준계로 근사해도 되는지는 다루는 운동에서 지구 자전의 영향이 작으냐에 달려 있습니다. 아래 짧은 진자·슬라이더 예제에서는 지면을 관성 기준계 N으로 둡니다.'),
    card('3. 성분이 두 개 있어도 자유도는 하나일 수 있습니다.',
         'Degree of freedom(자유도)은 configuration(계의 배치)을 정하는 데 필요한 독립적인 스칼라 수입니다. 길이 L이 고정된 평면 진자의 끝은 원 위에 있으므로 x²+y²=L²입니다. 아래쪽 수직선에서 잰 각 θ 하나만 정하면 x=L sinθ, y=−L cosθ입니다. 좌표 x와 y는 둘이지만 독립적으로 정할 수 없습니다.',
         'θ는 하나의 generalized coordinate(일반화좌표)이고 L은 값이 변하지 않는 매개변수입니다. 3차원 원뿔처럼 실제 물체의 여러 회전이 겹치면 virtual reference frame(가상 기준계)을 세워 일부 회전만 따라갈 수 있습니다. 이때 어느 축이 물체에 고정되고 어느 축이 분석을 위해 선택되었는지 먼저 표시합니다.'),
    card('4. 벡터를 미분할 때는 성분과 축을 함께 봅니다.',
         'D_A는 “기준계 A에서 본 시간미분”을 뜻합니다. 기저 a₁, a₂, a₃가 A에 고정되어 있고 p=Σpᵢaᵢ라면 D_A p=Σṗᵢaᵢ입니다. A에서는 축이 변하지 않기 때문입니다. 다른 기준계 N에서 같은 식을 미분하면 D_N p=Σ(ṗᵢaᵢ+pᵢD_N aᵢ)입니다. A가 N에 대해 회전하면 뒤 항을 버릴 수 없습니다.',
         '따라서 “A축으로 썼다”는 말은 미분을 A에서 했다는 뜻이 아닙니다. 문제에서 observed in N(N에서 관찰한)이라고 하면 N을 유지한 채 가장 편한 축을 씁니다. 점 P의 velocity(속도)와 acceleration(가속도)는 N에 고정된 원점 O에서 잰 p=OP에 대해 N|v|P=D_N p, N|a|P=D_N(N|v|P)입니다.'),
    card('5. 진자: 같은 위치벡터를 봐도 두 관찰자의 속도는 다릅니다.',
         '진자의 pivot(회전 지지점) O를 두 기준계의 공통 원점으로 두고, 지면의 축 n₁은 오른쪽, n₂는 위쪽으로 잡습니다. 막대에 고정된 a₂는 끝점 P에서 O 쪽, a₁은 θ가 증가하는 접선 방향입니다. 그러면 p=L sinθ n₁−L cosθ n₂=−L a₂입니다. 두 식은 같은 순간 같은 화살표입니다.',
         '지면에서 미분하면 N|v|P=Lθ̇(cosθ n₁+sinθ n₂)=Lθ̇ a₁입니다. 진자와 함께 회전하면 P는 늘 같은 자리에 있고 길이 L도 일정하므로 A|v|P=0입니다. 지상 속도 Lθ̇ a₁를 회전축 a₁로 썼는데도 0이 되지 않는다는 사실에 주목하십시오.'),
    card('6. 슬라이더: 반지름이 바뀌는 운동과 팔이 도는 운동을 더합니다.',
         '회전 팔의 원점 O, 팔을 따라 바깥쪽인 a₁, 그 방향에서 반시계로 90°인 a₂를 잡습니다. r은 O에서 슬라이더 B까지의 거리이고 θ는 지면 수평축에서 잰 팔의 각입니다. p=r a₁입니다. 팔에서 보면 a₁이 고정되어 A|v|B=ṙ a₁, A|a|B=r̈ a₁입니다.',
         '지면에서는 D_N a₁=θ̇ a₂이고 D_N a₂=−θ̇ a₁입니다. 길이 1인 화살표도 방향이 돌면 미분값이 생깁니다. 곱의 미분으로 N|v|B=ṙ a₁+rθ̇ a₂. 앞 항은 팔을 따라 미끄러지는 속도, 뒤 항은 그 순간 반지름 r인 점이 팔의 회전 때문에 갖는 접선속도입니다.'),
    card('7. 슬라이더 가속도에서 계수 2가 나오는 이유',
         '지상 속도의 첫 항 ṙ a₁을 미분하면 r̈ a₁+ṙθ̇ a₂입니다. 둘째 항 rθ̇ a₂를 미분하면 (ṙθ̇+rθ̈)a₂−rθ̇²a₁입니다. a₂ 방향에서 ṙθ̇가 두 번 더해지므로 N|a|B=(r̈−rθ̇²)a₁+(2ṙθ̇+rθ̈)a₂입니다.',
         '−rθ̇²는 중심을 향하는 centripetal acceleration(구심가속도), rθ̈는 회전 속도의 변화에 따른 접선 항입니다. 2ṙθ̇는 팔의 회전과 슬라이더의 상대운동이 함께 있을 때 나타나는 Coriolis term(코리올리 항)입니다. 반지름과 각속도가 모두 일정하면 지면에서는 −rθ̇²a₁만 남고, 팔에서는 0입니다. 이 경우만으로도 두 가속도의 차이를 확인할 수 있습니다.'),
    card('8. 두 번의 회전은 벡터 두 개의 덧셈처럼 순서를 바꿀 수 없습니다.',
         'Position vector(위치벡터)에 두 변위를 더할 때는 순서를 바꿔도 끝점이 같습니다. 하지만 3차원에서 서로 다른 고정축에 대한 finite rotations(유한 회전)은 일반적으로 순서를 바꾸면 최종 orientation(자세)이 달라집니다. 오른손 방향으로 90°씩 돌리고 처음 막대가 +y를 향하면, x축 다음 y축은 +y → +z → +x, y축 다음 x축은 +y → +y → +z입니다.',
         '따라서 3차원 자세를 세 각도의 보통 벡터합으로 취급하거나 그 세 각도의 미분을 곧바로 angular velocity(각속도)의 성분이라 할 수 없습니다. 각속도 자체는 벡터이며 angular acceleration(각가속도)은 각속도의 시간미분입니다. 하나의 고정축에 대한 평면 회전에서는 그 축 방향에 θ̇를 곱할 수 있습니다.'),
])

add(1, '강체 운동학 I', '원본 표지', 'Kinematics of Rigid Bodies I(강체 운동학 I). 입자의 위치에 더해 강체가 어느 방향을 향하는지, 그 운동을 누구의 시점에서 기술하는지 다룹니다.', role='Cover')
add(2, 'Lecture 9-1 · 도는 지구에서 보는 진자', 'Overview 00:17–01:01',
    'Foucault pendulum(푸코 진자)의 진동면은 북극의 지면을 기준으로 보면 하루에 한 바퀴 시계 방향으로 도는 것처럼 보입니다. 영상은 북반구에서의 Coriolis effect(코리올리 효과)도 예로 듭니다. 두 사례는 지면과 함께 도는 관찰자가 무엇을 보게 되는지를 묻는 도입입니다.', role='Divider')
add(3, 'Overview 보조 영상 링크', '원본 링크 페이지',
    '<a href="https://youtu.be/y1kPza_hzsY" target="_blank" rel="noreferrer">원본 슬라이드의 보조 영상 열기</a>. 이 링크는 강의 영상 5편과 별개입니다.', role='Link')
add(4, 'Lecture 9-2 · 기준계와 좌표', 'Contents 1', '기준계·좌표계·자유도를 구분한 뒤, 강체의 orientation(자세)을 위치벡터처럼 더할 수 있는지 살펴봅니다.', role='Divider')
add(5, '입자의 위치만으로는 강체가 향하는 방향을 알 수 없습니다.', 'Contents 1 00:18–00:53',
    'Particle(입자)에서는 한 점의 궤적을 알면 위치를 기술할 수 있었습니다. Rigid body(강체)는 서로 다른 두 점 사이의 거리가 일정한 물체입니다. 그중 한 점의 위치를 알아도 나머지 점들이 어느 방향에 놓였는지는 아직 모릅니다.',
    '예를 들어 막대의 한쪽 끝을 경첩에 고정하면 경첩의 위치는 계속 같지만, 반대쪽 끝은 원을 그릴 수 있습니다. 이 경우 위치에 더해 orientation(자세)을 기술해야 합니다. 원본이 입자 운동학의 방법을 그대로 적용할 수 없다고 한 대상은 특히 이 3차원 회전입니다.')
add(6, 'Reference frame(기준계)은 관찰자가 무엇에 고정되어 있는지를 정합니다.', 'Contents 1 00:58–02:58',
    '강의에서 reference frame(기준계)은 관심 물체와 함께 움직이는 이상적인 관찰 기준입니다. 강체의 운동은 따르지만 기준계 자체의 질량·부피를 계산하지 않습니다. A, D 같은 대문자가 기준계를, a₁,a₂,a₃처럼 번호가 붙은 소문자가 그 기준계에 붙인 축을 나타냅니다.',
    '관성 기준계에 대해 회전하지 않고 일정한 속도로 병진하는 기차도 관성 기준계로 쓸 수 있습니다. 반면 속력의 크기가 일정해도 원을 돌면 방향이 바뀌므로 가속도가 있습니다.',
    correction='“All points have zero acceleration”은 다른 관성 기준계에서 보았을 때 해당 기준계에 고정된 점들이 가속하지 않는다는 뜻입니다. 그 기준계에서 관찰하는 모든 물체의 가속도가 0이라는 뜻은 아닙니다.')
add(7, '뉴턴의 운동법칙에서 가속도를 재는 기준계', 'Contents 1 03:08–03:51',
    'ΣF=ma에서 a는 inertial reference frame(관성 기준계)에서 관측한 가속도입니다. 강의는 Newtonian frame(뉴턴 기준계), absolute frame(절대 기준계)도 같은 뜻으로 씁니다. 이 말이 우주에서 오직 한 기준계만 선택할 수 있다는 뜻은 아닙니다.',
    '지구는 자전하므로 지면에 붙인 축은 이상적인 관성 기준계가 아닙니다. 실험의 시간·거리 규모에서 자전 효과가 충분히 작으면 지면을 관성 기준계로 근사합니다. 푸코 진자처럼 바로 그 효과를 관찰하는 문제에서는 같은 근사가 관측하려는 현상을 지워 버립니다.',
    correction='Contents 1 자막의 “neutral reference frame”은 여기서 다루는 용어가 아닙니다. 원본에 적힌 inertial reference frame(관성 기준계)으로 읽습니다.')
add(8, '좌표계는 기하학적인 화살표에 숫자를 붙입니다.', 'Contents 1 04:00–05:43',
    'Position vector(위치벡터) OP는 출발점 O에서 끝점 P를 향하는 화살표입니다. 숫자를 매기기 전에도 길이와 방향은 있습니다. O를 원점으로 두고 단위벡터를 정하면 각 축에 투영한 값이 성분이 됩니다.',
    '강의에서 쓰는 세 축은 orthonormal(정규직교), 즉 길이가 각각 1이고 서로 수직입니다. Dextral 또는 right-handed(오른손 방향)라는 조건은 a₁에서 a₂로 오른손 손가락을 감을 때 엄지가 a₃를 향한다는 뜻입니다. 여기서는 이러한 기저를 사용하며 모든 종류의 좌표계에 이 조건이 필수인 것은 아닙니다.', eq='|a₁|=|a₂|=|a₃|=1; a₁·a₂=0; a₁×a₂=a₃')
add(9, '같은 화살표는 여러 좌표계로 표현할 수 있습니다.', 'Contents 1 05:51–08:13',
    'p=pₓ i+pᵧ j+p<sub>z</sub> k=p₁ a₁+p₂ a₂+p₃ a₃입니다. 각 성분 목록을 쓸 때 어느 basis(기저)에 대한 값인지 붙입니다. 같은 기준계에서도 두 축 집합을 쓸 수 있으므로 축 기호가 달라졌다고 관찰자가 바뀐 것은 아닙니다.',
    '시험용 보강: a₁=j, a₂=−i로 잡으면 p=i는 기존 축에서 (1,0), 새 축에서 (0,−1)입니다. 두 번째 성분이 음수인 까닭은 a₂가 왼쪽을 가리키기 때문입니다. 둘 다 오른쪽을 가리키는 같은 화살표입니다.')
add(10, '좌표의 개수와 자유도의 개수는 다를 수 있습니다.', 'Contents 1 08:19–09:06',
    'Coordinate(좌표)는 계의 configuration(배치)을 정하는 스칼라 변수입니다. 거리뿐 아니라 각도도 좌표가 됩니다. Degrees of freedom(자유도)는 구속조건을 만족하면서 독립적으로 지정할 수 있는 좌표의 최소 개수입니다.',
    'Generalized coordinate(일반화좌표)는 문제에 맞추어 고른 변수입니다. 강의는 흔히 독립적인 최소 개수를 고르지만 이것이 명칭의 절대적인 조건은 아니라고 설명합니다. 변수를 여럿 쓰면 그 사이의 constraint(구속조건)를 함께 써야 합니다.')
add(11, '진자 끝점의 x와 y 중 독립적으로 정할 수 있는 것은 하나입니다.', 'Contents 1 09:10–11:48',
    '그림의 θ는 아래쪽 수직선에서 오른쪽으로 잰 각입니다. 수평 투영은 +L sinθ이고, 수직 투영은 위쪽 축의 반대이므로 −L cosθ입니다. x²+y²=L²를 만족하므로 길이 L이 정해진 진자는 one degree of freedom(자유도 1)입니다. 원본 질문의 답은 θ 하나입니다.',
    'θ=0에서 끝점은 (0,−L)입니다. y를 x로 풀면 y=±√(L²−x²)이므로 x 하나로 y를 구할 때에는 위·아래 어느 가지에 있는지도 알아야 합니다. 그림처럼 아래쪽 가지에서는 음의 부호를 씁니다. 각도 θ를 좌표로 잡으면 어느 위치를 가리키는지가 직접 드러납니다.', eq='p=x i+y j=L sinθ i−L cosθ j<br>x²+y²=L²')
add(12, '실제 물체의 회전 일부만 따라가는 가상 기준계', 'Contents 1 11:54–12:13',
    'Virtual reference frame(가상 기준계)은 분석을 위해 도입하며 실제 강체와 모든 회전을 같이할 필요가 없습니다. 예를 들어 물체의 긴 축이 향하는 방향만 따라가되, 그 축 주위의 spin(자전)은 따라가지 않는 관찰자를 상상할 수 있습니다.',
    '어느 운동을 따라가고 어느 운동을 제외하는지 정해 두면, 여러 회전이 겹쳐 있는 그림에서도 물체가 그 기준계에 대해 어떻게 도는지 따로 읽을 수 있습니다.')
add(13, '구르는 원뿔: 지면 N, 원뿔 C, 가상 기준계 B', 'Contents 1 12:19–14:18',
    '그림의 n₁,n₂,n₃는 지면 N에 고정된 Newtonian frame(뉴턴 기준계)의 축입니다. c₁,c₂,c₃는 원뿔 C에 붙인 body frame(물체 기준계)의 축입니다. 원뿔 표면에 선을 그으면 c₂,c₃가 그 선과 함께 돕니다.',
    'b₁,b₂,b₃는 virtual frame(가상 기준계) B의 축입니다. b₁과 c₁은 원뿔의 긴 축 방향을 따르되 B는 C의 축 주위 자전까지 따라가지 않습니다. 따라서 자전만 보면 c₂,c₃가 b₂,b₃에 대해 회전합니다. 그렇다고 B가 지면에 고정됐다는 뜻은 아닙니다. 원뿔 축 자체가 방향을 바꾸면 B도 이를 따라갑니다.',
    correction='자막 말미의 “P1 B2”는 새 기준계 P를 도입한 것이 아닙니다. 원본의 축 표기와 영상 앞부분에 맞춰 b₁,b₂,b₃로 읽습니다.')
add(14, '벡터의 덧셈에는 순서와 묶음에 관한 규칙이 있습니다.', 'Contents 1 14:21–15:39',
    'Commutativity(교환법칙)는 x+y=y+x, associativity(결합법칙)는 (x+y)+z=x+(y+z), distributivity(분배법칙)는 α(x+y)=αx+αy입니다. 여기서 x,y,z는 벡터이고 α는 스칼라입니다.',
    '이 세 가지는 벡터 공간의 성질 중 일부입니다. 다음 장에서는 반대로 이 중 하나라도 성립하지 않으면 보통의 벡터 덧셈으로 해석할 수 없다는 점을 이용합니다.')
add(15, '서로 다른 축의 유한 회전은 순서가 중요합니다.', 'Contents 1 15:43–18:17',
    '같은 물체를 고정된 x축에 대해 돌린 뒤 y축에 대해 돌리는 경우와 순서를 뒤집는 경우를 비교합니다. 첫 회전이 물체의 방향을 바꾸므로, 둘째 회전이 작용할 때의 출발 자세가 달라집니다. 두 결과는 일반적으로 같지 않습니다.',
    '자세를 숫자로 표현할 수는 있습니다. 다만 세 숫자를 위치의 세 성분처럼 더해서 두 회전의 결과를 얻을 수는 없습니다. 한 고정축만 쓰는 평면 회전에서는 각도를 더할 수 있으므로, 순서 차이를 보여 주려면 서로 다른 축을 택합니다.',
    correction='원본의 θ₁i+θ₂j ≠ θ₂j+θ₁i에서 +는 회전의 연속 수행을 묘사한 표기입니다. 실제 벡터 덧셈이라면 양변은 같습니다. 회전의 합성은 RᵧRₓ와 RₓRᵧ로 구별합니다.')
add(16, 'Lecture 9-3 · 벡터의 시간미분', 'Contents 2',
    '같은 점을 회전하는 관찰자와 지상의 관찰자가 어떻게 다르게 보는지 살펴보고, 속도·가속도에 관찰자를 표시하는 표기법을 익힙니다.', role='Divider')
add(17, '시간에 따라 변하는 벡터를 성분과 기저로 나눕니다.', 'Contents 2 00:17–01:27',
    '기준계 A에 unit vectors(단위벡터) a₁,a₂,a₃를 고정합니다. 벡터 p(t)의 각 성분 p₁(t),p₂(t),p₃(t)는 그 축 방향으로 얼마나 뻗었는지를 재는 스칼라입니다. 슬라이드에서 (t)를 생략해도 시간에 따른 변화를 허용한다는 뜻은 같습니다.',
    'p는 우선 일반적인 벡터의 예입니다. p를 어떤 점의 position vector(위치벡터)로 선택했을 때에만 그 시간미분을 그 점의 속도와 연결합니다. 글자 p 또는 v만 보고 물리량을 단정하지 않습니다.', eq='p(t)=p₁(t)a₁+p₂(t)a₂+p₃(t)a₃')
add(18, 'A에 고정된 축은 A에서 미분할 때만 상수입니다.', 'Contents 2 01:33–02:56',
    'D_A를 “A에서 관측한 시간미분”이라 쓰겠습니다. 곱의 미분을 하면 D_A(p₁a₁)=ṗ₁a₁+p₁D_A a₁입니다. a₁은 A에 붙어 있으므로 A에서 바라본 길이와 방향이 모두 일정합니다. 따라서 둘째 항이 0이 됩니다. 나머지 두 축에도 같은 논리를 적용합니다.',
    '점 하나가 component(성분) 위에 있으면 시간에 대한 1차 미분, 점 둘이면 2차 미분입니다. 기준계를 바꾸더라도 축을 미분한 항이 0인지 먼저 확인해야 합니다. 특히 길이가 1이라는 사실만으로는 축의 미분이 0이 되지 않습니다.', eq='D_A aᵢ=0 (i=1,2,3)<br>D_A p=ṗ₁a₁+ṗ₂a₂+ṗ₃a₃')
add(19, '“어느 기준계에서 미분했는가”는 답의 일부입니다.', 'Contents 2 03:01–03:27',
    '같은 벡터 p라도 A에서는 방향이 일정하게 보이고 다른 기준계 B에서는 돌아가는 것으로 보일 수 있습니다. 이때 D_A p와 D_B p는 다릅니다. 원본의 possibly different(다를 수 있는)는 언제나 다르다는 뜻이 아닙니다.',
    '시험용 보강: 같은 화살표의 미분을 비교할 때 두 기준계 축의 상대 방향이 일정하면 미분값은 같습니다. 반면 서로 다른 원점에서 점까지 잰 위치벡터는 애초에 다른 화살표입니다. 다음 예에서 관찰자와 출발점을 분리해 읽어야 하는 이유입니다.')
add(20, '회전목마의 말에 탄 사람은 상하운동만 봅니다.', 'Contents 2 03:30–04:52',
    'Carousel(회전목마)에 고정된 기준계 C에서 보면 그림의 점 P는 같은 수평 위치에 붙어 위아래로만 움직입니다. 지면 N에서는 말이 위아래로 움직이는 동안 회전목마 중심 주위를 함께 돌아갑니다. 따라서 P에는 수평 이동도 있습니다.',
    '같은 순간의 같은 말에 관한 두 설명이 모두 맞습니다. “회전목마가 통째로 수평 이동한다”는 가정을 추가할 필요는 없습니다. 그림의 N과 C의 원점이 서로 다르면, 각각의 원점에서 P까지 그은 화살표의 차이도 함께 고려해야 합니다.')
add(21, '이미 구한 속도 화살표를 옮기는 것과 관찰자를 바꾸는 것은 다릅니다.', 'Contents 2 04:55–05:45',
    'Motion vectors(운동벡터)인 velocity(속도)와 acceleration(가속도)에는 관찰 기준계를 표시합니다. 지상에서 본 속도는 그림의 어디에 평행하게 다시 그려도 그 크기와 방향이 같습니다. 회전목마에서 본 속도를 구하려면 그 기준계에서 점의 위치가 어떻게 변하는지 다시 계산해야 합니다.',
    correction='영상의 “doesn’t depend on the origin”은 이미 정의된 속도·가속도 벡터를 자유벡터로 그릴 때의 설명입니다. 움직이는 원점에서 새로 잰 상대위치를 미분하면 원점 자체의 운동이 들어가므로, 어느 관찰자의 속도나 같다는 뜻으로 넓히면 안 됩니다.')
add(22, '왼쪽 위는 관찰자, 오른쪽 위는 관심 대상입니다.', 'Contents 2 05:46–07:23',
    'N|v|P는 “velocity of point P with respect to N(N에 대한 점 P의 속도)”입니다. 먼저 오른쪽 P를 보고 어느 점인지 확인한 뒤, 왼쪽 N을 보고 누가 관찰하는지 확인합니다. 아래 예제의 A|v|P는 점을 바꾼 것이 아니라 관찰 기준계를 바꾼 것입니다.',
    'Angular velocity(각속도)에는 관심 대상도 회전하는 물체나 기준계가 됩니다. 예를 들어 N|ω|A는 N에서 본 기준계 A의 각속도입니다. ω 오른쪽의 A는 점의 위치를 나타내지 않습니다.')
add(23, '가속도는 같은 기준계의 속도를 같은 기준계에서 다시 미분합니다.', 'Contents 2 07:29–09:23',
    'A에 고정된 원점에서 P까지 잰 p를 A축으로 쓰면 A|v|P=D_A p=Σṗᵢaᵢ입니다. B에 고정된 원점과 축으로 쓴 위치에는 B에서의 미분을 적용해 B|v|P를 얻습니다. 이후 두 예제에서는 원점 O를 두 기준계가 공유하므로 같은 OP 또는 OB를 출발점으로 비교할 수 있습니다.',
    'A|a|P를 구하려면 먼저 A|v|P를 구하고 여기에 D_A를 적용합니다. D_N을 적용하거나 N의 속도를 가져오면 다른 변화율입니다. 계산에 쓰는 축은 자유롭게 고를 수 있지만, 그 축이 관찰자에 대해 움직이면 축 미분까지 계산합니다.', eq='A|v|P=D_A p; A|a|P=D_A(A|v|P)<br>B|v|P=D_B p (B의 원점 기준)')
add(24, 'Lecture 9-4 · 세 가지 예제', 'Problem Solving',
    '진자 끝점의 속도, 회전 팔 위 슬라이더의 속도·가속도, 두 번의 유한 회전 순서를 차례로 풉니다.', role='Divider')
add(25, '예제 1 · 진자 끝점 P의 속도를 누구에게 묻는가', 'Problem Solving 00:17–01:08',
    '길이 L인 pendulum(진자)의 끝점 P에 대해, 지면 기준계 N에서 본 속도와 진자 기준계 A에서 본 속도를 각각 구합니다. θ(t)는 아래 수직선에서 잰 각이고 L은 일정합니다. 두 답에는 모두 대상 P를 표시합니다.',
    '문제는 θ(t)에서 velocity(속도)를 구하는 kinematics(운동학) 문제입니다. 질량 m이 그려져 있어도 중력이나 장력을 구할 필요는 없습니다. θ나 θ̇의 수치가 주어지지 않았으므로 결과도 기호로 남습니다.')
add(26, '예제 1 · 기준계 → 축 → 위치 → 미분 순서로 풉니다.', 'Problem Solving 01:15–01:55',
    '먼저 observed at N(N에서 관찰한), observed at A(A에서 관찰한)이라는 문구에 표시합니다. 그다음 N과 A 각각에 고정된 축을 정하고, 같은 원점 O에서 같은 점 P까지의 위치를 두 방식으로 씁니다.',
    '마지막에 각 관찰자에게 고정된 축을 이용하면 성분만 미분할 수 있습니다. 지상에서 본 속도와 진자에서 본 속도를 더하는 단계는 없습니다. 문제는 서로 다른 두 질문에 각각 답하라고 했습니다.')
add(27, '예제 1 · 지면에 N, 진자에 A를 붙입니다.', 'Problem Solving 01:59–02:33',
    'N은 지면을 inertial frame(관성 기준계)으로 근사한 관찰자이고, A는 진자 막대에 고정된 body frame(물체 기준계)입니다. A에서 보면 막대와 끝점 사이의 위치 관계는 바뀌지 않습니다.',
    '원본의 “each rigid body has one reference frame”은 이 풀이에서 물체에 대응하는 기준계 하나를 지정한다는 뜻입니다. 그 기준계에 붙일 coordinate system(좌표계)의 선택은 여전히 여러 가지입니다.')
add(28, '예제 1 · 두 기준계가 공유하는 원점과 축 방향', 'Problem Solving 02:39–03:53',
    '회전축 O를 공통 원점으로 정합니다. 지면의 n₁은 오른쪽, n₂는 위쪽, 오른손 규칙에 따른 n₃는 화면 밖입니다. A축은 막대와 함께 회전하며 a₂는 P에서 O 쪽, a₁은 막대에 수직인 θ 증가 방향입니다.',
    'θ=0에서는 a₁=n₁, a₂=n₂입니다. θ가 커지면 a₁은 오른쪽 위로 돌아가고 a₂는 왼쪽 위를 향합니다. 기준 자세에서 축을 먼저 그려 두면 다음 장의 음수 부호를 외울 필요가 없습니다.')
add(29, '예제 1 · 같은 OP를 두 기저로 표현합니다.', 'Problem Solving 03:56–05:49',
    '수직 아래에서 θ를 재므로 오른쪽 성분은 L sinθ, 위쪽 성분은 −L cosθ입니다. A축에서는 P가 O로부터 a₂의 반대 방향으로 거리 L만큼 떨어져 있습니다. 따라서 OP=−L a₂이고 a₁ 성분은 0입니다.',
    '직접 확인하려면 a₂=−sinθ n₁+cosθ n₂를 −L에 곱합니다. 지상 성분과 똑같아집니다. 이 등호는 같은 화살표의 두 표현 사이의 등호입니다. 다음 장의 두 미분 결과 사이에 그대로 옮길 수 있는 등호는 아닙니다.', eq='p=OP=L sinθ n₁−L cosθ n₂=−L a₂')
add(30, '예제 1 · 지면에서는 접선속도, 진자에서는 0', 'Problem Solving 05:52–08:05',
    'N에서는 n₁,n₂가 일정합니다. d(sinθ)/dt=cosθ·θ̇, d(−cosθ)/dt=sinθ·θ̇를 써서 N|v|P=Lθ̇(cosθ n₁+sinθ n₂)를 얻습니다. 괄호 속은 접선 방향 a₁입니다. θ̇가 음수이면 속도는 −a₁ 방향입니다.',
    'A에서는 p=−L a₂의 길이도 방향도 변하지 않습니다. 따라서 A|v|P=0입니다. 동일한 점이라도 진자와 함께 움직이는 관찰자에게는 정지해 있고, 지상에서는 원 궤적의 접선을 따라 움직일 수 있습니다.',
    correction='원본의 “Integrate twice” 지시는 이 문제의 연산과 일치하지 않습니다. 위치가 주어졌으므로 속도는 각 기준계에서 한 번 미분하여 구합니다.',
    eq='N|v|P=Lθ̇ a₁; A|v|P=0')
add(31, '예제 1 · 스칼라의 미분과 벡터의 미분을 구분합니다.', 'Problem Solving 08:05–08:38',
    '동일하게 정의한 scalar(스칼라) θ(t)의 시간미분 θ̇에는 축의 미분 항이 없습니다. 반면 한 벡터를 A축과 N축으로 분해한 성분은 처음부터 서로 다른 함수입니다. 예를 들어 −L은 일정하지만 지상의 x=L sinθ는 변할 수 있습니다.',
    '시험용 보강: 지상 속도 Lθ̇ a₁를 한 번 더 미분하면 N|a|P=Lθ̈ a₁+Lθ̇²a₂입니다. 여기서 +a₂는 지지점 쪽입니다. 순간적으로 θ̇=0이어도 θ̈가 0이라는 조건이 없으므로 가속도까지 0이라고 할 수 없습니다.',
    correction='원본의 “position vectors are identical”은 같은 두 점 O,P 사이의 화살표를 비교하는 경우입니다. 원점을 다른 곳으로 옮겨 새 화살표를 그려도 위치벡터가 같다는 뜻은 아닙니다.')
add(32, '예제 2 · 슬라이더 B의 속도 두 개와 가속도 두 개', 'Problem Solving 08:41–09:15',
    'Arm(팔)이 O 주위를 회전하고 slider(슬라이더) B가 그 위를 미끄러집니다. r(t)는 O에서 B까지의 거리이고 θ(t)는 수평 오른쪽에서 반시계 방향으로 잰 각입니다. 이번에는 길이 r도 변할 수 있습니다.',
    '구할 양은 N|v|B, N|a|B, A|v|B, A|a|B입니다. N은 지면, A는 팔입니다. B가 A에서 얼마나 움직이는지와 그 B가 지면을 어떻게 지나는지는 별개이므로, 답마다 왼쪽 위의 관찰자를 유지합니다.')
add(33, '예제 2 · 어떤 양이 시간에 따라 변하는지 먼저 적습니다.', 'Problem Solving 09:20–09:46',
    '원점 O를 고정하고 r과 θ를 시간의 함수로 둡니다. 지상 축에서는 x=r cosθ, y=r sinθ이므로 두 곱 모두 product rule(곱의 미분법)이 필요합니다. 진자 예제와 달리 ṙ 항을 생략할 수 없습니다.',
    '팔에 붙인 축에서는 p=r a₁ 하나로 충분합니다. 여기서도 관찰자가 누구인지는 별도로 결정합니다. A에서는 a₁이 고정되고, N에서는 a₁이 회전합니다.')
add(34, '예제 2 · A는 슬라이더가 아니라 팔에 붙은 기준계입니다.', 'Problem Solving 09:49–10:04',
    'N은 지면의 Newtonian frame(뉴턴 기준계), A는 팔의 body frame(물체 기준계)입니다. B는 운동을 구하려는 점입니다. A가 B와 항상 함께 미끄러지는 기준계인 것은 아닙니다.',
    '따라서 “A에서 본 위치”를 그릴 때에는 팔의 회전만 따라갑니다. B가 팔 위에서 바깥쪽으로 밀려가면 A에서도 그 이동이 보입니다. 이후 A|v|B가 일반적으로 0이 아닌 이유입니다.')
add(35, '예제 2 · 팔 끝에 그린 단위벡터가 원점을 바꾸지는 않습니다.', 'Problem Solving 10:08–11:23',
    'a₁은 팔을 따라 O에서 바깥쪽, a₂는 거기서 반시계로 90°, a₃은 화면 밖입니다. 단위벡터의 방향을 표시하는 작은 화살표를 같은 방향으로 평행하게 옮겨 그려도 기저는 같습니다. 원본 질문 “왜 O에 그리지 않았는가?”의 답은 축들이 겹치는 그림을 피하기 위해서입니다.',
    '실제 위치벡터의 꼬리는 계속 O입니다. 그림의 화살표 위치를 보고 회전 팔 끝을 새 원점으로 잡으면 다음 식 p=r a₁이 뜻하는 물리량이 달라집니다.',
    correction='원본에 남은 “body reference frame of pendulum”의 대상은 여기서는 pendulum(진자)이 아니라 arm(회전 팔)입니다. 34장의 정의와 영상 설명이 일치합니다.')
add(36, '예제 2 · 지면의 두 성분이 팔에서는 한 성분이 됩니다.', 'Problem Solving 11:27–12:04',
    'a₁=cosθ n₁+sinθ n₂이므로 r a₁을 전개하면 (r cosθ)n₁+(r sinθ)n₂입니다. θ는 이번에는 수평에서 잽니다. 따라서 진자 예제와 달리 x에 cosθ가 붙고 y에 sinθ가 붙습니다.',
    'θ=0일 때 OB가 오른쪽으로 r만큼 뻗는지를 확인하면 sin과 cos를 바꿔 쓰는 실수를 찾을 수 있습니다. 아래 계산에서는 계속 B를 관심 점으로 씁니다.',
    correction='두 번째 줄의 OP와 뒤 장 일부 수식의 오른쪽 위 P는 이 예제의 대상 B와 표기가 섞인 것입니다. 두 식 모두 같은 슬라이더까지의 OB로 읽습니다.',
    eq='p=OB=r cosθ n₁+r sinθ n₂=r a₁')
add(37, '예제 2 · 지상 속도에는 반지름 변화와 회전이 모두 들어갑니다.', 'Problem Solving 12:07–13:36',
    '지면에서는 n₁,n₂가 일정하므로 d(r cosθ)/dt=ṙ cosθ−rθ̇ sinθ, d(r sinθ)/dt=ṙ sinθ+rθ̇ cosθ입니다. 각 괄호의 첫 항은 r이 변해서, 둘째 항은 θ가 변해서 생깁니다.',
    '팔에서는 a₁과 a₂가 고정된 방향이므로 D_A(r a₁)=ṙ a₁입니다. ṙ가 0이고 θ̇만 남는 순간에는 B가 팔 위에서 정지해 보여도 지상에서는 접선 방향 속도가 남습니다.',
    eq='N|v|B=(ṙ cosθ−rθ̇ sinθ)n₁ + (ṙ sinθ+rθ̇ cosθ)n₂<br>A|v|B=ṙ a₁')
add(38, '예제 2 · 지상 가속도의 x, y 성분을 전개합니다.', 'Problem Solving 13:38–14:27',
    'x속도의 ṙ cosθ를 미분하면 r̈ cosθ−ṙθ̇ sinθ입니다. −rθ̇ sinθ를 미분하면 −ṙθ̇ sinθ−rθ̈ sinθ−rθ̇² cosθ입니다. 같은 항 두 개를 합쳐 −2ṙθ̇ sinθ를 얻습니다. y속도에서도 같은 순서로 전개하되 d(sinθ)/dt와 d(cosθ)/dt의 부호를 구별합니다.',
    '아래 aₓ,aᵧ는 N에서 본 B의 가속도 성분입니다. A에서는 A|v|B=ṙ a₁의 스칼라만 미분하므로 A|a|B=r̈ a₁입니다. 팔 안에서 미끄러짐의 속력이 일정하면 r̈=0일 수 있어도 지상 가속도는 남을 수 있습니다.',
    eq='aₓ=r̈ cosθ−2ṙθ̇ sinθ−rθ̈ sinθ−rθ̇² cosθ<br>aᵧ=r̈ sinθ+2ṙθ̇ cosθ+rθ̈ cosθ−rθ̇² sinθ<br>N|a|B=aₓ n₁+aᵧ n₂; A|a|B=r̈ a₁')
add(39, '예제 2 · 팔의 축으로 지상 가속도를 짧게 유도합니다.', 'Problem Solving 14:31–15:20',
    'a₁=cosθ n₁+sinθ n₂, a₂=−sinθ n₁+cosθ n₂입니다. N에서는 이를 미분하여 D_N a₁=θ̇ a₂, D_N a₂=−θ̇ a₁을 얻습니다. p=r a₁의 미분은 N|v|B=ṙ a₁+rθ̇ a₂입니다. 이 식의 오른쪽에 a축을 써도 관찰자는 여전히 N입니다.',
    '첫 항의 미분은 r̈ a₁+ṙθ̇ a₂입니다. 둘째 항은 스칼라 rθ̇의 미분 (ṙθ̇+rθ̈)a₂와 방향의 미분 rθ̇(−θ̇ a₁)로 나뉩니다. 따라서 a₁ 방향에는 r̈−rθ̇², a₂ 방향에는 2ṙθ̇+rθ̈가 남습니다. 이를 n₁,n₂로 투영하면 38장의 두 성분과 같습니다.',
    correction='원본 마지막 가속도 전개에 r이 들어가야 할 자리에 ṙ가 인쇄되어 있습니다. −rθ̇²와 rθ̈에는 길이 r이 곱해지고, 2ṙθ̇에는 반지름 변화율 ṙ가 곱해집니다. 예를 들어 rθ̇²의 단위는 m/s²이지만 ṙθ̇²는 m/s³으로 가속도가 아닙니다.',
    eq='N|a|B=(r̈−rθ̇²)a₁+(2ṙθ̇+rθ̈)a₂<br>A|a|B=r̈ a₁',
    extra=card('시험용 보강 · 반지름이 고정된 극한',
               'r이 일정하고 팔이 일정한 각속도 ω로 돌면 ṙ=r̈=θ̈=0입니다. 지상 답은 −rω²a₁, 팔에서 본 답은 0입니다. 지상에서는 B가 원의 중심을 향해 가속하고, 팔에 탄 사람에게는 B가 한자리에 붙어 있기 때문입니다.'))
add(40, '예제 3 · 회전 순서를 뒤집는 반례를 만듭니다.', 'Problem Solving 15:25–15:49',
    '두 연산이 항상 교환된다는 주장을 반박하려면 한 가지 counterexample(반례)이면 충분합니다. 동일한 초기 자세, 동일한 고정축, 동일한 각도를 사용하고 회전 순서만 바꾼 뒤 결과를 비교합니다.',
    correction='“Vector addition does not hold commutativity”를 문자 그대로 받아들이면 틀립니다. Ordinary vector addition(보통의 벡터 덧셈)은 교환됩니다. 반례가 겨냥하는 연산은 강체의 두 유한 회전을 연이어 수행하는 합성입니다.')
add(41, '예제 3 · 먼저 두 변위를 더하면 같은 곳에 도착합니다.', 'Problem Solving 15:50–16:39',
    'Displacement(변위) 2i와 3j를 더합니다. 오른쪽 두 칸, 위 세 칸으로 이동하든 위 세 칸, 오른쪽 두 칸으로 이동하든 최종 위치는 (2,3)입니다. 중간 경로는 달라도 시작점에서 최종점으로 향하는 화살표는 같습니다.',
    '이것이 벡터 덧셈의 commutativity(교환법칙)입니다. 다음 그림에서는 “두 변위를 더한다” 대신 “막대 자체를 두 번 돌린다”로 연산을 바꿉니다.', eq='2i+3j=3j+2i')
add(42, '예제 3 · x 다음 y이면 +x, y 다음 x이면 +z', 'Problem Solving 16:43–17:30',
    '시험용 보강: 그림의 두 회전을 고정된 x, y축에 대한 오른손 방향 90° 회전으로 계산합니다. 처음 막대가 +y를 향한다고 두면, x축으로 돌릴 때 +y는 +z로 갑니다. 이어 y축으로 돌리면 +z는 +x가 됩니다.',
    '반대 순서에서는 처음 막대가 y축과 나란하므로 y축 회전 뒤에도 그 방향은 +y입니다. 그다음 x축 회전으로 +z가 됩니다. 같은 초기 벡터의 최종 방향부터 다르므로 두 최종 자세는 같을 수 없습니다. 기호 RᵧRₓ에서는 오른쪽의 Rₓ를 먼저 적용합니다.',
    correction='원본 식은 두 순서를 등호로 연결하지만 바로 아래 그림과 결론은 서로 다른 결과를 보입니다. 유한 회전의 합성은 이 예에서 RᵧRₓ ≠ RₓRᵧ입니다.',
    eq='RᵧRₓ j=Rᵧ k=i<br>RₓRᵧ j=Rₓ j=k')
add(43, '각속도는 벡터지만 자세는 같은 방식으로 미분하지 않습니다.', 'Problem Solving 17:33–18:06',
    '3차원 orientation(자세)을 표현하는 각도들의 변화율을 그대로 angular velocity(각속도)의 직교 성분으로 놓을 수는 없습니다. 각도가 어떤 축에 대한 것이고 어떤 순서로 적용되는지에 따라 속도와의 관계가 달라집니다. 이것이 “자세를 위치벡터처럼 직접 미분할 수 없다”는 뜻입니다.',
    '반면 angular velocity(각속도) ω는 벡터입니다. 관찰 기준계를 정해 이를 미분하면 angular acceleration(각가속도) α를 구할 수 있습니다. 시험용 보강: 고정축 e에 대한 평면 회전에서는 ω=θ̇ e, α=θ̈ e입니다. 이 특수한 관계를 일반 3차원 자세 전체에 그대로 확장하지 않습니다.')
add(44, '참고문헌', '원본 References 페이지',
    '원본 수록 문헌: Beer 외, <i>Vector Mechanics for Engineers: Dynamics</i>, 12판, 15장. 유홍희, <i>동역학</i>, 1판, 문운당, 8장. 교재 본문은 이 노트의 별도 인용 자료로 사용하지 않았습니다.', role='Reference')

exams = [
    ('Distinguish(구별하라) a reference frame(기준계) from a coordinate system(좌표계).',
     'A reference frame specifies the observer relative to whom motion is measured. A coordinate system specifies the origin and basis used to express a vector. Several coordinate systems can be attached to the same frame.',
     'Measured relative to(~에 대해 측정되는)는 관찰 기준, expressed in(~로 표현된)은 성분 표기를 가리킵니다. 같은 속도에 두 표현이 함께 쓰일 수 있습니다.'),
    ('When can the Earth be treated as an inertial frame(관성 기준계로 취급될 수 있는가)?',
     'The rotating Earth is not exactly inertial. A ground-fixed frame may be treated as inertial when the effects of its acceleration and rotation are negligible for the motion under study.',
     'Negligible(무시할 만큼 작은)는 0이라는 뜻이 아닙니다. 어떤 운동에서 그 근사가 허용되는지 조건을 붙입니다.'),
    ('Determine(구하라) the degrees of freedom(자유도) of a planar pendulum(평면 진자) of fixed length(고정 길이).',
     'The constraint x² + y² = L² leaves one independent coordinate. The angle θ determines both x = L sinθ and y = −L cosθ, so the pendulum has one degree of freedom.',
     'Independent(독립적인)인지가 기준입니다. 끝점의 성분이 두 개여도 constraint(구속조건) 하나가 있으므로 θ 하나로 충분합니다.'),
    ('Explain(설명하라) why differentiating a vector(벡터를 미분하는 것) requires an observer(관찰자).',
     'A basis vector fixed in A has zero derivative in A, but its direction can change in N. Differentiating a vector in N therefore requires differentiating both its components and its basis vectors.',
     'Fixed in A(A에 고정된)와 fixed in N(N에 고정된)을 구별합니다. 길이가 일정해도 방향이 바뀌면 미분값은 0이 아닙니다.'),
    ('Find(구하라) the velocity of the pendulum tip(진자 끝점의 속도) as observed in N and A(N과 A에서 관찰한).',
     'The ground observer measures a tangential velocity Lθ̇ a₁. The pendulum observer measures zero velocity because the tip is fixed in A. Both observers use the same pivot O as the origin.',
     'Tangential(접선 방향인)은 N에서 본 방향입니다. A축으로 답을 썼더라도 관찰자는 N일 수 있습니다.'),
    ('Express(나타내라) the ground velocity(지상 속도) of a slider(슬라이더) in the arm basis(팔에 붙은 기저로).',
     'The position is r a₁. In N, the derivative of a₁ is θ̇ a₂, so the velocity is ṙ a₁ + rθ̇ a₂. In A, the basis is fixed and the relative velocity is only ṙ a₁.',
     'In the arm basis(팔의 기저로)는 답에 쓸 축을 지정합니다. As observed in the ground frame(지상 기준계에서 관찰한)는 어느 속도인지를 지정합니다.'),
    ('Identify(찾아라) the Coriolis term(코리올리 항) in the slider acceleration(슬라이더 가속도).',
     'The ground acceleration is (r̈ − rθ̇²)a₁ + (2ṙθ̇ + rθ̈)a₂. The term 2ṙθ̇ a₂ arises because the slider moves along a rotating arm. It vanishes if either the sliding speed or the angular velocity is zero.',
     'Radial(반지름 방향) 성분의 −rθ̇²와 transverse(반지름에 수직인 방향) 성분의 2ṙθ̇를 구별합니다. 각가속도에 의한 별도 항은 rθ̈입니다.'),
    ('Show by a counterexample(반례로 보여라) that finite rotations(유한 회전들) do not commute(교환되지 않는다).',
     'Start with a bar along +y and apply positive 90-degree rotations about fixed axes. Rotating about x and then y sends the bar to +x. Rotating about y and then x sends it to +z. The final orientations differ.',
     'Fixed axes(고정축), initial direction(초기 방향), order(순서)를 모두 적습니다. 일반적으로 순서가 중요함을 보이려면 한 반례면 충분합니다.'),
    ('Is angular velocity(각속도) the direct derivative(직접적인 미분) of three orientation angles(세 자세각)?',
     'Not in general. Finite rotations compose in an order-dependent way; the rates of three orientation angles are not generally the components of angular velocity. Angular velocity itself is a vector, and its time derivative in the specified frame gives angular acceleration.',
     'In general(일반적으로)이라는 범위를 밝혀 한 고정축에서 성립하는 ω=θ̇e를 배제하지 않습니다.'),
]
terms = [
    ('kinematics / kinetics','운동학 / 운동역학','운동의 기하학적 기술 / 힘과 운동의 관계'),
    ('rigid body / orientation','강체 / 자세','점 사이 거리 고정 / 물체가 공간에서 향하는 방향'),
    ('reference frame / observer','기준계 / 관찰자','움직임을 누구에 대해 측정하는가'),
    ('inertial / Newtonian frame','관성 / 뉴턴 기준계','ΣF=ma를 가속 기준계 보정 없이 적용하는 기준계'),
    ('body-fixed / ground-fixed','물체에 고정된 / 지면에 고정된','각각 어느 물체를 따라 움직이는지 지정'),
    ('virtual reference frame','가상 기준계','분석을 위해 실제 물체의 운동 중 일부만 따라갈 수도 있는 기준계'),
    ('coordinate system / coordinate','좌표계 / 좌표','원점과 축에 대한 약속 / 배치를 나타내는 스칼라'),
    ('basis / component','기저 / 성분','표현에 쓰는 축 방향들 / 그 방향에 대응하는 수'),
    ('unit vector / orthogonal','단위벡터 / 직교하는','길이 1 / 서로 수직'),
    ('orthonormal / dextral','정규직교인 / 오른손 방향인','서로 직교하는 단위벡터 / a₁×a₂=a₃의 방향'),
    ('origin / position vector','원점 / 위치벡터','출발점 / 그 점에서 대상까지의 화살표'),
    ('configuration / constraint','계의 배치 / 구속조건','계가 놓인 상태 / 좌표 간 허용 관계'),
    ('degree of freedom / independent','자유도 / 독립적인','배치에 필요한 독립 좌표의 수 / 서로 따로 정할 수 있는'),
    ('generalized coordinate','일반화좌표','문제의 배치에 맞게 고른 스칼라 변수; 각도도 가능'),
    ('commutativity / associativity / distributivity','교환법칙 / 결합법칙 / 분배법칙','연산의 순서 / 묶음 / 스칼라 곱의 분배'),
    ('finite / consecutive rotations','유한 회전 / 연속으로 수행하는 회전','크기를 무한소로 보지 않는 회전 / 차례로 합성하는 회전'),
    ('fixed axis / right-hand rule','고정축 / 오른손 규칙','공간에서 방향이 고정된 축 / 양의 회전 방향을 정하는 규칙'),
    ('time derivative / rate of change','시간미분 / 변화율','시간에 따른 변화; 벡터에는 관찰 기준계를 명시'),
    ('motion vector / free vector','운동벡터 / 자유벡터','속도·가속도 / 정해진 벡터를 평행하게 옮겨 그릴 수 있음'),
    ('observed in / expressed in','~에서 관찰한 / ~로 표현한','물리량의 관찰자 / 그 물리량을 적는 기저'),
    ('with respect to / attached to','~에 대하여 / ~에 고정된','관측 기준을 지정 / 축이 어느 물체를 따르는지 지정'),
    ('velocity / acceleration','속도 / 가속도','위치의 시간미분 / 같은 기준계에서 본 속도의 시간미분'),
    ('at rest relative to / constant','~에 대해 정지한 / 일정한','해당 기준계에서 속도 0 / 시간에 따라 값이 불변'),
    ('pendulum / pivot / tip','진자 / 회전 지지점 / 끝점','길이 L의 물체 / 공통 원점 O / 관심 점 P'),
    ('arm / slider / sliding speed','팔 / 슬라이더 / 미끄럼 속력','회전 부재 / 부재 위로 움직이는 점 B / 팔에서 본 속도의 크기 |ṙ|'),
    ('radial / transverse / tangential','반지름 방향의 / 반지름에 수직인 / 접선 방향의','팔의 a₁ / 반시계 방향인 a₂ / 지정한 곡선의 접선'),
    ('centripetal / Coriolis term','구심의 / 코리올리 항','중심을 향하는 −rθ̇²a₁ / 회전과 미끄럼이 함께 만드는 2ṙθ̇a₂'),
    ('angular velocity / angular acceleration','각속도 / 각가속도','회전하는 물체의 순간 각속도벡터 / 그 벡터의 시간미분'),
    ('counterexample / order-dependent','반례 / 순서에 의존하는','항상 성립한다는 주장을 반박하는 한 예 / 수행 순서에 따라 결과가 달라지는'),
    ('determine / express / differentiate','구하라 / 나타내라 / 미분하라','값이나 식을 결정 / 지정한 기저로 기술 / 관찰 기준계에서 시간미분'),
]
audit = [
    ('Overview 00:17–00:58 · 6–7장','fuku / Focus pendulum; inertia / neutral reference frame','Foucault pendulum(푸코 진자); inertial reference frame(관성 기준계)','Overview 첫 언급과 6–7장의 정의'),
    ('6장','all points have zero acceleration','다른 관성 기준계에서 보는, 기준계에 고정된 점들에 대한 설명','관찰되는 모든 입자의 가속도와 구별'),
    ('Contents 1 05:05–05:24 · 8장','dextron / unit factors','dextral(오른손 방향) / unit vectors(단위벡터)','원본 세 축 및 오른손 규칙'),
    ('Contents 1 11:43–11:48 · 11장','find y once x is given','구속곡선의 가지를 선택해야 y가 하나','x²+y²=L²'),
    ('Contents 1 12:48–14:18 · 13장','Neutron in different frame / P1 B2','N은 지면, C는 원뿔, B는 가상 기준계','원본 n,b,c 축과 영상의 세 기준계 구분'),
    ('15·40·42장','회전을 덧셈으로 표시; 두 순서 사이 등호','회전의 합성은 RᵧRₓ와 RₓRᵧ로 구별','42장 그림, Problem Solving 16:43–17:30'),
    ('Contents 2 00:28–01:18 · 17장','vector v / coordinates P1 P2','일반 벡터 p 및 그 스칼라 성분 pᵢ','슬라이드 기호 사용; 아직 속도에 한정하지 않음'),
    ('Contents 2 05:15–05:22 · 21장','motion vector doesn’t depend on the origin','이미 구한 벡터의 평행 이동으로 한정','새로 택한 움직이는 원점에서의 상대속도와 구별'),
    ('30장','Integrate twice','위치를 관찰 기준계에서 한 번 미분','문제의 요구와 05:52–08:05 풀이'),
    ('31장','position vectors are identical','같은 출발점 O와 같은 끝점 P에 한함','두 예제에서 공통 원점 O 사용'),
    ('35장','body reference frame of pendulum','회전 팔의 body frame(물체 기준계) A','34장과 Problem Solving 10:25–10:39'),
    ('36–39장','OB와 OP, 점 B와 P 혼용','슬라이더 B와 위치벡터 OB로 통일','32장의 미지수 및 그림의 B'),
    ('39장','−ṙθ̇² 및 ṙθ̈','−rθ̇² 및 rθ̈; 혼합항은 2ṙθ̇','38장의 직교 성분, 곱의 미분법 및 가속도의 단위'),
    ('Summary 00:49–01:06','drag cosine Matrix','direction cosine matrix(방향코사인행렬)로 해석','좌표계 사이의 관계를 다룬다는 문맥과 다음 강의 원본의 용어'),
]

roadmap = '''<section class="editorial-section section-divider" id="course-roadmap" aria-labelledby="roadmap-title">
<p class="section-kicker">Summary video · Course roadmap</p>
<h2 class="section-title" id="roadmap-title">Summary 영상 후반 · 다음 강의에서는 3차원 자세를 표현합니다.</h2>
<p class="section-lead">00:17–00:46에 복습한 기준계, 벡터 미분, 유한 회전의 순서 문제는 위 핵심 개념 요약에 반영했습니다. 00:49 이후는 이번 문제의 풀이가 아니라 다음 강의 안내입니다.</p></section>
<section class="editorial-section" id="roadmap-detail" aria-labelledby="roadmap-detail-title">
<p class="section-kicker">What comes next</p><h2 class="section-title" id="roadmap-detail-title">축 사이의 관계를 행렬로 나타내는 방법</h2>
<div class="card"><h3>Lecture 10 · Kinematics of Rigid Bodies II(강체 운동학 II)</h3><p>영상은 두 좌표계의 축을 연결하는 direction cosine matrix(방향코사인행렬), Euler angles(오일러각), rotation matrix(회전행렬)를 예고합니다. 이번 강의에서는 회전 순서가 결과를 바꾼다는 사실까지 이해하면 됩니다. 행렬을 구성하고 3차원 각속도를 구하는 절차는 다음 단원의 내용입니다.</p></div>
<div class="evidence"><span>Summary 00:49–01:06</span><span>강의 인덱스 · Week 10, 2026-11-04</span></div></section>'''


def fill(part, values):
    return re.sub(r'\{\{([^{}]+)\}\}', lambda m: values[m[1]], part)


def build():
    template = (SITE / 'templates/lecture-page.template.html').read_text(encoding='utf-8')
    template = re.sub(r'\s*<!--[\s\S]*?-->', '', template)
    slide = re.search(r'<section class="source-section"[\s\S]*?</section>', template).group()
    assert len(records) == 44
    sections = []
    for n, (title, evidence, blocks, role) in enumerate(records, 1):
        sections.append(fill(slide, dict(NN=f'{n:02d}', SLIDE_ROLE=role, SLIDE_HEADING=title,
            LECTURE_SLUG='lecture09', DESCRIPTIVE_ALT_TEXT=escape(f'Lecture 9 원본 슬라이드 {n:02d}: {title}'),
            CURRENT_PAGE=str(n), PAGE_COUNT='44', TRANSCRIPT_TIME_OR_SLIDE_ROLE=evidence, SLIDE_EXPLANATION_BLOCKS=blocks)))
    template = template.replace(slide, '\n\n'.join(sections))
    exam = re.search(r'<div class="exam-card">[\s\S]*?</p>\s*</div>', template).group()
    template = template.replace(exam, '\n'.join(fill(exam, dict(EXAM_QUESTION=q, MODEL_ANSWER=escape(a),
        KOREAN_ANSWER_EXPLANATION=fmt(ko))) for q, a, ko in exams))
    toc = [('overview','전체 개요'),('concept-map','개념 지도'),('concept-summary','핵심 개념 요약')] + [
        (f'slide-{n:02d}',f'{n:02d} · {record[0]}') for n,record in enumerate(records,1)] + [
        ('course-roadmap','Summary · 다음 단원'),('exam-english','시험 영어'),('glossary','용어집'),
        ('asr-log','원본·자막 교정'),('sources','출처')]
    pdf_url = 'https://github.com/leejinh0225/MC2103-Dynamics/raw/refs/heads/main/2026FA_Dynamics/lecture_notes/lecture09_note.pdf'
    source = '<ul class="plain-list"><li><a href="'+pdf_url+'">Lecture 9 원본 PDF</a> · MC2103 · 2026-10-28 · 44장</li>' + ''.join(
        f'<li><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{label} 영상</a> · 영어 자동생성 자막 원문</li>'
        for label,vid in videos) + '</ul>'
    source += p('영어 자동자막 5편(943개 시간 구간)을 2026-11-01 확보해 원본 슬라이드와 대조했습니다. 슬라이드 아래 시각은 설명이 관련되는 영상 구간이며 정확한 화면 전환 시각을 뜻하지 않습니다. 3장의 보조 영상은 링크만 보존했고 44장의 교재는 참고문헌 목록으로만 사용했습니다.')
    source += p('핵심 개념 요약에는 Summary 영상의 이번 강의 복습을 반영했습니다. 연쇄법칙·곱의 미분 전개, 단위와 고정 반지름 검산, 회전 순서에 따른 축 방향 추적은 이해와 시험 답안을 위한 보강입니다.')
    template = fill(template, dict(
        LECTURE_NUMBER='Lecture 9', LECTURE_TITLE='Kinematics of Rigid Bodies I',
        ONE_SENTENCE_DESCRIPTION='강체 운동학 I: 기준계에 따른 벡터 미분, 진자·회전 팔·유한 회전을 다루는 한국어 학습 노트',
        WEEK='Week 09', DATE_OR_날짜_미기재='2026-10-28', PAGE_COUNT='44',
        LECTURE_PROMISE='같은 진자 끝점이 지면에서는 움직이고 진자에서는 정지해 보이는 이유를 설명합니다. 회전 팔 위 슬라이더의 속도·가속도를 두 기준계에서 유도하고, 두 번의 회전이 왜 순서에 따라 다른 자세를 만드는지 확인합니다.',
        VIDEO_SET='Overview · Contents 1·2 · Problem Solving · Summary',
        ALL_CONTENTS_AND_PROBLEM_SOLVING_BUTTONS='\n'.join(f'<a class="button button--primary" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{name} 영상 열기</a>' for name,vid in videos[1:4]),
        ORIGINAL_PDF_URL=pdf_url, LECTURE_NOTE_FILENAME='lecture09_note.pdf',
        CORE_RELATIONSHIP_HEADLINE='진자 끝점의 속도가 0이라는 답과 0이 아니라는 답이 모두 맞을 수 있습니다.',
        CORE_RELATIONSHIP_EXPLANATION='진자에 탄 사람에게 끝점은 한자리에 머물고, 지면의 관찰자에게는 원을 따라 움직입니다. Reference frame(기준계)은 누구의 속도를 묻는지를 정하고, coordinate system(좌표계)은 그 답을 어느 축으로 쓸지 정합니다. 이 차이를 알면 회전하는 축을 언제 미분해야 하는지도 결정할 수 있습니다.',
        CONCEPT_MAP_HEADLINE='관찰자를 정하고, 축을 붙이고, 그 기준계에서 미분합니다.',
        CONCEPT_MAP_BLOCKS='<div class="grid-3">' + card('Reference frame(기준계)','누구와 함께 움직이는가? 지면 N, 물체 A, 분석을 위한 가상 기준계를 구분합니다.') + card('Coordinate(좌표)','어떤 축과 수로 쓰는가? 한 위치를 여러 기저로 쓰고 독립적인 좌표의 수를 셉니다.') + card('Time derivative(시간미분)','무엇이 변하는가? 관찰자에게 돌아가는 기저는 성분과 함께 미분합니다.') + '</div>',
        STANDALONE_CONCEPT_SUMMARY=summary, DISTINCT_SUMMARY_VIDEO_SECTION_IF_NEEDED=roadmap,
        EXAM_SECTION_TITLE='관찰 기준과 회전 순서를 설명하는 영어 답안',
        BILINGUAL_GLOSSARY_TABLE=table(['영어(한국어)','의미와 사용'],[(f'{en}({ko})', desc) for en,ko,desc in terms]),
        AUDIT_SECTION_TITLE='원본 슬라이드·영어 자동자막 교정 기록',
        ASR_CORRECTION_TABLE=p('원본 이미지와 영어 자동자막 파일은 그대로 보존했습니다. 아래는 한국어 해설에서 채택한 용어·조건·수식과 그 근거입니다. 자막의 표기가 실제 발화인지 음성 인식 오류인지는 단정하지 않습니다.') + table(['위치','원문 또는 쟁점','본문 처리','근거'], audit),
        SOURCE_LIST_AND_PROVENANCE_NOTE=source, TABLE_OF_CONTENTS_LINKS=''.join(f'<li><a href="#{key}">{val}</a></li>' for key,val in toc)))
    template = template.replace('이 부분만 읽어도 렉처의 핵심 정의, 개념 관계, 가정과 풀이 흐름을 이해할 수 있도록 작성합니다.',
        '기준계와 좌표를 구별하는 법에서 시작해 진자·슬라이더의 답과 유한 회전의 반례까지 연결합니다. 각 유도와 그림은 아래 원본 슬라이드별 해설에서 이어집니다.')
    (SITE / 'lecture09.html').write_text(template, encoding='utf-8')
    print(f'Built Lecture 9: {len(records)} slides, {len(exams)} English answers, {len(terms)} glossary entries.')


if __name__ == '__main__':
    build()
