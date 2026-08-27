import openai
import json
from dotenv import load_dotenv
import os


# ==========================================
# OpenAI 설정
# ==========================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT_VERSION = os.getenv("GPT_VERSION")

openai.api_key = OPENAI_API_KEY

# 실제로 구현한다면 날씨 정보 api를 이용해야 되지만 여기서는 예시를 위해 간단하게 하드 코딩된 함수를 제공합니다.
def get_current_weather(location, unit = 'fahrenheit'):
    '''location 으로 받은 지역의 날씨를 알려주는 기능'''
    weather_info = {
        'location' : location,
        "temperature": "72",
        'unit': unit,
        'forecast' : ["sunny", "windy"],
    }

    return json.dumps(weather_info)

def run_conversation():
    #1단계 : message  뿐만 아니라 사용할 수 있는 함수에 대한 설명 추가
    messages = [{'role': 'user', 'content': 'What`s the weather like in Boston?'}]
    functions = [
        {
            'name': 'get_current_weather',
            'description': 'get the current weather in a given location',
            'parameters': {
                'type': 'object',
                'properties': {
                    'location': {
                        'type': 'string', 
                        'description': 'the city and state, e.g. San francisco, CA'
                    },
                    'unit': {'type': 'string', 'enum': ['celsius', 'fahrenheit']}
                },
                'required': ['location']
            }
        }
    ]
    response = openai.ChatCompletion.create(
        model=GPT_VERSION,
        messages = messages,
        functions = functions,
        function_call = 'auto'
    )
    # assistant_message = response.choices[0].message.content
    response_message = response.choices[0].message

    print(response_message)

    #gpt의 응답이 function을 실행해해야된도다고 판단했는지 확인하기
    if response_message.get("function_call"):
       available_functions = {'get_current_weather': get_current_weather}
       function_name = response_message['function_call']['name']
       function_to_call = available_functions[function_name]
       function_args = json.loads(response_message['function_call']['arguments'])
       function_response=function_to_call(
           location = function_args.get('location'),
           unit = function_args.get("unit"),
       )

       #실행한 결과를 GPT에게 보내 답을 받아오기 위한 부분
       messages.append({
           'role': 'function',
           'name' : function_name,
           'content': function_response,
           })
       second_response = openai.ChatCompletion.create(
           model = GPT_VERSION,
           messages=messages,
       ) #함수 실행 결과를 GPT에 보내 새로운 답변 받아오기
       return second_response

print(run_conversation())
       
