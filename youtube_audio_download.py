import csv
import os
from youtube_search import YoutubeSearch #유튜브 검색 모듈
import yt_dlp #유튜브 내려받기 모듈
import re

def normalize_text(text):
    text = text.lower()

    # 특수문자를 공백으로 변경
    text = re.sub(r'[^가-힣a-z0-9]+', ' ', text)

    # 여러 공백을 하나로 변경
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def is_relevant_video_title(video_title, song_title, song_artist):

    video = normalize_text(video_title)
    title = normalize_text(song_title)

    # 제목 확인
    title_match = title in video

    # 아티스트를 "-" 기준으로 나눔
    artist_names = song_artist.split('-')

    artist_match = False

    for artist_name in artist_names:

        artist_name = normalize_text(artist_name)

        if artist_name and artist_name in video:
            artist_match = True
            break

    print(
        f"영상: {video_title} | "
        f"제목: {title_match} | "
        f"가수: {artist_match}"
    )

    return title_match and artist_match

# 파일명에서 부적절한 문자를 제거하고 공백 문자를 대체하는 함수
def sanitize_filename(filename):
    return re.sub('[\\\\/:*?"<>|]', '', filename).replace(' ', '_')

# 파일 다운로드
def download_song(title, artist):
    query=f"{title} {artist} audio"

    # youtubeSearch 모듈로 쿼리에 대한 검색 결과를 리스트로 받아오기
    search_result = YoutubeSearch(query, max_results=5).to_dict()

    print(f'search_result {search_result}')

    file_name = sanitize_filename(f'{title}_{artist}')

    for searched in search_result:
        video = searched
        # video_url = f"https://www.youtube.com{search_result[0]['url_suffix']}"
        video_id = video['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        if is_relevant_video_title(video['title'], title, artist):

            #유튜브 내려받기 옵션
            ydl_opts = {
                'format': 'bestaudio/best', #최상의품질
                'postprocessors': [ #추출한 파일을 mp3로 변환
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192'
                    }, #비트율 192
                ],
                'ffmpeg_location': '/usr/local/bin',
                # 'outtmpl': f"{title} - {artist}.%(ext)s", #파일명설정
                'quiet': True, #내려받는 도중에 출력되는 로그 숨기기
                'socket_timeout': 30,
                'noplaylist': True,
                'outtmpl': f"./mp3/{file_name}.%(ext)s",
            }

            #yt_dlp 라이브러리를 이용해 동영상 내려받기
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            return f"./mp3/{file_name}.mp3"
    return None

# csv 파일에 있는 노래들을 내려받는 함수
def download_songs_in_csv(csv_file):
    result_dict = dict()

    # 파일을 읽어거 각 행을 처리
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        # csv.DictReader를 이용해 CSV 파일 읽기
        reader = csv.DictReader(csvfile, delimiter=';')

        #필드명
        if 'mp3' not in reader.fieldnames:
            fieldnames = reader.fieldnames + ['mp3']
        else :
            fieldnames = reader.fieldnames

        #결과를 저장할 새 csv 파일 생성하기
        temp_ouptut_file = csv_file.replace('.csv', '__emp.csv')
        with open(temp_ouptut_file, 'w', encoding='utf-8', newline='') as output_csvfile:
            # 작성자 객체 생성하고 필드명 사용하기
            writwer = csv.DictWriter(output_csvfile, fieldnames=fieldnames, delimiter=';')
            writwer.writeheader() #헤더 작성

            # 각 행마다 반복해서 download_song 함수 호출하기
            for row in reader:
                title = row['Title']
                artist = row['Artist']

                filepath = download_song(title, artist)
                if filepath:
                    row['mp3'] = filepath
                    result_dict[f'{title} - {artist}'] = filepath
                else :
                    row['mp3'] = 'Not found'
                    result_dict[f'{title} - {artist}'] = 'Not found'

                writwer.writerow(row) #새로운 csv 파일에 행 작성하기

        #원본 csv파일을 삭제하고 temp_output_file의 이름을 csv_file로 바꾸기
        os.remove(csv_file)
        os.rename(temp_ouptut_file, csv_file)

        return result_dict

if __name__ == '__main__':
    #입력파일의 경로
    # file_path = './1.csv'
    file_path = './playlist/hiphop2015.csv'

    result = download_songs_in_csv(file_path)
    for k, r in result.items():
        print(k, r)



