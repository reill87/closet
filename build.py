#!/usr/bin/env python3
"""~/Documents/내옷장 → 공개용 closet.json + 위치정보 없는 사진 + index.html 생성."""
import csv, json, os, re, datetime
from PIL import Image, ImageOps

SRC = os.path.expanduser('~/Documents/내옷장')
OUT = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://reill87.github.io/closet/'
CAT = {'아우터': ('outer', 'o'), '상의': ('top', 't'), '하의': ('bottom', 'b')}
SPORTY = ['아디다스', '나이키', '푸마', '널디', '카파', '그래픽', '트랙탑']
ACCENT = {'카키', '그린', '민트', '버건디', '오렌지', '블루'}

def office_ok(r):
    sub, name = r['종류'], r['이름']
    casual = sub in ('후드', '집업', '플리스', '바람막이', '맨투맨', '츄리닝') or any(k in name for k in SPORTY) \
        or '연청' in name or '워싱' in name or '반팔' in name
    return (not casual) or sub == '셔츠'

items, n = [], {}
for r in csv.DictReader(open(os.path.join(SRC, '옷장목록.csv'), encoding='utf-8-sig')):
    if r['상태'] == '정리예정':
        continue
    cat, pre = CAT[r['구분']]
    n[pre] = n.get(pre, 0) + 1
    iid = f'{pre}{n[pre]:02d}'
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, r['사진파일']))).convert('RGB')
    im.thumbnail((600, 600))
    im.save(os.path.join(OUT, 'img', iid + '.jpg'), 'JPEG', quality=72)   # exif 미포함 = GPS 제거
    items.append({
        'id': iid, 'category': cat, 'category_ko': r['구분'], 'type': r['종류'],
        'name': re.sub(r'\(상의 더미\)', '', r['이름']).strip(), 'color': r['메인색'],
        'warmth': int(r['보온(0~4)'] or 1), 'office_ok': office_ok(r),
        'accent_color': r['메인색'] in ACCENT, 'has_hood': '후드' in r['이름'],
        'status': r['상태'] or None, 'image': BASE + 'img/' + iid + '.jpg',
    })

doc = {
    'updated': datetime.date.today().isoformat(),
    'description': '한 사람의 옷장 목록. 아우터+상의+하의 조합 추천용 데이터.',
    'fields': {
        'warmth': '0(반팔)~4(패딩). 옷 종류로 추정한 보온 정도',
        'office_ok': '출근(오피스 캐주얼)에 입을 수 있는지',
        'accent_color': '네이비·그레이·블랙 등 무채색이 아닌 포인트 색인지',
    },
    'recommend_hints': {
        'outer_by_morning_low_c': {'<=-3': [4], '-2~3': [3, 4], '4~8': [2, 3], '9~13': [1, 2], '14~18': [1], '>=19': '아우터 없음'},
        'top_by_daytime_high_c': {'<=12': '보온 2(니트·맨투맨·후드)', '13~19': '보온 1~2', '>=20': '보온 1'},
        'avoid': ['포인트색 2개 이상', '상의·하의 같은 색', '후드 상의 + 후드 아우터', '셋 다 같은 색', '츄리닝(type=츄리닝) + 코트·블레이저'],
        'note': '셔츠 + 얇은 아우터로 아침 6도 이하면 경량 조끼(type=조끼)를 받쳐 입기',
    },
    'items': items,
}
json.dump(doc, open(os.path.join(OUT, 'closet.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 보드 페이지: 템플릿 재사용, 사진 경로만 공개용으로
board = [{'id': i['id'], 'cat': i['category_ko'], 'sub': i['type'], 'color': i['color'], 'warm': i['warmth'],
          'name': i['name'], 'img': 'img/' + i['id'] + '.jpg', 'office': i['office_ok'],
          'accent': i['accent_color'], 'hood': i['has_hood']} for i in items]
html = open(os.path.join(SRC, '_보드템플릿.html'), encoding='utf-8').read()
html = html.replace('/*__ITEMS__*/[]', json.dumps(board, ensure_ascii=False))
html = html.replace('<h1>내 옷장 보드</h1>', '<h1>내 옷장 보드</h1>\n  <p class="sub">데이터: <a href="closet.json" style="color:inherit">closet.json</a></p>')
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(html)
print(len(items), 'items')
