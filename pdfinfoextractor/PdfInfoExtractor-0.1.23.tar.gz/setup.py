from setuptools import setup

setup(
    name='PdfInfoExtractor',
    version='0.1.23',    
    description = """A python package that can extract images from PDF and can classify documents as Aadhaar, PAN, etc and can extract info if given the path of an extracted image.
    Instructions:
    1. After importing the library from PdfInfoExtractor import ImagesExtractor, ClassifyFiles, extract_info 
    use the following link to download a model and extract it in the current directory. 
    https://drive.google.com/file/d/1_LVQj5z-yFuRG_bTvZll82b_aTz0lwll/view?usp=share_link
    """,
    url='https://github.com/alphaepsilonpi/PdfInfoExtractor',
    author='Steve Richards, Mehak Singal, Nidhish Kumar',
    author_email='steve007richards@gmail.com',
    license='MIT License',
    packages=['PdfInfoExtractor'],
    install_requires=['PyPDF2==3.0.1',
                      'boto3==1.26.56',                     
                      'pillow', 
                      'regex', 
                      'pytest-shutil==1.7.0', 
                      'keras==2.9.0', 
                      'tensorflow==2.9.2'],

    classifiers=[
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)