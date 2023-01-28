import pytube
import io
import moviepy.editor
import threading


class YoutubeDowloader:
    def __init__(self, url, mode, quality, name, extention, destination) -> None:
        print('Starting downloader')
        self.url = url
        self.mode = mode
        self.quality = quality
        self.name = name
        self.extention = extention
        self.destination = destination
        
        self.yt: list[pytube.YouTube] = self._create_video_obj()


    def _create_video_obj(self) -> list[pytube.YouTube]:
        """Return a list containing one or more pytube.YouTube elemenst

        Returns:
            list[pytube.YouTube]: list of pytube.YouTube objects
        """
        if "watch?v=" in self.url:
            return [pytube.YouTube(self.url)]  # Return as a list

        elif "playlist?list=" in self.url:
            return list(pytube.Playlist(self.url).videos)


    def get_av_stream(self, yt: pytube.YouTube) -> tuple[pytube.Stream, pytube.Stream]:
        """Get the audio and video stream matching the class atributes

        Args:
            yt (pytube.YouTube): The youtube object

        Returns:
            tuple[pytube.Stream, pytube.Stream]: Audio and video streams respectively
        """
        # get streams
        stream = yt.streams

        # get the rigth steam for the the rigth mode:
        stream_audio = stream.filter(only_audio=True) if self.mode == 'audio' else pytube.StreamQuery([])  # empty stream query
        stream_video = stream.filter(only_video=True) if self.mode == 'video' else pytube.StreamQuery([])

        # sort the streams
        stream_audio = stream_audio.order_by('abr')
        stream_video = stream_video.order_by('resolution')

        # get the stream acordiong to the determined quality
        stream_audio = stream_audio.last() if self.quality == 'high' else (None if IndexError else stream_audio[len(stream_audio) // 2]) if self.quality == 'medium' else stream_audio.first()
        stream_video = stream_video.last() if self.quality == 'high' else (None if IndexError else stream_video[len(stream_video) // 2]) if self.quality == 'medium' else stream_video.first()
        
        return stream_audio, stream_video
        
    def merge_streams(self, stream_audio: pytube.Stream, stream_video: pytube.Stream) -> moviepy.editor.VideoFileClip:
        """Merge togheter audio and video streams into a moviepy.editor.VideoFileClip object 

        Args:
            stream_audio (pytube.Stream): Audio stream
            stream_video (pytube.Stream): Video steam

        Returns:
            moviepy.editor.VideoFileClip: Video with audio
        """
        # Create a BytesIO object from the audio stream data
        audio_data = io.BytesIO()
        stream_audio.download(audio_data)
        audio_data.seek(0)
        
        # Create a BytesIO object from the video stream data
        video_data = io.BytesIO()
        stream_video.download(video_data)
        video_data.seek(0)

        # Create an audio clip object
        audio = moviepy.editor.AudioFileClip(audio_data)
        
        # Create a video clip object
        video = moviepy.editor.VideoFileClip(video_data)

        # Set the audio of the video clip
        video.audio = audio

        # Return the video with the audio
        return video
    
    def download_file(self, video_file: moviepy.editor.VideoFileClip):
        video_file.write_videofile(filename=f'{self.destination}/{self.name}.{self.extention}')
    
    def dowload_stream(self, stream: pytube.Stream):
        stream.download(output_path=self.destination, filename=f"{self.name}.{self.extention}")

    def start(self):
        pass # todo
