<p align="center">
  <img src="http://thispersondoesnotexist.com/image" width=100 />
</p>

# TPDNE Downloader

A simple python script to automate downloading any number of pictures from [This Person Does Not Exist](https://thispersondoesnotexist.com/).

## Install

1. Clone the repository to your computer

```
  git clone git@bitbucket.org:djb000m/tpdne-downloader.git
```

2. Create a new python virtual environment:

```
  python -m venv {environment_location}

```

3. Activate the virtual environment and Use pip to install the script:

```
  cd {script_directory}
  source {environment_location}/bin/activate
  pip install .
```

4. Run the script:

```
  Usage: download-new-face [OPTIONS]

  A tool to download a number of generated images from
  https://thispersondoesnotexist.com

Options:
  -n, --number INTEGER      The number of images you wish to save
  -l, --save-location PATH  The directory in which to save the images - this
                            can be absolute or relative
  --help                    Show this message and exit.

```

> #### Notes:
>
> _If **--number** is not specified then one image will be downloaded._
>
> _If **--save-location** is not specified then a directory **images** will be created in the current working directory_
>
> _Downloaded files will be named person_00n.jpg_
