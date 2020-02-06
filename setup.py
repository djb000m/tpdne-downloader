from setuptools import setup

setup(
    name="download-new-face",
    version="1.0",
    author="djb000m",
    description=(
        "A little tool to download faces from https://thispersondoesnotexist.com"
    ),
    py_modules=["face_downloader"],
    install_requires=[
        "colorama; platform_system=='Windows'",  # Colorama is only required for Windows.
        "click",
        "requests",
    ],
    entry_points="""
        [console_scripts]
        download-new-face=face_downloader:cli
    """,
)
