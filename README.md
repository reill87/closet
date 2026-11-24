# closet

한 사람의 옷장(아우터·상의·하의) 데이터와 조합 보드.

- 보드: https://reill87.github.io/closet/
- 데이터(JSON): https://reill87.github.io/closet/closet.json

## 에이전트용 안내

`closet.json` 을 GET 하면 된다. 인증 없음, 읽기 전용.

| 필드 | 의미 |
|---|---|
| `items[].id` | `o`=아우터, `t`=상의, `b`=하의 + 번호 |
| `items[].category` | `outer` / `top` / `bottom` |
| `items[].type` | 패딩·코트·자켓·니트·셔츠·데님·슬랙스 등 |
| `items[].color` | 메인 색 |
| `items[].warmth` | 0(반팔)~4(패딩), 옷 종류로 추정 |
| `items[].office_ok` | 출근(오피스 캐주얼) 가능 여부 |
| `items[].image` | 사진 URL (위치정보 제거됨) |
| `recommend_hints` | 기온별 보온 기준과 피할 조합 |

추천 예: 그날 아침 최저/낮 최고 기온을 구한 뒤 `recommend_hints` 기준으로 아우터 1 + 상의 1 + 하의 1 을 고르고, 옷 `name` 과 `image` 를 함께 보낸다.

## 갱신

원본은 로컬 `~/Documents/내옷장/옷장목록.csv`. `python3 build.py` 로 다시 만든다.
