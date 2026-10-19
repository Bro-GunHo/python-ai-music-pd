from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips, TextClip, CompositeVideoClip
import pandas as pd
import os
import time

def create_text_clip(text, fontsize, duration, position, start):

    font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"

    txt_clip = TextClip(text=text,
        font=font_path,
        font_size=fontsize,
        color='white')
    txt_clip = txt_clip.with_position(position).with_duration(duration).with_start(start)
    return txt_clip

def combine_videos_and_music(mp3_files, video_files, titles, artists, output_filename):
    # 영상 파일 합치기
    video_clips = [VideoFileClip(video_file) for video_file in video_files]
    concat_video = concatenate_videoclips(video_clips)

    # 오디오 파일 합치기
    audio_clips = [AudioFileClip(mp3_file) for mp3_file in mp3_files]
    concat_audio = concatenate_audioclips(audio_clips)

    # 합쳐진 동영상의 길이와 플레이리스트의 길이 비교하기
    video_duration = concat_video.duration
    audio_duration = concat_audio.duration

    if video_duration > audio_duration:
        concat_video = concat_video.subclipped(0, audio_duration)
    while video_duration < audio_duration:
        remainder = audio_duration - video_duration
        if remainder > video_duration:
            remainder = video_duration
        extra_video = concat_video.subclipped(0, remainder)
        concat_video = concatenate_videoclips([concat_video, extra_video])

        video_duration = concat_video.duration
        audio_duration = concat_audio.duration

    # 영상의 소리를 없애고 플레이 리스트로 대체하기
    concat_video = concat_video.with_audio(concat_audio)

    # 곡 제목과 아티스트명 표기하기
    text_clips = []
    start_time = 0

    # 영상의 길이와 높이에 따라 글자 크기 설정하기
    video_width, video_height = concat_video.size
    title_font_size = int(video_height * 0.05)  # 영상 높이의 5%로 글자 크기 설정
    artist_font_size = int(video_height * 0.08)  # 영상 높이의 8%로 글자 크기 설정
    left_margin=title_font_size
    title_y = int(video_height * 0.7)  # 영상 높이의 70% 위치에 제목 표시
    artist_y = int(title_y + title_font_size * 1.2)  # 영상 높이의

    for idx, audio_clip in enumerate(audio_clips):
        title_text = create_text_clip(titles[idx], title_font_size, audio_clip.duration, (left_margin, title_y), start_time)
        artist_text = create_text_clip(artists[idx], artist_font_size, audio_clip.duration, (left_margin, artist_y), start_time)
        text_clips.append([title_text, artist_text])

        start_time += audio_clip.duration

    composite_clips = [concat_video] + [text for text_group in text_clips for text in text_group]
    final_video = CompositeVideoClip(composite_clips)

    encoding_start_at = time.time()
    final_video.write_videofile(output_filename, audio_codec='aac', fps=24)
    encoding_finish_at = time.time()

    print(encoding_start_at)
    print(encoding_finish_at)
    time_passed = encoding_finish_at - encoding_start_at
    print(f'{time_passed} sec')
    print(f'{time_passed // 60} min \t {time_passed % 60} sec')

    return output_filename

def generate_video_using_mp4(csv_file, video_filess):
    df_playlist = pd.read_csv(csv_file, sep=';', encoding='utf-8')
    df_playlist = df_playlist.loc[df_playlist['mp3'] != 'Nout found']
    df_playlist.reset_index(inplace=True)
    df_playlist.drop(columns=['index'], inplace=True)
    mp3_files = df_playlist['mp3']
    titles = df_playlist['Title']
    artists = df_playlist['Artist']

    # csv 파일명을 이용해 동영상 파일명 만들기
    dir, file_full_name= os.path.split(csv_file)
    file_name, ext = os.path.splitext(file_full_name)
    video_file_path = f"./videos/{file_name}.mp4"

    return combine_videos_and_music(mp3_files, video_filess, titles, artists, video_file_path)


if __name__ == "__main__":
    video_files = [
        "./videos/1.mp4",
        "./videos/2.mp4",
        "./videos/3.mp4"        
    ]

    df_playlist = pd.read_csv("./playlist/hiphop2015.csv", sep=';', encoding='utf-8')
  
    csv_file = "./playlist/hiphop2015.csv"
    video_file_path = generate_video_using_mp4(csv_file, video_files)
    print(video_file_path)

