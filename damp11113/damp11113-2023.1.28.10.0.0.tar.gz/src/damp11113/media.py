import libscrc
import pyaudio
import vlc
import pafy, pafy2
import ffmpeg
import cv2
import string
import tqdm
import numpy as np
import qrcode
import barcode
from barcode.writer import ImageWriter
import os
from PIL import Image
from .utils import get_size_unit
from .randoms import rannum
from .file import sizefolder3, removefile, allfiles, sort_files
import yt_dlp as youtube_dl2
from pyzbar import pyzbar
import colorsys

class vlc_player:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def load(self, file_path):
        self.media = self.instance.media_new(file_path)
        self.player.set_media(self.media)
        return f"Loading {file_path}"

    def play(self):
        self.player.play()
        return f"Playing {self.media.get_mrl()}"

    def pause(self):
        self.player.pause()
        return f"Pausing {self.media.get_mrl()}"

    def stop(self):
        self.player.stop()
        return f"Stopping {self.media.get_mrl()}"

    def get_position(self):
        return self.player.get_position()

    def set_position(self, position):
        self.player.set_position(position)
        return f"Setting position to {position}"

    def get_state(self):
        return self.player.get_state()

    def get_length(self):
        return self.media.get_duration()

    def get_time(self):
        return self.player.get_time()

    def set_time(self, time):
        self.player.set_time(time)
        return f"Setting time to {time}"

    def get_rate(self):
        return self.player.get_rate()

    def set_rate(self, rate):
        self.player.set_rate(rate)
        return f"Setting rate to {rate}"

    def get_volume(self):
        return self.player.audio_get_volume()

    def set_volume(self, volume):
        self.player.audio_set_volume(volume)
        return f"Setting volume to {volume}"

    def get_mute(self):
        return self.player.audio_get_mute()

    def set_mute(self, mute):
        self.player.audio_set_mute(mute)
        return f"Setting mute to {mute}"

    def get_chapter(self):
        return self.player.get_chapter()

    def set_chapter(self, chapter):
        self.player.set_chapter(chapter)
        return f"Setting chapter to {chapter}"

    def get_chapter_count(self):
        return self.media.get_chapter_count()

    def get_title(self):
        return self.player.get_title()

    def set_title(self, title):
        self.player.set_title(title)
        return f"Setting title to {title}"

    def get_title_count(self):
        return self.media.get_title_count()

    def get_video_track(self):
        return self.player.video_get_track()

    def set_video_track(self, track):
        self.player.video_set_track(track)
        return f"Setting video track to {track}"

    def get_video_track_count(self):
        return self.media.get_video_track_count()

    def get_audio_track(self):
        return self.player.audio_get_track()

    def set_audio_track(self, track):
        self.player.audio_set_track(track)
        return f"Setting audio track to {track}"

    def get_audio_track_count(self):
        return self.media.get_audio_track_count()

    def get_spu_track(self):
        return self.player.video_get_spu()

    def set_spu_track(self, track):
        self.player.video_set_spu(track)
        return f"Setting subtitle track to {track}"

    def get_spu_track_count(self):
        return self.media.get_spu_track_count()

    def get_chapter_description(self, chapter):
        return self.media.get_chapter_description(chapter)

    def toggle_fullscreen(self):
        self.player.toggle_fullscreen()
        return f"Toggling fullscreen"

    def get_fullscreen(self):
        return self.player.get_fullscreen()

    def get_video_resolution(self):
        return (self.player.video_get_width(), self.player.video_get_height())

    def get_fps(self):
        return self.player.get_fps()

class youtube_stream:
    def __init__(self, url):
        self.stream = pafy.new(url)

    def video_stream(self, resolution=None):
        if resolution is None:
            best = self.stream.getbestvideo()
        else:
            best = self.stream.getbestvideo().resolution(resolution)
        return best.url

    def audio_stream(self):
        best = self.stream.getbestaudio()
        return best.url

    def best_stream(self, resolution=None):
        if resolution is None:
            best = self.stream.getbest()
        else:
            best = self.stream.getbest().resolution(resolution)
        return best.url

    def get_title(self):
        return self.stream.title

    def get_dec(self):
        return self.stream.description

    def get_length(self):
        return self.stream.length

    def get_thumbnail(self):
        return self.stream.thumb

    def get_author(self):
        return self.stream.author

    def get_likes(self):
        return self.stream.likes

    def get_dislikes(self):
        return self.stream.dislikes

    def get_views(self):
        return self.stream.viewcount

