import tkinter as tk
from tkinter import scrolledtext
import openai
from dotenv import load_dotenv
import os
import pandas
from tkinter import filedialog
import json
from youtube_audio_download import download_songs_in_csv

# ==========================================
# OpenAI 설정
# ==========================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT_VERSION = os.getenv('GPT_VERSION')

openai.api_key = OPENAI_API_KEY

temperature = 0.1

global csv_file_path

# ==========================================
# 대화 기록
# ==========================================

message_log = [
    { 
        "role": "system", 
        "content": '''
- 당신은 플레이리스트를 만드는 DJ어시스턴트입니다. 
- 사용자는 한국인이므로 한국어로 의사소통해야 하지만, 아티스트명과 각 노래의 제목, 아티스트, 발매연도를 목록 형식으로 표시 한 뒤에.
사용자에게 '이 플레이리스트를 CSV로 저장하겠습니까?' 라고 물어보아야 합니다.
- 저장하려면 세미콜론(;)으로 구분한 CSV 형식의 헤더와 'YYYY' 형식의 발매 연도로 플레이리스트를 보여 주세요. 
CSV형식은 반드시 새로운 줄에서 시작해야 하고, CSV파일의 헤더는 반드시 영어여야 하며, 'Title; Artist; Release Date' 
형식으로 구성해야 합니다.
- 플레이리스트 csv 파일을 저장완료 했다면, 저장된 경로에 대한 file_path 를 무조건(must show) 보여주고, 플레이리스트를 mp3파일로 다운로드 할 건지 물어봐야 됩니다.
- 오류가 발생했다면 파이썬 오류 상세 내역을 답변해야됩니다.
            '''
    }
]

functions = [
    {
        'name': 'save_playlist_as_csv',
        'description': 'Save the given playlist data into a CSV file when the user confirms the playlist.',
        'parameters': {
            'type': 'object',
            'properties': {
                'playlist_csv': {
                    'type': 'string',
                    'description': '''A playlist in CSV format separated by ';'. 
                    It must contatins a header and the release year should follow the 'YYYY' format.
                    The CSV content must starts with a new line. 
                    The header of the CSV file must be in English and it should be 
                    formatted as follows: 'Title;Arrtist;Released'. '''
                }
            },
            'required': ['playlist_csv'],
        }
    },
    {
        'name': 'download_songs_in_csv',
        'description': 'Download mp3 of songs in the recent CSV file.',
        'parameters': {
            'type': 'object',
            'properties': {
                'csv_file': {
                    'type': 'string',
                    'description': 'The recent csv file path',
                }
            },
            'required': ['csv_file'],
        }
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
    input_box.delete('1.0', tk.END)

    # 종료 
    if user_input.lower() == 'quit' :
        root.destroy()
        return


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
            model=GPT_VERSION,
            messages=message_log,
            temperature=temperature,
            functions=functions,
            function_call = 'auto',
        )


        # ==================================
        # AI 응답 가져오기
        # ==================================

        response_message = response.choices[0].message.content
        response_message_obj = response.choices[0].message

        if response_message_obj.get("function_call"):
            available_functions = {
                'save_playlist_as_csv': save_playlist_as_csv,
                'download_songs_in_csv': download_songs_in_csv,
            }
            function_name = response_message_obj['function_call']['name']
            function_to_call = available_functions[function_name]
            function_args = json.loads(response_message_obj['function_call']['arguments'])
            #사용하는 함수에 따라 사용하는 인자의 개수와 내용이 달라질 수 있으므로 function_args 로 처리하기
            function_response = function_to_call(**function_args)

            if function_name == 'save_playlist_as_csv':
                function_response, csv_file_path = function_response

            #답변과 함수 실행 결과를 메시지로그에 추가
            message_log.append(response_message_obj)
            message_log.append({
                'role': 'function',
                'name': function_name,
                'content': f'{function_response}',
            })

            #실행 결과를 GPT에 보내 새 답변 받아내기
            response = openai.ChatCompletion.create(
                model = GPT_VERSION,
                messages = message_log,
                temperature = temperature,
            )

            response_message = response.choices[0].message.content
        

        # ==================================
        # 대화 기록에 AI 응답 추가
        # ==================================

        message_log.append({
            "role": "assistant",
            "content": response_message
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
            f"Assistant: {response_message}\n\n",
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
# 판다스 데이터프레임
# ==========================================

def extract_dataframe(response_text):

    lines = response_text.splitlines()

    csv_lines = []
    csv_started = False

    for line in lines:

        line = line.strip()

        # CSV 헤더 발견
        if line.lower() == "title; artist; release date":
            csv_started = True
            csv_lines.append(line)
            continue

        # CSV가 시작된 이후
        if csv_started:

            # 빈 줄이면 CSV 종료
            if not line:
                break

            # 세미콜론이 없으면 CSV 종료
            if ";" not in line:
                break

            csv_lines.append(line)

    # CSV가 없으면 None
    if not csv_lines:
        return None

    from io import StringIO

    csv_text = "\n".join(csv_lines)

    df = pandas.read_csv(
        StringIO(csv_text),
        sep=";"
    )

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 데이터 공백 제거
    df = df.map(
        lambda x: x.strip() if isinstance(x, str) else x
    )

    return df

# ==========================================
# CSV파일로 저장하기
# ==========================================
def save_to_csv(df):
    file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    if file_path:
        df.to_csv(file_path, sep=';', index=False)
        return f'파일을 저장했습니다. 저장 경로는 다음과 같습니다.\n{file_path}\n이 플레이리스트의 음원을 내려받겠습니까?', file_path
    return '저장을 취소했습니다', None

def save_playlist_as_csv(playlist_csv):
    if ';' in playlist_csv:
        lines = playlist_csv.strip().split('\n')
        csv_data = []

        for line in lines:
            if ';' in line:
                csv_data.append(line.split(';'))

        if len(csv_data) > 0:
            df = pandas.DataFrame(csv_data[1:], columns=csv_data[0])
            return save_to_csv(df)
    return f'저장에 실패했습니다. \n저장에 실패한 내용은 다음과 같습니다. \n{playlist_csv}', None


# ==========================================
# GUI 생성
# ==========================================

root = tk.Tk()

root.title("GPT Powered DJ")

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