import struct
import binascii
import shutil
import boto3.session
from PIL import Image, ImageDraw, ImageFont, ExifTags
import os
import random
from alive_progress import alive_bar
from shapely.geometry import Polygon
from shapely.geometry import box
from smart_open import open as op

end_point_url = "https://kr.object.ncloudstorage.com"
origin_data_path = "../data/origin/"
label_data_path = "../data/label/"

"""
    TTA 데이터 품질 검증 프로젝트에서 데이터 전처리 하면서 필요한 모듈들을 정리
    S3 버킷에 접속, 버킷내 파일 확인, 필요한 샘플링 작업 진행!!
    압축 파일 생성, 시각화 이미지, box, polygon IoU 값 계산 등
    필요한 메소드들을 차근히 정리해서 만들어 놓자
"""


class S3_controll:
    def __init__(self) -> None:
        global end_point_url

        # bucket_name 변수
        self.__bucket = str()
        # target_path 즉, 버킷 내의 경로 변수
        self.__prefix = str()
        self.__aws_access_key_id = str()
        self.__aws_secret_access_key = str()
        self.__endpoint_url = end_point_url
        self.__profile_name = str()
        self.__region_name = str()
        self.__s3_client = boto3.session
        self.__data_path_list = list()
        self.__s3_resource = str()

    # ---------------------------------------------------
    # Check of S3 configure setting Value
    # ---------------------------------------------------

    def _s3_connect_test(self):
        """
            s3 접속에 잘 되었는지 확인하는 함수
        """
        try:
            obj_list = self.__s3_resource.list_objects(
                Bucket=self.__bucket,
                Prefix=self.__prefix
            )
            try:
                contents_list = obj_list["Contents"]
                if contents_list is not Exception:
                    print("AWS Connect Success, Thank you.")
            except Exception as contents_e:
                print("Not Found Contents - Plz Check your Prefix\n", self.__prefix)

        except Exception as e:
            print("AWS Connect ERROR - View Context = ", e)

    # ---------------------------------------------------
    # AWS S3 configure setting
    # ---------------------------------------------------

    def s3_configure(
            self,
            bucket=None,
            prefix=None,
            aws_access_key_id=None,
            aws_secret_access_key=None,
            # endpoint_url='https://kr.object.ncloudstorage.com',
            profile_name=None,
            region_name=None
    ):
        send_your_except = "{} is required to connect to AWS S3."

        # ------------------------------------------------------
        # Bucket Name 저장
        # ------------------------------------------------------
        if bucket is not None:
            self.__bucket = bucket
        else:
            print(send_your_except.format("BUCKET NAME"))
            return
        # ------------------------------------------------------
        # Prefix 경로 저장
        # ------------------------------------------------------
        if prefix is not None:
            self.__prefix = prefix
        else:
            print(send_your_except.format("PREFIX"))
            return
        # ------------------------------------------------------
        # __profile_name 저장
        # 만약 __profile_name 존재할 경우 --> aws_access_key_id, aws_secret_access_key 필요 X
        # 없으면 aws_access_key_id랑 key 값을 입력해야 한다.
        # ------------------------------------------------------
        if profile_name is not None:
            self.__profile_name = profile_name
            s3_client = self.__s3_client.Session(
                profile_name=self.__profile_name
            )
            if self.__endpoint_url is not None:
                self.__s3_resource = s3_client.client(
                    service_name='s3',
                    endpoint_url=self.__endpoint_url
                )
            else:
                self.__s3_resource = s3_client.client(
                    service_name='s3'
                )
        else:
            if aws_access_key_id is None or aws_secret_access_key is None or region_name is None:
                print(send_your_except.format(
                    "'aws_access_key_id' & 'aws_secret_access_key' & '__region_name'"))
                return
            else:
                self.__aws_access_key_id = aws_access_key_id
                self.__aws_secret_access_key = aws_secret_access_key
                self.__region_name = region_name
                s3_client = self.__s3_client.Session(
                    aws_access_key_id=self.__aws_access_key_id,
                    aws_secret_access_key=self.__aws_secret_access_key,
                    region_name=self.__region_name
                )
                if self.__endpoint_url is not None:
                    self.__s3_resource = s3_client.client(
                        service_name='s3',
                        endpoint_url=self.__endpoint_url
                    )
                else:
                    self.__s3_resource = s3_client.client(
                        service_name='s3')

        self._s3_connect_test()

        # ------------------------------------------
        # botocore.client.S3 값을 리턴!!
        # ------------------------------------------
        return self.__s3_resource

    def s3_get_path_list(self):
        if self.__bucket == '' or self.__prefix == '':
            print("To use s3_get_sample(), s3_configure() must be set.")
        else:
            with alive_bar(0, title="파일 확인: ", force_tty=True)as bar:
                pages = self.__s3_resource.get_paginator("list_objects_v2").paginate(
                    Bucket=self.__bucket,
                    Prefix=self.__prefix
                )
                for page in pages:
                    for content in page["Contents"]:
                        obj_name = content["Key"]
                        obj_size = content["Size"]

                        if obj_size == 0:
                            continue
                        self.__data_path_list.append(obj_name)
                        bar.text = os.path.basename(obj_name)
                        bar()

        return self.__data_path_list


