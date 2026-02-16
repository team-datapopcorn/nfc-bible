# ✝️ NFC Bible (오늘의 말씀)

**NFC 태그를 통해 스마트폰으로 매일 새로운 성경 말씀을 만나는 프로젝트입니다.**

이 저장소는 웹 애플리케이션, 오프라인 굿즈(NFC 스티커) 디자인, 그리고 3D 프린팅 모델링 도구까지 포함하는 종합 프로젝트입니다.

## 📂 프로젝트 구조

```
nfc-bible/
├── index.html          # 메인 웹 애플리케이션 (모바일 최적화)
├── sticker_designs/    # NFC 스티커 인쇄용 디자인 및 가이드
├── scripts/            # 3D 모델링 생성용 Blender 스크립트
├── images/             # 웹 앱 및 SNS 공유용 이미지 리소스
└── stitch_..._variant/ # 디자인 실험 및 변형 시안
```

---

## 📱 웹 애플리케이션 (Web Application)

`index.html`은 사용자가 NFC 태그를 태깅했을 때 접속하게 되는 모바일 웹 앱입니다.

### 주요 기능
- **랜덤 말씀 뽑기**: 화면을 터치하거나 버튼을 눌러 새로운 성경 구절을 확인할 수 있습니다.
- **북마크 저장소**: 마음에 드는 말씀을 개인 보관함에 저장할 수 있습니다. (닉네임 기반 로컬 저장)
- **손쉬운 공유**: 카카오톡 공유하기 및 텍스트 복사 기능을 지원합니다.
- **감각적인 디자인**: 네오 브루털리즘(Neo-Brutalism) 스타일과 부드러운 애니메이션을 적용했습니다.

### 실행 방법
GitHub Pages를 통해 호스팅하여 사용하거나, 로컬에서 `index.html` 파일을 직접 열어 실행할 수 있습니다.

---

## 🏷️ NFC 스티커 (NFC Stickers)

`sticker_designs/` 폴더에는 실제 판매 및 배포 가능한 NFC 스티커 제작 리소스가 있습니다.

- **디자인 파일**: 원형, 라운드 사각, 직사각 등 3가지 형태의 인쇄용 디자인 (`.png`)
- **제작 가이드**: [`sticker_designs/PRINT_GUIDE.md`](sticker_designs/PRINT_GUIDE.md) 파일에서 인쇄 발주 사양, NFC 칩(NTAG213) 부착 위치, 포장 방법 등을 자세히 확인할 수 있습니다.

---

## 🗝️ 3D 프린팅 키링 (3D Printed Keyring)

`scripts/bible_keyring.py`는 3D 모델링 툴인 **Blender**에서 실행 가능한 Python 스크립트입니다.

### 기능
- **자동 모델링**: 실행 시 "I AM WHO I AM" 문구가 양각된 성경책 모양의 키링 모델을 자동으로 생성합니다.
- **맞춤 설정**: 스크립트 상단의 변수를 수정하여 크기, 두께, 텍스트 등을 변경할 수 있습니다.

### 사용법
1. Blender 실행 후 `Scripting` 탭으로 이동
2. `New`를 눌러 새 스크립트 생성 후코드 붙여넣기
3. 스크립트 실행 (Run Script)
4. 생성된 `BibleKeyring` 컬렉션 확인 및 Export

---

## 🎨 디자인 변형 (Design Variants)

`stitch_bible_verse_glassmorphism_variant/` 폴더에는 Tailwind CSS를 활용한 실험적인 디자인 시안이 포함되어 있습니다. 글래스모피즘(Glassmorphism)과 네오 브루털리즘을 결합한 색다른 UI를 테스트하는 공간입니다.
