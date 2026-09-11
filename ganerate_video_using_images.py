import os
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, VideoFileClip, concatenate_videoclips
import pandas as pd

def create_video(mp3_path, img_path):
    # 오디오 파일과 이미지 파일 열기
    audio_clip = AudioFileClip(mp3_path)
    image_clip = ImageClip(img_path)

    # 이미지를 오디오 길이에 맞게 설정
    image_clip = image_clip.with_duration(audio_clip.duration)

    # 동영상 생성하기
    video_clip = CompositeVideoClip([image_clip], size=image_clip.size)
    video_clip = video_clip.with_audio(audio_clip)

    # 이미지 파일명을 이용해 동영상 파일명 만들기
    dri, img_file_full_name = os.path.split(img_path)
    file_name, ext = os.path.splitext(img_file_full_name)

    print(dri)
    print(img_file_full_name)
    print(file_name)

    # videos 폴더가 없으면 생성
    os.makedirs("./videos", exist_ok=True)

    # 동영상 저장하기
    video_path = f"./videos/{file_name}.mp4"
    video_clip.write_videofile(video_path, fps=24)

    # 리소스 정리
    video_clip.close()
    audio_clip.close()

    return os.path.abspath(video_path)

#csv파일에서 mp3와 이미지 경로를 읽어와서 동영상을 생성하는 함수
def create_videos_from_playlist_csv(csv_file):
    df_playlist = pd.read_csv(csv_file, sep=';', encoding='utf-8')

    videos = list()
    for i, row in df_playlist.iterrows():
        if row['mp3'] == 'Not found' or row['info_image'] == 'Not found':
            videos.append(None)
        else:
            video_path = create_video(row['mp3'], row['info_image'])
            videos.append(video_path)

    return videos   


#머지
def merge_videos(video_paths, output_path):
    clips = [VideoFileClip(video) for video in video_paths]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, fps=24)

    # 리소스 정리
    final_clip.close()
    for clip in clips:
        clip.close()

    return output_path

def genertate_video_using_images(csv_file):
    videos = create_videos_from_playlist_csv(csv_file)
    videos = [video for video in videos if video is not None]  # None 값 제거

    dir, file_full_name = os.path.split(csv_file)
    file_name, ext = os.path.splitext(file_full_name)
    video_file_path = f'./videos/{file_name}.mp4'

    merge_videos(videos, video_file_path)

    return video_file_path

if __name__ == "__main__":
    genertate_video_using_images('./playlist/hiphop2015.csv')
    
    # vidoes = create_videos_from_playlist_csv('./playlist/hiphop2015.csv')
    # for video in vidoes:
    #     print(video)

    # video_path = create_video(
    #     mp3_path="./mp3/Can't_Stop_the_Feeling!_Justin_Timberlake.mp3",
    #     img_path="./images/Can't Stop the Feeling!_Justin Timberlake_album_art.jpg"
    # )

    # print(video_path)