class S3_wavfile_check:
    """
        TypeError: no default __reduce__ due to non-trivial __cinit__ 
            --> pickle 문제가 있는데 이부분은 좀더 공부해야 되지만 현재는 멀티프레싱 하기에는 다소 문제점이 있음
            --> multiprocessing시 각각의 CPU가 접속하기 위해 계속적인 리셋이 필요하기에 새로이 클래스 선정
    """

    def __init__(self, bucket_name, profile_name) -> None:
        global end_point_url

        self.__bucket = bucket_name
        self.__s3_client = boto3.session
        self.__profile_name = profile_name
        self.__s3_resource = str()
        self.__endpoint_url = end_point_url

    def s3_wavfile_playtime_check(self, wav_path, error_list=[]):

        blocks_2 = [["Subchunk1ID", "B", 4], ["Subchunk1", "L", 4], ["AudioFormat", "L", 2], ["NumChannels", "L", 2], ["SampleRate", "L", 4],
                    ["ByteRate", "L", 4], ["BlockAlign", "L", 2], ["BitsPerSample", "L", 2]]
        i = 0
        extra = 0
        # sampleRate = ""
        # audioFormat = ""
        # numChannels = ""
        # bitsPerSample = ""
        play_time = 0
        data_length = 0
        tmp_arr = []  # self로 변수 설정하였더니 중복되는 값이 발생한 거 같음 그래서 함수 시작할 때마다 리셋이 필요한거 같음!!

        s3_client = self.__s3_client.Session(profile_name=self.__profile_name)
        self.__s3_resource = s3_client.client(
            service_name="s3", endpoint_url=self.__endpoint_url)

        def Little(data):
            if len(data) == 4:
                data = struct.pack("<I", int(binascii.b2a_hex(data), 16))
                return binascii.b2a_hex(data)
            elif len(data) == 2:
                data = struct.pack("<h", int(binascii.b2a_hex(data), 16))
                return binascii.b2a_hex(data)

        def Big(data):
            return binascii.b2a_hex(data)

        def check_s3_bucket_file_size(path):

            response = self.__s3_resource.get_object(
                Bucket=self.__bucket, Key=path)
            content_lenght = response["ContentLength"]

            return content_lenght

        def output_duration(length):
            hours = length // 3600
            length %= 3600
            mins = length // 60
            length %= 60
            seconds = length

            return hours, mins, seconds

        with op(f"s3://{self.__bucket}/{wav_path}", "rb", transport_params={"client": self.__s3_resource})as wf:
            end_flag = True
            wav_binary_data = wf.readline()
            while end_flag:
                wav_binary_data_2 = wf.readline()
                if b"data" in wav_binary_data:
                    wav_binary_data += wav_binary_data_2
                    end_flag = False
                else:
                    wav_binary_data += wav_binary_data_2

            try:
                i = str(binascii.b2a_hex(wav_binary_data))[2:].index(
                    str(binascii.hexlify(b'fmt '))[2:-1]) // 2

            except:
                print(wav_path)
                print(wav_binary_data)
                error_list.append(
                    {"file_path": wav_path, "binary_data": wav_binary_data})
                pass
            for blc in blocks_2:
                # if blc[1] == "B":
                #     print(f"{blc[0]} = {Big(wav_binary_data[i:i+blc[2]])} ({wav_binary_data[i:i+blc[2]]})")
                if blc[0] == "AudioFormat":

                    audioFormat = int(Little(wav_binary_data[i:i+blc[2]]), 16)
                elif blc[0] == "NumChannels":
                    numChannels = int(Little(wav_binary_data[i:i+blc[2]]), 16)
                elif blc[0] == "SampleRate":
                    sampleRate = int(Little(wav_binary_data[i:i+blc[2]]), 16)
                elif blc[0] == "BitsPerSample":
                    bitsPerSample = int(
                        Little(wav_binary_data[i:i+blc[2]]), 16)
                # else:
                #     print(f"{blc[0]} = {Little(wav_binary_data[i:i+blc[2]])} ({wav_binary_data[i:i+blc[2]]})")
                i += blc[2]

            # extra = str(binascii.b2a_hex(wav_binary_data))[2:].index(str(binascii.hexlify(b'data'))[2:-1]) //2 - i
            # extra_blocks = [["ExtraParmSize", "L", 2], ["ExtraParams", "L", extra - 2]]
            # if extra > 0:
            #     for blc in extra_blocks:
            #         if blc[1] == "B":
            #             print(f"{blc[0]} = {Big(wav_binary_data[i:i+blc[2]])} ({wav_binary_data[i:i+blc[2]]})")
            #         else:
            #             print(f"{blc[0]} = {Little(wav_binary_data[i:i+blc[2]])} ({wav_binary_data[i:i+blc[2]]})")
            #         i += blc[2]
            file_size = check_s3_bucket_file_size(wav_path)
            if numChannels == 1 and bitsPerSample == 8:
                data_length = file_size - 44
                play_time = int(data_length / sampleRate)
            elif numChannels == 2 and bitsPerSample == 16:
                data_length = int(file_size / 4 - 11)
                play_time = int(data_length / sampleRate)
            else:
                data_length = int(file_size / 2 - 22)
                play_time = int(data_length / sampleRate)
            hours, mins, seconds = output_duration(play_time)
            tmp_arr.append({"file_path": wav_path, "total_play_time": f"{hours}시간 {mins}분 {seconds}초",
                            "origin_seconds": play_time, "fs": sampleRate, "len_data": data_length})
        return tmp_arr


