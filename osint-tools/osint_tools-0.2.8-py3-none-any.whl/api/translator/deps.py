
from ..base import *
from .schema.schema import *

import cv2
from tempfile import NamedTemporaryFile
import numpy as np
import os.path
from io import BytesIO
from zipfile import ZipFile

from PIL import Image as PILImage
# from werkzeug.utils import secure_filename
from deep_translator import GoogleTranslator
import hashlib
from pytesseract import (
    Output, 
    image_to_string, 
    # image_to_boxes, 
    image_to_data, 
    # image_to_osd, 
    # image_to_pdf_or_hocr
)
from fastapi import (
    UploadFile, 
    File, 
    Depends
)

# async def stage_2_check_convert_file_or_404(
#     file_data: FileTuple = Depends(stage_1_check_file_ext_or_404),
#     ) -> FileTuple:
#     try:
#         f_name, f_ext, f_bytes = file_data.data
#         # if jpeg, convert to jpg
#         # textract does not allow jpeg
#         # could be done by simply changing file extension as well.
#         # not sure if there is tradeoff atm.
#         if f_ext in settings.FILE_CONVERSION_LIST:
#             f_ext, f_bytes = await fio.convert_image_to_image(
#                 f_bytes, 
#                 ext='jpg', 
#                 is_bytes=True
#             )
#         return FileTuple(data=[f_name, f_ext, f_bytes])
#     except Exception as err:
#         err_msg = str(err)
#         logger.error(err_msg)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
#             detail=err_msg
#         )

# async def stage_1_check_file_ext_or_404(
#     file: UploadFile = File(..., description="Uploaded File.")
#     ):
#     try:
#         file_name = secure_filename(file.filename)
#         logger.info(str(file_name))

#         f_name, f_ext = os.path.splitext(os.path.basename(file_name))
#         logger.info(f"f_name {f_name}, f_ext: {f_ext}")

#         # if f_ext in settings.ACCEPT_FILES:
#             # f_bytes = await file.read()
#             # return FileTuple(data=[f_name, f_ext, f_bytes])
#         # else:
#             # raise Exception(
#                 # f'{f_ext} file not allowed -> Accepted Files: {str(settings.ACCEPT_FILES)}')
#     except Exception as err:
#         err_msg = str(err)
#         logger.error(err_msg)
#         raise PostException(
#             detail=err_msg,
#             status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
#         )

async def stream_image_bytes(image) -> bytes:
    try:
        img = PILImage.open(BytesIO(image))
        return img
    except Exception as e:
        logger.error(e)
        raise Exception(e)


# async def upload_file(
#     file: UploadFile = File(..., description="Upload Single Image File")
#     ) -> UploadFile:
#     try:
#         return file
#     except Exception as e:
#         logger.error(e)
#         raise Exception(e)

# async def read_upload_file(
#     file = Depends(upload_file)
#     ) -> bytes:
#     try:
#         im = await stream_image_bytes(await file.read())
#         return im
#     except Exception as e:
#         logger.error(e)
#         raise Exception(e)


# async def bytes_to_tesseract(
#     translate_from: TranslatorLangCodes, 
#     translate_to: TranslatorLangCodes,
#     image_bytes: bytes = Depends(read_upload_file)
#     ) -> tuple:
#     try:
#         config = r'-l {0} --psm 4'.format(TessLangCodes[translate_from])
#         logger.info(config)

#         text = image_to_string(
#             image_bytes, 
#             output_type=Output.STRING, 
#             config=config
#         )
#         return (translate_from, translate_to, text)
#     except Exception as e:
#         logger.error(e)
#         raise Exception(e)

# async def translate_text_string( 
#     data: Tuple[str, str, str] = Depends(bytes_to_tesseract)
#     ) -> str:
#     '''https://medium.com/analytics-vidhya/how-to-translate-text-with-python-9d203139dcf5'''

#     translate_from, translate_to, text = data
#     try:
#         text = GoogleTranslator(
#             source=translate_from.name, 
#             target=translate_to.name
#             ).translate(text)
#         return text
#     except Exception as e:
#         logger.error(e)
#         raise Exception(e)

async def ocr_from_file(
    image, 
    lang: TessLangCodes
    ) -> str:
    try:
        config = r'-l {0} --psm 4'.format(lang.value)
        logger.info(config)

        im = await stream_image_bytes(image)
        text = image_to_string(
            im, 
            output_type=Output.STRING, 
            config=config
        )
        return text
    except Exception as e:
        logger.error(e)
        raise Exception(e)





