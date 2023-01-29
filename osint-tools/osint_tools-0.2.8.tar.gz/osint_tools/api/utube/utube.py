# from pytube import YouTube
import subprocess
'''
download utube stream in chunks while it is in progress

url="https://www.youtube.com/watch?v=kEfldEpDMQA"

chunk_stream() {
    # youtube-dl --list-formats $1
    local manifest=$(youtube-dl -f 95 -g $1)
    echo $manifest

    ffmpeg -i $manifest -c copy utube.mp4
    # ffmpeg -i $manifest -c copy -f segment -segment_time 10 output-part%d.mp4
    # ffmpeg -i 'https://....m3u8' -c copy -f segment -segment_time 1800 output-part%d.mp4

}
chunk_stream $url
'''

'''
Looking for someone who can write a python script that will accept the video id of a YouTube Livestream, and record it to a local mp4 file.

Please respond with a proposal and include an estimated min/max cost.

More details:
- You can use whatever open source python libs needed.
- The script should always choose the 720p stream from YouTube, and the resulting mp4 file should be 720p
- The script should accept 3 arguments: 
    - url of the YT LiveStream ID, 
    - duration for each recorded 'chunk', 
    - how many chunks to record.
- You can use this live stream url for testing: https://www.youtube.com/watch?v=kEfldEpDMQA

example:
to record the livestream above, for 3 chunks of 15 minutes per chunk, you would run something similar to the following:
$ python you_tube_recorder.py kEfldEpDMQA 15 3

The implementation does not have to be *exactly* what is suggested above, that's just an example.  
Anything that achieves the outcome desired will be acceptable.

- 1/3 when you can demo the script working (either via a screen recording or a quick zoom call/screenshare)
- 1/3 payment will be made upon delivery of the script
- Final 1/3 payment will be made when the script is tested good/working on our end using the test URL above.
'''

def get_props(yt):
    s = f'''
    title:   {yt.title}
    thumb:   {yt.thumbnail_url}
    streams: {yt.streams}
    '''
    return s


def chunck_stream(url):
    '''
    - on_progress_callback function will run whenever a chunk is downloaded from a video, and is called with three arguments: 
        - the stream, 
        - the data chunk, 
        - the bytes remaining in the video. 
            - This could be used, for example, to display a progress bar.
            
    - on_complete_callback function will run after a video has been fully downloaded, and is called with two arguments: 
        - the stream and the file path. 
        - This could be used, to perform post-download processing on a video like trimming the length of it.

    >>> yt = YouTube(
        'http://youtube.com/watch?v=2lAe1cqCOXo',
        on_progress_callback=progress_func,
        on_complete_callback=complete_func,
        proxies=my_proxies,
        use_oauth=False,
        allow_oauth_cache=True
    )
    '''
    # yt = YouTube(url)
    # return yt
    return ''

def get_chunck_stream(url: str, duration: int, chunk_count: int):
    get_meta = f'$(youtube-dl -f 95 -g {url})'
    cmd = f"ffmpeg -i {get_meta} -c copy -f segment -segment_time {duration} output-part%d.mp4"
    output = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    print(output)

