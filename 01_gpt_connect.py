import openai
from dotenv import load_dotenv
import os

#ai 연결 기본 text질문

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def ask_to_gpt(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        top_p=0.5,
        temperature=0.5,
        messages=[
            # {"role": "system", "content": "You are a helpful assistant."},
            # {"role": "system", "content": "You are the mirror of Show White. You must pretend like the mirror of the story."},
            {"role": "system", "content": "You are the Joker of Batman movie. You must pretend like Joker of the story. when you speak in Korean, you must use 반말"},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

users_request = '''
거울아 거울아 이 세상에서 누가 제일 예쁘니?
'''

r = ask_to_gpt(users_request)
print(r)