class BaseOCRTranslate(GoogleTranslator):

    @staticmethod
    async def convert_image_to_image(
        img: UploadFile | bytes, 
        ext: str
        ):
        """In route async methood to convert an uploaded image to another,
        format in memory.

        Args:
            img (UploadFile, bytes): Uploaded file from client.
            ext (str): Extension of file to convert to. Defaults to 'png'.
            is_bytes: (str, bytes): img is bytes or loccal file.

        Returns:
            tuple[str, bytes]: Byte string of image in converted format.
        """
        if isinstance(img, bytes):
            im = PILImage.open(BytesIO(img))
        else:
            im = PILImage.open(BytesIO(await img.read()))
        # print('data: ', im.format)
        # print('data: ', im.filename)
        # print('data: ', im.info)
        with BytesIO() as buf:
            # save image to an in-memory bytes buffer
            im.save(buf, format=ext)
            view = buf.getvalue()
            buf.close()
            return (f'.{ext}', view)


    async def goog_langs(self, **kwargs):
        """output: [arabic, french, english etc...]
        Returns:
            (List | Dict): list or dict or supported translation laguages 
        """
        try:
            langs = GoogleTranslator().get_supported_languages(kwargs)
            return langs
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    def translate_batch(
        self,
        from_lang: TranslatorLangCodes, 
        to_lang: TranslatorLangCodes,
        text_list: list[str]
        ) -> list[str]:
        try:
            translated: list[str] = GoogleTranslator(
                from_lang.name, 
                to_lang.name
            ).translate_batch(text_list)
            return translated
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    @property
    def get_langs(self):
        return self.get_supported_languages()

    def calculate_md5(self, upload_file_dot_file):
        # md5 = hashlib.md5(image.read()).hexdigest()
        file_hash = hashlib.md5()
        while chunk := upload_file_dot_file.read(8192):
            file_hash.update(chunk)
        return file_hash.hexdigest()

    def tess_to_bbox(
        self, 
        img, 
        lang: str,
        ext: str,
        show: bool = False
        ) -> bytes | None:

        d = image_to_data(
            img,
            lang=lang, 
            output_type=Output.DICT
        )
        n_boxes = len(d['level'])
        for i in range(n_boxes):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if show:# remove for prod
            cv2.imshow('img', img)# remove for prod
            cv2.waitKey(0)# remove for prod
        else:
            logger.info(ext)# remove for prod
            assert '.' in ext, 'must have "." in file extension'# remove for prod
            is_success, buffer = cv2.imencode(ext, img)
            if is_success:
                return buffer.tobytes()


class ExtractText(BaseOCRTranslate):

    async def image_to_text(
        self,
        image: UploadFile = File(...),
        language: TranslatorLangCodes = TranslatorLangCodes.english
        ) -> FileSchema:
        '''Returns text from image for a given language
        - if no language is specified textract will auto detect.
            - assuming tessract language model exists.
        '''
        f_name = image.filename
        try:
            if os.path.splitext(f_name)[1] \
                    not in ['.png', '.pdf', '.jpg', '.jpeg', '.gif']:
                raise Exception(f'Incorrect File Type: {f_name}')

            # f_path = np.fromfile(image.file, dtype=np.uint8)
            # lang = language
            lang = TessLangCodes[language].value
            logger.info(f'LANG_CODE: {lang}')
            config = r'-l {0} --psm 4'.format(lang)

            f_path = await stream_image_bytes(await image.read())
            text = image_to_string(
                f_path, 
                # lang=lang,
                output_type=Output.STRING,
                config=config
            )
            md5 = self.calculate_md5(image.file)
            logger.info(md5)
            ent = Entity(text=text)
            resp = FileSchema(
                name=f_name,
                md5=md5, 
                entities=[ent]
            )
            return resp
        except Exception as e:
            err_msg = str(e)
            logger.error(err_msg)
            raise Exception(err_msg)

    def image_to_bbox_image(
        self,
        lang: Optional[TranslatorLangCodes] = TranslatorLangCodes.english,
        image: UploadFile = File(...)
        ) -> bytes:

        lang = TessLangCodes[lang.value].value
        try:
            data = np.fromfile(image.file, dtype=np.uint8)
            img = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)# remove for prod
            ext = os.path.splitext(image.filename)[1]
            rgb = self.tess_to_bbox(
                img, 
                lang, 
                ext
            )
            return rgb
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    async def ocr_file_list(
        self,
        language: Optional[TranslatorLangCodes] = TranslatorLangCodes.english,
        files: List[UploadFile] = File(..., description="Files List")
        ) -> FileList:
        try:
            file_list = []
            for _file in files:
                data = np.fromfile(_file.file, dtype=np.uint8)
                decoded = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
                f_path = cv2.cvtColor(decoded, cv2.COLOR_BGR2GRAY)

                lang = TessLangCodes[language.value].value
                text = image_to_string(
                    f_path, 
                    lang=lang,
                    output_type=Output.STRING
                )
                md5 = self.calculate_md5(_file.file)
                logger.info(md5)
                ent = Entity(text=text)
                resp = FileSchema(
                    name=_file.filename,
                    md5=md5, 
                    entities=[ent]
                )
                file_list.append(resp)
            return FileList(file_list=file_list)
        except Exception as e:
            logger.error(e)
            raise Exception(e)



