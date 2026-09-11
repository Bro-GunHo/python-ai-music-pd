from PIL import Image, ImageDraw, ImageFont
import os


def make_album_art(
    image_path,
    title,
    artist,
    font_path="/System/Library/Fonts/Supplemental/AppleGothic.ttf"
):
    """
    원본 정사각형 이미지에 곡 제목과 아티스트명을 추가하여
    앨범 커버 스타일의 이미지를 생성합니다.

    - 제목은 이미지 폭의 90%를 넘지 않도록 폰트 크기 자동 조절
    - 이미지 밝기에 따라 글자색 자동 선택
    - 글자 외곽선과 그림자로 가독성 향상
    - 하단에 자연스러운 어두운 그라데이션 적용
    """

    # --------------------------------------------------
    # 1. 이미지 불러오기
    # --------------------------------------------------
    image = Image.open(image_path).convert("RGB")

    width, height = image.size

    # 정사각형이 아니면 중앙 기준으로 Crop
    if width != height:
        size = min(width, height)

        left = (width - size) // 2
        top = (height - size) // 2

        image = image.crop(
            (left, top, left + size, top + size)
        )

        width, height = image.size


    # --------------------------------------------------
    # 2. Draw 객체
    # --------------------------------------------------
    draw = ImageDraw.Draw(image)


    # --------------------------------------------------
    # 3. 제목 폰트 크기 자동 결정
    #
    # 기본 크기 = 이미지 폭의 10.5%
    # 최대 폭 = 이미지 폭의 90%
    # --------------------------------------------------
    max_title_width = int(width * 0.90)

    title_size = int(width * 0.105)

    while title_size > 20:

        title_font = ImageFont.truetype(
            font_path,
            title_size
        )

        bbox = draw.textbbox(
            (0, 0),
            title,
            font=title_font
        )

        title_width = bbox[2] - bbox[0]

        # 90% 이하라면 종료
        if title_width <= max_title_width:
            break

        # 제목이 너무 길면 폰트 크기를 줄임
        title_size -= 2


    # --------------------------------------------------
    # 4. 아티스트 폰트
    # --------------------------------------------------
    artist_size = int(width * 0.045)

    artist_font = ImageFont.truetype(
        font_path,
        artist_size
    )


    # --------------------------------------------------
    # 5. 제목 / 아티스트 영역 계산
    # --------------------------------------------------
    title_bbox = draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )

    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]


    artist_bbox = draw.textbbox(
        (0, 0),
        artist,
        font=artist_font
    )

    artist_width = artist_bbox[2] - artist_bbox[0]
    artist_height = artist_bbox[3] - artist_bbox[1]


    # --------------------------------------------------
    # 6. 텍스트 위치
    # --------------------------------------------------
    bottom_margin = int(height * 0.09)

    artist_y = height - bottom_margin - artist_height

    title_y = (
        artist_y
        - int(height * 0.035)
        - title_height
    )

    title_x = (width - title_width) // 2
    artist_x = (width - artist_width) // 2


    # --------------------------------------------------
    # 7. 텍스트가 들어가는 영역의 평균 밝기 계산
    #
    # 제목 주변 이미지가 밝은지 어두운지 판단
    # --------------------------------------------------
    sample_box = (
        int(width * 0.05),
        max(0, title_y - int(height * 0.05)),
        int(width * 0.95),
        min(height, artist_y + artist_height)
    )

    sample = image.crop(sample_box)

    # RGB 평균값 계산
    pixels = list(sample.getdata())

    avg_r = sum(pixel[0] for pixel in pixels) / len(pixels)
    avg_g = sum(pixel[1] for pixel in pixels) / len(pixels)
    avg_b = sum(pixel[2] for pixel in pixels) / len(pixels)

    # 사람 눈에 가까운 밝기 계산
    luminance = (
        0.299 * avg_r
        + 0.587 * avg_g
        + 0.114 * avg_b
    )


    # --------------------------------------------------
    # 8. 배경 밝기에 따라 글자색 결정
    #
    # 어두운 배경 -> 흰색
    # 밝은 배경 -> 검은색
    # --------------------------------------------------
    if luminance < 145:

        text_color = (255, 255, 255, 255)
        stroke_color = (0, 0, 0, 190)
        shadow_color = (0, 0, 0, 170)

    else:

        text_color = (20, 20, 20, 255)
        stroke_color = (255, 255, 255, 220)
        shadow_color = (255, 255, 255, 180)


    # --------------------------------------------------
    # 9. 하단 그라데이션
    #
    # 이미지와 글자 색이 비슷한 경우를 보완
    # --------------------------------------------------
    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    overlay_pixels = overlay.load()

    gradient_start = int(height * 0.45)

    for y in range(gradient_start, height):

        progress = (
            y - gradient_start
        ) / (height - gradient_start)

        # 아래로 갈수록 조금 더 진하게
        alpha = int(150 * progress)

        for x in range(width):

            overlay_pixels[x, y] = (
                0,
                0,
                0,
                alpha
            )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    )

    draw = ImageDraw.Draw(image)


    # --------------------------------------------------
    # 10. 그림자 설정
    # --------------------------------------------------
    shadow_offset = max(
        2,
        int(width * 0.005)
    )

    stroke_width = max(
        1,
        int(width * 0.003)
    )


    # --------------------------------------------------
    # 11. 제목 출력
    # --------------------------------------------------

    # 그림자
    draw.text(
        (
            title_x + shadow_offset,
            title_y + shadow_offset
        ),
        title,
        font=title_font,
        fill=shadow_color,
        stroke_width=stroke_width,
        stroke_fill=shadow_color
    )

    # 제목
    draw.text(
        (
            title_x,
            title_y
        ),
        title,
        font=title_font,
        fill=text_color,
        stroke_width=stroke_width,
        stroke_fill=stroke_color
    )


    # --------------------------------------------------
    # 12. 제목과 아티스트 사이 구분선
    # --------------------------------------------------
    line_width = int(width * 0.12)
    line_height = max(
        2,
        int(width * 0.003)
    )

    line_x = (width - line_width) // 2

    line_y = (
        title_y
        + title_height
        + int(height * 0.025)
    )

    draw.rounded_rectangle(
        (
            line_x,
            line_y,
            line_x + line_width,
            line_y + line_height
        ),
        radius=line_height,
        fill=text_color
    )


    # --------------------------------------------------
    # 13. 아티스트명 출력
    # --------------------------------------------------
    artist_y = line_y + int(height * 0.035)

    artist_x = (width - artist_width) // 2

    # 그림자
    draw.text(
        (
            artist_x + shadow_offset // 2,
            artist_y + shadow_offset // 2
        ),
        artist,
        font=artist_font,
        fill=shadow_color
    )

    # 아티스트
    draw.text(
        (
            artist_x,
            artist_y
        ),
        artist,
        font=artist_font,
        fill=text_color
    )


    # --------------------------------------------------
    # 14. RGB로 변환
    # --------------------------------------------------
    result = image.convert("RGB")


    # --------------------------------------------------
    # 출력 경로
    # --------------------------------------------------
    output_dir = "images"

    # images 폴더가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(
        output_dir,
        f"{title}_{artist}_album_art.jpg"
    )

    # --------------------------------------------------
    # 저장
    # --------------------------------------------------
    result.save(
        output_path,
        quality=95
    )

    return output_path


if __name__ == "__main__":
    img_with_info_path = make_album_art(
        image_path="images/Can't Stop the Feeling!_Justin Timberlake.png",
        title="Can't Stop the Feeling!",
        artist="Justin Timberlake",
    )

    print(f"Album art with info saved at: {img_with_info_path}")