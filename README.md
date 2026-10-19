# Python AI Music PD

**AI 기반 음악 콘텐츠 제작 자동화 프로젝트**

Python과 생성형 AI를 활용하여 음악 콘텐츠의 기획부터 자료 수집, 앨범 커버 제작, 동영상 편집까지 자동화하는 PD 애플리케이션입니다.

음악 플레이리스트를 구성하고, 음원을 수집하고, 이미지와 음악을 결합하여 최종 동영상을 제작하는 전체 워크플로를 구현하는 것을 목표로 합니다.

## 주요 기능

- **콘텐츠 기획**: GPT를 활용한 음악 콘텐츠 아이디어 및 자료 준비
- **음원 수집**: YouTube 검색 및 음원 다운로드 자동화
- **앨범 커버 제작**: 음악 제목과 아티스트 정보를 활용한 이미지 제작
- **동영상 생성**: 이미지와 음악을 결합한 영상 제작
- **영상 편집 자동화**: 여러 영상과 음원을 결합하여 최종 MP4 파일 생성
- **GUI**: Tkinter를 활용한 콘텐츠 제작 기능 통합

## 기술 스택

- **Language**: Python 3.11
- **AI**: OpenAI API
- **Image Processing**: Pillow
- **Video Processing**: MoviePy, FFmpeg
- **Data Processing**: Pandas, JSON
- **GUI**: Tkinter
- **Environment**: macOS, Python virtual environment, Google Colab

## 프로젝트 결과물

### New York Music Playlist

뉴욕을 주제로 선정한 음악과 앨범 커버를 활용하여 제작한 플레이리스트 결과물입니다.

**동영상**

[▶ New York 플레이리스트 동영상 보기](https://youtu.be/q7gzLYN4uX8)

**플레이리스트 데이터**

[New York 플레이리스트 CSV](playlist/newyork.csv)

### Album Art Gallery

프로젝트에서 생성한 음악별 앨범 커버 이미지 샘플입니다.

#### Welcome to New York — Taylor Swift

![Welcome to New York - Taylor Swift](images/Welcome%20to%20New%20York_Taylor%20Swift_album_art.jpg)

#### Empire State of Mind — Jay-Z feat. Alicia Keys

![Empire State of Mind - Jay-Z feat. Alicia Keys](images/Empire%20State%20of%20Mind_Jay-Z%20feat.%20Alicia%20Keys_album_art.jpg)

## 개발 환경

Python 3.11 기반의 가상환경을 사용합니다.

```bash
/usr/local/bin/python3.11 -m venv .venv
source .venv/bin/activate
```

## 개발 과정 및 개선 사항

- MacBook 로컬 환경의 이미지 생성 성능 한계 개선
- Google Colab GPU 환경을 활용한 이미지 생성 시도
- GPT 기반 이미지 생성 기능 적용
- 음원 다운로드, 앨범 커버 제작, 영상 생성 기능을 Python 함수로 모듈화
- 여러 미디어 파일을 결합하는 동영상 자동 제작 기능 개발

## 향후 개선 계획

- 메인 커버 이미지 추가
- 제작 설정 및 결과물 관리를 위한 GUI 개선
- mp3다운받을 때 이미 존재하는 파일 스킵
- 결과물 및 제작 이력 관리 기능 추가

## 프로젝트 목표

단순한 Python 학습을 넘어 생성형 AI와 미디어 처리 라이브러리를 결합하여 실제 콘텐츠 제작에 활용할 수 있는 자동화 애플리케이션을 구현합니다.