class S3_download:

    def __init__(self, profile_name, bucket_name) -> None:
        global label_data_path, origin_data_path, end_point_url

        self.__profile_name = profile_name
        self.__bucket_name = bucket_name
        self.__endpoint_url = end_point_url
        # json 파일 다운로드 위치
        self.__label_data_path = label_data_path
        # 원천 데이터 파일 다운로드 위치
        self.__origin_data_path = origin_data_path
        self.__s3_client = boto3.session
        self.__s3_resource = str()

    def s3_bucket_file_download(self, path):

        session = self.__s3_client.Session(
            profile_name=self.__profile_name)
        self.__s3_resource = session.client(
            service_name="s3", endpoint_url=self.__endpoint_url)

        if path.endswith(".json"):
            os.makedirs(
                f"{self.__label_data_path}{os.path.dirname(path)}", exist_ok=True)
            file_path = os.path.join(self.__label_data_path, path)
        else:
            os.makedirs(
                f"{self.__origin_data_path}{os.path.dirname(path)}", exist_ok=True)
            file_path = os.path.join(self.__origin_data_path, path)

        self.__s3_resource.download_file(self.__bucket_name, path, file_path)

        return path


class Ph_use_method:
    def __init__(self) -> None:
        # 압축하려는 원천데이터 경로
        self.__source = str()
        # 압축하고자 하는 원천데이터 폴더 경로
        self.__destination = str()
        # 구분자 .(dot) 개수를 파악해서 기입
        self.__num = int()
        # 해당 폴더내에 있는 파일 수량 확인
        self.__folder_path = str()
        # 시각화 이미지를 하기위한 좌표 리스트(안에는 딕셔너리 형태로 {"file_path": file_path, "bbox": bbox_list, "polygon": polygon_list, "type": annotation_type})표현 필수
        # 이미지 오픈할 경로
        self.__img_path = str()
        # 시각화할 좌표값
        self.__data = list()
        # 리스트 내에 데이터를 랜덤으로 추출할 때 필요한 원천 리스트
        self.__folder_list = list()
        # IOU 값 계산할 때 필요한 좌표값
        self.__pred_bbox = list()
        self.__gt_bbox = list()
        self.__pred_polygon = list()
        self.__gt_polygon = list()

    def make_archive(self, source=None, destination=None, num=1) -> None:
        self.__source = source
        self.__destination = destination
        self.__num = num
        base = os.path.basename(self.__destination)
        # 폴더명에 '.' 가 있을 경우 그 숫자를 판단해야 한다. 다르게 하는 방법 모색
        name = base.split(".")[self.__num]
        format = base.split(".")[self.__num + 1]
        archive_from = os.path.dirname(self.__source)
        archive_to = os.path.basename(self.__source.strip(os.sep))
        print(archive_from)
        print(archive_to)
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move(f"{name}.{format}", self.__destination)

    def loadfont(fontsize=50):
        # ttf파일의 경로를 지정합니다.
        ttf = '/Users/parkhwan/Downloads/D2Coding-Ver1.3.2-20180524/D2CodingLigature/D2CodingBold-Ver1.3.2-20180524-ligature.ttf'
        return ImageFont.truetype(font=ttf, size=fontsize,)

    def get_files_count(self, folder_path=None):
        self.__folder_path = folder_path
        dirListing = os.listdir(self.__folder_path)

        return dirListing

    def image_draw(self, data):
        """
            Polygon, keypoint, polyline 구조는 [[x1, y1], [x2, y2] ... [Xx, Yy]] 이런식으로 이중 배열 구조로 되어 있어야 함
            bbox 구조는 [[x1, y1, x2, y2], [x1, y1, x2, y2], ...]
            함수에 사용되는 인자 구조는 [{"file_path": file_path, "bbox or polygons or keypoints or polyline": bbox or polygon or keypoints or polyline, 
            "type": "bbox","polygon","etc."}]
            이러한 형태로 와야 함 
        """
        self.__font = loadfont()
        self.__img_path = data["file_path"]
        self.__type = data["type"]
        if self.__type == "bbox":
            self.__data = data["bbox"]
        elif self.__type == "polygon":
            self.__data = data["polygons"]
        elif self.__type == "keypoints":
            self.__data = data["keypoints"]
        else:
            self.__data = data["polyline"]
        os.makedirs(
            f"../output/masking/{os.path.dirname(self.__img_path)}", exist_ok=True)
        img = Image.open(f"{origin_data_path}{self.__img_path}").convert("RGB")
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == "Orientation":
                    break
            exif = dict(img.getexif().items())

            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            print("EXIF 데이터가 없습니다.")
            pass
        draw = ImageDraw.Draw(img)
        if self.__type == "polygon":
            try:
                tuple_poly = tuple(tuple(x) for x in self.__data)
                draw.line(tuple_poly + tuple_poly[0], fill="red", width=3)
            except:
                print(
                    f"이미지에 그림 그려질 Polygon 좌표가 없는 경우의 파일 경로: {self.__img_path}")
        elif self.__type == "bbox":
            for data in self.__data:
                try:
                    draw.rectangle(data, outline=(255, 0, 0), width=2)
                except:
                    print(
                        f"이미지에 그림 그려질 bbox 좌표가 없는 경우의 파일 경로: {self.__img_path}")
        else:
            try:
                tuple_poly = tuple(tuple(x) for x in self.__data)
                draw.line(tuple_poly, fill="red", width=3)
            except:
                print(
                    f"이미지에 그림 그려질 kepoint, polyline 좌표가 없는 경우의 파일 경로: {self.__img_path}")
        img.save(f"../output/masking/{self.__img_path}")

    def get_random(self, folder_list, cnt):
        self.__folder_list = folder_list
        tmp_list = self.__folder_list
        random.shuffle(tmp_list)

        return tmp_list[:cnt]

    def get_bbox_IoU(self, pred_bbox, gt_bbox):
        """
            bbox iou 값 계산 공식
            Input: 
                bbox 구조 ex>
                pred_bbox = [{"left": 10, "top": 20, "width": 12, "height": 20}]
                gt_bbox = [{"left": 10, "top": 20, "width": 12, "height": 20}]
            Output:
                iou = 두개의 bbox 영역을 계산하여 산출해낸 iou 값
        """
        self.__pred_bbox = pred_bbox
        self.__gt_bbox = gt_bbox

        def make_bbox(bboxs):
            # (x1,y1,x2,y2) 튜플 형태로 만든다
            for bbox in bboxs:
                x1 = bbox["left"]
                y1 = bbox["top"]
                x2 = bbox["width"] + x1
                y2 = bbox["height"] + y1

                bbox_tuple = (x1, y1, x2, y2)

            return bbox_tuple

        pred_bbox_point = make_bbox(self.__pred_bbox)
        gt_bbox_point = make_bbox(self.__gt_bbox)
        pred_poly = Polygon(box(
            pred_bbox_point[0], pred_bbox_point[1], pred_bbox_point[2], pred_bbox_point[3]))
        gt_poly = Polygon(
            box(gt_bbox_point[0], gt_bbox_point[1], gt_bbox_point[2], gt_bbox_point[3]))

        iou = round(pred_poly.intersection(gt_poly).area /
                    pred_poly.union(gt_poly).area, 10)

        return iou

    def get_polygon_IoU(self, pred_polygon, gt_polygon):
        """
            Input:
                polygon 구조 ex>
                pred_polygon = [{"x": 1, "y": 2}, {"x": 5, "y": 10} ....]
                gt_polygon = [{"x": 1, "y": 2}, {"x": 5, "y": 10} ....]
            Output:
                iou = 2개의 polygon 좌표 영역을 계산하여 산출해낸 iou 값
        """

        self.__pred_polygon = pred_polygon
        self.__gt_polygon = gt_polygon
        # buffer(0)이 없으면 TopologyException: Input geom 0 is invalid 발생 가능!!
        pred_polygon_shape = Polygon(
            [(p["x"], p["y"]) for p in self.__pred_polygon]).buffer(0)
        gt_polygon_shape = Polygon([(p["x"], p["y"])
                                   for p in self.__gt_polygon]).buffer(0)

        # intersection (겹치는 영역)
        intersection_area = pred_polygon_shape.intersection(
            gt_polygon_shape).area
        # union area (합집합 형태의) 전체 영역
        union_area = pred_polygon_shape.union(gt_polygon_shape).area

        # iou 값 단순히 계산
        iou = round(intersection_area/union_area, 2)

        return iou
