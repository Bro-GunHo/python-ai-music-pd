from gpt_image_gen import generate_gpt_image
from dream_like_diffusion_image_gen import generate_dreamlike_image
from add_info_to_album_art import make_album_art
import pandas as pd
import torch
import time

def generate_images_for_songs(csv_file):
    df_playlist = pd.read_csv(csv_file, sep=';', encoding='utf-8')

    is_cuda_or_mps_available = torch.cuda.is_available() or torch.backends.mps.is_available()

    image_file_path = list()
    info_image_file_path = list()

    response_str = '다음 곡의 이미지를 생성했습니다.'

    print(f"CUDA or MPS available: {is_cuda_or_mps_available}")

    for i, row in df_playlist.iterrows():
        print(f"Processing row {i}: {row['Title']} - {row['Artist']}")
        if row['mp3'] == 'Not found':
            image_file_path.append(None)
            info_image_file_path.append(None)
        else:
            if is_cuda_or_mps_available:
                image_file = generate_dreamlike_image(row['Title'], row['Artist'])
            else:
                try:
                    image_file = generate_gpt_image(row['Title'], row['Artist'])
                except:
                    print('Something went wrong...')
                    image_file = None
                time.sleep(5)  # 이미지 생성 후 5초 대기
            image_file_path.append(image_file)

            info_image_file = make_album_art(image_file, row['Title'], row['Artist'])
            info_image_file_path.append(info_image_file)

            response_str += f"\n{row['Title']}\t{row['Artist']}\t{image_file}"

    df_playlist['image'] = image_file_path
    df_playlist['info_image'] = info_image_file_path

    df_playlist.to_csv(csv_file, sep=';', encoding='utf-8')

    return response_str


if __name__ == "__main__":
    csv_file = './playlist/hiphop2015.csv'
    response_str = generate_images_for_songs(csv_file)
    print(response_str)
    