import os
import sys
from uuid import uuid4
import cv2
from argparse import ArgumentParser
from typing import TypedDict
from utils import exists_file, mk_dir


class DataType(TypedDict):
    path: str
    output: str
    threshold: float
    number_screenshots: int
    remove_duplicates: bool


def get_video_duration(video_path: str) -> float:
    """Obtém a duração do vídeo em segundos usando OpenCV."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f'Não foi possível abrir o vídeo: {video_path}')
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    return frame_count / fps if fps > 0 else 0

def is_not_pixelated(image, threshold=100):
    """Verifica se a imagem não está pixelada usando a variação dos gradientes."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian > threshold

def calculate_orb_similarity(img1, img2):
    """Calcula a similaridade entre duas imagens usando ORB e BFMatcher."""
    orb = cv2.ORB.create()
    kp1, des1 = orb.detectAndCompute(cv2.UMat(img1), cv2.UMat())
    kp2, des2 = orb.detectAndCompute(cv2.UMat(img2), cv2.UMat())
    
    if des1 is None or des2 is None or len(kp1) == 0 or len(kp2) == 0:
        return 0
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1.get(), des2.get())
    
    return len(matches) / max(len(kp1), len(kp2))

def remove_duplicates(image_path: str, threshold: float):
    """Remove imagens duplicadas com base na similaridade ORB."""
    image_paths = [os.path.join(image_path, file) for file in os.listdir(image_path)]
    unique_images = []
    removed_images = []
    
    for img_path in image_paths:
        img = cv2.imread(img_path)
        if img is None:
            continue
        
        is_unique = True
        for u_img_path in unique_images:
            u_img = cv2.imread(u_img_path)
            similarity = calculate_orb_similarity(img, u_img)
            if similarity >= threshold:
                is_unique = False
                break
        
        if is_unique:
            unique_images.append(img_path)
        else:
            os.remove(img_path)
            removed_images.append(img_path)
            print(f'Removendo imagem duplicada: {img_path}')

def capture_screenshots(info: DataType):
    """Captura screenshots distribuídos ao longo do tempo do vídeo."""
    video_path, output, num_screenshots = info['path'], info['output'], info['number_screenshots']
    duration = get_video_duration(video_path)
    interval = duration / num_screenshots

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f'Não foi possível abrir o vídeo: {video_path}')

    fps = cap.get(cv2.CAP_PROP_FPS)

    for i in range(num_screenshots):
        timestamp = i * interval
        frame_number = int(timestamp * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, frame = cap.read()
        if success and is_not_pixelated(frame):
            output_image = os.path.join(output, f'screenshot_{uuid4()}.jpg')
            cv2.imwrite(output_image, frame)
            print(f'Screenshot {i + 1} salvo: {output_image}')
    cap.release()

def main(args: DataType):
    capture_screenshots(args)
    if args['remove_duplicates']:
        remove_duplicates(args['output'], args['threshold'])

if __name__ == '__main__':
    parser = ArgumentParser(
        prog='screenshot-video',
    )

    parser.add_argument(
        '--path',
        help='caminho do video',
        type=exists_file,
        required=True
    )

    parser.add_argument(
        '--output', '-o',
        help='caminho do diretório de saída (padrão: %(default)s)',
        type=mk_dir,
        default=os.path.join(os.path.curdir, 'output')
    )

    parser.add_argument(
        '--number-screenshots', '--num-sshots',
        help='número de screenshots (padrão: %(default)s)',
        type=int,
        default=200
    )

    parser.add_argument(
        '--threshold', '-t',
        help='limite de similaridade (padrão: %(default)s)',
        type=float,
        default=0.6
    )

    parser.add_argument(
        '--remove-duplicates', '-r',
        help='remover os prints duplicados (padrão: %(default)s)',
        action='store_true'
    )

    args = parser.parse_args(sys.argv[1:])
    main_args: DataType = args.__dict__ # type: ignore
    main(main_args)