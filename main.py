# IMPORTS #
from downloader import filter_stream_query, merge_streams, dowload_any
import argparse
import os
import re
import pytube


def format_destination_path(path: str) -> str:
    return path.rstrip("/\\")


def dowloads_path() -> str:
    folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
    return folder if os.path.exists(folder) else None
    
    
def validate_youtube_url(url: str) -> str:
    video_pattern = r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/watch\?v=[a-zA-Z0-9\-_]+$"
    playlist_pattern = r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/playlist\?list=[a-zA-Z0-9\-_]+$"
    match_video = re.match(video_pattern, url)
    match_playlist = re.match(playlist_pattern, url)
    if not (match_video or match_playlist):
        raise argparse.ArgumentTypeError("This url is invalid. A valid url should look like this: https://www.youtube.com/watch?v=dQw4w9WgXcQ")  
    return url


def download_single(yt: pytube.YouTube, stream_type: str, quality: str, destination) -> str:
    print(f'Colecting video {yt.title}')
    query = yt.streams

    print('Setting download preferences')
    if stream_type == 'av':
        stream = (filter_stream_query(query, 'audio', quality),
                  filter_stream_query(query, 'video', quality))
    else:
        stream = (filter_stream_query(query, stream_type, quality), None)
            
    file = merge_streams(*stream) if stream[1] is not None else stream[0]
    
    name = stream[0].default_filename
    extention = 'mp3' if stream_type == 'audio' else 'mp4'
    
    print('Downloading file')
    dowload_any(file, destination, name, extention)
    print(f'Downloaded {yt.title}')
    return f'{destination}/{name}/{extention}'


def main(args: argparse.Namespace) -> int:
    print('Starting...')
    
    download = None
    
    if "watch?v=" in args.url:  # single video
        print('Video detected')
        download = download_single(pytube.YouTube(args.url), args.mode, args.quality, args.destination)

    else:
        print('Playlist detected')
        playlist = pytube.Playlist(args.url)
        for yt in playlist.videos:
            download = download_single(yt, args.mode, args.quality, args.destination)
    
    print(f'Done! Download in: {download}')
    return 0


if __name__ == '__main__':    
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Youtube video dowloader')

    parser.add_argument('url', type=validate_youtube_url, help='The url of the video, shorts, or playlist')
    parser.add_argument('-m', '--mode', type=str, help='Just audio; just video; or audio and video', metavar='', choices=['audio', 'video', 'av'], default='av')
    parser.add_argument('-q', '--quality', type=str, help='Preferred quality of the dowload', metavar='', choices=['high', 'medium', 'low'], default='medium')
    parser.add_argument('-d', '--destination', type=format_destination_path, help='Path to here to dowload the file', metavar='', default=dowloads_path() or os.getcwd())
    
    args = parser.parse_args()
    main(args)
