#!/usr/bin/env python3
"""Build the MECHA INTELLI homepage.

Writes two pages from the same sources:
  docs/index.html   full document for mechaintelli.com (head, SEO, OG tags), plus robots.txt, sitemap.xml, CNAME
  artifact.html     page body for the Claude artifact preview (no doctype/head; the artifact host adds them; not committed)
Edit the data below or src/*.{css,html,js}, then run:  python3 build.py
"""
import datetime
import html
import json
import os
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'docs')
IMG = os.path.join(SITE, 'assets', 'img')

# Fill these in once 메카인텔리 confirms them; empty values show a dashed "입력 필요" marker on the page.
CONTACT = {'tel': '070-7507-5112', 'tel_intl': '+82-70-7507-5112', 'email': 'ceo@mechaintelli.com'}
DOMAIN = 'https://mechaintelli.com/'

FONTS = ('https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..800'
         '&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+KR:wght@400;500;600;700&display=swap')

e = html.escape


def dims_of(name):
    with Image.open(os.path.join(IMG, name + '.webp')) as im:
        return im.size


def img(name, alt, kind='render'):
    w, h = dims_of(name)
    return {'src': f'assets/img/{name}.webp', 'alt': alt, 'kind': kind, 'w': w, 'h': h}


CATS = [  # filter key, filter label
    ('display', '디스플레이'),
    ('battery', '2차전지'),
    ('semi', '반도체'),
    ('auto', '자동차·정밀'),
    ('logi', '물류·검사'),
]

FLOW = lambda h: f'좌 → 우 ({h} ±50 mm)'
SIZE = lambda l, w, h: f'L {l:,} × W {w:,} × H {h:,} mm'
MAT = 'Min 50 × 85 ~ Max 250 × 250 mm'
COVER_FULL = '제관 + PROFILE + 아크릴'