class youtube_stream2:
    def __init__(self, url):
        self.stream = pafy2.new(url)
        self.ydl = youtube_dl2.YoutubeDL()
        self.url = url

    def video_stream(self, resolution=None):
        if resolution is None:
            best = self.stream.getbestvideo()
        else:
            best = self.stream.getbestvideo().resolution(resolution)
        return best.url

    def audio_stream(self):
        best = self.stream.getbestaudio()
        return best.url

    def best_stream(self, preftype="mp4"):
        best = self.stream.getbest(preftype=preftype)
        return best.url

    def get_streams(self):
        return self.ydl.extract_info(self.url, download=False)['formats']

    def get_id(self):
        return self.ydl.extract_info(self.url, download=False)['id']

    def get_title(self):
        return self.ydl.extract_info(self.url, download=False)['title']

    def get_dec(self):
        return self.ydl.extract_info(self.url, download=False)['description']


class ffmpeg_stream:
    def __init__(self) -> None:
        pass

    def load(self, file_path):
        self.stream = ffmpeg.input(file_path)
        return f"Loaded {file_path}"

    def write(self, file_path, acodec='mp4', ac=2, hz='44100', bitrate='320'):
        ffmpeg.run(self.stream.output(file_path, acodec=acodec, ac=ac, ar=hz, **{'b:a': f'{bitrate}k'}))
        return f"Writing {file_path}"

    def streaming(self, url, acodec='mp4', ac=2, hz='44100', bitrate='320'):
        ffmpeg.run(self.stream.output(url, acodec=acodec, ac=ac, ar=hz, **{'b:a': f'{bitrate}k'}))
        return f"Streaming {url}"


def clip2frames(clip_path, frame_path, currentframe=1, filetype='png'):
    try:
        clip = cv2.VideoCapture(clip_path)
        length = int(clip.get(cv2.CAP_PROP_FRAME_COUNT))
        progress = tqdm.tqdm(total=length, unit='frame')
        progress.set_description(f'set output to {frame_path}')
        if not os.path.exists(frame_path):
            os.mkdir(frame_path)
            progress.set_description(f'create output folder {frame_path}')
        progress.set_description(f'converting... ')
        while True:
            size = get_size_unit(sizefolder3(frame_path))
            ret, frame = clip.read()
            PILframe = CV22PIL(frame)
            PILframe.save(f'{frame_path}/{str(currentframe)}' + f'.{filetype}')
            progress.set_description(f'converting... | filetype .{filetype} | converted {currentframe}/{length} | file {currentframe}.{filetype} | used {size}')
            currentframe += 1
            progress.update(1)
            if currentframe == length:
                progress.set_description(f'converted {currentframe} frame | used {size} MB')
                progress.close()
                break
    except Exception as e:
        progress = tqdm.tqdm(total=0)
        progress.set_description(f'error: {e}')
        progress.close()

