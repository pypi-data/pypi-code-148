from setuptools import setup, find_packages

setup(
    name='coldwavebook',
    version='1.0.0',
    packages=find_packages(),

    # 作者、プロジェクト情報
    author='jiro yamada',
    author_email='ryafi58@mama3.org',

    #プロジェクトのホームページのURL
    url='https://example.com/',

    # 短い説明文と長い説明文を用意
    # content_typeは下記のいずれか
    # text/plain, text/x-rst, text/markdown
    description='This is a sample package for me.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    # python のバージョンは3.6以上で4未満
    python_requires='>=3.6',

    # PyPI 上で検索、閲覧のために利用される
    # ライセンス、Pythonのバージョン、OSを含める
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],

    # プログラム動作に必要な依存パッケージ
    install_requires=[
        'click>=8',
    ],
)