EQUIP = [
    dict(id='roll-lamination', cat='display', tag='DISPLAY', en='ROLL LAMINATION SYSTEM', ko='롤 라미네이션',
         desc='폴더블 스마트폰의 메탈 내장 힌지와 공정용 필름을 비전 얼라인한 뒤 롤러로 합착합니다.',
         key=[('물류 높이', '1,200 ±50 mm'), ('자재', '50×85 ~ 250×250 mm')],
         spec=[('물류 방향 (높이)', FLOW('1,200')), ('자재 SIZE', MAT), ('설비 SIZE', SIZE(3500, 2400, 2000)), ('COVER', COVER_FULL)],
         dims=(3500, 2400, 2000),
         images=[img('roll-lamination', '롤 라미네이션 시스템 3D 모델')]),
    dict(id='utg-lamination', cat='display', tag='DISPLAY', en='UTG ROLL LAMINATION SYSTEM', ko='UTG 롤 라미네이션',
         desc='폴더블 스마트폰용 UTG(Ultra Thin Glass)에 OCA(Optical Clear Adhesive)를 비전 얼라인해 양면으로 롤러 합착합니다.',
         key=[('물류 높이', '1,200 ±50 mm'), ('자재', '50×85 ~ 250×250 mm')],
         spec=[('물류 방향 (높이)', FLOW('1,200')), ('자재 SIZE', MAT), ('설비 SIZE', SIZE(8500, 2400, 2200)), ('COVER', COVER_FULL)],
         dims=(8500, 2400, 2200),
         images=[img('utg-lamination', 'UTG 롤 라미네이션 시스템 3D 모델')]),
    dict(id='fpcb-bending', cat='display', tag='DISPLAY', en='FPCB BENDING SYSTEM', ko='FPCB 벤딩',
         desc='디스플레이 패널에 연결된 COF·FPC·FPCB를 조립하기 쉽게 벤딩해 패널에 부착합니다.',
         key=[('물류 높이', '1,100 ±50 mm'), ('자재', '50×85 ~ 250×250 mm')],
         spec=[('물류 방향 (높이)', FLOW('1,100')), ('자재 SIZE', MAT), ('설비 SIZE', SIZE(9500, 2400, 2100)), ('COVER', COVER_FULL)],
         dims=(9500, 2400, 2100),
         images=[img('fpcb-bending', 'FPCB 벤딩 시스템 3D 모델')]),
    dict(id='cof-cop', cat='display', tag='DISPLAY', en='COF / COP BONDING SYSTEM', ko='COF·COP 본딩',
         desc='3"~15.6" 패널에 ACF를 부착하고 COF 또는 칩을 비전 얼라인해 열압착 본딩합니다.',
         key=[('정밀도', 'COP ±3 ㎛ · COF ±4 ㎛'), ('TACT', '15 s (1 COF)')],
         spec=[('대상', '3" ~ 15.6" 패널'), ('물류 방향 (높이)', FLOW('1,050')), ('제품', 'PANEL / COF (TAB·IC) / IC'),
               ('TACT TIME', ['15 s (1 COF)', '22 s (2 COF)', '62 s (6 COF)']),
               ('정밀도 (3σ)', ['ACF X ±0.1 mm · Y ±0.08 mm', 'COF X·Y ±4 ㎛', 'COP X·Y ±3 ㎛', 'CUTTING ±50 ㎛']),
               ('설비 SIZE', SIZE(3000, 2200, 1800)), ('COVER', COVER_FULL)],
         dims=(3000, 2200, 1800),
         images=[img('cof-cop', 'COF·COP 본딩 시스템 3D 모델')]),
    dict(id='fof-fop', cat='display', tag='DISPLAY', en='FOF / FOP BONDING SYSTEM', ko='FOF·FOP 본딩',
         desc='3"~15.6" 패널에 ACF를 부착하고 FPC를 비전 얼라인해 열압착 본딩합니다.',
         key=[('정밀도', 'FOP ±10 ㎛ · FOF ±15 ㎛'), ('TACT', 'FOP 18 s · FOF 20 s')],
         spec=[('대상', '3" ~ 15.6" 패널'), ('물류 방향 (높이)', FLOW('1,050')), ('제품', 'PANEL + COF (TAB·IC) / PANEL / FPC'),
               ('TACT TIME', ['FOF 20 s (1 FPC)', 'FOP 18 s (1 FPC)']),
               ('정밀도 (3σ)', ['ACF X ±0.1 mm · Y ±0.08 mm', 'FOF X·Y ±15 ㎛', 'FOP X·Y ±10 ㎛']),
               ('설비 SIZE', SIZE(3500, 1250, 1800)), ('COVER', COVER_FULL)],
         dims=(3500, 1250, 1800),
         images=[img('fof-fop', 'FOF·FOP 본딩 시스템 3D 모델')]),
    dict(id='inline', cat='display', tag='DISPLAY', en='DISPLAY IN-LINE SYSTEM', ko='디스플레이 인라인 본딩 라인',
         desc='로더부터 플라즈마, ACF 본더, 가압착·본압착, FPC 본딩, 디스펜서, 언로더까지 13개 모듈을 한 라인으로 연결합니다.',
         key=[('구성', 'LOADER ~ UNLOADER 13개 모듈'), ('본딩', 'COF/COG · FOF/FOG')],
         spec=[('COF / COG', ['LOADER · PLASMA · ACF BONDER', 'COF PRESS · PRE BONDER · MAIN BONDER']),
               ('FOF / FOG', ['ACF BONDER · FPC LOADER · MAIN BONDER', '반전기 · ART · DISPENSER · UNLOADER'])],
         dims=None,
         images=[img('inline-system', '디스플레이 인라인 본딩 라인 3D 모델')]),
    dict(id='loader', cat='display', tag='DISPLAY', en='LOADER / UNLOADER SYSTEM', ko='로더·언로더',
         desc='트레이 단분리·회전, 제품 핸들러, 다이버터, 컨베이어로 공정 설비의 자재 투입과 배출을 자동화합니다.',
         key=[('구성', 'TRAY 단분리·회전 · HANDLER'), ('이송', 'DIVERTER · CONVEYOR')],
         spec=[('구성', ['TRAY 단분리 / 회전', '제품 HANDLER', 'DIVERTER', 'CONVEYOR']), ('적용', '디스플레이 공정 설비 자재 투입·배출')],
         dims=None,
         images=[img('loader-render', '로더·언로더 3D 모델 (컨베이어, 다이버터, 핸들러, 트레이 단분리·회전)'),
                 img('loader-cell', '로더·언로더 셀 3D 모델'),
                 img('loader-frame', '로더·언로더 프레임 3D 모델'),
                 img('loader-photo-1', '제작 완료한 로더·언로더 설비', 'photo'),
                 img('loader-photo-2', '로더·언로더 설비 측면', 'photo'),
                 img('loader-photo-3', '로더·언로더 설비 설치 모습', 'photo')]),
    dict(id='forming', cat='battery', tag='BATTERY', en='FORMING · FILLING · DEGAS · SEALING', ko='단동 포밍·주액·디개싱·실링',
         desc='2차전지 셀 공정의 파우치 포밍, 전해액 주액, 디개싱, 실링을 단동(Stand-alone) 설비로 구성합니다.',
         key=[('공정', '포밍 · 주액 · 디개싱 · 실링'), ('형태', '단동 설비 4종')],
         spec=[('공정', ['FORMING (파우치 포밍)', 'FILLING (전해액 주액)', 'DEGAS (디개싱)', 'SEALING (실링)']), ('형태', '단동 (Stand-alone)')],
         dims=None,
         images=[img('forming-1', '단동 설비 3D 모델 1'), img('forming-2', '단동 설비 3D 모델 2'),
                 img('forming-3', '단동 설비 3D 모델 3'), img('forming-4', '단동 설비 3D 모델 4')]),
    dict(id='inline-filling', cat='battery', tag='BATTERY', en='IN-LINE FILLING · SEALING', ko='인라인 주액·실링',
         desc='전해액 주액과 실링 공정을 하나의 인라인 설비로 연결해 연속 생산에 대응합니다.',
         key=[('공정', '전해액 주액 · 실링'), ('형태', '인라인')],
         spec=[('공정', ['FILLING (전해액 주액)', 'SEALING (실링)']), ('형태', '인라인')],
         dims=None,
         images=[img('inline-filling-1', '인라인 주액·실링 설비 3D 모델 1'), img('inline-filling-2', '인라인 주액·실링 설비 3D 모델 2')]),
    dict(id='bma', cat='battery', tag='BATTERY', en='BMA / BSA ASSEMBLY LINE', ko='BMA·BSA 조립라인',
         desc='배터리 모듈(BMA)과 배터리 시스템(BSA) 조립라인을 설계·제작하고 현장 셋업까지 수행합니다.',
         key=[('대표 실적', '배터리 모듈 조립라인 (수량 16)'), ('범위', '설계 · 제작 · 셋업')],
         spec=[('수행 실적', ['배터리 모듈 조립라인 (16)', 'ESS 배터리 패킹 라인 (1)', '전동화 부품(PE) 조립라인 · 개조 (1)', 'BEV 부품 조립라인 (1)']),
               ('수행 범위', '설계 · 제작 · 셋업 (개조 포함)')],
         dims=None,
         images=[img('bma-line', 'BMA/BSA 조립라인 3D 모델'), img('bma-layout', 'BMA/BSA 조립라인 평면 레이아웃', 'drawing')]),
    dict(id='ic-tray', cat='semi', tag='SEMICONDUCTOR', en='IC TRAY AUTO PACKING SYSTEM', ko='IC 트레이 자동 포장',
         desc='Final Test를 마친 IC 트레이에 습도 인디케이터와 실리카겔을 자동 공급하고, PP 밴딩 후 알루미늄 방습백에 넣어 진공 실링합니다.',
         key=[('포장 단위', '11단 (Cover Tray 포함)'), ('TRAY', 'JEDEC 322.6×135.9×12.19')],
         spec=[('물류 방향 (높이)', FLOW('1,000')), ('제품', 'JEDEC IC TRAY 322.6 × 135.9 × 12.19 mm'), ('포장 단위', '11단 (Cover Tray 포함)'),
               ('설비 SIZE', SIZE(10000, 2400, 1900)), ('COVER', 'PROFILE + 아크릴')],
         dims=(10000, 2400, 1900), fit='contain',
         images=[img('ic-photo', 'IC 트레이 자동 포장 설비 외관', 'photo'), img('ic-layout', 'IC 트레이 자동 포장 설비 평면 배치', 'drawing')]),
    dict(id='auto', cat='auto', tag='AUTOMOTIVE', en='AUTOMOTIVE ASSEMBLY', ko='자동차 부품 정밀 조립',
         desc='자동차 컴프레셔 조립 설비, PCB 조립기, 볼트 체결기, 커넥터 체결기 등 부품 조립 자동화 설비를 제작합니다.',
         key=[('조립', '컴프레셔 · PCB'), ('체결', 'BOLT · CONNECTOR')],
         spec=[('설비', ['자동차 컴프레셔 조립 설비', 'PCB 조립기', 'BOLT 체결기', 'CONNECTOR 체결기'])],
         dims=None,
         images=[img('auto-compressor', '자동차 컴프레셔 조립 설비', 'photo'), img('auto-pcb', 'PCB 조립기', 'photo'),
                 img('auto-bolt', 'BOLT 체결기', 'photo'), img('auto-connector', 'CONNECTOR 체결기', 'photo')]),
    dict(id='laser', cat='auto', tag='PRECISION', en='LASER MARKING SYSTEM', ko='레이저 마킹',
         desc='컨베이어로 투입된 PCB의 상면과 배면에 바코드와 문자를 레이저로 마킹한 뒤 배출합니다.',
         key=[('제품', 'PCB 50×50 ~ 250×250 mm'), ('방식', 'Top·Bottom · Dual 공급')],
         spec=[('대상', '3" ~ 16"'), ('물류 방향 (높이)', FLOW('900')), ('제품', ['PCB 50 × 50 ~ 250 × 250 mm', 'Dual 공급 Type', 'Top & Bottom Marking']),
               ('설비 SIZE', SIZE(1400, 2400, 1900)), ('COVER', 'PROFILE + 아크릴')],
         dims=(1400, 2400, 1900),
         images=[img('laser-marking', '레이저 마킹 시스템 3D 모델')]),
    dict(id='agv', cat='logi', tag='LOGISTICS', en='PRODUCT LOADING AGV', ko='제품 적재 AGV',
         desc='랙에 제품을 자동으로 적재하는 물류 AGV 제작에 참여했습니다.',
         key=[('용도', '랙 제품 자동 적재'), ('수행', '물류 AGV 제작 참여')],
         spec=[('용도', '랙 제품 자동 적재'), ('수행', '제품 적재 물류 AGV 제작 참여')],
         dims=None,
         images=[img('agv', '제품 적재 AGV 3D 모델'), img('agv-rack', 'AGV가 랙에 제품을 적재하는 순서', 'drawing')]),
    dict(id='xray', cat='logi', tag='INSPECTION', en='2D X-RAY INSPECTION SYSTEM', ko='2D X-RAY 검사기',
         desc='2D X-RAY 투과 영상으로 제품 내부를 검사하는 설비입니다.',
         key=[('검사', '2D X-RAY 투과 검사'), ('형태', '단독형 캐비닛')],
         spec=[('검사 방식', '2D X-RAY'), ('형태', '단독형 캐비닛')],
         dims=None,
         images=[img('xray', '2D X-RAY 검사기 3D 모델')]),
]

