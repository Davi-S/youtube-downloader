# IMPORTS #
import argparse
import os
import re
import pytube
import concurrent.futures
import time
import moviepy.editor

def filter_stream_query(stream_query: pytube.StreamQuery, stream_type: str, quality: str) -> pytube.Stream:
        """Get the audio/video stream from streamquery that matches the class atributes (quality and mode)

        Args:
            yt (pytube.YouTube): The youtube object

        Returns:
            pytube.Stream: Video stream
        """
        # get the rigth mode and sort
        streams_mode = stream_query.filter(only_audio=stream_type == 'audio', only_video=stream_type == 'video')
        stream_sort = streams_mode.order_by('abr' if stream_type == 'audio' else 'resolution')
        
        if quality == 'high':
            stream = stream_sort.last()
        
        elif quality == 'medium':
            stream = stream_sort[len(stream_sort) // 2]
        
        elif quality == 'low':
            stream = stream_sort.first()
            
        return stream
    

def merge_streams(stream_audio: pytube.Stream, stream_video: pytube.Stream) -> moviepy.editor.VideoFileClip:
    """Merge togheter audio and video streams into a moviepy.editor.VideoFileClip object 

    Args:
        stream_audio (pytube.Stream): Audio stream
        stream_video (pytube.Stream): Video steam

    Returns:
        moviepy.editor.VideoFileClip: Video with audio
    """
    audio = moviepy.editor.AudioFileClip(stream_audio.url)
    video = moviepy.editor.VideoFileClip(stream_video.url)

    # Set the audio of the video clip and return it
    video.audio = audio
    return video


def _download_file(file: moviepy.editor.VideoFileClip, destination: str, name: str, extention: str='mp4') -> None:
    file.write_videofile(filename=f'{destination}/{name}.{extention}', threads=15, logger=None)


def _dowload_stream(stream: pytube.Stream, destination: str, name: str, extention: str) -> None:
    stream.download(output_path=destination, filename=f"{name}.{extention}")


def dowload_any(file, destination: str, name: str, extention: str) -> None:
    if type(file) == pytube.Stream:
        _dowload_stream(file, destination, name, extention)
    else:
        _download_file(file, destination, name, extention)


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
    print(f'{"Colecting video":<30} {yt.title}')
    query = yt.streams

    print(f'{"Setting preferences to":<30} {yt.title}')
    if stream_type == 'av':
        stream = (filter_stream_query(query, 'audio', quality),
                  filter_stream_query(query, 'video', quality))
    else:
        stream = (filter_stream_query(query, stream_type, quality), None)
            
    file = merge_streams(*stream) if stream[1] is not None else stream[0]
    
    name = stream[0].default_filename
    extention = 'mp3' if stream_type == 'audio' else 'mp4'
    
    print(f'{"Downloading":<30} {yt.title}')
    dowload_any(file, destination, name, extention)
    print(f'{"Downloaded":<30} {yt.title}')
    return f'{destination}/{name}/{extention}'


def main(args: argparse.Namespace) -> int:
    start_time = time.perf_counter()
    print('Starting...')
    
    if "watch?v=" in args.url:  # single video
        print('Video detected')
        download_single(pytube.YouTube(args.url), args.mode, args.quality, args.destination)

    else:
        print('Playlist detected')
        playlist = pytube.Playlist(args.url)
        
        if args.thread:
            print('Using multithread')
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_results = [executor.submit(download_single, yt, args.mode, args.quality, args.destination) for yt in playlist.videos]
                _ = [future.result() for future in concurrent.futures.as_completed(future_results)]

        else: 
            for yt in playlist.videos:
                download_single(yt, args.mode, args.quality, args.destination)
        
    print(f'Done! Download in: {args.destination}')
    
    print(f'Executed in {time.perf_counter() - start_time:.2f} seconds')
    return 0


def pre_main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Youtube video dowloader')

    parser.add_argument('url', type=validate_youtube_url, help='The url of the video, shorts, or playlist')
    parser.add_argument('-m', '--mode', type=str, help='Just audio, just video, or audio and video', choices=['audio', 'video', 'av'], default='av')
    parser.add_argument('-q', '--quality', type=str, help='Preferred quality of the dowload. High quality may result in long download time', choices=['high', 'medium', 'low'], default='medium')
    parser.add_argument('-d', '--destination', type=format_destination_path, help='Path to here to dowload the file', default=dowloads_path() or os.getcwd())
    parser.add_argument('-t', '--thread', action='store_true', help='Use multithread to process playlists')
    
    args = parser.parse_args()
    
    main(args)
    
if __name__ == '__main__':
    pre_main()
    
