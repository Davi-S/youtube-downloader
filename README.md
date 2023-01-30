# youtube-downloader

A simple, yet powerful command-line utility to download YouTube videos and audio.

## Usage

```
usage: youtube-downloader.py [-h] [-m {audio,video,av}] [-q {high,medium,low}] [-d DESTINATION] [-t] url

Youtube video dowloader

positional arguments:
    url                                                 The url of the video, shorts, or playlist

optional arguments:
    -h, --help                                          show this help message and exit
    -m {audio,video,av}, --mode {audio,video,av}        Just audio, just video, or audio and video
    -q {high,medium,low}, --quality {high,medium,low}   Preferred quality of the dowload. High quality may result in long download time
    -d DESTINATION, --destination DESTINATION           Path to here to dowload the file
    -t, --thread                                        Use multithread to process playlists
```

## Requirements

- moviepy==1.0.3
- pytube==12.1.2

## Installation

```
pip install moviepy pytube
```


## Contribute

Feel free to contribute to the project by submitting issues and/or pull requests.