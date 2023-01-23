# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['owoi_audio_to_clip']

package_data = \
{'': ['*']}

install_requires = \
['Google-Images-Search>=1.4.6,<2.0.0',
 'black>=22.10.0,<23.0.0',
 'google-cloud-speech>=2.16.2,<3.0.0',
 'google-cloud-storage>=2.5.0,<3.0.0',
 'moviepy>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'owoi-audiotoclip',
    'version': '0.1.1',
    'description': 'Package to convert audio to video with google speech to text and google image search',
    'long_description': '# OWOI_AudioToClip\nPython module used for the school project OWOI (One Word One Image)\n\n## Installation\n\nAfter git cloning the repository, you can install the dependencies with the following command:\n\n```bash\npoetry install\n```\n\n## Credentials\n\nPlease provide your credentials in the following environment variables:\n\n```bash\nexport GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"\nexport GOOGLE_IMAGES_SEARCH_TOKEN="token"\nexport GOOGLE_SEARCH_ID="id"\n```\n\n## Classes\n\n### TranscriptFactory\n\nThis class is used to create a transcript from a text file. It will create a list of words and a list of timestamps.\n\n```python\t\nfrom audio_to_clip import ClipMakerFactory\n\ntranscript_factory = TranscriptFactory(gcs_uri="gs://bucket/file.mp3")\n```\n\nMethods:\n- ***transcribe_audio_to_text() -> list[dict]***: transcribe audio to text from the gcs_uri and returns a list of dict with the following keys: "word", "start_time" and "end_time"\n- ***get_word_timestamps() -> list[dict]***: returns a list of dict with the following keys: "word", "start_time" and "end_time"\n\nThis Class should be used to create a transcript from a text file before creating a clip with the ClipMakerFactory.\n\n### ClipMakerFactory\n\nThis class is used to create a clip from a transcript.\n\n```python\nfrom audio_to_clip import ClipMakerFactory\n\nclip_makfer_factory = ClipMagerFactory(video_name, username, transcript, gcs_bucket_dest, local_storage_dest, gcs_bucket_audio)\n```\n\nParams:\n- ***video_name***:str -> name of the video\n- ***username***:str -> name of the user\n- ***transcript***:list[WordTimestamp] -> list of WordTimestamp\n- ***gcs_bucket_dest***:str -> name of the gcs bucket destination\n- ***local_storage_dest***:str -> path to the local storage destination\n- ***gcs_bucket_audio***:str -> name of the gcs bucket where the audio is stored\n\nMethods:\n- ***clip_maker(word_timestamps: list[WordTimestamp]) -> VideoFileClip***: creates a clip from the transcript and returns a VideoFileClip\n- ***upload_video_to_gcs() -> None***: uploads the video to the gcs bucket with the name: `username/video_name.mp4`, should be called after clip_maker',
    'author': 'Pierre-Louis Sergent',
    'author_email': 'papa.louis59@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
