from say.TTS.engine import TTS, Response, Error, load_models
from say.TTS import utils

import os
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import perf_counter
import toml
from sanic import Sanic, response
from sanic.log import logger

def as_service(
    models_path,
    config_path,
    speakers_file_path,
    vocoder_path,
    vocoder_config_path,
    use_cuda,
    tts_languages_file=None,
    encoder_checkpoint="",
    encoder_config="",
    debug=False,
):
    
    CONFIG = utils.get_config_or_default()

    # Load app configs and initialize STT model
    try:
        n_proc_available = CONFIG['service']['n_proc'] or utils.get_available_cpu_count()
    except Exception as e:
        print(e)
        print("Using 2 instead.")
        n_proc_available = 2

    synthesizer, use_multi_speaker, speaker_manager, use_gst = load_models(
            models_path,
            config_path,
            speakers_file_path,
            vocoder_path,
            vocoder_config_path,
            use_cuda,
            tts_languages_file=None,
            encoder_checkpoint="",
            encoder_config="",
        )

    engine = TTS(
        synthesizer, use_multi_speaker, speaker_manager, use_gst
    )

    # Initialze Sanic and ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=n_proc_available)
    app = Sanic("tts_service")


    @app.route("/", methods=["GET"])
    async def healthcheck(_):
        return response.text("Welcome to say.sock: TTS as a Service!")


    @app.websocket("/api/v1/tts")
    async def tts(request, ws):
        logger.debug(f"Received {request.method} request at {request.path}")
        try:
            _text = await ws.recv()
            json_data = json.loads(_text.decode('utf-8', 'ignore'))
            logger.debug("With parameters:")
            logger.debug(json_data)
            inference_start = perf_counter()
            wav = await app.loop.run_in_executor(executor, lambda: engine.run(json_data.get('text'), json_data.get('language'), json_data.get('speaker_idx'), json_data.get('style_wav')))
            inference_end = perf_counter() - inference_start
            logger.debug(f"Completed {request.method} request at {request.path} in {inference_end} seconds")
            await ws.send(wav.getvalue())
            logger.debug("Sent audio to client")
            
        except Exception as e:  # pylint: disable=broad-except
            logger.debug(f"Failed to process {request.method} request at {request.path}. The exception is: {str(e)}.")
            await ws.send(b"Something went wrong")
            raise e
        finally:
            await ws.close()
    
    return app

if __name__ == '__main__':
    from say.entry_points import run_say
    run_say.run()