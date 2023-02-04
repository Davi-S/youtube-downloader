from setuptools import setup

setup(
    
    name='youtube-downloader',
    version='0.0.3',
    entry_points={
        'console_scripts': [
            'ytd=main:pre_main'
        ]
    }
)