CAT_LABEL = {
    'DISPLAY': 'DISPLAY SOLUTIONS', 'BATTERY': 'BATTERY SOLUTIONS', 'SEMICONDUCTOR': 'SEMICONDUCTOR SOLUTIONS',
    'AUTOMOTIVE': 'AUTOMOTIVE SOLUTIONS', 'PRECISION': 'PRECISION AUTOMATION', 'LOGISTICS': 'LOGISTICS AUTOMATION',
    'INSPECTION': 'INSPECTION SOLUTIONS'}

# hero: target point on the render (from the brochure's own callouts) and balloon position, % of the image box
HERO = [
    (1, 'LOADER', 'cof', (13.8, 85.6), (25.5, 96.0)),
    (2, 'PLASMA', 'cof', (20.9, 78.2), (31.5, 90.5)),
    (3, 'ACF BONDER', 'cof', (27.3, 74.1), (37.5, 84.5)),
    (4, 'COF PRESS', 'cof', (25.6, 57.9), (11.5, 50.0)),
    (5, 'PRE BONDER', 'cof', (35.8, 67.0), (44.5, 78.0)),
    (6, 'MAIN BONDER', 'cof', (41.9, 59.9), (51.5, 71.0)),
    (7, 'ACF BONDER', 'fof', (57.5, 36.7), (47.5, 26.0)),
    (8, 'FPC LOADER', 'fof', (64.0, 27.6), (55.0, 14.5)),
    (9, 'MAIN BONDER', 'fof', (54.0, 51.4), (63.5, 63.0)),
    (10, '반전기', 'fof', (60.3, 44.6), (70.5, 56.0)),
    (11, 'ART', 'fof', (69.9, 37.6), (78.5, 49.0)),
    (12, 'DISPENSER', 'fof', (76.8, 30.2), (86.5, 42.0)),
    (13, 'UNLOADER', 'fof', (89.7, 24.2), (95.5, 34.5)),
]

