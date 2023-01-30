import pytube
import io
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
    file.write_videofile(filename=f'{destination}/{name}.{extention}', logger=None)


def _dowload_stream(stream: pytube.Stream, destination: str, name: str, extention: str) -> None:
    stream.download(output_path=destination, filename=f"{name}.{extention}")


def dowload_any(file, destination: str, name: str, extention: str) -> None:
    if type(file) == pytube.Stream:
        _dowload_stream(file, destination, name, extention)
    else:
        _download_file(file, destination, name, extention)
