"""Fill the fixed lecture template with Lecture 10 source-reviewed Korean notes."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT/'site'
records = []
videos = [('Overview','8-cbq84asB4'),('Contents 1','XcUjJyywyfU'),
          ('Contents 2','QnkRdVLMy8o'),('Problem Solving','PsLITXfcJug'),('Summary','GeIUzTOQs1c')]
C = '<sup>A</sup>R<sup>B</sup>'
CT = '(<sup>A</sup>R<sup>B</sup>)ᵀ'
PA, PB = '[p]<sub>A</sub>', '[p]<sub>B</sub>'
QA, QB = '[AB]<sub>A</sub>', '[AB]<sub>B</sub>'


def p(s):
    return s if s.startswith('<table') else '<p>'+s+'</p>'


def card(title,*body,kind='card'):
    return f'<div class="{kind}"><h3>{title}</h3>'+''.join(map(p,body))+'</div>'


def formula(s):
    return '<span class="formula">'+s+'</span>'


def table(head, rows, caption=''):
    return '<table class="term-table">'+('<caption>'+caption+'</caption>' if caption else '')+'<thead><tr>'+''.join(
        '<th scope="col">'+s+'</th>' for s in head)+'</tr></thead><tbody>'+''.join(
        '<tr>'+''.join('<td>'+s+'</td>' for s in row)+'</tr>' for row in rows)+'</tbody></table>'


def matrix(name, rows):
    return table(['1열','2열','3열'],rows,caption=name+' — 각 줄이 행렬의 한 행입니다.')


def add(n,title,time,*body,eq='',extra='',correction='',role='Concept'):
    assert n==len(records)+1
    blocks = card('원본 교정 · 적용 조건',correction,kind='callout') if correction else ''
    blocks += card('핵심 해설' if role=='Concept' else '슬라이드 안내',*body,
                   kind='card' if role=='Concept' else 'quiet-card')
    if eq:
        blocks += card('식과 기호',formula(eq))
    records.append((title,time,blocks+extra,role))


MREL = [['0.866','0.250','0.433'],['0','0.866','−0.500'],['−0.500','0.433','0.750']]
MBODY = [['0.750','−0.217','0.625'],['0.433','0.875','−0.217'],['−0.500','0.433','0.750']]
MSPACE = [['0.750','−0.433','0.500'],['0.650','0.625','−0.433'],['−0.125','0.650','0.750']]
summary = ''.join([
    card('1. 자세를 알면 물체에 붙인 세 축이 향하는 방향을 알 수 있습니다.',
         'Orientation 또는 attitude(자세)는 rigid body(강체)가 어느 방향을 향하는지입니다. 물체의 위치와는 다릅니다. 제자리에 놓인 주사위도 돌리면 자세가 바뀝니다. 기준 자세의 오른손 정규직교축을 a₁,a₂,a₃, 비교할 자세의 축을 b₁,b₂,b₃라 정하고 두 축 집합의 관계를 수로 나타냅니다.',
         '물체를 먼저 x축, 다음 y축으로 돌리는 결과와 그 순서를 뒤집은 결과는 일반적으로 다릅니다. 따라서 세 각도를 보통 벡터의 성분처럼 더할 수 없습니다. 이 강의는 그 대신 direction cosine matrix(방향코사인행렬)와 Euler angles(오일러각)를 사용합니다.',kind='callout'),
    card('2. 방향코사인행렬은 축끼리의 내적을 모은 표입니다.',
         f'Direction cosine matrix(방향코사인행렬) C={C}의 i행 j열은 cᵢⱼ=aᵢ·bⱼ입니다. 축은 unit vectors(단위벡터)이므로 내적은 두 축 사이 각의 cos입니다. 같은 방향은 1, 수직은 0, 반대 방향은 −1입니다. j열은 bⱼ를 A축으로 나타낸 성분이고 i행은 aᵢ를 B축으로 나타낸 성분입니다.',
         f'같은 화살표 p의 coordinate vector(좌표벡터)를 {PA}, {PB}라 쓰면 {PA}=C{PB}입니다. 오른쪽에 B성분을 넣어 왼쪽의 A성분을 얻습니다. C를 “A에서 B로 가는 행렬”이라고만 외우지 말고, 이 입력·출력 식을 먼저 적어야 전치 방향을 실수하지 않습니다.'),
    card('3. 원소는 아홉 개이지만 독립적인 자세 정보는 세 개입니다.',
         '각 행의 길이가 1이라는 조건이 세 개이고 서로 다른 두 행의 내적이 0이라는 조건이 세 개입니다. 따라서 행렬의 아홉 원소에는 여섯 제약이 있습니다. 세 개의 독립적인 변수로 3차원 자세를 매개화할 수 있지만, 행렬의 아무 원소 세 개나 고르면 나머지가 항상 유일하게 정해진다는 뜻은 아닙니다.',
         'Orthogonal matrix(직교행렬)는 RᵀR=I를 만족하므로 inverse(역행렬)가 transpose(전치행렬)와 같습니다. 즉 R⁻¹=Rᵀ이며 행과 열을 바꾸면 역변환입니다. 시험용 보강: 오른손 축 사이의 순수 회전은 det R=+1도 만족합니다. 길이·각도를 보존해도 det R=−1인 반사까지 회전이라고 부르지는 않습니다.'),
    card('4. 하나의 축을 돌릴 때는 그 축 성분이 그대로 남습니다.',
         'X(θ), Y(φ), Z(ψ)는 각각 x,y,z축에 대한 right-hand rotation(오른손 방향 회전)입니다. 예를 들어 Z(ψ)는 (x,y,z)를 (x cosψ−y sinψ, x sinψ+y cosψ, z)로 보냅니다. z값은 그대로이고 x,y 평면만 돕니다. Z(90°)(1,0,0)ᵀ=(0,1,0)ᵀ로 부호를 확인할 수 있습니다.',
         'X(θ)에서는 x를 유지하고 y,z를 돌립니다. Y(φ)에서는 y를 유지하고 x′=x cosφ+z sinφ, z′=−x sinφ+z cosφ입니다. Y행렬의 sin 부호는 X나 Z의 작은 정사각형을 그대로 복사해 정하면 틀리기 쉽습니다.'),
    card('5. 오일러각은 각도 세 개뿐 아니라 순서와 축 종류까지 필요합니다.',
         'Euler angles(오일러각)는 세 번의 consecutive rotations(연속 회전)으로 자세를 나타냅니다. Body/intrinsic axis(물체/내재축)는 물체와 함께 돌아가는 현재 축이고, space/extrinsic axis(공간/외재축)는 처음 정한 방향을 유지하는 축입니다. 문제의 new axis(새 축)는 전자, original axis(원래 축)는 후자를 가리킵니다.',
         '몸에 붙은 x축 다음 새 y축 다음 새 z축이면 R=X(θ)Y(φ)Z(ψ)입니다. 새 회전을 오른쪽에 붙이는 postmultiplication(후곱)입니다. 원래 x축 다음 원래 y축 다음 원래 z축이면 R=Z(ψ)Y(φ)X(θ)입니다. 새 회전을 왼쪽에 붙이는 premultiplication(전곱)입니다.'),
    card('6. 행렬은 오른쪽부터 작용하는데 물체축에서는 왜 순서대로 쓰는가',
         '시험용 보강: 현재 자세행렬을 R, 다음 물체축 회전을 Q라 둡니다. 이 회전의 축 자체가 이미 R만큼 돌아가 있으므로 고정축에서 같은 회전은 RQRᵀ입니다. 현재 자세에 작용시키면 (RQRᵀ)R=RQ가 되어 새 행렬이 오른쪽에 붙습니다. 공간축이면 새 회전 S를 그대로 적용하므로 SR입니다.',
         '따라서 “물체축 후곱”은 행렬 곱셈 규칙의 예외가 아닙니다. 축이 움직인다는 조건을 반영한 결과입니다. 세 회전의 축과 각도 쌍을 통째로 역순으로 나열하면 body-axis sequence(물체축 순서)와 space-axis sequence(공간축 순서)가 같은 최종 자세를 만들 수 있습니다. 이것은 원래 자세로 되돌리는 inverse rotation(역회전)과 다릅니다.'),
    card('7. 예제 1·2: 축의 내적과 회전의 합성으로 자세행렬을 구합니다.',
         f'비행 시뮬레이터에서 N은 지면, A는 control cube(제어 상자), B는 cab(탑승실)입니다. A축과 B축이 모두 N성분으로 주어지면 aᵢ·bⱼ를 계산해 {C}를 만듭니다. 예를 들어 c₁₁=0.866×0.750+0.500×0.433≈0.866입니다. 아래 세 행이 예제 1의 상대 자세입니다.',
         matrix(C+' ≈',MREL),
         '예제 2의 z→y→x 회전은 모두 30°입니다. New axes(새 축들)이면 Z(30°)Y(30°)X(30°), original axes(원래 축들)이면 X(30°)Y(30°)Z(30°)입니다. 첫 행만 비교해도 각각 (0.750, −0.217, 0.625), (0.750, −0.433, 0.500)으로 다른 자세입니다.'),
    card('8. 예제 3: 같은 AB의 좌표만 바꿀 때는 전치가 필요합니다.',
         f'문제에서 {QA}=(0.683,0.366,1.183)ᵀ를 주고 {QB}를 묻습니다. 기본식 {QA}=C{QB}에서 왼쪽에 C⁻¹=Cᵀ를 곱하면 {QB}=Cᵀ{QA}≈(0,1,1)ᵀ입니다. 이때 화살표 AB는 움직이지 않았고 성분을 재는 축만 바꿨습니다.',
         'AB는 항상 점 A에서 점 B까지의 같은 displacement vector(변위벡터)입니다. 축을 그린 원점 위치는 이 벡터의 기저변환에 영향을 주지 않습니다. 반면 서로 다른 원점에서 같은 점까지 잰 위치좌표를 바꾸는 문제라면 원점 사이의 translation(병진)도 따로 더해야 합니다.'),
    card('9. 예제 4: 실제로 돌린 뒤에는 같은 고정 축에서 결과를 읽습니다.',
         '원본은 (0,1,1)ᵀ를 x축에 대해 +45° 돌려 X(45°)(0,1,1)ᵀ=(0,0,√2)ᵀ≈(0,0,1.414)ᵀ를 구합니다. y성분은 cos45°−sin45°=0이고 z성분은 sin45°+cos45°=√2입니다. 회전 전후 길이는 √2로 같습니다.',
         '여기서 b₁,b₂,b₃는 추가 회전 직전 방향에 고정해 둔 측정 축입니다. 물체와 함께 새로 회전한 축으로 답을 읽으면 물체에 붙은 점의 성분은 계속 (0,1,1)입니다. “같은 벡터·다른 축”인 예제 3과 “다른 벡터·같은 축”인 예제 4를 분리해 읽는 것이 이 강의의 핵심입니다.'),
])

add(1,'강체 운동학 II','원본 표지','Orientation(자세)을 direction cosine matrix(방향코사인행렬)와 Euler angles(오일러각)로 나타내고, 같은 행렬을 좌표변환과 실제 회전에 각각 사용하는 방법을 다룹니다.',role='Cover')
add(2,'Lecture 10-1 · 주사위와 로봇의 자세','Overview 00:17–00:46',
    '주사위의 어느 면이 위를 향하는지, 로봇의 끝단이 어느 방향을 향하는지를 수로 표현하려면 orientation(자세)의 기준과 매개변수가 필요합니다. Overview는 이러한 응용을 소개합니다.',role='Divider')
add(3,'Overview 보조 영상 링크','원본 링크 페이지',
    '<a href="https://youtu.be/55yHll1Adfc" target="_blank" rel="noreferrer">원본에 수록된 보조 영상 열기</a>. 이 링크는 본강의 5편과 별도로 보존합니다.',role='Link')
add(4,'Lecture 10-2 · 방향코사인행렬','Contents 1','기준 자세와 회전한 자세의 축을 비교하여 orientation(자세)을 나타내는 아홉 개의 수를 구성합니다.',role='Divider')
add(5,'지난 강의의 기준계에서 이번 강의의 자세 표현으로','Contents 1 00:17–00:34',
    'Lecture 9에서는 reference frame(기준계)에 따라 벡터의 시간미분이 달라지고, 3차원 finite rotation(유한 회전)은 보통 벡터의 덧셈처럼 순서를 바꿀 수 없음을 배웠습니다. 이번에는 어떤 자세에 도달했는지를 계산 가능한 형태로 표현합니다.',
    '로봇·항공기·인공위성의 위치를 안다고 방향까지 아는 것은 아닙니다. 여기서 구하는 것은 orientation(자세)이며, 힘이나 토크로 그 회전이 왜 생겼는지를 구하는 문제는 아닙니다.')
add(6,'자세도 비교할 기준이 있어야 수로 나타낼 수 있습니다.','Contents 1 00:37–01:02',
    'Orientation 또는 attitude(자세)는 강체가 공간에서 향하는 방향입니다. Position(위치)을 원점에 대해 재듯, 자세는 reference orientation(기준 자세)에 대해 잽니다. 같은 물체도 무엇을 기준으로 보느냐에 따라 상대 자세를 나타내는 수가 달라집니다.',
    '시험용 보강: 주사위를 회전시키지 않고 오른쪽으로 밀면 위치만 바뀝니다. 제자리에서 돌리면 기준점의 위치를 유지하면서 자세만 바뀔 수 있습니다. 이 강의의 행렬은 두 번째 변화인 방향 관계를 나타냅니다.')
add(7,'자세는 순서에 의존하는 회전으로 만들어집니다.','Contents 1 01:08–04:15',
    '원본은 +y를 향하는 막대를 x축으로 90°, 이어 y축으로 90° 돌리는 경우와 그 반대 순서를 비교합니다. Fixed axes(고정축)를 기준으로 첫 경우는 +y→+z→+x, 둘째는 +y→+y→+z가 됩니다. 같은 각도들을 사용해도 최종 방향이 다릅니다.',
    '“Orientation is not a vector(자세는 벡터가 아니다)”는 회전을 평범한 벡터합으로 취급할 수 없다는 뜻입니다. 자세를 숫자나 행렬로 표현할 수 없다는 뜻은 아닙니다. 이후 행렬의 noncommutativity(비가환성)가 이 순서 차이를 그대로 담습니다.')
add(8,'물체에 붙인 세 축으로 자세를 추적합니다.','Contents 1 04:17–04:33',
    'Rigid body(강체)에 body-attached coordinate system(물체에 고정된 좌표계)을 붙입니다. 물체가 회전하면 세 축도 같은 회전을 합니다. 그러므로 물체 표면의 모든 점을 나열하는 대신 세 축이 어디를 향하는지 기술하면 자세를 알 수 있습니다.',
    '두 기준계에 고정된 축은 모두 right-handed orthonormal basis(오른손 정규직교 기저)로 정합니다. 이후 투영과 역변환은 이 단위 길이·수직 조건을 사용합니다.')
add(9,'회전 전 세 축을 기준 자세로 남겨 둡니다.','Contents 1 04:37–05:30',
    'a₁,a₂,a₃의 triad(세 축 묶음)는 기준 자세에서의 x,y,z 방향입니다. Triad(세 축 묶음)라는 말은 여기서 서로 수직인 단위벡터 세 개를 함께 다룬다는 뜻입니다.',
    '기준 자세를 정한 다음 강체를 회전합니다. 물체를 돌린 후에도 비교를 위해 회전 전 방향의 a축을 기준으로 유지합니다. 회전 전후 축에 같은 이름만 쓰면 둘의 관계를 적기 어려워집니다.')
add(10,'회전한 자세의 축을 b₁,b₂,b₃로 구분합니다.','Contents 1 05:32–07:18',
    '영상은 동일한 물체의 회전 전후를 구별하려고 b₁,b₂,b₃라는 이름을 새로 붙였다고 설명합니다. 반드시 서로 다른 두 실제 물체가 있어야 하는 것은 아닙니다. 같은 물체의 기준 자세와 현재 자세를 비교해도 됩니다.',
    'Direction cosine matrix(방향코사인행렬)는 두 축 집합 사이의 방향 관계를 담습니다. 본문에서는 12·29·30장의 정의에 맞춰 cᵢⱼ=aᵢ·bⱼ로 고정하며, 성분 변환의 방향은 식으로 확인합니다.',
    correction='원본의 “maps a to b”는 축의 상대 자세를 연결한다는 설명입니다. 숫자 좌표벡터의 입력·출력은 반대로 보일 수 있으므로, 이 강의의 정의에서는 [p]A=C[p]B임을 명시합니다.')
add(11,'축 하나를 다른 세 축으로 투영하면 한 행이 만들어집니다.','Contents 1 07:20–11:00',
    'a₁을 B기저로 분해합니다. b₁ 방향의 signed scalar projection(부호 있는 스칼라 투영)은 a₁·b₁이며 여기에 b₁을 곱하면 그 방향의 벡터 성분입니다. b₂,b₃ 방향 성분까지 더하면 원래 a₁이 복원됩니다.',
    '같은 절차를 a₂,a₃에도 적용합니다. 서로 수직인 unit vectors(단위벡터)이기 때문에 각 내적이 바로 성분이 됩니다. 내적 자체는 수이고, 그 수에 축을 곱한 항은 벡터입니다.',
    eq='aᵢ=(aᵢ·b₁)b₁+(aᵢ·b₂)b₂+(aᵢ·b₃)b₃<br>cᵢⱼ=aᵢ·bⱼ=cos∠(aᵢ,bⱼ)')
add(12,'방향코사인 표는 행으로도, 열로도 읽습니다.','Contents 1 11:02–15:49',
    'i행을 가로로 읽으면 aᵢ=cᵢ₁b₁+cᵢ₂b₂+cᵢ₃b₃입니다. j열을 세로로 읽으면 bⱼ=c₁ⱼa₁+c₂ⱼa₂+c₃ⱼa₃입니다. 같은 표가 두 축 표현을 모두 제공하지만, 어떤 쪽의 축을 구하려는지에 따라 행과 열을 구분해야 합니다.',
    '원본은 세 벡터를 세로로 쌓은 표기를 abuse of notation(편의상 확장한 표기)이라고 설명합니다. 이를 숫자 세 개짜리 좌표벡터와 혼동하지 않도록 각 줄을 앞 장의 벡터 등식으로 읽습니다. 29장의 숫자 좌표벡터 곱셈에서는 보통의 행렬 곱을 그대로 씁니다.',
    extra=table(['A축 / B축','첫째 축','둘째 축','셋째 축'],[['a₁','a₁·b₁','a₁·b₂','a₁·b₃'],['a₂','a₂·b₁','a₂·b₂','a₂·b₃'],['a₃','a₃·b₁','a₃·b₂','a₃·b₃']]))
add(13,'행의 길이와 수직 관계가 여섯 개의 제약을 만듭니다.','Contents 1 15:53–18:24',
    '각 row(행)는 A축 하나를 B축으로 표현한 성분입니다. 원래 A축 길이가 1이므로 각 행의 제곱합도 1입니다. 서로 다른 A축끼리는 수직이므로 그 성분 행끼리의 내적도 0입니다.',
    '길이 제약 세 개와 서로 다른 축 쌍 (1,2),(1,3),(2,3)의 직교 제약 세 개를 합치면 여섯 개입니다. 0인지 비교하는 값은 행렬 원소 하나가 아니라 행끼리 내적한 합입니다.',
    eq='Σⱼcᵢⱼ²=1 (i=1,2,3)<br>Σⱼc₁ⱼc₂ⱼ=Σⱼc₁ⱼc₃ⱼ=Σⱼc₂ⱼc₃ⱼ=0')
add(14,'독립적인 자세 변수는 세 개이며, 아홉 원소를 마음대로 고르지는 못합니다.','Contents 1 18:27–19:19',
    '아홉 원소에 여섯 독립 제약이 있으므로 orientation(자세)의 degrees of freedom(자유도)은 3입니다. 이것이 다음 절에서 회전 각도 세 개를 사용하는 이유입니다. 위치까지 포함한 강체의 배치와, 위치를 제외한 자세의 자유도를 구별합니다.',
    '시험용 보강: “세 값으로 정한다”는 말에는 사용할 회전 순서와 축 규약을 정했다는 전제가 있습니다. 같은 축을 360° 더 돌리면 같은 자세이므로, 서로 다른 각도 세트가 같은 자세를 나타낼 수도 있습니다. 행렬의 임의의 원소 세 개가 항상 충분하다는 뜻도 아닙니다.')
add(15,'Lecture 10-3 · 오일러각과 회전행렬','Contents 2',
    '세 번의 회전을 구성하고 순서대로 합성한 뒤, 얻은 행렬로 좌표를 바꾸거나 점을 실제로 회전시키는 방법을 다룹니다.',role='Divider')
add(16,'오일러각은 세 번의 회전으로 자세를 매개화합니다.','Contents 2 00:17–01:23',
    'Parameterization(매개화)은 원하는 상태를 몇 개의 변수로 기술하는 것입니다. Euler angles(오일러각)는 3차원 자세를 세 번의 consecutive rotations(연속 회전)의 각도로 나타내는 방식입니다. 세 각도는 해당 규약 아래 자세를 정하지만 그 자체를 보통의 3차원 벡터처럼 합치지는 않습니다.',
    '원본과 영상은 여러 방법 중 한 가지라고 설명합니다. 이 강의에서는 세 번의 회전 축과 각도를 지정한 후 각 단순 회전행렬을 곱하는 방식을 사용합니다. 각도만 적고 축의 순서를 생략하면 자세가 정해지지 않습니다.')
add(17,'x회전 θ, y회전 φ, z회전 ψ를 서로 다른 변수로 둡니다.','Contents 2 01:27–02:04',
    '예시의 시간 순서는 x축에 대한 θ, 그다음 y축에 대한 φ, 마지막 z축에 대한 ψ입니다. Followed by(~가 뒤따르는)는 앞의 회전이 먼저이고 뒤의 회전이 다음이라는 뜻입니다.',
    '이 문장만으로는 아직 각 축이 original(처음의 방향을 유지하는)인지 new(앞 회전으로 바뀐)인지 구분되지 않았습니다. 다음 장에서 body axis(물체축)와 space axis(공간축)를 추가해 회전 규약을 완성합니다.',
    correction='원본은 첫째·둘째 회전각을 모두 θ로 인쇄했지만 영상 01:35–01:52와 21–23장의 행렬은 x:θ, y:φ, z:ψ입니다. 본문도 이 세 기호를 구분합니다.')
add(18,'인접한 두 축을 다르게 택하면 12가지 축 순서가 됩니다.','Contents 2 02:08–06:19',
    'Body axis(물체축)는 물체와 함께 돌고 space axis(공간축)는 바깥에 고정됩니다. 둘 중 하나를 정한 뒤 세 회전의 축 순서를 고릅니다. 이 강의는 XYZ처럼 세 축이 모두 다른 경우와 XYX처럼 첫째·셋째가 같은 경우를 함께 Euler angles(오일러각)로 부릅니다.',
    '첫 축 선택은 3가지, 둘째는 앞 축을 제외한 2가지, 셋째도 바로 앞 축을 제외한 2가지이므로 3×2×2=12가지입니다. 축 종류까지 붙이면 24가지 표현 규약입니다. 24개의 서로 다른 자세만 가능하다는 뜻은 아니며 각 회전각은 연속적으로 달라질 수 있습니다.',
    'ZZY처럼 같은 축이 연달아 나오면 앞의 Z회전 두 개는 각도를 합친 한 번의 회전입니다. 영상의 30°+20°는 50°가 되어 독립적인 회전 변수가 줄어듭니다. 회전 동작 자체가 불가능한 것이 아니라 일반적인 3변수 자세 표현으로는 부족하다는 뜻입니다.',
    eq='모두 다른 축: XYZ, XZY, YXZ, YZX, ZXY, ZYX<br>첫째·셋째 같은 축: XYX, XZX, YXY, YZY, ZXZ, ZYZ')
add(19,'시험의 new와 original은 행렬을 붙이는 쪽을 결정합니다.','Contents 2 06:25–08:01',
    'Local/relative/intrinsic axis(국소/상대/내재축)는 이 강의에서 body axis(물체축)를 가리키는 표현입니다. 첫 회전을 하고 나면 둘째에 사용할 축도 이미 방향이 바뀌어 있습니다. New y-axis(새 y축)는 바로 그 갱신된 물체축입니다.',
    'Global/absolute/extrinsic axis(전역/절대/외재축)는 space axis(공간축)의 표현입니다. 물체가 돌아도 회전에 사용할 축은 처음 정한 방향을 유지합니다. 여기서 absolute(절대)는 우주에 유일한 기준이 있다는 뜻이 아니라 문제에서 고정한 축이라는 뜻입니다.',
    extra=table(['문제의 표현','축의 의미','행렬 갱신'],[
        ['new / current / body / intrinsic(새 / 현재 / 물체 / 내재)','물체를 따라 변한 축','R → RQ: postmultiplication(후곱)'],
        ['original / fixed / space / extrinsic(원래 / 고정 / 공간 / 외재)','처음 방향을 유지하는 축','R → QR: premultiplication(전곱)']]))
add(20,'단순 회전행렬은 한 축을 고정하고 나머지 두 방향을 돌립니다.','Contents 2 08:09–08:37',
    'Simple rotation matrix(단순 회전행렬)는 x,y,z 중 한 축에 대한 회전을 나타냅니다. 그 축 방향 성분은 변하지 않고, 수직인 평면의 두 성분이 sin과 cos로 섞입니다. 모든 각도는 right-hand rule(오른손 규칙)을 따릅니다.',
    '양의 축 쪽에 서서 원점을 바라보면 양의 회전이 반시계로 보입니다. 보는 쪽을 뒤집으면 화면상 회전 방향도 뒤집히므로, 그림의 시계·반시계 인상만으로 부호를 정하지 않습니다.')
add(21,'x축 회전: x는 그대로이고 y,z가 섞입니다.','Contents 2 08:39–12:57',
    'a₁=b₁은 회전축입니다. b₂는 a₂에서 a₃ 쪽으로 θ만큼 돌아가므로 b₂=cosθ a₂+sinθ a₃입니다. b₃는 b₂와 수직을 유지하여 b₃=−sinθ a₂+cosθ a₃입니다. 이 세 b축의 A성분을 열에 나란히 놓으면 아래 X(θ)를 얻습니다.',
    '예를 들어 (0,1,0)ᵀ를 +90° 회전시키면 (0,0,1)ᵀ입니다. −sinθ는 새 z축이 기존 y축의 음의 방향으로 투영되는 데서 나옵니다. 기억이 불확실할 때에는 θ=90°에서 축이 어디로 가는지로 검산합니다.',
    extra=matrix('X(θ)',[['1','0','0'],['0','cosθ','−sinθ'],['0','sinθ','cosθ']]),
    eq='(x′,y′,z′)=(x, y cosθ−z sinθ, y sinθ+z cosθ)')
add(22,'y축 회전: x,z의 sin 부호를 오른손 규칙으로 확인합니다.','Contents 2 14:20–18:23 · y축 비교 설명',
    '회전축 a₂=b₂는 고정됩니다. 양의 y축 회전에서는 b₃가 a₃에서 a₁ 쪽으로 가므로 b₃=sinφ a₁+cosφ a₃입니다. 이에 직교하는 b₁=cosφ a₁−sinφ a₃의 z성분에는 음수가 붙습니다.',
    '따라서 Y(90°)는 +z를 +x로, +x를 −z로 보냅니다. 이 결과는 y축 주위의 오른손 회전입니다. X나 Z와 달리 행렬의 남는 x,z 두 줄을 위에서 아래로 읽을 때 sin의 부호 위치가 반대인 이유입니다.',
    extra=matrix('Y(φ)',[['cosφ','0','sinφ'],['0','1','0'],['−sinφ','0','cosφ']]),
    eq='(x′,y′,z′)=(x cosφ+z sinφ, y, −x sinφ+z cosφ)')
add(23,'z축 회전: 익숙한 평면 회전을 3차원에 넣습니다.','Contents 2 13:01–18:23 · z축 설명과 행렬 패턴',
    'b₁=cosψ a₁+sinψ a₂이고 b₂=−sinψ a₁+cosψ a₂입니다. a₃=b₃이므로 마지막 성분은 바뀌지 않습니다. 익숙한 2차원 평면 회전행렬에 z방향의 1을 더한 형태입니다.',
    'X,Y,Z 모두 회전축의 대각 원소가 1이고 그 행·열의 나머지는 0입니다. 나머지 두 대각에는 cos가, 대칭인 두 칸에는 부호가 반대인 sin이 들어갑니다. 이 모양을 참고하되 최종 부호는 축의 투영으로 판단합니다.',
    extra=matrix('Z(ψ)',[['cosψ','−sinψ','0'],['sinψ','cosψ','0'],['0','0','1']]),
    eq='Z(90°)(1,0,0)ᵀ=(0,1,0)ᵀ')
add(24,'여러 회전은 더하지 않고 행렬을 곱해 합성합니다.','Contents 2 18:26–19:16',
    'Composition(합성)은 한 회전의 결과에 다음 회전을 적용하는 것입니다. 앞서 정한 유효한 세 축 순서를 사용하면 하나의 3차원 자세를 단순 회전행렬 세 개의 곱으로 표현할 수 있습니다.',
    'Matrix multiplication(행렬 곱셈)은 교환법칙을 일반적으로 만족하지 않습니다. 그래서 원본 7장의 회전 순서 차이를 나타낼 수 있습니다. 덧셈 X+Y+Z로 대체하지 않으며, body axis(물체축)인지 space axis(공간축)인지에 따라 곱하는 순서를 정합니다.')
add(25,'물체축 XYZ 회전은 X(θ)Y(φ)Z(ψ)입니다.','Contents 2 19:19–21:54',
    '회전할 때마다 새롭게 변한 body axes(물체축들)를 사용합니다. 처음 R=I에서 X(θ)를 적용하고, 다음 회전 Y(φ)를 오른쪽에 붙여 R=XY, 마지막에 R=XYZ로 만듭니다. 이것이 postmultiplication(후곱)입니다.',
    '행렬 전개에서는 cθ=cosθ, sθ=sinθ처럼 약기합니다. 먼저 XY의 세 행은 (cφ,0,sφ), (sθsφ,cθ,−sθcφ), (−cθsφ,sθ,cθcφ)입니다. 여기에 Z의 각 열을 내적하면 아래 아홉 원소를 얻습니다. 세 번째 열 (0,0,1)과 곱하면 XY의 세 번째 열이 그대로 남습니다.',
    correction='원본 전개 결과의 (2,3),(3,3) 원소에 cosψ가 적혀 있지만 각각 −sinθ cosφ, cosθ cosφ여야 합니다. Z의 세 번째 열은 (0,0,1)ᵀ이므로 결과의 세 번째 열에는 ψ가 들어가지 않습니다.',
    eq='R = X(θ)Y(φ)Z(ψ)',
    extra=card('전개 결과 · 1행',formula('R₁₁=cφcψ<br>R₁₂=−cφsψ<br>R₁₃=sφ'))+
          card('전개 결과 · 2행',formula('R₂₁=cθsψ+sθsφcψ<br>R₂₂=cθcψ−sθsφsψ<br>R₂₃=−sθcφ'))+
          card('전개 결과 · 3행',formula('R₃₁=sθsψ−cθsφcψ<br>R₃₂=sθcψ+cθsφsψ<br>R₃₃=cθcφ'))+
          card('시험용 보강 · 후곱의 이유','현재 자세 R에서 물체축에 대한 Q회전을 지면 기준으로 바꾸면 RQRᵀ입니다. 이를 현재 자세에 작용시키면 (RQRᵀ)R=RQ입니다. 새 회전축이 이미 돌아가 있다는 조건 때문에 오른쪽에 붙습니다.'))
add(26,'공간축 XYZ 회전은 Z(ψ)Y(φ)X(θ)입니다.','Contents 2 21:58–23:28',
    'Space axes(공간축들)는 처음의 방향을 유지합니다. 같은 고정축 성분으로 쓴 점 p에 X를 먼저 작용시키면 Xp, 다음 Y를 작용시키면 Y(Xp), 마지막 Z를 작용시키면 Z(Y(Xp))입니다. 따라서 R=ZYX입니다. 새 회전이 왼쪽에 붙는 premultiplication(전곱)입니다.',
    '아래도 cθ=cosθ, sθ=sinθ 등의 약기를 씁니다. 첫 두 행은 ψ에 따라 섞이지만 세 번째 행은 마지막 z축 회전의 영향을 받지 않습니다. 25장과 각도가 같아도 축 종류가 달라 일반적으로 결과가 다릅니다.',
    eq='R = Z(ψ)Y(φ)X(θ)',
    extra=card('전개 결과 · 1행',formula('R₁₁=cφcψ<br>R₁₂=−cθsψ+sθsφcψ<br>R₁₃=sθsψ+cθsφcψ'))+
          card('전개 결과 · 2행',formula('R₂₁=cφsψ<br>R₂₂=cθcψ+sθsφsψ<br>R₂₃=−sθcψ+cθsφsψ'))+
          card('전개 결과 · 3행',formula('R₃₁=−sφ<br>R₃₂=sθcφ<br>R₃₃=cθcφ')))
add(27,'직교행렬의 역은 전치이며, 회전은 길이를 보존합니다.','Contents 2 23:32–26:13',
    '원본은 direction cosine matrix(방향코사인행렬)와 rotation matrix(회전행렬)가 같은 수치 행렬로 쓰이지만 의미는 다르다고 설명합니다. 전자는 두 기저의 상대 방향을, 후자는 같은 기저 안에서 점을 다른 위치로 돌리는 동작을 나타냅니다.',
    'Orthogonal(직교인) 행렬에서는 RᵀR=I이므로 R⁻¹=Rᵀ입니다. 한 축의 +30° 회전을 되돌리는 것은 −30° 회전이고, X(−30°)=X(30°)ᵀ로 확인할 수 있습니다. 일반 행렬처럼 역행렬을 복잡하게 계산할 필요가 없습니다.',
    extra=card('시험용 보강 · 순수 회전의 검산','q=Rp이면 qᵀq=pᵀRᵀRp=pᵀp이므로 길이가 같습니다. 서로 다른 두 벡터의 내적도 보존합니다. RᵀR=I 외에 det R=+1이면 오른손 방향을 보존하는 순수 회전입니다. 영상의 SO(3)는 special orthogonal group(특수직교군)입니다.'))
add(28,'같은 벡터 p와 서로 다른 숫자 좌표벡터를 구분합니다.','Contents 2 26:17–27:57',
    f'기하학적인 화살표 p는 하나지만 p=pₐ₁a₁+pₐ₂a₂+pₐ₃a₃=pᵦ₁b₁+pᵦ₂b₂+pᵦ₃b₃로 표현할 수 있습니다. 숫자만 세로로 모은 {PA}와 {PB}는 서로 다른 coordinate vectors(좌표벡터들)입니다. 본문은 이를 대괄호와 아래첨자로 명확히 표시합니다.',
    '두 표현이 같다는 것은 숫자 세 개가 같다는 뜻이 아닙니다. 숫자와 해당 기저를 다시 곱해서 더하면 같은 화살표가 된다는 뜻입니다. 기저 없이 성분만 비교하면 같은 물리량인지 알 수 없습니다.')
add(29,'양변에 a₁을 내적하면 첫 번째 성분 변환식이 나옵니다.','Contents 2 28:08–31:47',
    '앞 장의 벡터 등식에 a₁을 내적합니다. 왼쪽은 pₐ₁(a₁·a₁)+pₐ₂(a₂·a₁)+pₐ₃(a₃·a₁)=pₐ₁입니다. 오른쪽은 (a₁·b₁)pᵦ₁+(a₁·b₂)pᵦ₂+(a₁·b₃)pᵦ₃입니다.',
    'a₂,a₃로도 같은 계산을 하면 세 개의 스칼라 식이 모입니다. 계수는 정확히 cᵢⱼ입니다. 이제 행렬 양쪽의 열은 숫자로 된 좌표벡터이므로 일반적인 행렬 곱셈입니다.',
    eq=f'pₐᵢ=Σⱼcᵢⱼpᵦⱼ<br>{PA}={C}{PB}')
add(30,'A R B는 B성분을 입력받아 A성분을 내놓습니다.','Contents 2 31:49–32:18',
    f'{C}는 “A에 대한 B의 자세”를 나타냅니다. 열마다 b축이 A기저에서 어디를 향하는지가 담겨 있습니다. 따라서 B기저로 쓰인 {PB}에 곱하면 A기저로 쓰인 {PA}가 나옵니다.',
    f'반대로 A성분을 B성분으로 바꾸려면 {PB}={CT}{PA}입니다. 본문 대괄호 표기 [p]A와 원본의 오른쪽 위 A가 붙은 p는 모두 좌표벡터를 뜻합니다. Lecture 9에서 속도 왼쪽 위에 붙였던 관찰 기준계 표시와 기호 위치·역할을 구별합니다.',
    eq=f'{PA}={C}{PB}<br>{PB}={CT}{PA}')
add(31,'같은 축 안에서 (1,0,0)을 실제로 돌리면 (0,1,0)이 됩니다.','Contents 2 32:24–33:31',
    '이번에는 coordinate change(좌표변환)가 아니라 active rotation(능동 회전)입니다. 측정 축을 고정한 채 점을 원점 주위로 +90° 돌립니다. 처음 p=(1,0,0)ᵀ이고 z축 회전 후에는 q=Z(90°)p=(0,1,0)ᵀ입니다.',
    '처음과 나중에 같은 x,y,z축으로 성분을 적습니다. 반대로 점은 그대로 두고 측정 축만 +90° 돌리면 새 축에서의 성분은 (0,−1,0)ᵀ입니다. 뒤 비교는 시험용 보강이며, 실제 점을 돌리는 것과 축을 돌리는 것의 부호 차이를 보여 줍니다.',
    eq='q=Z(90°)p; p=(1,0,0)ᵀ → q=(0,1,0)ᵀ')
add(32,'실제 회전식에서는 입력과 출력의 기저가 같습니다.','Contents 2 33:33–33:38',
    'p<sub>rotated</sub>=Rp<sub>original</sub>에서 original(회전 전)과 rotated(회전 후)는 서로 다른 벡터입니다. 둘을 비교하기 위해 동일한 고정 기저의 숫자 좌표로 나타냅니다.',
    '시험용 보강: 이 단순식은 원점을 지나는 축에 대한 회전입니다. 회전 중심 c가 원점과 다르면 먼저 p−c로 중심까지 옮겨 계산하고 q=c+R(p−c)로 되돌립니다. 이 강의 예제 4는 점 A에서 잰 상대벡터 AB를 써서 A가 회전 중심이 됩니다.')
add(33,'회전행렬을 쓰기 전에 무엇을 바꾸는지 결정합니다.','Contents 2 33:40–34:20',
    f'Basis change(기저변환)에서는 같은 p에 대해 {PA}=C{PB}를 씁니다. 기하학적 벡터는 같고 숫자를 적는 기저가 다릅니다. Active rotation(능동 회전)에서는 q=Rp를 쓰며 기저는 같고 벡터가 다릅니다.',
    '두 식이 같은 형태이므로 행렬 이름만으로 구분되지 않습니다. “Express in terms of(~의 성분으로 나타내라)”인지 “rotate the point(점을 회전시켜라)”인지를 읽고, 결과의 기저와 대상을 미리 표시하면 선택할 식이 정해집니다.',
    extra=table(['구분','고정된 것','달라지는 것'],[['기저변환','기하학적 벡터 p','A성분과 B성분'],['능동 회전','숫자를 재는 기저','회전 전 p와 회전 후 q']] ))

add(34,'Lecture 10-4 · 비행 시뮬레이터 예제','Problem Solving',
    '축의 내적, 연속 회전의 합성, 좌표변환, 실제 점의 회전을 같은 비행 시뮬레이터에서 차례로 계산합니다.',role='Divider')
add(35,'예제 1 · 제어 상자에 대한 탑승실의 상대 자세','Problem Solving 00:17–00:36',
    'Flight simulator(비행 시뮬레이터)의 control cube(제어 상자)와 cab(탑승실)는 서로 다른 방향을 향할 수 있습니다. 문제는 두 물체의 relative orientation(상대 자세)을 direction cosine matrix(방향코사인행렬)로 표현하라고 요구합니다.',
    '위치나 원점 사이의 거리를 구하는 문제가 아닙니다. 각 물체에 붙인 축들의 방향을 알아내고, 두 축 집합 사이의 아홉 내적을 계산하면 됩니다.')
add(36,'예제 1의 절차: 기준계 → 축 → 내적','Problem Solving 00:40–01:31',
    '먼저 움직임을 구분할 reference frames(기준계들)를 정합니다. 다음으로 각 기준계에 right-handed orthonormal axes(오른손 정규직교축)를 붙입니다. 마지막으로 aᵢ·bⱼ를 i행 j열에 넣습니다.',
    '서로 다른 축의 숫자 성분을 내적하려면 두 축이 같은 기저로 표현되어 있어야 합니다. 여기서는 지면 N의 n₁,n₂,n₃ 성분이 공통 언어가 됩니다. A성분으로 쓴 숫자와 B성분으로 쓴 숫자를 그대로 곱하지 않습니다.')
add(37,'N은 지면, A는 제어 상자, B는 탑승실입니다.','Problem Solving 01:34–02:58',
    'Ground frame(지면 기준계) N은 실험실 바닥을 따라갑니다. Control-cube frame(제어 상자 기준계) A와 cab frame(탑승실 기준계) B는 각각의 물체와 함께 움직입니다. N은 A와 B의 축 방향을 공통 성분으로 적는 중간 기준입니다.',
    '두 물체 사이의 자세만 묻더라도 N축으로 각각의 방향을 알면 상대 자세를 계산할 수 있습니다. 이후 행렬의 왼쪽 위 A와 오른쪽 위 B는 이 기준계 표기입니다.')
add(38,'축은 운동을 읽기 편하도록 붙이되 세 방향을 끝까지 유지합니다.','Problem Solving 03:01–05:37',
    'N에 n₁,n₂,n₃, A에 a₁,a₂,a₃, B에 b₁,b₂,b₃를 붙입니다. 회전 지지축과 한 축을 나란히 정하면 그 회전을 단순 회전행렬로 표현하기 쉬워집니다. 나머지 두 축도 서로 직교하고 오른손 방향이 되도록 정합니다.',
    '그림에서 회전축을 설명하는 단순화와 다음 장에서 주어진 실제 수치 자세를 구분합니다. 예제 계산에서는 39장에 명시된 세 축의 N성분을 사용합니다. 그 값에 따르면 b₃에는 수평 성분도 있으므로 b₃=a₃라고 두지 않습니다.')
add(39,'주어진 여섯 축은 모두 N기저의 성분입니다.','Problem Solving 05:38–05:59',
    '아래 표의 한 행은 한 축의 (n₁,n₂,n₃) 성분입니다. 예를 들어 a₁=0.866n₁+0.500n₂, b₁=0.750n₁+0.433n₂−0.500n₃입니다. N축끼리는 정규직교하므로 같은 열끼리 곱해서 더하면 축 사이의 내적입니다.',
    '주어진 값은 소수 셋째 자리로 반올림되었습니다. 따라서 길이의 제곱이 정확히 1이 아니거나 직교하는 축의 내적이 아주 작은 수로 남을 수 있습니다. 중간 계산을 더 정밀한 원자료로 바꾸었다고 가정하지 않고 근삿값으로 표시합니다.',
    extra=table(['축','첫째 성분','둘째 성분','셋째 성분'],[
        ['a₁','0.866','0.500','0'],['a₂','−0.500','0.866','0'],['a₃','0','0','1'],
        ['b₁','0.750','0.433','−0.500'],['b₂','−0.217','0.875','0.433'],['b₃','0.625','−0.217','0.750']]))
add(40,'예제 1 답: 각 행은 a축 하나와 세 b축의 내적입니다.','Problem Solving 06:01–06:59',
    '첫 행은 c₁₁=0.866×0.750+0.500×0.433=0.866000, c₁₂=0.866×(−0.217)+0.500×0.875=0.249578, c₁₃=0.866×0.625+0.500×(−0.217)=0.432750입니다.',
    '둘째 행은 c₂₁=−0.000022, c₂₂=0.866250, c₂₃=−0.500422입니다. 셋째 행은 a₃=(0,0,1)이므로 각 b축의 셋째 성분 −0.500,0.433,0.750을 그대로 읽습니다. 원본은 이를 아래의 간결한 근사 행렬로 제시합니다.',
    extra=matrix(C+' ≈',MREL)+card('시험용 보강 · 공통 기준계로 연결하는 식',
        'N에서 본 A축을 열로 모은 행렬을 U, N에서 본 B축을 열로 모은 행렬을 V라 두면 C=UᵀV입니다. Uᵀ의 i행과 V의 j열을 곱하면 바로 aᵢ·bⱼ가 됩니다. N성분으로 읽은 축들을 먼저 같은 기저로 맞추는 절차를 행렬로 쓴 식입니다.'))
add(41,'내적을 계산하면 상대 자세를 얻습니다.','Problem Solving 07:09–07:38',
    '예제 1은 회전각을 직접 주지 않아도 축의 방향 성분만으로 direction cosine matrix(방향코사인행렬)를 구성할 수 있음을 보여 줍니다. 각 원소에는 두 축 사이 각의 cos라는 기하학적 의미가 있습니다.',
    '같은 수치 행렬은 두 자세 사이의 rotation(회전)을 나타낼 수도 있습니다. 다만 좌표변환과 실제 회전에서 입력·출력의 의미가 같아지는 것은 아닙니다. 예제 3과 4에서 이 차이를 다시 사용합니다.')
add(42,'예제 2 · z, y, x축으로 각각 30°씩 회전합니다.','Problem Solving 07:44–09:25',
    '시간 순서는 z축 30°, 이어 y축 30°, 마지막 x축 30°입니다. 문제는 두 경우를 구별합니다. (a) new axes(새 축들)를 사용하고, (b) original axes(원래 축들)를 사용합니다.',
    '각도가 모두 같아도 회전축이 앞선 회전을 따라 바뀌는지에 따라 최종 자세가 달라집니다. 지금의 z→y→x 순서는 25·26장에서 연습했던 x→y→z 순서와 반대이므로, 공식을 이름만 보고 복사하지 않습니다.')
add(43,'예제 2의 절차: 축 종류를 먼저 결정합니다.','Problem Solving 09:31–10:00',
    'New axes(새 축들)는 body axes(물체축들)입니다. 새 회전행렬을 오른쪽에 붙여 R=Z(30°)Y(30°)X(30°)로 둡니다. Original axes(원래 축들)는 space axes(공간축들)이며 새 행렬을 왼쪽에 붙여 R=X(30°)Y(30°)Z(30°)로 둡니다.',
    '그다음 cos30°=√3/2, sin30°=1/2를 각 행렬에 대입합니다. 행렬의 행과 열을 곱해 최종 아홉 원소를 계산하고, 마지막에 소수로 반올림합니다.')
add(44,'예제 2(a): 새 축 z→y→x는 ZYX입니다.','Problem Solving 10:04–10:48',
    'c=√3/2, s=1/2로 두면 YX의 세 행은 (c,s²,sc), (0,c,−s), (−s,cs,c²)입니다. 여기에 Z를 왼쪽에서 곱합니다. 결과 첫 행은 (c², cs²−sc, c²s+s²)=(3/4,−√3/8,5/8)입니다.',
    '둘째 행은 (sc,s³+c²,s²c−cs)=(√3/4,7/8,−√3/8), 셋째 행은 (−s,cs,c²)=(−1/2,√3/4,3/4)입니다. 이 결과의 각 열은 회전 후 물체축을 회전 전 고정축으로 표현한 성분입니다.',
    eq='R<sub>body</sub>=Z(30°)Y(30°)X(30°)',extra=matrix('Rbody ≈',MBODY))
add(45,'예제 2(b): 원래 축 z→y→x는 XYZ입니다.','Problem Solving 10:50–11:45',
    '이번에는 Z를 먼저 적용한 벡터에 Y, 다시 X를 적용합니다. 따라서 XYZ입니다. YZ의 세 행은 (c²,−cs,s), (s,c,0), (−sc,s²,c)입니다. X를 왼쪽에 곱하면 첫 행은 그대로 (3/4,−√3/4,1/2)입니다.',
    '둘째 행은 (cs+s²c,c²−s³,−sc)=(3√3/8,5/8,−√3/4)입니다. 셋째 행은 (s²−sc²,sc+cs²,c²)=(−1/8,3√3/8,3/4)입니다. 44장의 행렬과 달라서 같은 30° 세 번으로도 다른 자세가 됩니다.',
    eq='R<sub>space</sub>=X(30°)Y(30°)Z(30°)',extra=matrix('Rspace ≈',MSPACE))
add(46,'물체축과 공간축의 역순 대응은 역회전이 아닙니다.','Problem Solving 11:50–12:14',
    'Body-axis z→y→x(물체축 z→y→x) 회전은 space-axis x→y→z(공간축 x→y→z) 회전과 같은 ZYX를 만듭니다. 축 종류를 바꾸면서 축·각도 쌍을 역순으로 쓰면 같은 최종 자세를 표현할 수 있습니다.',
    '시험용 보강: 되돌아가는 inverse rotation(역회전)은 순서만 뒤집지 않습니다. 각도의 부호도 바꿉니다. (Z(ψ)Y(φ)X(θ))⁻¹=X(−θ)Y(−φ)Z(−ψ)입니다. “같은 자세를 다른 규약으로 표현”하는 것과 “처음 자세로 복귀”하는 것을 구분합니다.')
add(47,'예제 3 · 같은 AB를 탑승실 축의 성분으로 바꿉니다.','Problem Solving 12:23–13:25',
    f'문제는 {QA}=(0.683,0.366,1.183)ᵀ를 주고 탑승실 B의 기저 b₁,b₂,b₃로 나타내라고 요구합니다. Express in terms of(~의 성분으로 나타내라)는 여기서 basis change(기저변환)의 지시입니다.',
    'AB의 A와 B는 화살표의 시작점·끝점 이름입니다. 아래첨자 A와 B는 성분을 적는 기준계 이름입니다. 같은 글자를 쓰더라도 역할이 다릅니다. 두 표현에서 AB의 시작점과 끝점은 바뀌지 않습니다.')
add(48,'예제 3의 절차: 상대 자세행렬을 구한 뒤 방향을 뒤집습니다.','Problem Solving 13:28–13:50',
    f'예제 1에서 구한 C={C}를 사용합니다. 그 정의는 {QA}=C{QB}입니다. 주어진 것은 왼쪽의 A성분이고 구할 것은 오른쪽의 B성분이므로 역행렬을 곱해 식을 풉니다.',
    'Orthogonal matrix(직교행렬)이므로 inverse(역행렬)는 transpose(전치행렬)입니다. 외워 둔 “C를 곱한다”가 아니라, 주어진 기저와 원하는 기저를 먼저 식에 적으면 곱할 행렬을 결정할 수 있습니다.')
add(49,'예제 1의 행렬은 B성분을 A성분으로 보냅니다.','Problem Solving 13:51–14:27',
    f'아래 C는 b₁,b₂,b₃를 A기저로 표현한 열들입니다. 따라서 {QB}의 각 성분을 해당 열에 곱해 더하면 {QA}가 됩니다. 예제 1과 같은 상대 자세이므로 새로운 내적을 계산할 필요가 없습니다.',
    extra=matrix(C+' ≈',MREL),eq=f'{QA}=C{QB}')
add(50,'양변에 Cᵀ를 곱하면 원하는 B성분만 남습니다.','Problem Solving 14:30–16:05',
    f'기본식의 양변에 Cᵀ를 왼쪽에서 곱합니다. Cᵀ{QA}=CᵀC{QB}이고 CᵀC=I이므로 오른쪽이 {QB}가 됩니다. 숫자처럼 곱셈 위치를 임의로 옮기지 않습니다.',
    'Transpose(전치)는 행과 열을 바꾸는 연산입니다. C의 첫 열 (0.866,0,−0.500)이 Cᵀ의 첫 행이 되고, 두 번째 열과 세 번째 열도 같은 방식으로 옮깁니다.',
    eq=f'{QB}=Cᵀ{QA}',extra=matrix('Cᵀ ≈',list(map(list,zip(*MREL)))))
add(51,'예제 3 답: AB ≈ b₂+b₃입니다.','Problem Solving 16:08–16:56',
    '첫 성분은 0.866×0.683+0×0.366−0.500×1.183=−0.000022입니다. 둘째 성분은 0.250×0.683+0.866×0.366+0.433×1.183=0.999945입니다.',
    '셋째 성분은 0.433×0.683−0.500×0.366+0.750×1.183=0.999989입니다. 따라서 주어진 정밀도에서는 (0,1,1)ᵀ이고, 기저까지 붙이면 AB≈b₂+b₃입니다. 원문에 길이 단위가 명시되지 않았으므로 임의로 m를 붙이지 않습니다.',
    correction='원본의 (0,1,1)은 반올림된 입력을 사용한 근사 결과입니다. 표시된 숫자를 그대로 곱한 결과와 이상적인 값 사이의 작은 차이는 반올림 오차로 구분합니다.',
    eq=f'{QB}≈(0,1,1)ᵀ',extra=card('역방향 검산','C(0,1,1)ᵀ는 C의 둘째 열과 셋째 열의 합입니다. (0.250+0.433,0.866−0.500,0.433+0.750)ᵀ=(0.683,0.366,1.183)ᵀ로 주어진 A성분이 복원됩니다.'))
add(52,'원점과 무관하다는 말은 같은 AB의 기저변환에 한정합니다.','Problem Solving 16:59–17:25',
    '이번 변환은 같은 displacement vector(변위벡터) AB를 두 기저로 적습니다. 그 화살표를 평행하게 옮겨 그려도 방향과 길이가 같으므로 축을 그린 원점 위치는 필요하지 않습니다.',
    '시험용 보강: 같은 점 P를 서로 다른 원점 Oₐ,Oᵦ에서 측정한 position vector(위치벡터)는 서로 다릅니다. OₐP=OₐOᵦ+OᵦP이므로 A성분에서는 [OₐP]A=[OₐOᵦ]A+C[OᵦP]B입니다. 이 경우에는 원점 사이의 translation(병진)을 생략할 수 없습니다.')
add(53,'예제 4 · 탑승실을 추가로 45° 회전시킵니다.','Problem Solving 17:33–18:00',
    '예제 3의 AB≈b₂+b₃에서 시작하여 그림의 x축에 대해 탑승실을 +45° 더 회전시킵니다. 영상은 이 동작을 pitch(피치)라고 부릅니다. 회전축은 이름만으로 추정하지 않고 54·55장에 제시된 x축을 따릅니다.',
    '이하 추가 회전 직전의 b축 방향을 고정해 둔 측정 기저를 B₀, 탑승실과 함께 추가 회전한 기저를 B₁이라 구별합니다. 이 표기는 원본 답이 어느 기저에서 성립하는지 명확히 하기 위한 해설용 보강입니다.',
    correction='원본의 (0,0,1.414)라는 답은 회전 전 b축을 고정한 채 회전 후 AB를 표현할 때 성립합니다. 회전 후에도 탑승실을 따라가는 축으로 성분을 적는 경우와 구별해야 합니다.')
add(54,'예제 4의 절차: 점의 벡터를 실제로 회전시킵니다.','Problem Solving 18:04–18:12',
    'Active rotation(능동 회전)이므로 q=X(45°)p를 사용합니다. p는 회전 전 AB의 B₀성분 (0,1,1)ᵀ, q는 회전 후 AB의 B₀성분입니다. 두 숫자벡터는 같은 측정 기저에 대한 값입니다.',
    '예제 3에서 사용한 Cᵀ는 같은 벡터의 A성분을 B성분으로 바꿨습니다. 이번에는 그 변환을 이미 마친 (0,1,1)ᵀ를 시작값으로 사용하고, 추가 회전 X(45°)를 적용합니다.')
add(55,'x축 45° 행렬에 회전 전 성분을 곱합니다.','Problem Solving 18:15–19:02',
    'cos45°=sin45°=√2/2입니다. 회전축인 x성분은 그대로이고 y,z성분만 섞입니다. 첫 행의 결과는 0, 둘째 행은 (√2/2)×1−(√2/2)×1, 셋째 행은 (√2/2)×1+(√2/2)×1입니다.',
    extra=matrix('X(45°)',[['1','0','0'],['0','√2/2','−√2/2'],['0','√2/2','√2/2']]),eq='q=X(45°)(0,1,1)ᵀ')
add(56,'예제 4 답: 회전 전 고정 축에서 AB ≈ √2 b₃입니다.','Problem Solving 19:07–19:29',
    'y성분에서는 같은 두 수가 상쇄되어 0이 되고 z성분에서는 합쳐져 √2가 됩니다. 회전 전 AB는 yz평면에서 +y와 +z 사이를 향했고, +x축 주위로 45° 더 돌면서 +z방향과 나란해집니다.',
    '시험용 보강: 처음 길이는 √(0²+1²+1²)=√2, 나중 길이도 √(0²+0²+(√2)²)=√2입니다. Rotation(회전)은 길이를 바꾸지 않으므로 간단한 검산이 됩니다. 1.414는 √2의 반올림값입니다.',
    eq='q=(0,0,√2)ᵀ≈(0,0,1.414)ᵀ')
add(57,'기저변환과 실제 회전의 차이를 마지막으로 연결합니다.','Problem Solving 19:31–19:42',
    '기저변환에서는 같은 AB의 성분이 A에서 B로 달라졌습니다. 실제 회전에서는 B₀기저를 유지하면서 AB 자체가 다른 방향으로 바뀌었습니다. 수치 행렬이 회전을 표현한다는 사실만으로 이 두 작업을 같게 취급하지 않습니다.',
    '시험용 보강: 점 B가 탑승실에 붙어 있고 측정 기저도 B₁처럼 함께 돌면 상대 성분은 변하지 않습니다. B₀에서 구한 q=(0,0,√2)ᵀ를 B₁로 바꾸면 X(45°)ᵀq=(0,1,1)ᵀ가 됩니다. 회전 동작과 기저변환을 차례로 적용하면 이 차이가 계산으로 확인됩니다.')
add(58,'참고문헌','원본 References 페이지',
    '원본 수록 문헌: Beer 외, <i>Vector Mechanics for Engineers: Dynamics</i>, 12판, 15장. 유홍희, <i>동역학</i>, 1판, 문운당, 8장. 교재 본문을 별도 열람·인용한 것으로 취급하지 않고 원본 참고문헌 목록을 보존합니다.',role='Reference')

exams = [
    ('Define(정의하라) a direction cosine matrix(방향코사인행렬).',
     'Let aᵢ and bⱼ be unit basis vectors of A and B. The entry cᵢⱼ is aᵢ·bⱼ, the cosine of the angle between them. The jth column contains the A-components of bⱼ. Therefore [p]A = C[p]B.',
     'Unit basis vectors(단위 기저벡터들)라는 전제와 행·열의 순서를 함께 적습니다. Maps(연결한다)라는 단어만 쓰는 대신 입력·출력 기저를 식으로 제시합니다.'),
    ('Explain(설명하라) why orientation(자세) has three degrees of freedom(자유도).',
     'The nine matrix entries satisfy three unit-length constraints and three pairwise-orthogonality constraints. Hence the rotation matrix has three independent parameters. This does not imply that any three entries uniquely determine the entire matrix.',
     'Independent(독립적인) 변수의 수를 셉니다. Arbitrary entries(임의의 원소들) 세 개만 고르면 된다는 주장과 구분합니다.'),
    ('Distinguish(구별하라) rotations about new axes(새 축에 대한 회전) and original axes(원래 축에 대한 회전).',
     'New axes move with the body, so each new elementary rotation is postmultiplied. Original axes remain fixed, so each new rotation is premultiplied. For an x-y-z sequence, the products are XYZ and ZYX, respectively.',
     'Postmultiplied(오른쪽에 곱해지는), premultiplied(왼쪽에 곱해지는)를 축의 성질과 연결합니다. Respectively(각각)는 앞의 두 경우와 뒤의 두 답을 같은 순서로 대응합니다.'),
    ('Determine(구하라) the product for 30° about z, followed by(이어서) 30° about the new y-axis(새 y축), then the new x-axis(새 x축).',
     'This is a body-axis z-y-x sequence. Thus R = Z(30°)Y(30°)X(30°). Its rows are approximately (0.750, −0.217, 0.625), (0.433, 0.875, −0.217), and (−0.500, 0.433, 0.750).',
     'Followed by(이어서)는 시간 순서를 지정하고 new(새)는 축 종류를 지정합니다. 둘을 따로 읽어야 행렬의 순서가 정해집니다.'),
    ('Use original axes(원래 축을 사용하라) for the same z-y-x sequence(같은 z-y-x 순서).',
     'The axes are fixed in space. The final vector is X(30°)[Y(30°)[Z(30°)p]], so R = X(30°)Y(30°)Z(30°). Its first row is approximately (0.750, −0.433, 0.500), which differs from the body-axis result.',
     'Fixed in space(공간에 고정된)가 핵심 조건입니다. 같은 각도 세 번이어도 축이 같지 않으면 결과가 달라집니다.'),
    ('Find(구하라) the inverse(역행렬) of R = Z(ψ)Y(φ)X(θ).',
     'A rotation matrix is orthogonal, so R⁻¹ = Rᵀ. Reversing the order and negating each angle gives R⁻¹ = X(−θ)Y(−φ)Z(−ψ). This rotation returns the body to its original orientation.',
     'Reverse the order(순서를 뒤집다)와 negate each angle(각 각도의 부호를 바꾸다)가 모두 필요합니다. 물체축·공간축의 동등한 표현을 찾는 문제와 다릅니다.'),
    ('Express(나타내라) the given vector(주어진 벡터) in the cab basis(탑승실 기저로).',
     'Since [AB]A = C[AB]B, premultiplication by Cᵀ gives [AB]B = Cᵀ[AB]A. Using the supplied values gives approximately (0, 1, 1)ᵀ. Hence AB is approximately b₂ + b₃.',
     '벡터의 끝점은 그대로이고 기저만 바뀝니다. Approximately(대략)는 소수로 반올림된 입력을 사용한다는 뜻이며 풀이가 미완성이라는 뜻이 아닙니다.'),
    ('Does a change of origin(원점 변경) affect this basis transformation(기저변환)?',
     'Not for the same displacement vector AB: its endpoints remain A and B. However, position vectors measured from different origins are different vectors. Their conversion also requires the displacement between the origins.',
     'Same displacement vector(같은 변위벡터)와 position vectors from different origins(서로 다른 원점에서 잰 위치벡터들)를 구분해 조건을 적습니다.'),
    ('Rotate(회전시켜라) p = (0,1,1)ᵀ by +45° about x and express the result in the same fixed basis(같은 고정 기저로 결과를 나타내라).',
     'The active rotation gives q = X(45°)p. Thus qx = 0, qy = cos45° − sin45° = 0, and qz = sin45° + cos45° = √2. The length remains √2, as required for a rotation.',
     'Same fixed basis(같은 고정 기저)가 원본 예제 4의 답을 해석하는 조건입니다. 벡터와 함께 회전한 축에서 성분을 묻는다면 (0,1,1)이 유지됩니다.'),
    ('Compare(비교하라) an active rotation(능동 회전) with a passive basis change(수동 기저변환).',
     'An active rotation changes the vector while its components are expressed in the same basis. A passive basis change keeps the vector fixed but changes its components. For a basis rotated by R, the new components of the unchanged vector are Rᵀp.',
     'Fixed(고정된)가 벡터를 수식하는지 축을 수식하는지를 봅니다. 두 설명에서 고정되는 대상이 서로 다릅니다.'),
    ('Show(보여라) that a rotation preserves length(길이를 보존한다).',
     'For q = Rp and RᵀR = I, qᵀq = pᵀRᵀRp = pᵀp. Therefore the squared length, and hence the length, is unchanged. A proper rotation also has determinant +1.',
     '시험용 보강입니다. Orthogonal(직교인) 조건으로 길이 보존을 증명하고, proper rotation(방향을 보존하는 순수 회전)의 determinant(행렬식) 조건을 별도로 적습니다.'),
]
terms = [
    ('orientation / attitude','자세','물체가 어느 방향을 향하는지; 위치와 구별'),
    ('reference orientation / relative orientation','기준 자세 / 상대 자세','비교의 기준 / 한 물체에 대한 다른 물체의 방향'),
    ('rigid body / body-attached','강체 / 물체에 고정된','점 사이 거리가 고정된 물체 / 물체와 함께 움직이는'),
    ('direction cosine matrix','방향코사인행렬','cᵢⱼ=aᵢ·bⱼ; 두 축 집합 사이의 내적 표'),
    ('unit vector / orthonormal basis','단위벡터 / 정규직교 기저','길이 1인 벡터 / 서로 수직인 단위벡터들'),
    ('dot product / projection','내적 / 투영','같은 기저에서 성분끼리 곱해 합함 / 지정 방향에 해당하는 성분'),
    ('row / column / entry','행 / 열 / 원소','가로줄 / 세로줄 / 행렬의 한 칸'),
    ('constraint / independent','구속조건 / 독립적인','허용되는 값의 관계 / 다른 변수로 결정되지 않는'),
    ('degree of freedom / parameterization','자유도 / 매개화','필요한 독립 변수의 수 / 그 변수로 상태를 표현하는 방법'),
    ('Euler angles / consecutive rotations','오일러각 / 연속 회전','축 순서를 정한 세 각도 / 차례로 수행하는 회전'),
    ('body / intrinsic / local axis','물체 / 내재 / 국소축','현재 물체와 함께 회전한 축'),
    ('space / extrinsic / global axis','공간 / 외재 / 전역축','처음의 방향을 유지하는 고정축'),
    ('new / current / original / fixed','새 / 현재의 / 원래의 / 고정된','회전 문제에서 사용할 축의 상태를 지정하는 표현'),
    ('followed by / respectively','이어서 / 각각','앞 동작 이후 다음 동작 / 앞뒤 항목을 순서대로 대응'),
    ('right-handed / right-hand rule','오른손 방향의 / 오른손 규칙','기저의 방향 규약 / 양의 회전 방향 규약'),
    ('simple / elementary rotation','단순 / 기본 회전','한 좌표축에 대한 회전'),
    ('composition / noncommutative','합성 / 교환되지 않는','여러 회전을 차례로 적용 / 순서를 바꾸면 보통 결과가 다른'),
    ('postmultiplication / premultiplication','후곱 / 전곱','새 행렬을 오른쪽에 곱함 / 왼쪽에 곱함'),
    ('orthogonal matrix / identity matrix','직교행렬 / 단위행렬','RᵀR=I인 행렬 / 곱해도 원래 벡터를 유지하는 I'),
    ('inverse / transpose','역행렬 / 전치행렬','원래 변환을 되돌리는 행렬 / 행과 열을 바꾼 행렬'),
    ('determinant / proper rotation','행렬식 / 방향을 보존하는 순수 회전','정사각행렬에서 계산하는 스칼라값 / 직교이고 행렬식 +1인 회전'),
    ('coordinate vector / component','좌표벡터 / 성분','한 기저에 대한 숫자들을 모은 열 / 그 기저 방향의 계수'),
    ('basis change / coordinate transformation','기저변환 / 좌표변환','같은 벡터를 다른 축의 성분으로 표현하는 작업'),
    ('active rotation / passive transformation','능동 회전 / 수동 변환','벡터 자체를 돌림 / 벡터를 두고 표현 기저를 바꿈'),
    ('original / rotated vector','회전 전 / 회전 후 벡터','같은 기저에서 비교하는 서로 다른 두 벡터'),
    ('displacement / position vector','변위 / 위치벡터','지정된 두 점 사이의 화살표 / 정한 원점에서 점까지의 화살표'),
    ('origin / translation','원점 / 병진','위치 측정의 출발점 / 방향을 유지한 위치 이동'),
    ('cab / control cube / flight simulator','탑승실 / 제어 상자 / 비행 시뮬레이터','예제의 B / 예제의 A / 이들 물체가 연결된 장치'),
    ('pitch / axis of rotation','피치 / 회전축','원본 예제 4의 추가 회전 명칭 / 해당 그림과 행렬에서 정할 축'),
    ('approximately / rounded','대략 / 반올림된','유한 정밀도의 결과 / 표시 자릿수로 줄여 쓴 값'),
    ('preserve / unchanged / attached','보존하다 / 변하지 않는 / 붙어 있는','변환 전후 값을 유지 / 어떤 기준에 대해 불변 / 물체를 따라 움직이는'),
    ('express in terms of / determine / distinguish','~의 성분으로 나타내라 / 구하라 / 구별하라','기저를 바꾸어 기술 / 식이나 값을 결정 / 대상 사이의 차이 설명'),
]
audit = [
    ('Overview 00:24','thighs','dice(주사위)','그림의 주사위와 orientation(자세) 설명'),
    ('Contents 1 00:33 · 5장','wizard bodies','rigid bodies(강체들)','강의 제목과 앞 강의 복습'),
    ('Contents 1 05:07 이후 · 9–11장','unit factors / urine factors','unit vectors(단위벡터들)','단위 길이와 정규직교축의 투영'),
    ('Contents 1 11:09–13:56 · 12장','ofuse / obvious notation','abuse of notation(편의상 확장한 표기)','원본 문장; 벡터를 행렬처럼 쌓은 표기와 숫자 좌표벡터의 구별'),
    ('Contents 1 12:36·15:56 · 12–13장','dragon / traction cosine matrix','direction cosine matrix(방향코사인행렬)','원본 제목과 cᵢⱼ=aᵢ·bⱼ'),
    ('10·12·30장','maps a to b','기하학적 축 관계와 숫자 좌표변환을 구별','12·29·30장의 [p]A=C[p]B 정의'),
    ('Contents 2 01:27–02:04 · 17장','둘째 각도도 θ로 인쇄; 자막 angle C','x:θ, y:φ, z:ψ','영상 각도 열거 및 21–23장 행렬'),
    ('Contents 2 02:22·19:26 · 18–25장','party axis / SpaceX','body axis(물체축) / space axis(공간축)','new와 original 축의 구분'),
    ('25장','(2,3),(3,3)에 cosψ','−sinθ cosφ, cosθ cosφ','X(θ)Y(φ)Z(ψ)의 직접 행렬곱; 서로 다른 각도에서도 검산'),
    ('Contents 2 26:10 · 27장','pressure orthogonal group','special orthogonal group(특수직교군) SO(3)','직교행렬 및 순수 회전의 det R=+1 조건'),
    ('Problem Solving 04:22 · 38장','theory of freedom','degree of freedom(자유도)','회전 가능한 축의 수를 설명하는 문맥'),
    ('37–39장','제목·절차 표기와 실제 기준계/축 지정이 엇갈림','기준계 N,A,B를 정한 뒤 각 기저 n,a,b를 지정','그림·본문에서 실제로 수행한 작업'),
    ('Problem Solving 05:18–05:59 · 38–39장','간단한 축 정렬 설명과 일반 자세의 수치','계산에는 39장의 명시적 축 성분 사용','주어진 b₃에는 n₁,n₂ 성분이 있어 a₃와 일치하지 않음'),
    ('39–40·51장','반올림한 축·행렬에 정확한 등호 사용','근사 기호와 실제 계산 잔차 제시','주어진 소수값의 내적 및 Cᵀ[AB]A 계산'),
    ('52장','원점 위치가 영향을 주지 않음','같은 AB의 기저변환으로 한정','서로 다른 원점의 위치벡터에는 병진항 필요'),
    ('Problem Solving 17:39 · 53–57장','peachy / pitch; 회전 후 b축 해석','pitch(피치); 원본의 x축 회전; B₀와 B₁ 구분','54·55장의 X(45°), 56장의 √2 b₃, 57장의 same coordinate system'),
    ('Summary 00:17–01:18','현재 복습과 다음 강의 예고가 함께 있음','복습은 개념 요약, 미분·속도 예고는 별도 후반부','00:55 이후 next lecture 전환'),
]
roadmap = '''<section class="editorial-section section-divider" id="course-roadmap" aria-labelledby="roadmap-title">
<p class="section-kicker">Summary video · Course roadmap</p>
<h2 class="section-title" id="roadmap-title">Summary 영상 후반 · 다음에는 회전하는 축에서 미분합니다.</h2>
<p class="section-lead">00:17–00:51의 방향코사인행렬·오일러각·회전 합성 복습은 위 핵심 개념 요약에 반영했습니다. 00:55–01:18은 다음 강의의 벡터 미분과 속도·가속도 예고입니다.</p></section>
<section class="editorial-section" id="roadmap-detail" aria-labelledby="roadmap-detail-title">
<p class="section-kicker">What comes next</p><h2 class="section-title" id="roadmap-detail-title">자세를 표현한 다음, 그 자세가 변하는 속도를 다룹니다.</h2>
<div class="card"><h3>Lecture 11 · Kinematics of Rigid Bodies III(강체 운동학 III)</h3><p>영상은 서로 다른 기준계에서 vector differentiation(벡터 미분)을 연결하는 공식, angular velocity(각속도)의 합성, 강체의 한 점 및 두 점 사이의 linear velocity(선속도)·acceleration(가속도)를 예고합니다. 이번 강의의 행렬은 자세와 성분 변환을 제공하며, 시간에 따른 운동을 구하는 미분 절차는 다음 단원에서 이어집니다.</p></div>
<div class="evidence"><span>Summary 00:55–01:18</span><span>강의 인덱스 · Week 11, 2026-11-11</span></div></section>'''


def fill(part, values):
    return re.sub(r'\{\{([^{}]+)\}\}', lambda m: values[m[1]], part)


def build():
    template = (SITE/'templates/lecture-page.template.html').read_text(encoding='utf-8')
    template = re.sub(r'\s*<!--[\s\S]*?-->', '', template)
    slide = re.search(r'<section class="source-section"[\s\S]*?</section>',template).group()
    assert len(records)==58
    sections=[]
    for n,(title,evidence,blocks,role) in enumerate(records,1):
        sections.append(fill(slide,dict(NN=f'{n:02d}',SLIDE_ROLE=role,SLIDE_HEADING=title,
            LECTURE_SLUG='lecture10',DESCRIPTIVE_ALT_TEXT=escape(f'Lecture 10 원본 슬라이드 {n:02d}: {title}'),
            CURRENT_PAGE=str(n),PAGE_COUNT='58',TRANSCRIPT_TIME_OR_SLIDE_ROLE=evidence,SLIDE_EXPLANATION_BLOCKS=blocks)))
    template=template.replace(slide,'\n\n'.join(sections))
    exam=re.search(r'<div class="exam-card">[\s\S]*?</p>\s*</div>',template).group()
    template=template.replace(exam,'\n'.join(fill(exam,dict(EXAM_QUESTION=q,MODEL_ANSWER=escape(a),KOREAN_ANSWER_EXPLANATION=ko)) for q,a,ko in exams))
    toc=[('overview','전체 개요'),('concept-map','개념 지도'),('concept-summary','핵심 개념 요약')]+[
        (f'slide-{n:02d}',f'{n:02d} · {r[0]}') for n,r in enumerate(records,1)]+[
        ('course-roadmap','Summary · 다음 단원'),('exam-english','시험 영어'),('glossary','용어집'),('asr-log','원본·자막 교정'),('sources','출처')]
    pdf_url='https://github.com/leejinh0225/MC2103-Dynamics/raw/refs/heads/main/2026FA_Dynamics/lecture_notes/lecture10_note.pdf'
    source='<ul class="plain-list"><li><a href="'+pdf_url+'">Lecture 10 원본 PDF</a> · MC2103 · 2026-11-04 · 58장</li>'+''.join(
        f'<li><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{name} 영상</a> · 영어 자동생성 자막 원문</li>' for name,vid in videos)+'</ul>'
    source+=p('영어 자동자막 5편(1,520개 시간 구간)을 2026-11-16 확보해 원본 슬라이드와 대조했습니다. 슬라이드 아래 시각은 관련 설명 구간이며 정확한 화면 전환 시각을 뜻하지 않습니다. 3장의 보조 영상은 링크만 보존했고 58장의 교재는 참고문헌 목록으로만 사용했습니다.')
    source+=p('Summary 영상의 현재 개념 복습을 핵심 개념 요약에 반영했습니다. 행렬의 상세 곱셈, 물체축 후곱의 이유, 원점이 다른 위치좌표의 병진항, 회전 전후 기저 구분, 길이·행렬식 검산은 이해와 시험 답안을 위한 보강입니다. 원본 이미지와 영어 자막 파일은 수정하지 않았습니다.')
    template=fill(template,dict(
        LECTURE_NUMBER='Lecture 10',LECTURE_TITLE='Kinematics of Rigid Bodies II',
        ONE_SENTENCE_DESCRIPTION='강체 운동학 II: 방향코사인행렬, 오일러각, 물체축·공간축 회전과 좌표변환을 다루는 한국어 학습 노트',
        WEEK='Week 10',DATE_OR_날짜_미기재='2026-11-04',PAGE_COUNT='58',
        LECTURE_PROMISE='세 축의 내적으로 강체의 자세를 나타내고, 물체축과 공간축에 따른 회전 합성 순서를 설명합니다. 비행 시뮬레이터 예제 네 개를 통해 같은 벡터의 좌표변환과 벡터 자체의 회전을 구분합니다.',
        VIDEO_SET='Overview · Contents 1·2 · Problem Solving · Summary',
        ALL_CONTENTS_AND_PROBLEM_SOLVING_BUTTONS='\n'.join(f'<a class="button button--primary" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noreferrer">{name} 영상 열기</a>' for name,vid in videos[1:4]),
        ORIGINAL_PDF_URL=pdf_url,LECTURE_NOTE_FILENAME='lecture10_note.pdf',
        CORE_RELATIONSHIP_HEADLINE='같은 행렬을 쓰더라도, 축을 바꾸는 것과 물체를 돌리는 것은 다릅니다.',
        CORE_RELATIONSHIP_EXPLANATION='고정된 화살표를 다른 축으로 표현하면 숫자가 달라집니다. 축을 고정하고 화살표를 회전시켜도 숫자가 달라집니다. 이번 강의는 direction cosine matrix(방향코사인행렬)와 rotation matrix(회전행렬)를 구성하고, 무엇이 고정되어 있는지를 기준으로 이 두 작업을 구별합니다.',
        CONCEPT_MAP_HEADLINE='축의 내적 → 회전의 합성 → 좌표변환과 실제 회전',
        CONCEPT_MAP_BLOCKS='<div class="grid-3">'+card('Direction cosines(방향코사인)','두 기저의 축끼리 내적하여 상대 자세를 아홉 원소로 표현합니다.')+card('Euler angles(오일러각)','세 회전의 각도·축·순서를 정하고, 움직이는 축인지에 따라 곱하는 쪽을 정합니다.')+card('Transform or rotate(변환 또는 회전)','같은 벡터의 기저를 바꾸는지, 같은 기저에서 벡터를 돌리는지 구분합니다.')+'</div>',
        STANDALONE_CONCEPT_SUMMARY=summary,DISTINCT_SUMMARY_VIDEO_SECTION_IF_NEEDED=roadmap,
        EXAM_SECTION_TITLE='행렬의 방향과 회전 순서를 설명하는 영어 답안',
        BILINGUAL_GLOSSARY_TABLE=table(['영어(한국어)','의미와 사용'],[(f'{en}({ko})',desc) for en,ko,desc in terms]),
        AUDIT_SECTION_TITLE='원본 슬라이드·영어 자동자막 교정 기록',
        ASR_CORRECTION_TABLE=p('원본 이미지와 영어 자동자막 파일은 그대로 보존했습니다. 아래는 해설에 채택한 용어·수식·적용 조건과 그 근거입니다. 자막의 표기가 실제 발화인지 음성 인식 오류인지는 단정하지 않습니다.')+table(['위치','원문 또는 쟁점','본문 처리','근거'],audit),
        SOURCE_LIST_AND_PROVENANCE_NOTE=source,TABLE_OF_CONTENTS_LINKS=''.join(f'<li><a href="#{key}">{val}</a></li>' for key,val in toc)))
    template=template.replace('이 부분만 읽어도 렉처의 핵심 정의, 개념 관계, 가정과 풀이 흐름을 이해할 수 있도록 작성합니다.',
        '자세를 나타내는 축의 내적에서 시작해 회전 합성의 순서와 네 예제의 답까지 연결합니다. 상세한 유도·계산과 원본 그림은 아래 슬라이드별 해설에서 이어집니다.')
    (SITE/'lecture10.html').write_text(template,encoding='utf-8')
    print(f'Built Lecture 10: {len(records)} slides, {len(exams)} English answers, {len(terms)} glossary entries.')


if __name__=='__main__':
    build()