TOL = [  # name, axis note, tolerance in µm (half width), shown value
    ('COP 본딩', 'X·Y축', 3, '±3 ㎛'),
    ('COF 본딩', 'X·Y축', 4, '±4 ㎛'),
    ('FOP 본딩', 'X·Y축', 10, '±10 ㎛'),
    ('FOF 본딩', 'X·Y축', 15, '±15 ㎛'),
    ('커팅', 'COF·COP 설비', 50, '±50 ㎛'),
    ('ACF 부착', 'Y축', 80, '±0.08 mm'),
    ('ACF 부착', 'X축', 100, '±0.1 mm'),
]

ARROW = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4.5 12 8l-3.5 3.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def hero_parts():
    lines, marks, cof, fof = [], [], [], []
    for n, name, grp, (tx, ty), (bx, by) in HERO:
        lines.append(f'<line data-k="{n}" x1="{tx * 11.42:.1f}" y1="{ty * 7.94:.1f}" x2="{bx * 11.42:.1f}" y2="{by * 7.94:.1f}"/>')
        marks.append(f'<span class="tgt" data-k="{n}" style="--x:{tx}%;--y:{ty}%"></span>'
                     f'<span class="bal" data-k="{n}" style="--x:{bx}%;--y:{by}%" aria-hidden="true">{n}</span>')
        li = f'<li data-k="{n}"><i aria-hidden="true">{n}</i>{e(name)}</li>'
        (cof if grp == 'cof' else fof).append(li)
    return ''.join(lines), '\n          '.join(marks), ''.join(cof), ''.join(fof)


