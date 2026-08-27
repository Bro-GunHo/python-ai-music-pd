import openai
from dotenv import load_dotenv
import os

# 대화형 프로그램

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def send_message(message_log):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = message_log,
        temperature=0.5, #높을수록 창의적
    )

    #텍스트가 포함된 쳇봇의 첫 응답 찾기(일부 응답에는 텍스트가 없을수 있음)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    print(f"response.choices: {response.choices}")

    #텍스트가 포함된 응답이 없는경우 첫번째 응답 반환(빈값일숭있음)
    return response.choices[0].message.content


def main():
    massage_log = [
        {"role": "system", "content": "you are a helpful assistant"}
    ]

    # quit를 입력할때까지 실행되는 루프
    while True:

        #터미널에서 사용자의 입력받기
        user_input = input("You: ")

        if user_input.lower() == 'quit':
            print("Goodbuy!")
            break

        #사용자의 입력을 대화기록(log)에 추가하기
        massage_log.append({"role": "user", "content": user_input})

        #쳇봇에게 대화 기록을 보내 응답받기
        response = send_message(massage_log)

        #대화 기록에 챗봇의 응답을 추가하고 콘솔에 출력하기
        massage_log.append({"role": "assistant", "content": response})
        print(f"assistant: {response}")

if __name__ == "__main__":
    main()