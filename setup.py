from setuptools import setup, find_packages
from xpost import __version__
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()
setup(
    name="xpost",
    version=__version__,
    author="Darshan P.",
    author_email="drshnp@outlook.com",
    license="MIT",
    description="A CLI for managing Twitter APIs and Twitter posts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1darshanpatil/xpost",
    packages=find_packages(),
    install_requires=[
        "tweepy>=3.10.0",
        "fire>=0.5.0",
        "cryptography>=3.4.7",
    ],
    entry_points={
        "console_scripts": [
            "xpost=xpost.cli:virgin",
            "x=xpost.cli:tweet",
            "x-config=xpost.cli:tweet_config",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    keywords="twitter, cli, api, tweet, social media",
    project_urls={
        "Documentation": "https://github.com/1darshanpatil/xpost#readme",
        "Source": "https://github.com/1darshanpatil/xpost",
        "Tracker": "https://github.com/1darshanpatil/xpost/issues",
    },
)