def footprint(L, W, H):
    s = 17 / 1000  # 17 units per metre, 10 m x 2.5 m floor
    fw, fh = 170, 42.5
    g = [f'<rect class="fp-floor" x="1" y="1" width="{fw}" height="{fh}"/>']
    g += [f'<line class="fp-grid" x1="{1 + 17 * i}" y1="1" x2="{1 + 17 * i}" y2="{1 + fh}"/>' for i in range(1, 10)]
    g += [f'<line class="fp-grid" x1="1" y1="{1 + 17 * j}" x2="{1 + fw}" y2="{1 + 17 * j}"/>' for j in (1, 2)]
    g.append(f'<rect class="fp-m" x="1" y="1" width="{L * s:.1f}" height="{W * s:.1f}"/>')
    return (f'<figure class="fp"><svg viewBox="0 0 172 45" role="img" aria-label="평면도: 길이 {L:,} mm, 폭 {W:,} mm. 한 칸은 1 m">{"".join(g)}</svg>'
            f'<figcaption><span>L {L:,} × W {W:,} × H {H:,} mm</span><span>1칸 1 m</span></figcaption></figure>')


def card(q):
    first = q['images'][0]
    fit = q.get('fit')
    media_kind = 'photo' if (first['kind'] == 'photo' and fit != 'contain') else 'render'
    count = f'<span class="count">{len(q["images"])}장</span>' if len(q['images']) > 1 else ''
    key = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in q['key'])
    fp = footprint(*q['dims']) if q['dims'] else ''
    return f'''<article class="eq" data-cat="{q['cat']}" id="eq-{q['id']}">
          <button type="button" class="eq-media well {media_kind}" data-open="{q['id']}" aria-label="{e(q['ko'])} 사양 보기">
            <img src="{first['src']}" alt="{e(first['alt'])}" width="{first['w']}" height="{first['h']}" loading="lazy" decoding="async">
            <span class="tag">{q['tag']}</span>{count}
          </button>
          <div class="eq-body">
            <p class="eq-en">{e(q['en'])}</p>
            <h3>{e(q['ko'])}</h3>
            <p class="eq-desc">{e(q['desc'])}</p>
            <dl class="eq-key">{key}</dl>
            {fp}
            <button type="button" class="eq-more" data-open="{q['id']}">상세 사양{ARROW}</button>
          </div>
        </article>'''


