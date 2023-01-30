from setuptools import setup, find_packages

print(find_packages())

setup(
    name='nonebot-plugin-naturel-gpt',
    version='1.0.2',
    license='Apache License 2.0',
    packages= find_packages(),
    requires=['nonebot2', 'openai', 'transformers'],
    description="一个基于NoneBot框架的Ai聊天插件，对接OpenAi文本生成接口",
    author="KroMiose",
    url="https://github.com/KroMiose/nonebot_plugin_naturel_gpt",
    platforms=["all"],
        classifiers=[
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Natural Language :: Chinese (Simplified)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Software Development :: Libraries'
        ],
)