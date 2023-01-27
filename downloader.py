import pytube
import argparse

class YoutubeDowloader:
    def __init__(self, args: argparse.Namespace) -> None:
        print('Starting downloader')
        self.args: argparse.Namespace = args
        self.yt: list[pytube.YouTube] = self._create_video_obj()
        self.streams: list[pytube.Stream] = self._get_stream()

    def _create_video_obj(self) -> list[pytube.YouTube]:
        if "watch?v=" in self.args.url:
            return [pytube.YouTube(self.args.url)]  # Return as a list

        elif "playlist?list=" in self.args.url:
            return list(pytube.Playlist(self.args.url).videos)

    def _get_stream(self):  # todo: download audio and video to merge them in high quality moviepy
        strm = []
        for count, video in enumerate(self.yt, start=1):
            print(f'Colecting video {count}/{len(self.yt)}')
            stream = video.streams
            stream = stream.filter(only_audio=self.args.mode == 'mp3',
                                   progressive=self.args.mode == 'mp4')
            stream = stream.order_by('abr' if self.args.mode == 'mp3' else 'resolution')
            
            if self.args.quality == 'medium':
                stream = stream[len(stream)//2]
            else:
                stream = stream.last() if self.args.quality == 'high' else stream.first()
                
            print(f'Video colected {count}/{len(self.yt)}')
            
            if self.args.fast_dowload:  # download the stream just after colection
                print(f'Starting download {count}/{len(self.yt)}')
                self._dowload_single(stream)
                print(f'Download complete {count}/{len(self.yt)}')
            
            else:  # save stream
                strm.append(stream)
                
        return strm
    
    def _dowload_single(self, stream:pytube.Stream):
        stream.download(filename=f"{self.args.name if self.args.name is not None else stream.title}.{self.args.mode}",
                        output_path=self.args.destination)

    def download(self):
        # if 'self.args.fast_dowload' is true 'self.streams' will be empty and nothing will happend here      
        for count, stream in enumerate(self.streams, start=1):
            print(f'Starting download {count}/{len(self.streams)}')
            self._dowload_single(stream)
            print(f'Download complete {count}/{len(self.streams)}')
        
        return