def filters():
    total = len(EQUIP)
    out = [f'<button type="button" class="chip" data-f="all" aria-pressed="true">전체 <small>{total}</small></button>']
    for k, label in CATS:
        n = sum(1 for q in EQUIP if q['cat'] == k)
        out.append(f'<button type="button" class="chip" data-f="{k}" aria-pressed="false">{label} <small>{n}</small></button>')
    return ''.join(out)


def tol_rows():
    rows = []
    for name, note, t, val in TOL:
        rows.append(f'<div class="tol-row"><span class="tol-name">{e(name)}<small>{e(note)}</small></span>'
                    f'<span class="tol-track" role="img" aria-label="{e(name)} {e(note)} 허용 오차 {e(val)}"><span class="tol-band" style="--t:{t}"></span></span>'
                    f'<span class="tol-val">{e(val)}</span></div>')
    return ''.join(rows)


def works():
    out = []
    for i in range(1, 7):
        w, h = dims_of(f'proj-{i}')
        out.append(f'<li class="well"><img src="assets/img/proj-{i}.webp" alt="" width="{w}" height="{h}" loading="lazy" decoding="async"></li>')
    return ''.join(out)


def contact_value(kind):
    v = CONTACT.get(kind, '').strip()
    if not v:
        return f'<span class="todo">{"대표번호" if kind == "tel" else "이메일"} 입력 필요</span>'
    vid = 'c-' + kind
    href = 'tel:' + v.replace('-', '') if kind == 'tel' else 'mailto:' + v
    return (f'<a class="big" id="{vid}" href="{e(href)}">{e(v)}</a>'
            f'<button type="button" class="lk" data-copy="{e(v)}" data-target="{vid}">복사</button>')


def footer_contact():
    out = []
    if CONTACT.get('tel'):
        out.append(f'<span>TEL {e(CONTACT["tel"])}</span>')
    if CONTACT.get('email'):
        out.append(f'<span>E-mail {e(CONTACT["email"])}</span>')
    return ''.join(out)


def eq_json():
    data = {}
    for q in EQUIP:
        data[q['id']] = {
            'en': q['en'], 'ko': q['ko'], 'desc': q['desc'], 'cat': CAT_LABEL[q['tag']],
            'spec': [[k, v] for k, v in q['spec']],
            'images': q['images'], 'dims': list(q['dims']) if q['dims'] else None,
        }
    return json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def body():
    src = open(os.path.join(ROOT, 'src', 'body.html'), encoding='utf-8').read()
    lines, marks, cof, fof = hero_parts()
    rep = {
        '{{HERO_LINES}}': lines, '{{HERO_MARKS}}': marks, '{{PARTS_COF}}': cof, '{{PARTS_FOF}}': fof,
        '{{FILTERS}}': filters(), '{{TOTAL}}': str(len(EQUIP)), '{{CARDS}}': '\n        '.join(card(q) for q in EQUIP),
        '{{TOL_ROWS}}': tol_rows(), '{{WORKS}}': works(), '{{TEL}}': contact_value('tel'),
        '{{EMAIL}}': contact_value('email'), '{{EQ_JSON}}': eq_json(), '{{FTR_CONTACT}}': footer_contact(),
    }
    for k, v in rep.items():
        assert k in src, k
        src = src.replace(k, v)
    assert '{{' not in src
    return src


