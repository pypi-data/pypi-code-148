from fastapi import FastAPI, Depends, HTTPException
from osint_tools.api import TranslateFiles, ExtractText
from .utils import logger

app = FastAPI()
tf = TranslateFiles()
et = ExtractText()

@app.post(
    "/translate/image/{translate_from}/{translate_to}",
    summary='Post a single image to extract and translate text')
async def translate_single_image(resp = Depends(tf.image_to_translate)):
    """Extracts and translates text from a single image.
    Single image to be extracted and translated for the given language codes
    """
    logger.info(resp)
    try:
        return resp
    except Exception as e:
        logger.error(e)
        raise HTTPException(e)

@app.post("/ocr/image/{language}")
async def extract_single_image_text(resp = Depends(et.image_to_text)):
    """Extract english text from a single image.
    """
    return resp

@app.post(
    "/translate/zip/{from_lang}/{to_lang}",
    summary='OCR + Translate zip folder of images.')
async def translate_zip_file(resp = Depends(tf.translate_compressed_file)):
    """Translate a `.zip` file of images.

    Args:
        resp (_type_, optional): _description_. Defaults to Depends(tf.translate_compressed_file).

    Returns:
        _type_: _description_
    """
    return resp

# @app.post(
    # "/ocr/zip/{lang}",
    # summary='OCR zip folder of images.')
# async def ocr_zip_file(resp = Depends(tf.translate_compressed_file)):
    # return resp


@app.post("/translate/image/list")
async def translate_image_list(resp = Depends(tf.translate_file_list)):
    return resp

@app.post("/ocr/image/list/{language}")
async def ocr_image_list(resp = Depends(et.ocr_file_list)):
    return resp

# @app.get(
#     "/translate/lang/list",
#     summary='Languages supported for translation.')
# async def available_languages_list(resp = Depends(tf.available_languages)):
#     '''Available Languages for Translation
#     This is the full list of languages available for translation
#     '''
#     return resp

# @app.get(
#     "/translate/lang/goog",
#     include_in_schema=False)
# async def available_goog_langs(resp = Depends(tf.goog_langs)):
#     return resp

# @app.post("/translate/test/one")
# async def translate_test_one(resp = Depends(tf.translate_testing)):
    # return resp



