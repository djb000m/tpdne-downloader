#!/usr/bin/env python

import glob
import os
import time
import click
import requests
from requests.exceptions import HTTPError


def get_images_session(url, number, save_location):
    """
    Creates a session on the supplied url and downloads the specified number of jpg images to the specified directory
    
    Args:
        url (String): the target URL
        number (Int): the number of images to download
        save_location (String): the directory in which to save the images
    """

    # avoid a connection-refused error by specifying a browser user-agent in headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
    }

    # find the number of existing images with the same naming convention
    num_existing_images = check_images(save_location)

    # create a new session connected to the url
    with requests.session() as session:
        with click.progressbar(
            range(num_existing_images, number + num_existing_images),
            label="Downloading Fresh Faces",
        ) as total_requests:
            for n in total_requests:
                try:
                    r = session.get(url, headers=headers, stream=True, timeout=1)
                    r.raise_for_status()
                except HTTPError as http_err:
                    click.secho(
                        f"\nHTTP error occurred: {http_err}\n", fg="red", bold=False
                    )
                    return False
                except TimeoutError as timeout_err:
                    click.secho(
                        f"\nRequest timed out: {timeout_err}\n", fg="red", bold=False
                    )
                    return False
                except Exception as err:
                    click.secho(
                        f"\nOther error occurred: {err}\n", fg="red", bold=False
                    )
                    return False
                else:
                    # no errors...
                    # open a new image file and write the streamed response to it in blocks
                    try:
                        # create a new file named person_00n.jpg and save it to the specified location
                        with open(
                            f"{save_location}{os.sep}person_{n+1:03d}.jpg", "wb"
                        ) as handle:
                            for block in r.iter_content(1024):
                                if not block:
                                    break

                                handle.write(block)
                    except OSError as os_err:
                        click.secho(
                            f"\nError writing to file: {os_err}\n", fg="red", bold=False
                        )

                # if not the last request, wait for a time before making next request
                if n < number + num_existing_images:
                    time.sleep(1.5)

    return True


def check_images(target_dir):
    """
    Finds the files name in the right convention (person_*) in the target directory 
    returns the number of the largest filename
    
    Args:
        target_dir (String): the target directory where this script aims to save images
    
    Returns:
        Int: Returns the highest number appended to an expected filename (person_***)
             returns 0 if no files are found
    """

    try:
        return int(
            "".join(
                filter(str.isdigit, max(glob.iglob(f"{target_dir}{os.sep}person_*")))
            )
        )
    except ValueError:
        return 0


@click.command()
@click.option("--number", "-n", help="The number of images you wish to save", default=1)
@click.option(
    "--save-location",
    "-l",
    help="The directory in which to save the images - this can be absolute or relative",
    default="images",
    type=click.Path(resolve_path=True),
)
def cli(number, save_location):
    """
    A tool to download a number of generated images from https://thispersondoesnotexist.com
    """
    url = "https://thispersondoesnotexist.com/image"

    # create the directory to save the images in
    try:
        os.makedirs(save_location)
    except OSError:
        # the directory already exists, do not try and create it
        pass

    # clear the screen
    click.clear()

    # get the images
    if get_images_session(url, number, save_location):
        click.secho(
            "\nGreat Success!\n", fg="green", blink=True, underline=True, bold=True
        )
    else:
        click.secho(
            "\nDeferred Success! There were errors, but I'm sure you can fix the problem...\n",
            bg="red",
            fg="white",
            bold=True,
        )
