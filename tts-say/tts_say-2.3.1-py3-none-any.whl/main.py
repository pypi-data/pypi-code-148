from say.TTS import as_client, utils, exception

import sys, os
import asyncio

def main(ARGS):
    exit_code = 0
    try:

        si, sw = utils.get_speaker(ARGS.speaker_idx, ARGS.speaker_wav)

        if ARGS.version:
            as_client.say_version(ARGS.lang, speaker_idx=si, style_wav=sw)
            sys.exit(exit_code)

        elif ARGS.text:
            _text = [" ".join(ARGS.text),]
            _show_version = False
            _no_newline = False
            if ARGS.e:
                _enable_interpretation = True
                _disable_interpretation = False
            else:
                _enable_interpretation = False
                _disable_interpretation = True

            if ARGS.lang == "fr":
                lang = "fr-fr"
            elif ARGS.lang == "en":
                lang = ARGS.lang
            else:
                lang = ARGS.lang
            
            asyncio.run(as_client._say(_text, lang, speaker_idx=si, style_wav=sw, save_output=ARGS.out_path, show_version=_show_version, enable_interpretation=_enable_interpretation, disable_interpretation=_disable_interpretation, no_newline=_no_newline))
            sys.exit(exit_code)
        else:
            _text = [
                "No attribute `text`.",
                "say --help",
                "For more information.",
                "Starting server now.",
                "Please wait."
            ]
            _show_version = False
            _enable_interpretation = True
            _disable_interpretation = False
            _no_newline = False
            for t in _text:
                utils.echo(t, show_version=_show_version, enable_interpretation=_enable_interpretation, disable_interpretation=_disable_interpretation, no_newline=_no_newline)
            
            from say.TTS.as_service import as_service

            if ARGS.list_models:
                utils.manager.list_models()
                sys.exit(exit_code)
            
            # Check if conf exist
            CONFIG = utils.get_config_or_default()

            is_allowed_to_speak = utils.is_allowed_to_speak(CONFIG)
            
            if not is_allowed_to_speak:
                raise exception.NotAllowedToSpeakError(utils.CONFIG_PATH)

            model_name = utils.get_models_name(ARGS.model_name, CONFIG)
            

            # update in-use models to the specified released models.
            model_path = None
            config_path = None
            speakers_file_path = None
            vocoder_path = None
            vocoder_config_path = None

            if model_name is not None and not ARGS.model_path:
                model_path, config_path, model_item = utils.manager.download_model(model_name)
                ARGS.vocoder_name = model_item["default_vocoder"] if ARGS.vocoder_name is None else ARGS.vocoder_name
            
            if ARGS.vocoder_name is not None and not ARGS.vocoder_path:
                vocoder_path, vocoder_config_path, _ = utils.manager.download_model(ARGS.vocoder_name)
            
            if ARGS.model_path is not None:
                model_path = ARGS.model_path
                config_path = ARGS.config_path
                speakers_file_path = ARGS.speakers_file_path

            if ARGS.vocoder_path is not None:
                vocoder_path = ARGS.vocoder_path
                vocoder_config_path = ARGS.vocoder_config_path
            
            app = as_service(model_path, config_path, speakers_file_path, vocoder_path, vocoder_config_path, ARGS.use_cuda)

            app.run(
                host=CONFIG["service"]["host"],
                port=CONFIG["service"]["port"],
                debug=ARGS.debug,
            )
    except Exception as err:
        exit_code = 1
        raise err
    
    sys.exit(exit_code)