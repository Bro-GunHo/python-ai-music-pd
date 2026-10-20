# 작업 규칙

## 소통
- 답변은 한국어로 한다.
- 분석만 요청하면 파일을 수정하지 않는다.

## Git
- 코드 수정 전에 `before-<작업명>` 태그를 붙이고 `fix/<작업명>` 브랜치에서 작업한다.
- 수정 항목마다 커밋을 따로 나눈다.
- push, 병합, 태그 업로드는 반드시 먼저 물어본다.

## 환경
- 파이썬은 `.venv/bin/python`을 사용한다.
- requirements.txt는 `.venv/bin/python -m pip freeze`로 만든다.
- 앱은 프로젝트 루트에서 실행해야 한다 (상대경로 사용).

## 백업
- 압축 백업에서 mp3/, images/, videos/, .venv/는 제외한다.

# 프로젝트 구조

GPT와 대화해 플레이리스트를 만들고 CSV 저장 → MP3 다운로드 → 앨범아트 생성 → 동영상 제작까지 하는 Tkinter 앱.
openai는 레거시 0.28 API(`openai.ChatCompletion`, `functions`/`function_call`)를 쓴다. 1.x 문법으로 바꾸지 않는다.

## 파일 역할
| 파일 | 역할 |
|---|---|
| `app_main.py` | 진입점. Tkinter 채팅 GUI + GPT function calling으로 아래 함수들을 호출. `save_playlist_as_csv`, `select_mp4_files_and_generate_video`는 여기 정의 |
| `youtube_audio_download.py` | `download_songs_in_csv(csv)`: YouTube 검색 → yt-dlp로 `./mp3/`에 저장, CSV에 `mp3` 컬럼 추가 |
| `generate_image.py` | `generate_images_for_songs(csv)`: 곡별 이미지 생성 + 앨범아트 합성, CSV에 `image`, `info_image` 컬럼 추가 |
| `gpt_image_gen.py` | GPT로 프롬프트 생성 → `gpt-image-2`로 이미지 생성 (GPU 없을 때) |
| `dream_like_diffusion_image_gen.py` | Stable Diffusion(dreamlike)로 이미지 생성 (CUDA/MPS 있을 때) |
| `add_info_to_album_art.py` | `make_album_art()`: 이미지에 제목·아티스트를 넣어 `images/{title}_{artist}_album_art.jpg` 저장 |
| `generate_video_using_images.py` | 앨범아트 + MP3로 곡별 영상 생성 후 이어 붙여 `./videos/{csv이름}.mp4` |
| `generate_video_using_mp4.py` | 사용자가 고른 MP4를 반복·연결하고 MP3와 자막을 합성해 `./videos/{csv이름}.mp4` |
| `01_`~`12_*.py`, `dreamlike-diffusion.py`, `*.ipynb` | 학습·실험용. 메인 앱과 무관 |

## 실행 흐름
1. `app_main.py` 실행 → GUI에서 사용자 입력 → `ChatCompletion.create(functions=..., function_call='auto')`
2. GPT가 함수를 고르면 `available_functions`에서 실행 → 결과를 `role: function`으로 넣고 한 번 더 호출해 답변 표시
3. 입력 한 번에 함수는 최대 1개 실행. 단계 순서는 코드가 아니라 system 프롬프트가 정한다.
4. CSV 경로는 코드에 저장되지 않고 GPT가 대화 기록에서 다시 넘겨준다.

## CSV 형식 (`playlist/*.csv`, `;` 구분, `index=False`)
- 단계마다 컬럼이 늘어난다: `Title;Artist;Release Date` → `+mp3` → `+image;info_image`
- 실패한 곡은 해당 컬럼에 `'Not found'` 문자열을 기록하고, 다음 단계는 이 문자열로 거른다.
- 예전 CSV에는 맨 앞에 이름 없는 인덱스 컬럼이 있을 수 있다 (`generate_image.py`는 읽을 때 `Unnamed` 컬럼을 제거).

## 주의할 점
- 모든 경로가 상대경로(`./mp3`, `./videos`, `images`)라 프로젝트 루트에서 실행해야 한다.
- 다운로드·이미지 생성·인코딩이 메인 스레드에서 동기로 돌아 그동안 GUI가 멈춘다.
- macOS 전용 하드코딩: 폰트 `/System/Library/Fonts/Supplemental/AppleGothic.ttf`, ffmpeg `/usr/local/bin`.
- 비밀 키는 `.env`(`OPENAI_API_KEY`, `GPT_VERSION`). mp3/, images/, videos/는 git에서 제외.