class TranslateFiles(BaseOCRTranslate):
    '''
    Tessdata lang codes: https://tesseract-ocr.github.io/tessdoc/Data-Files
    google_trans_new: https://github.com/lushan88a/google_trans_new
    https://towardsdatascience.com/language-translation-using-python-bd8020772ccc
    '''
    # async def image_to_translate(
    #     self, 
    #     text = Depends(translate_text_string),
    #     ) -> str:
    #     try:
    #         return text
    #     except Exception as e:
    #         logger.error(e)
    #         raise Exception(e)

    async def image_to_translate(
        self, 
        translate_from: TranslatorLangCodes, 
        translate_to: TranslatorLangCodes,
        file: UploadFile = File(...)
        ) -> str:
        try:
            img = await stream_image_bytes(await file.read())

            config = r'-l {0} --psm 4'.format(TessLangCodes[translate_from])
            text = image_to_string(
                img, 
                output_type=Output.STRING, 
                config=config
            )
            text = GoogleTranslator(
                source=translate_from.name, 
                target=translate_to.name
                ).translate(text)
            return text
    
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    async def translate_compressed_file(
        self,
        from_lang: TranslatorLangCodes, 
        to_lang: TranslatorLangCodes,
        file: UploadFile = File(..., description="Upload Single Image File")
        ) -> list[str]:

        lst = []
        try:
            with NamedTemporaryFile(suffix='.zip') as temp:
                temp.write(await file.read())
                with ZipFile(temp.name) as zp:
                    file_list = zp.namelist()
                    for file_name in file_list:
                        with zp.open(file_name) as z_file:
                            text = await ocr_from_file(
                                z_file.read(), 
                                lang=TessLangCodes[from_lang]
                            )
                            lst.append(text)
                            z_file.close()
                    zp.close()
                temp.close()

            translated_list = self.translate_batch(
                from_lang, 
                to_lang, 
                lst
            )
            return translated_list
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    async def translate_file_list(
        self,
        language: Optional[TranslatorLangCodes] = TranslatorLangCodes.english,
        files: List[UploadFile] = File(..., description="File List")
        ):
        try:
            return {"filenames": [_file.filename for _file in files]}
        except Exception as e:
            logger.error(e)
            raise Exception(e)




    # def save_V1(self, content_type, arr):
    #     try:
    #         ext = content_type.split('/')[-1]
    #         is_success, buffer = cv2.imencode(f".{ext}", arr)
    #         if is_success:
    #             return buffer.tobytes()
    #         raise Exception('np.array could not be encoded')
    #     except Exception as err:
    #         err_msg = f'{err}'
    #         logger.warn(err_msg)
    #         raise Exception(err_msg)

    # def upload_v1(
    #     self, 
    #     file: UploadFile = File(...)
    #     ):
    #     try:
    #         contents = file.file.read()
    #         with open(file.filename, 'wb') as f:
    #             f.write(contents)
    #     except Exception as e:
    #         raise Exception(e)
    #     else:
    #         try:
    #             text = image_to_string(
    #                 contents, 
    #                 output_type=Output.STRING
    #             )
    #             logger.info(text)
    #             return text
    #         except Exception as e2:
    #             raise Exception(e2)
    #     finally:
    #         file.file.close()

    # async def image_to_bbox_image_exp1(
    #     self,
    #     image: UploadFile = File(...),
    #     lang: Optional[TranslatorLangCodes] = TranslatorLangCodes.english
    #     ) -> dict:
    #     try:
    #         data = np.fromfile(image.file, dtype=np.uint8)
    #         image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
    #         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #         thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #         # Draw bounding boxes
    #         cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #         cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    #         for c in cnts:
    #             x,y,w,h = cv2.boundingRect(c)
    #             cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)

    #         lang = TessLangCodes[lang.value].value
    #         # text = image_to_string(
    #         #     255 - thresh, 
    #         #     lang=lang,
    #         #     config='--psm 6',
    #         #     output_type=Output.DICT
    #         #     # output_type=Output.BYTES
    #         # )
    #         text = image_to_boxes(
    #             255 - thresh, 
    #             lang=lang,
    #             config='--psm 6',
    #             output_type=Output.DICT
    #             # output_type=Output.BYTES
    #         )
    #         return text
    #     except Exception as e:
    #         err_msg = str(e)
    #         logger.error(err_msg)
    #         raise Exception(err_msg)




