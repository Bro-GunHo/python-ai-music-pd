import openai
from dotenv import load_dotenv
import os
import base64
from PIL import Image
from io import BytesIO
from IPython.display import display
from pathlib import Path

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT_VERSION = os.getenv('GPT_VERSION')

openai.api_key = OPENAI_API_KEY

temperature = 0.2
# model = 'dall-e-3' 삭제됨
model = 'gpt-image-2'

def gpt_prompt_generator(song_title, artist):
    response = openai.ChatCompletion.create(
        model=GPT_VERSION,
        top_p=0.1,
        temperature=temperature,
        messages=[
            {"role": "system", "content": """
            당신은 gpt-image-2 모델의 이미지 생성 프롬프트를 만드는
            AI 어시스턴트입니다.

            사용자가 노래 제목과 아티스트를 제공하면,
            해당 음악에서 연상되는 분위기, 감정, 장면, 장소,
            색감, 조명, 시간대 및 시각적 요소를 상상하여
            독창적인 이미지 생성 프롬프트를 작성하세요.

            노래 제목이나 아티스트의 이름을 최종 프롬프트에 포함하지 마세요.
            유명인이나 실제 인물을 묘사하지 마세요.
            특정 뮤직비디오나 앨범 커버를 그대로 재현하지 마세요.

            범죄, 마약, 과도한 폭력 등의 요소는 직접적으로 표현하지 말고
            안전하고 비폭력적인 시각적 요소로 대체하세요.

            최종 결과는 gpt-image-2에 전달할 영어 이미지 프롬프트만
            출력하세요.
            """
             },
            {"role": "user", "content": f"Song title: {song_title}\nArtist: {artist}"}
        ]
    )
    return response.choices[0].message.content

def generate_gpt_image(song_title, artist):

    prompt = gpt_prompt_generator(song_title, artist)
    print(f"Prompt: {prompt}")

    response = openai.Image.create(
        model=model,
        prompt=prompt,
        size="1024x1024", #해상도
        n=1 #이미지 개수
    )

    # print(response)


    image_data = response['data'][0]['b64_json']

    image = Image.open(
        BytesIO(base64.b64decode(image_data))
    )


    DATA_DIR = Path(os.getcwd()) / "images"
    DATA_DIR.mkdir(exist_ok=True)
    # DATA_DIR = os.path.join(os.getcwd(), "images")

    # display(image)
    file_name = DATA_DIR / f"{song_title}_{artist}.png"

    image_file = DATA_DIR / f"{file_name}"
    image.save(image_file)
    print("이미지 저장 완료")
    return image_file


if __name__ == "__main__":
    song_title = "When I Was Your Man"
    artist = "Bruno Mars"
    generate_gpt_image(song_title, artist)

    # generate_gpt_image("A man is dancing in the night in the middle of Gangnam, Seoul", "Dancing_Man")

