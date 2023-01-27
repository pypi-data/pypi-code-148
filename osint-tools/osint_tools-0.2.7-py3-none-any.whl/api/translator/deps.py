
from ..base import *
from .schema.schema import *

import cv2
from tempfile import NamedTemporaryFile
import numpy as np
from io import BytesIO
from zipfile import ZipFile
from PIL import Image as PILImage
from deep_translator import GoogleTranslator
from pytesseract import Output, image_to_string
from fastapi import (
    UploadFile, 
    File, 
    Depends
)

async def stream_image_bytes(image) -> bytes:
    try:
        img = PILImage.open(BytesIO(image))
        return img
    except Exception as e:
        logger.error(e)
        raise Exception(e)


async def upload_file(
    file: UploadFile = File(..., description="Upload Single Image File")
    ) -> UploadFile:
    try:
        return file
    except Exception as e:
        logger.error(e)
        raise Exception(e)

async def read_upload_file(
    file = Depends(upload_file)
    ) -> bytes:
    try:
        im = await stream_image_bytes(await file.read())
        return im
    except Exception as e:
        logger.error(e)
        raise Exception(e)


async def bytes_to_tesseract(
    translate_from: TranslatorLangCodes, 
    translate_to: TranslatorLangCodes,
    image_bytes: bytes = Depends(read_upload_file)
    ) -> tuple:
    try:
        config = r'-l {0} --psm 4'.format(TessLangCodes[translate_from])
        logger.info(config)

        text = image_to_string(
            image_bytes, 
            output_type=Output.STRING, 
            config=config
        )
        return (translate_from, translate_to, text)
    except Exception as e:
        logger.error(e)
        raise Exception(e)

async def translate_text_string( 
    data: Tuple[str, str, str] = Depends(bytes_to_tesseract)
    ) -> str:
    '''https://medium.com/analytics-vidhya/how-to-translate-text-with-python-9d203139dcf5'''

    translate_from, translate_to, text = data
    try:
        text = GoogleTranslator(
            source=translate_from.name, 
            target=translate_to.name
            ).translate(text)
        return text
    except Exception as e:
        logger.error(e)
        raise Exception(e)

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

    # async def available_languages(self) -> List[str]:
    #     try:
    #         return [code.value for code in TranslatorLangCodes]
    #     except Exception as e:
    #         logger.error(f'Error Available Langs: {e}')
    #         raise Exception(e)

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

class ExtractText:

    async def extract_image_text(
        self,
        image: UploadFile = File(...),
        lang: TranslatorLangCodes = TranslatorLangCodes.english
        ) -> str:
        '''Returns text from image for a given language
        - if no language is specified textract will auto detect.
            - assuming tessract language model exists.
        '''
        try:
            data = np.fromfile(image.file, dtype=np.uint8)
            image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
            f_path = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            lang = TessLangCodes[lang.value].value
            logger.info(f'LANG_CODE: {lang}')

            text = image_to_string(
                f_path, 
                lang=lang,
                output_type=Output.STRING
            )
            return text
        except Exception as e:
            err_msg = str(e)
            logger.error(err_msg)
            raise Exception(e)


class TranslateFiles(BaseOCRTranslate):
    '''
    Tessdata lang codes: https://tesseract-ocr.github.io/tessdoc/Data-Files
    google_trans_new: https://github.com/lushan88a/google_trans_new
    https://towardsdatascience.com/language-translation-using-python-bd8020772ccc
    '''
    async def translate_image_file(
        self, 
        text = Depends(translate_text_string),
        ) -> str:
        try:
            return text
        except Exception as e:
            logger.error(f'Error Translate Image File: {e}')
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

    async def translate_image_file_list(
        self,
        files: List[UploadFile] = File(..., description="Upload Multiple Files")
        ):
        try:
            return {"filenames": [_file.filename for _file in files]}
        except Exception as e:
            logger.error(e)
            raise Exception(e)