def main():
    css = open(os.path.join(ROOT, 'src', 'style.css'), encoding='utf-8').read()
    js = open(os.path.join(ROOT, 'src', 'app.js'), encoding='utf-8').read()
    b = body()
    fonts = (f'<link rel="preconnect" href="https://fonts.googleapis.com">\n'
             f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
             f'<link rel="stylesheet" href="{FONTS}">')

    # 1) artifact page: the host wraps this in doctype/head/body
    art = (f'<title>메카인텔리 홈페이지</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{fonts}\n'
           f'<style>\n{css}</style>\n{b}\n<script>\n{js}</script>\n')
    with open(os.path.join(ROOT, 'artifact.html'), 'w', encoding='utf-8') as f:
        f.write(art)

    # 2) deployable document for mechaintelli.com
    desc = ('㈜메카인텔리는 2차전지·반도체·디스플레이 및 정밀 자동화 설비를 설비 기획부터 정밀 설계, 제작, '
            '설치·시운전, 양산 안정화까지 일괄 수행하는 천안 소재 자동화 설비 전문 기업입니다.')
    ld = {
        '@context': 'https://schema.org', '@type': 'Organization', 'name': '㈜메카인텔리', 'alternateName': 'MECHA INTELLI',
        'url': DOMAIN, 'logo': DOMAIN + 'assets/logo-full.png', 'foundingDate': '2024-05-09',
        'address': {'@type': 'PostalAddress', 'streetAddress': '입장면 도림길 26-24', 'addressLocality': '천안시 서북구',
                    'addressRegion': '충청남도', 'addressCountry': 'KR'},
        'numberOfEmployees': {'@type': 'QuantitativeValue', 'value': 20},
    }
    if CONTACT.get('tel'):
        ld['telephone'] = CONTACT.get('tel_intl') or CONTACT['tel']
    if CONTACT.get('email'):
        ld['email'] = CONTACT['email']
    head = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>㈜메카인텔리 MECHA INTELLI | 2차전지·반도체·디스플레이 자동화 설비</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="메카인텔리, MECHA INTELLI, 자동화 설비, 2차전지 설비, 디스플레이 본딩, COF 본딩, FOF 본딩, 롤 라미네이션, BMA 조립라인, IC 트레이 포장, 천안">
<link rel="canonical" href="{DOMAIN}">
<meta name="theme-color" content="#FFFFFF">
<meta property="og:type" content="website">
<meta property="og:site_name" content="㈜메카인텔리">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="㈜메카인텔리 | 2차전지·반도체·디스플레이 자동화 설비">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{DOMAIN}">
<meta property="og:image" content="{DOMAIN}assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="64x64" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
{fonts}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>
{css}</style>
</head>
<body>
'''
    doc = head + b + f'\n<script>\n{js}</script>\n</body>\n</html>\n'
    with open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(doc)
    with open(os.path.join(SITE, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}sitemap.xml\n')
    with open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                f'  <url><loc>{DOMAIN}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>\n</urlset>\n')
    host = DOMAIN.split('//', 1)[1].strip('/')
    with open(os.path.join(SITE, 'CNAME'), 'w', encoding='utf-8') as f:
        f.write(host + '\n')
    open(os.path.join(SITE, '.nojekyll'), 'w').close()
    print('artifact.html', len(art.encode()), 'bytes; docs/index.html', len(doc.encode()), 'bytes')


if __name__ == '__main__':
    main()
