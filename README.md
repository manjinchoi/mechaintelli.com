# mechaintelli.com

㈜메카인텔리 회사 홈페이지입니다. https://mechaintelli.com

## 폴더 구성

| 경로 | 내용 |
| --- | --- |
| `docs/` | 실제로 공개되는 홈페이지. GitHub Pages가 이 폴더를 그대로 올립니다. |
| `docs/index.html` | 홈페이지 본문 (`build.py`로 만든 결과물) |
| `docs/assets/` | 설비 이미지, 로고, 공유 이미지, 아이콘 |
| `docs/CNAME` | 사용자 도메인 `mechaintelli.com` (지우면 도메인 연결이 끊김) |
| `src/` | 홈페이지 원본: `body.html` 본문, `style.css` 디자인, `app.js` 동작 |
| `build.py` | 연락처와 설비 라인업 데이터를 넣어 `docs/index.html`을 만드는 스크립트 |

## 수정하는 방법

1. 원본을 고칩니다.
   - 대표전화·이메일: `build.py` 위쪽 `CONTACT`
   - 설비 라인업(이름, 설명, 사양, 이미지): `build.py`의 `EQUIP` 목록
   - 그 밖의 문구와 섹션: `src/body.html`
   - 색상과 배치: `src/style.css`
2. `python3 build.py`를 실행합니다. (Pillow 필요: `pip install pillow`)
3. `main` 브랜치에 올리면 1~2분 뒤 mechaintelli.com에 반영됩니다.

`docs/index.html`을 직접 고치면 다음에 `build.py`를 실행할 때 덮어써집니다. 원본(`src/`, `build.py`)을 고쳐 주세요.

## 배포

- 호스팅: GitHub Pages, `main` 브랜치의 `/docs` 폴더
- 도메인: mechaintelli.com (가비아 등록, DNS도 가비아)
- `www.mechaintelli.com`으로 접속하면 `mechaintelli.com`으로 넘어갑니다.