def im2ascii(image, width=None, height=None, new_width=None, chars=None, pixelss=25):
    try:
        try:
            img = Image.open(image)
            img_flag = True
        except:
            print(image, "Unable to find image ")

        if width is None:
            width = img.size[0]
        if height is None:
            height = img.size[1]
        if new_width is None:
            new_width = width
        aspect_ratio = int(height)/int(width)
        new_height = aspect_ratio * new_width * 0.55
        img = img.resize((new_width, int(new_height)))

        img = img.convert('L')

        if chars is None:
            chars = ["@", "J", "D", "%", "*", "P", "+", "Y", "$", ",", "."]
            #chars = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
            #chars = list(string.printable)

        pixels = img.getdata()
        new_pixels = [chars[pixel//pixelss] for pixel in pixels]
        new_pixels = ''.join(new_pixels)
        new_pixels_count = len(new_pixels)
        ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
        ascii_image = "\n".join(ascii_image)
        return ascii_image

    except Exception as e:
        raise e

def im2pixel(image, i_size, output):
    img = Image.open(image)
    small_img = img.resize(i_size, Image.BILINEAR)
    res = small_img.resize(img.size, Image.NEAREST)
    res.save(output)

def repixpil(pilarray, i_size):
    small_img = pilarray.resize(i_size, Image.BILINEAR)
    res = small_img.resize(pilarray.size, Image.NEAREST)
    return res

def resizepil(pilarray, i_size):
    return pilarray.resize(i_size, Image.ANTIALIAS)

def qrcodegen(text, showimg=False, save_path='./', filename='qrcode', filetype='png', version=1, box_size=10, border=5, fill_color="black", back_color="white", error_correction=qrcode.constants.ERROR_CORRECT_L, fit=True):
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=fit)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    if showimg:
        img.show()
    else:
        img.save(f'{save_path}{filename}.{filetype}')

def barcodegen(number, type='ean13', showimg=False, save_path='./', filename='barcode', filetype='png', writer=ImageWriter()):
    barcode_img = barcode.get(type, number, writer=writer)
    if showimg:
        img = Image.open(barcode_img.save(f'{save_path}{filename}.{filetype}'))
        img.show()
        removefile(barcode_img.save(f'{save_path}{filename}.{filetype}'))
    else:
        barcode_img.save(f'{save_path}{filename}.{filetype}')

def imseq2clip(imseq, path, videoname='video.mp4', fps=30):
    progress = tqdm.tqdm()
    progress.set_description(f'please wait...')
    simseq = sort_files(allfiles(imseq), reverse=False)
    img = []
    for i in simseq:
        i = path+i
        img.append(i)
    progress.set_description(f'converting...')
    progress.total = len(img)
    progress.unit = 'frame'
    cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(path+videoname, cv2_fourcc, fps)
    for i in range(len(img)):
        progress.set_description(f'converting... | frame {i}/{len(img)}')
        frame = cv2.imread(img[i])
        video.write(frame)
        progress.update(1)

    video.release()
    progress.set_description(f'converted')

def readbqrcode(image):
    image = Image.open(image)
    qr_code = pyzbar.decode(image)[0]
    data = qr_code.data.decode("utf-8")
    type = qr_code.type
    return (data, type)

def PIL2CV2(pil_image):
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

def CV22PIL(cv2_array):
    return Image.fromarray(cv2.cvtColor(cv2_array, cv2.COLOR_BGR2RGB))

def image_high_pass(image, opath):
    img = cv2.imread(image)
    hpf = img - cv2.GaussianBlur(img, (21, 21), 3)+127
    cv2.imwrite(opath, hpf)

def image_levels(image, minv=0, maxv=255, gamma=1.0):
    class Level(object):
        def __init__(self, minv, maxv, gamma):
            self.minv= minv/255.0
            self.maxv= maxv/255.0
            self._interval= self.maxv - self.minv
            self._invgamma= 1.0/gamma

        def new_level(self, value):
            if value <= self.minv: return 0.0
            if value >= self.maxv: return 1.0
            return ((value - self.minv)/self._interval)**self._invgamma

        def convert_and_level(self, band_values):
            h, s, v= colorsys.rgb_to_hsv(*(i/255.0 for i in band_values))
            new_v= self.new_level(v)
            return tuple(int(255*i)
                    for i
                    in colorsys.hsv_to_rgb(h, s, new_v))
    """Level the brightness of image (a PIL.Image instance)
    All values ≤ minv will become 0
    All values ≥ maxv will become 255
    gamma controls the curve for all values between minv and maxv"""

    if image.mode != "RGB":
        raise ValueError("this works with RGB images only")

    new_image= image.copy()

    leveller= Level(minv, maxv, gamma)
    levelled_data= [
        leveller.convert_and_level(data)
        for data in image.getdata()]
    new_image.putdata(levelled_data)
    return new_image

def image2stripes(image, opath, radius=10, minv=0, maxv=255, gamma=1.0):
    background = Image.open(image)
    img = PIL2CV2(background)
    hpf = img - cv2.GaussianBlur(img, ((radius * 10) +1, (radius * 10) +1), 1)+(9*20)
    output = image_levels(CV22PIL(hpf), minv=minv, maxv=maxv, gamma=gamma)
    output.save(opath)

def ranpix(opath, size=(512, 512)):
    im = Image.new("RGB", size=size)
    width, height = im.size
    for x in range(width):
        for y in range(height):
            L = rannum(0, 255)
            R = rannum(0, 255)
            G = rannum(0, 255)
            B = rannum(0, 255)
            LRGB = (L, R, G, B)
            im.putpixel((x, y), LRGB)
    im.save(opath)

def PIL2DPG(pil_image):
    return CV22DPG(PIL2CV2(pil_image))

def CV22DPG(cv2_array):
    data = np.flip(cv2_array, 2)
    data = data.ravel()
    data = np.asfarray(data, dtype='f')
    return np.true_divide(data, 255.0)

def PromptPayQRcode(account,one_time=True,country="TH",money="",currency="THB"):
    """
    text_qr(account,one_time=True,country="TH",money="",currency="THB")
    account is phone number or  identification number.
    one_time : if you use once than it's True.
    country : TH
    money : money (if have)
    currency : THB
    """
    Version = "0002"+"01" # เวชั่นของ  PromptPay
    if one_time==True: # one_time คือ ต้องการให้โค้ดนี้ครั้งเดียวหรือไม่
        one_time="010212" # 12 ใช้ครั้งเดียว
    else:
        one_time="010211" # 11 ใช้ได้้หลายครั้ง
    merchant_account_information="2937" # ข้อมูลผู้ขาย
    merchant_account_information+="0016"+"A000000677010111" # หมายเลขแอปพลิเคชั่น PromptPay
    if len(account)!=13: # ใช้บัญชีใช้เป็นเบอร์มือถือหรือไม่ ถ้าใช่ จำนวนจะไม่เท่ากับ 13
        account=list(account)
        merchant_account_information+="011300" # 01 หมายเลขโทรศัพท์ ความยาว 13 ขึ้นต้น 00
        if country=="TH":
            merchant_account_information+="66" # รหัสประเทศ 66 คือประเทศไทย
        del account[0] # ตัดเลข 0 หน้าเบอร์ออก
        merchant_account_information+=''.join(account)
    else:
        merchant_account_information+="02"+account.replace('-','') # กรณีที่ไม่รับมือถือ แสดงว่าเป็นเลขบัตรประชาชน
    country="5802"+country # ประเทศ
    if currency=="THB":
        currency="5303"+"764" # "764"  คือเงินบาทไทย ตาม https://en.wikipedia.org/wiki/ISO_4217
    if money!="": # กรณีกำหนดเงิน
        check_money=money.split('.') # แยกจาก .
        if len(check_money)==1 or len(check_money[1])==1: # กรณีที่ไม่มี . หรือ มีทศนิยมแค่หลักเดียว
            money="54"+"0"+str(len(str(float(money)))+1)+str(float(money))+"0"
        else:
            money="54"+"0"+str(len(str(float(money))))+str(float(money)) # กรณีที่มีทศนิยมครบ
    check_sum=Version+one_time+merchant_account_information+country+currency+money+"6304" # เช็คค่า check sum
    check_sum1=hex(libscrc.ccitt(check_sum.encode("ascii"),0xffff)).replace('0x','')
    if len(check_sum1)<4: # # แก้ไขข้อมูล check_sum ไม่ครบ 4 หลัก
        check_sum1=("0"*(4-len(check_sum1)))+check_sum1
    check_sum+=check_sum1
    return check_sum.upper() # upper ใช้คืนค่าสตริงเป็นตัวพิมพ์ใหญ่

def change_color_bit(image, output, colorbit=64):
    img = Image.open(image)
    a = img.convert("P", palette=Image.ADAPTIVE, colors=colorbit)
    a.save(output)

#-----------------pyaudio-effect-------------------------
def stretch(snd_array, factor, window_size, h):
    """ Stretches/shortens a sound, by some factor. """
    phase = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros(int(len(snd_array) / factor + window_size))
    for i in np.arange(0, len(snd_array) - (window_size + h), h*factor):
        i = int(i)
        # Two potentially overlapping subarrays
        a1 = snd_array[i: i + window_size]
        a2 = snd_array[i + h: i + window_size + h]

        # The spectra of these arrays
        s1 = np.fft.fft(hanning_window * a1)
        s2 = np.fft.fft(hanning_window * a2)

        # Rephase all frequencies
        phase = (phase + np.angle(s2/s1)) % 2*np.pi

        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
        i2 = int(i/factor)
        result[i2: i2 + window_size] += hanning_window*a2_rephased.real
    return result.astype('int16')

def speedx(sound_array, factor):
    """ Multiplies the sound's speed by some `factor` """
    indices = np.round( np.arange(0, len(sound_array), factor) )
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[ indices.astype(int) ]

def pitchshift(snd_array, n, window_size=2**13, h=2**11):
    """ Changes the pitch of a sound by ``n`` semitones. """
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)

def speed_change(sound, speed=1.0):
    """
    To using

    from pydub import AudioSegment

    sound = AudioSegment.from_file(infile)

    slow_sound = speed_change(sound, 0.850)

    slow_sound.export(outfile, format="mp3")


    """
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def getinputdevice():
    lis = []
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            lis.append([i, p.get_device_info_by_host_api_device_index(0, i).get('name')])
    return lis

def EdgeDetection(cvarray):
    # Convert to graycsale
    img_gray = cv2.cvtColor(cvarray, cv2.COLOR_BGR2GRAY)
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)  # Canny Edge Detection
    return edges