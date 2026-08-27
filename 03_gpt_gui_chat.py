import tkinter as tk
from tkinter import scrolledtext
import openai
from dotenv import load_dotenv
import os


# ==========================================
# OpenAI 설정
# ==========================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY


# ==========================================
# 대화 기록
# ==========================================

message_log = [
    {
        "role": "system",
        "content": "you are a helpful assistant"
    }
]


# ==========================================
# 메시지 전송
# ==========================================

def send_message():

    # 입력창에서 사용자 메시지 가져오기
    user_input = input_box.get("1.0", tk.END).strip()

    if not user_input:
        return

    # 입력창 비우기
    input_box.delete("1.0", tk.END)


    # ======================================
    # 사용자 메시지 출력
    # ======================================

    chat_box.config(state="normal")

    chat_box.insert(
        tk.END,
        f"You: {user_input}\n\n",
        "user"
    )


    # ======================================
    # 생각중... 표시
    # ======================================

    chat_box.insert(
        tk.END,
        "Assistant: 생각중...\n",
        "thinking"
    )

    chat_box.config(state="disabled")

    chat_box.see(tk.END)

    # 화면 갱신
    root.update()


    # ======================================
    # 대화 기록에 사용자 메시지 추가
    # ======================================

    message_log.append({
        "role": "user",
        "content": user_input
    })


    try:

        # ==================================
        # OpenAI API 호출
        # ==================================

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_log,
            temperature=0.5,
        )


        # ==================================
        # AI 응답 가져오기
        # ==================================

        assistant_message = response.choices[0].message.content


        # ==================================
        # 대화 기록에 AI 응답 추가
        # ==================================

        message_log.append({
            "role": "assistant",
            "content": assistant_message
        })


        # ==================================
        # 생각중... 삭제
        # ==================================

        chat_box.config(state="normal")

        # thinking 태그가 적용된 부분 찾기
        start = chat_box.tag_ranges("thinking")

        if start:
            chat_box.delete(
                start[0],
                start[1]
            )


        # ==================================
        # 실제 AI 응답 출력
        # ==================================

        chat_box.insert(
            tk.END,
            f"Assistant: {assistant_message}\n\n",
            "assistant"
        )

        chat_box.config(state="disabled")

        chat_box.see(tk.END)


    except Exception as e:

        # ==================================
        # 오류 발생
        # ==================================

        chat_box.config(state="normal")

        # 생각중... 삭제
        start = chat_box.tag_ranges("thinking")

        if start:
            chat_box.delete(
                start[0],
                start[1]
            )

        chat_box.insert(
            tk.END,
            f"오류 발생: {e}\n\n",
            "assistant"
        )

        chat_box.config(state="disabled")

        chat_box.see(tk.END)


# ==========================================
# Enter 키 처리
# ==========================================

def enter_pressed(event):

    send_message()

    # Enter로 줄바꿈되는 것 방지
    return "break"


# ==========================================
# GUI 생성
# ==========================================

root = tk.Tk()

root.title("AI Chatbot")

root.geometry("600x700")


# ==========================================
# 대화 결과창
# ==========================================

chat_box = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Arial", 12),
    state="disabled"
)

chat_box.pack(
    padx=10,
    pady=10,
    fill=tk.BOTH,
    expand=True
)


# ==========================================
# 메시지 배경색 설정
# ==========================================

# 사용자 메시지
chat_box.tag_config(
    "user",
    background="lightblue"
)

# AI 메시지
chat_box.tag_config(
    "assistant",
    background="lightgray"
)

# 생각중 메시지
chat_box.tag_config(
    "thinking",
    background="lightgray"
)


# ==========================================
# 사용자 입력창
# ==========================================

input_box = tk.Text(
    root,
    height=5,
    font=("Arial", 12)
)

input_box.pack(
    padx=10,
    pady=(0, 10),
    fill=tk.X
)


# ==========================================
# 전송 버튼
# ==========================================

send_button = tk.Button(
    root,
    text="전송",
    command=send_message,
    height=2
)

send_button.pack(
    padx=10,
    pady=(0, 10),
    fill=tk.X
)


# ==========================================
# Enter 키로 전송
# ==========================================

input_box.bind(
    "<Return>",
    enter_pressed
)


# ==========================================
# 프로그램 실행
# ==========================================

root.mainloop()