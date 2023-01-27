# IMPORTS #
import argparse
import os
import re
from downloader import YoutubeDowloader

def get_dowloads_path():
        folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
        return folder if os.path.exists(folder) else None
    
    
def valid_youtube_url(url: str) -> bool:
    video_pattern = r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/watch\?v=[a-zA-Z0-9\-_]+$"
    playlist_pattern = r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/playlist\?list=[a-zA-Z0-9\-_]+$"
    match_video = re.match(video_pattern, url)
    match_playlist = re.match(playlist_pattern, url)
    if not (match_video or match_playlist):
        raise argparse.ArgumentTypeError("This url is invalid. A valid url should look like this: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return url


def main(args: argparse.Namespace):
    YoutubeDowloader(args).download()
    print('Done!')


if __name__ == '__main__':    
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Youtube video dowloader')

    parser.add_argument('url', type=valid_youtube_url, help='The url of the video, shorts, or playlist')
    parser.add_argument('-m', '--mode', type=str, help='"mp3" just audio; or "mp4" audio and video', metavar='', choices=['mp3', 'mp4'], default='mp4')
    parser.add_argument('-q', '--quality', type=str, help='Preferred quality of the dowload', metavar='', choices=['high', 'medium', 'low'], default='high')
    parser.add_argument('-d', '--destination', type=str, help='Where to dowload the file', metavar='', default=get_dowloads_path() or os.getcwd())
    parser.add_argument('-n', '--name', type=str, help='The name that the file will be saved', metavar='')
    parser.add_argument('-f', '--fast_dowload', action='store_true', help='Dowload the video rigth after collecting it')
    
    args = parser.parse_args()
    main(args)
