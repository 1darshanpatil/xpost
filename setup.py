from setuptools import setup, find_packages

setup(
    name='xpost',
    version='0.0.1',
    author='Darshan P.',
    author_email='drshnp@outlook.com',
    description='A CLI for managing Twitter interactions and credentials',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/1darshanpatil/xpost',
    packages=find_packages(),
    install_requires=[
        'tweepy>=3.10.0', 
        'fire>=0.4.0',     
        'cryptography>=3.4.7',  
    ],
    entry_points={
        'console_scripts': [
            'tweet=xpost.cli:tweet',  
            'tweet-config=xpost.cli:tweet_config', 
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

