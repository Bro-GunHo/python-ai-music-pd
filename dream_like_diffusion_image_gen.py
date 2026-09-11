import openai
from dotenv import load_dotenv
import os
import re

#import touch
from diffusers import StableDiffusionPipeline

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT_VERSION = os.getenv('GPT_VERSION')

openai.api_key = OPENAI_API_KEY

temperature = 0.2

def text_to_image_prompt_generator(song_title, artist):
    response = openai.ChatCompletion.create(
        model=GPT_VERSION,
        top_p=0.1,
        temperature=temperature,
        messages=[
            {'role':'system', 'content': 'You are an AI assistant designed to generate prompts for text-to-image models. '
            'when a user provides a song title and artist, you should summarize then song`s lyrics in a single English sentence, and indicate its genre and mood.'},
            {"role": "user", "content": f"{song_title} - {artist}"}
        ],
    )
    return response['choices'][0]['message']['content']

# 주어진 텍스트에서 한글, 숫자가 아닌 문자를 밑줄(_)로 치환하는 함수
def replace_non_alphanumberic(text):
    pattern = r'[^가-힣a-zA-Z0-9\s]'
    result = re.sub(pattern, '_', text)
    return result

# 노래 제목과 아티스트를 입력 받아 이미지를 생성하는 함수
def generate_dreamlike_image(song_title, artist):
    model_id = "dreamlike-art/dreamlike-diffusion-1.0"
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to("cuda")
    #pipe-pipe.to("mps")  # For Apple Silicon (M1/M2) users, uncomment this line and comment out the previous line

    about = text_to_image_prompt_generator(song_title, artist)

    # 이미지 생성에 사용할 프롬프트 작성하기
    prompt = f"""
    dreamlikeart,
    {about},
    diramatic lighting, illustration by greg rutkowski, yoji shinkawa, 4k, digital art, concept art, trending on artstation
    """

    # 이미지 생성에 사용할 부정적 프롬프트 작성하기
    negative_prompt = """
    text, deformed, cripple, ugly, additional arms, additional legs, additional head, two heads
    """

    file_name = replace_non_alphanumberic(f"{song_title} {artist}")
    image = pipe(prompt=prompt, negative_prompt=negative_prompt).images[0]
    file_path = f"./images/{file_name}.png"
    image.save(file_path)
    return file_path

if __name__ == "__main__":
    r = generate_dreamlike_image("Beat It", "Michael Jackson")
    print(f"Image saved at: {r}")